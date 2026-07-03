import axios from 'axios';
import { config } from '../config.js';

export class DBClient {
    private url: string;

    constructor() {
        this.url = config.dbBridgeUrl;
    }

    async run(sql: string, params: any[] = []): Promise<void> {
        await axios.post(`${this.url}/query`, null, {
            params: {
                sql,
                params: JSON.stringify(params)
            }
        });
    }

    async saveRun(data: any): Promise<void> {
        const query = `
      INSERT INTO runs (
        id, timestamp, prompt, mode, test_id,
        c_nr, c_ri, c_if, total_coherence,
        landauer_cost, entropy_loss,
        answer, duration_ms, metadata
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;

        const values = [
            data.run_id,
            data.timestamp_utc,
            data.prompt.text,
            data.provider,
            data.trace_id,
            data.kernel_response.C_NR,
            data.kernel_response.C_RI,
            data.kernel_response.C_IF,
            data.kernel_response.C_total,
            data.kernel_response.landauer_cost,
            data.kernel_response.entropy_loss,
            data.response.text,
            data.observables.latency_ms,
            JSON.stringify(data)
        ];

        await this.run(query, values);
    }
}
