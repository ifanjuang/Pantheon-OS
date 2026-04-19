export interface ModuleStatus {
  name: string;
  status: "loaded" | "disabled";
  version: string;
  prefix: string;
  description: string;
  depends_on: string[];
}

export interface RunSummary {
  run_id: string;
  criticite: string;
  status: string;
  instruction_excerpt: string;
  agents_involved: string[];
  started_at: string;
  duration_ms: number | null;
  veto_severity: string | null;
  affaire_id: string | null;
  error_message: string | null;
}

export interface TraceEvent {
  type: string;
  run_id: string;
  timestamp: string;
  agent: string | null;  // identité lowercase (ex: "zeus")
  role: string | null;   // responsabilité (ex: "orchestrator")
  payload: Record<string, unknown>;
}

export interface ErrorEntry {
  severity: "error" | "warning" | "info";
  source: string;
  message: string;
  run_id: string | null;
  timestamp: string;
}

export type WsMessage =
  | { type: "init"; modules: ModuleStatus[]; runs: RunSummary[]; errors: ErrorEntry[] }
  | { type: "run.update"; data: RunSummary }
  | { type: "errors.refresh"; errors: ErrorEntry[] }
  | { type: "heartbeat"; ts: string };
