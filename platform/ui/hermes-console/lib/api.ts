const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const WS_BASE = BASE.replace(/^http/, "ws");

export const API = {
  modules: () => fetch(`${BASE}/control/modules`).then((r) => r.json()),
  runs: (params?: { status?: string; criticite?: string; limit?: number }) => {
    const q = new URLSearchParams();
    if (params?.status) q.set("status", params.status);
    if (params?.criticite) q.set("criticite", params.criticite);
    if (params?.limit) q.set("limit", String(params.limit));
    return fetch(`${BASE}/control/runs?${q}`).then((r) => r.json());
  },
  trace: (runId: string) =>
    fetch(`${BASE}/control/runs/${runId}/trace`).then((r) => r.json()),
  errors: () => fetch(`${BASE}/control/errors`).then((r) => r.json()),
  wsUrl: () => `${WS_BASE}/control/stream`,
};

export function fmtDuration(ms: number | null): string {
  if (ms == null) return "—";
  if (ms < 1000) return `${ms}ms`;
  if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
  return `${Math.round(ms / 60000)}m`;
}

export function fmtTime(iso: string): string {
  return new Date(iso).toLocaleTimeString("fr-FR", {
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
}

export function relTime(iso: string): string {
  const delta = Date.now() - new Date(iso).getTime();
  if (delta < 60000) return `${Math.round(delta / 1000)}s ago`;
  if (delta < 3600000) return `${Math.round(delta / 60000)}m ago`;
  return fmtTime(iso);
}
