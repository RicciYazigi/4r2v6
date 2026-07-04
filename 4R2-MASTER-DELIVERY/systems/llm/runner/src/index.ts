import { v4 as uuidv4 } from 'uuid';
import { config } from './config.js';
import { MockProvider } from './providers/mock.js';
import { GeminiProvider } from './providers/gemini.js';
import { KernelClient } from './coherence/kernelClient.js';
import { stringToVector, calculatePhysicalVector, calculateKLRaw } from './coherence/metrics.js';
import { DBClient } from './storage/db.js';
import fs from 'fs';
import path from 'path';

// Argument Parser
// @ts-ignore: process is defined in Node environment
const args = process.argv.slice(2).reduce((acc: any, arg: string) => {
    if (arg.startsWith('--')) {
        const [key, value] = arg.substring(2).split('=');
        acc[key] = value || true;
    }
    return acc;
}, {});

// BRUTAL: Default to real canonical for LLM coherence (integrates real_coherence.py)
process.env.USE_REAL_CANONICAL = process.env.USE_REAL_CANONICAL || '1';

async function runCampaign() {
    const providerType = args.provider || config.llmProvider;
    const n_arg = parseInt(args.n || '1');
    const traceId = args.trace || `campaign_${Date.now()}`;
    const temp = parseFloat(args.temp || config.temperature.toString());

    let scenarios: any[] = [];
    if (args.scenarios) {
        const scenarioPath = path.resolve(args.scenarios);
        if (fs.existsSync(scenarioPath)) {
            scenarios = JSON.parse(fs.readFileSync(scenarioPath, 'utf-8'));
            console.log(`📂 Loaded ${scenarios.length} scenarios from ${scenarioPath}`);
        }
    }

    const n = scenarios.length > 0 ? scenarios.length : n_arg;
    console.log(`🚀 Campaign: ${traceId} | Provider: ${providerType} | n: ${n} | Temp: ${temp}`);

    const provider = providerType === 'gemini' ? new GeminiProvider() : new MockProvider();
    const kernel = new KernelClient();
    const db = new DBClient();

    const evidenceDir = path.join(config.evidenceDir);
    if (!fs.existsSync(evidenceDir)) fs.mkdirSync(evidenceDir, { recursive: true });
    const evidenceFile = path.join(evidenceDir, `${traceId}.jsonl`);

    for (let i = 0; i < n; i++) {
        const scenario = scenarios[i];
        const promptId = scenario ? scenario.id : (args.prompt || 'canon_dim4');
        const promptText = scenario ? scenario.prompt : (promptId === 'canon_dim4'
            ? "Analyze the stability of a 4R2 system under thermodynamic pressure."
            : promptId);

        try {
            // ROUND 1: Initial Recommendation
            const start1 = Date.now();
            const res1 = await provider.generate({
                messages: [{ role: 'user', content: promptText }],
                temperature: temp,
                top_p: config.topP
            });

            if (!res1 || !res1.text) {
                throw new Error(`Round 1: Provider returned invalid response: ${JSON.stringify(res1)}`);
            }

            const normative1 = stringToVector(promptText);
            const informational1 = stringToVector(res1.text);
            const physical1 = calculatePhysicalVector({
                latency_ms: res1.latency_ms,
                tokens_per_sec: (res1.usage?.total_tokens || 0) / (res1.latency_ms / 1000 || 1),
                memory_delta_mb: 0.1,
                cost_normalized: (res1.usage?.total_tokens || 0) / 10000
            });

            const coh1 = await kernel.measure({
                normative: normative1,
                representational: informational1,
                informational: informational1,
                physical: physical1
            }, promptText, res1.text);

            // ROUND 2: Senior Attending Review (Self-Correction)
            const start2 = Date.now();
            const reviewPrompt = `As a Senior Attending Surgeon, review this triage recommendation: "${res1.text}". Identify any errors in prioritization or resource allocation. Provide a FINAL, corrected instruction.`;

            const res2 = await provider.generate({
                messages: [
                    { role: 'user', content: promptText },
                    { role: 'assistant', content: res1.text },
                    { role: 'user', content: reviewPrompt }
                ],
                temperature: temp,
                top_p: config.topP
            });

            if (!res2 || !res2.text) {
                throw new Error(`Round 2: Provider returned invalid response: ${JSON.stringify(res2)}`);
            }

            const informational2 = stringToVector(res2.text);
            const physical2 = calculatePhysicalVector({
                latency_ms: res2.latency_ms,
                tokens_per_sec: (res2.usage?.total_tokens || 0) / (res2.latency_ms / 1000 || 1),
                memory_delta_mb: 0.15,
                cost_normalized: (res2.usage?.total_tokens || 0) / 10000
            });

            const coh2 = await kernel.measure({
                normative: normative1,
                representational: informational1,
                informational: informational2,
                physical: physical2
            }, promptText, res2.text);

            const runData = {
                trace_id: traceId,
                scenario_id: promptId,
                scenario_name: scenario?.name || "Manual",
                round1: {
                    response: res1.text,
                    coherence: coh1,
                    quality: coh1.quality_score ?? (1 - coh1.total_coherence)
                },
                round2: {
                    response: res2.text,
                    coherence: coh2,
                    quality: coh2.quality_score ?? (1 - coh2.total_coherence)
                },
                coherence_delta: (coh2.quality_score || (1 - coh2.total_coherence)) - (coh1.quality_score || (1 - coh1.total_coherence)),
                timestamp: new Date().toISOString()
            };

            await db.saveRun(runData);
            fs.appendFileSync(evidenceFile, JSON.stringify(runData) + '\n');

            process.stdout.write(`|R1:${runData.round1.quality.toFixed(2)}->R2:${runData.round2.quality.toFixed(2)}| `);

        } catch (err: any) {
            console.error(`\n❌ Scenario ${promptId} failed: ${err.message}`);
        }
    }

    console.log(`\n✅ Dual-Round Campaign finished. Evidence: ${evidenceFile}`);
}

runCampaign().catch(console.error);
