"use client";
import type { RunSummary, TraceEvent } from "@/lib/types";
import { fmtTime, fmtDuration } from "@/lib/api";

const AGENT_COLOR: Record<string, string> = {
  orchestra: "text-zinc-400",
  hermes:    "text-violet-400",
  zeus:      "text-blue-400",
  athena:    "text-emerald-400",
  themis:    "text-orange-400",
  hephaistos:"text-orange-300",
  apollon:   "text-fuchsia-400",
  ares:      "text-red-400",
  hestia:    "text-amber-400",
  mnemosyne: "text-cyan-400",
  chronos:   "text-teal-400",
  argos:     "text-lime-400",
  promethee: "text-yellow-400",
  dionysos:  "text-pink-400",
  iris:      "text-sky-400",
  aphrodite: "text-rose-400",
  dedale:    "text-indigo-400",
};

function agentColor(agent: string | null): string {
  if (!agent) return "text-zinc-500";
  const base = agent.split(".")[0].toLowerCase();
  return AGENT_COLOR[base] ?? "text-zinc-300";
}

function eventDot(type: string): string {
  if (type.includes("failed") || type === "veto.raised") return "bg-red-500";
  if (type.includes("hitl") || type.includes("awaiting")) return "bg-amber-400";
  if (type.includes("completed") || type.includes("orchestra.completed")) return "bg-blue-500";
  if (type.includes("running") || type.includes("started")) return "bg-emerald-500";
  return "bg-zinc-600";
}

interface Props {
  run: RunSummary | null;
  events: TraceEvent[];
  loading: boolean;
}

export default function TraceViewer({ run, events, loading }: Props) {
  if (!run) {
    return (
      <div className="flex items-center justify-center h-full text-zinc-700 text-xs">
        Sélectionne un run pour voir sa trace
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center gap-3 px-3 py-2 border-b border-border flex-shrink-0">
        <span className="text-zinc-400 text-xs uppercase tracking-widest">Trace</span>
        <span className="text-zinc-500 text-xs font-mono">{run.run_id.split("-")[0]}</span>
        <span className={`text-xs font-semibold ${
          run.criticite === "C5" ? "text-red-400" :
          run.criticite === "C4" ? "text-orange-400" :
          run.criticite === "C3" ? "text-amber-400" : "text-blue-400"
        }`}>{run.criticite}</span>
        <span className="text-zinc-600 text-xs">{run.status}</span>
        {run.duration_ms && (
          <span className="text-zinc-600 text-xs ml-auto">{fmtDuration(run.duration_ms)}</span>
        )}
      </div>

      {/* Instruction */}
      <div className="px-3 py-2 border-b border-border bg-white/[0.01] flex-shrink-0">
        <span className="text-zinc-500 text-xs italic">{run.instruction_excerpt}</span>
        {run.instruction_excerpt.length >= 80 && (
          <span className="text-zinc-700 text-xs">…</span>
        )}
      </div>

      {/* Events */}
      <div className="flex-1 overflow-y-auto px-3 py-2">
        {loading && (
          <div className="text-zinc-700 text-xs py-2">Chargement…</div>
        )}
        {!loading && events.length === 0 && (
          <div className="text-zinc-700 text-xs py-2">Aucun événement disponible</div>
        )}
        {events.map((ev, i) => (
          <EventRow key={i} event={ev} />
        ))}
      </div>

      {/* Veto banner */}
      {run.veto_severity && (
        <div className={`px-3 py-2 border-t flex-shrink-0 text-xs ${
          run.veto_severity === "bloquant"
            ? "border-red-900 bg-red-950/40 text-red-300"
            : "border-amber-900 bg-amber-950/30 text-amber-300"
        }`}>
          <span className="font-semibold">⊘ Veto {run.veto_severity}</span>
        </div>
      )}
    </div>
  );
}

function EventRow({ event: ev }: { event: TraceEvent }) {
  const color = agentColor(ev.agent);
  const dot = eventDot(ev.type);
  const payloadStr = Object.entries(ev.payload)
    .filter(([, v]) => v != null && v !== "" && v !== false)
    .map(([k, v]) => `${k}:${JSON.stringify(v)}`.slice(0, 60))
    .join("  ");

  return (
    <div className="flex items-start gap-2 py-1 group">
      {/* Timeline dot + line */}
      <div className="flex flex-col items-center flex-shrink-0 mt-1.5">
        <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${dot}`} />
      </div>

      {/* Time */}
      <span className="text-zinc-700 text-xs flex-shrink-0 w-14">{fmtTime(ev.timestamp)}</span>

      {/* Type */}
      <span className={`text-xs flex-shrink-0 font-medium ${color}`}>
        {ev.type}
      </span>

      {/* Payload */}
      {payloadStr && (
        <span className="text-zinc-600 text-xs truncate min-w-0 opacity-0 group-hover:opacity-100 transition-opacity">
          {payloadStr}
        </span>
      )}
    </div>
  );
}
