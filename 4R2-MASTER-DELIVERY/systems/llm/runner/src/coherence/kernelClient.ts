import axios from 'axios';
import { config } from '../config.js';
import { spawn } from 'child_process';
import path from 'path';

export interface CoherenceRequest {
    normative: number[];
    representational: number[];
    informational: number[];
    physical: number[];
}

export interface CoherenceResponse {
    c_nr: number;
    c_ri: number;
    c_if: number;
    total_coherence: number;
    landauer_cost: number;
    entropy_loss: number;
    quality_score: number;
    timestamp: string;
}

export class KernelClient {
    private url: string;
    private useRealCanonical: boolean;

    constructor() {
        this.url = config.basicKernelUrl;
        // BRUTAL REAL INTEGRATION: Use real_coherence.py (canonical + AGW ready) for LLM scoring by default
        // This makes the harness use the real kernel natively when texts are provided.
        this.useRealCanonical = process.env.USE_REAL_CANONICAL !== '0';
    }

    private async measureRealCanonical(prompt: string, responseText: string, physical: number[]): Promise<CoherenceResponse> {
        return new Promise((resolve, reject) => {
            // Path from runner/src/coherence to llm/real_coherence.py
            const realScript = path.resolve(__dirname, '../../../../real_coherence.py');
            const python = spawn('python3', [realScript, prompt, responseText, JSON.stringify(physical)]);
            let output = '';
            python.stdout.on('data', (data) => { output += data.toString(); });
            python.stderr.on('data', (data) => { console.error(data.toString()); });
            python.on('close', (code) => {
                if (code !== 0) return reject(new Error('real_coherence failed'));
                try {
                    const res = JSON.parse(output.trim());
                    resolve({
                        c_nr: res.C_NR,
                        c_ri: res.C_RI,
                        c_if: res.C_IF,
                        total_coherence: res.C_total,
                        landauer_cost: 0,
                        entropy_loss: res.L_4R2,
                        quality_score: 1 - res.C_total,
                        timestamp: new Date().toISOString()
                    } as CoherenceResponse);
                } catch (e) { reject(e); }
            });
        });
    }

    async measure(request: CoherenceRequest, promptForReal?: string, responseForReal?: string): Promise<CoherenceResponse> {
        if (this.useRealCanonical && promptForReal && responseForReal) {
            // Use real canonical directly for full integration
            return this.measureRealCanonical(promptForReal, responseForReal, request.physical);
        }
        try {
            const response = await axios.post(`${this.url}/api/coherence/measure`, request);
            const data = response.data;
            
            // Normalización de claves para compatibilidad (C_* -> c_*)
            return {
                c_nr: data.c_nr ?? data.C_NR,
                c_ri: data.c_ri ?? data.C_RI,
                c_if: data.c_if ?? data.C_IF,
                total_coherence: data.total_coherence ?? data.C_total,
                landauer_cost: data.landauer_cost,
                entropy_loss: data.entropy_loss,
                quality_score: data.quality_score,
                timestamp: data.timestamp
            } as CoherenceResponse;
        } catch (error: any) {
            if (error.response) {
                console.error('Kernel Error Data:', JSON.stringify(error.response.data));
            }
            throw error;
        }
    }
}
