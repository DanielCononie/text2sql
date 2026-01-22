export interface SqlResponse {
    sql: string;
    needs_clarification: boolean;
    questions: string[];
    columns: string[];
    rows: any[];
}
