export type LLMRequest = {
    messages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
    temperature: number;
    top_p: number;
};

export type LLMResponse = {
    text: string;
    raw: any;
    model: string;
    usage?: { input_tokens?: number; output_tokens?: number; total_tokens?: number };
    latency_ms: number;
};

export interface LLMProvider {
    generate(request: LLMRequest): Promise<LLMResponse>;
}
