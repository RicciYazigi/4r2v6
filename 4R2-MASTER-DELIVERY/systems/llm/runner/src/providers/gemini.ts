import { GoogleGenerativeAI } from "@google/generative-ai";
import { LLMProvider, LLMRequest, LLMResponse } from './index.js';
import { config } from '../config.js';

export class GeminiProvider implements LLMProvider {
    private genAI: GoogleGenerativeAI;
    private model: any;

    constructor() {
        this.genAI = new GoogleGenerativeAI(config.geminiApiKey);
        this.model = this.genAI.getGenerativeModel({ model: "gemini-pro" });
    }

    async generate(request: LLMRequest): Promise<LLMResponse> {
        const start = Date.now();
        const contents = request.messages.map(m => ({
            role: m.role === "user" ? "user" : "model", // Simple mapping
            parts: [{ text: m.content }]
        }));

        const result = await this.model.generateContent({
            contents,
            generationConfig: {
                temperature: request.temperature,
                topP: request.top_p,
            }
        });

        const response = await result.response;
        const text = response.text();

        return {
            text,
            raw: response,
            model: "gemini-pro",
            // Gemini JS SDK usage reporting is minimal, we might need to estimate
            usage: { total_tokens: text.length / 4 },
            latency_ms: Date.now() - start
        };
    }
}
