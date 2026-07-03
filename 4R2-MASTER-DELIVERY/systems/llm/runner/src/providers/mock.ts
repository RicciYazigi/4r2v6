import { LLMProvider, LLMRequest, LLMResponse } from './index.js';

export class MockProvider implements LLMProvider {
    async generate(request: LLMRequest): Promise<LLMResponse> {
        const start = Date.now();
        const messages = request.messages;
        const lastMsg = messages[messages.length - 1].content;
        const isReview = lastMsg.includes("Senior Attending Surgeon");

        let text = "";
        if (isReview) {
            text = `[SENIOR ATTENDING] CORRECTION APPLIED: Re-allocating resources. Priority shifted to Pediatric Trauma in Bay 4. Metric Delta: +0.4.`;
        } else {
            text = `[MOCK TRIAGE] Immediate assessment: Yellow tag. Vitals stable. Await surgical consult.`;
        }

        return {
            text,
            raw: { mock: true, mode: isReview ? "correction" : "triage" },
            model: "mock-v1",
            usage: { input_tokens: 10, output_tokens: 20, total_tokens: 30 },
            latency_ms: Date.now() - start
        };
    }
}
