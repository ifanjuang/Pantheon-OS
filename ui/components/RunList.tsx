"use client";
import type { RunSummary } from "@/lib/types";
import { fmtDuration, relTime } from "@/lib/api";

const CRITICITE_COLOR: Record<string, string> = {
  C1: "text-blue-400 border-blue-900 bg-blue-950/40",
  C2: "text-emerald-400 border-emerald-900 bg-emerald-950/40",
  C3: "text-amber-400 border-amber-900 bg-amber-950/40",
  C4: "text-orange-400 border-orange-900 bg-orange-950/40",
  C5: "text-red-400 border-red-900 bg-red-950/40",
};

const STATUS_ICON: Record<string, React.ReactNode> = {
  running: <span className="w-2 h-2 rounded-full bg-emerald-500 pulse-dot inline-block" />,
  completed: <span className="w-2 h-2 rounded-full bg-blue-500 inline-block" />,
  failed: <span className="text-red-500 text-xs">✗</span>,
  awaiting_approval: <span className="w-2 h-2 rounded-full bg-amber-400 pulse-dot inline-block" />,
};

interface Props {
  runs: RunSummary[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

export default function RunList({ runs, selectedId, onSelect }: Props) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-3 py-2 border-b border-border">
        <span className="text-zinc-400 text-xs uppercase tracking-widest">Runs</span>
        <span className="text-zinc-500 text-xs">{runs.length}</span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {runs.length === 0 && (
          <div className="px-3 py-6 text-zinc-600 text-xs">Aucun run</div>
        )}
        {runs.map((run) => (
          <RunRow
            key={run.run_id}
            run={run}
            selected={run.run_id === selectedId}
            onClick={() => onSelect(run.run_id)}
          />
        ))}
      </div>
    </div>
  );
}

function RunRow({
  run,
  selected,
  onClick,
}: {
  run: RunSummary;
  selected: boolean;
  onClick: () => void;
}) {
  const crit = CRITICITE_COLOR[run.criticite] ?? "text-zinc-400 border-zinc-800 bg-zinc-900/40";
  const short = run.run_id.split("-")[0];

  return (
    <div
      onClick={onClick}
      className={`flex items-center gap-2 px-3 py-2 cursor-pointer border-l-2 transition-colors ${
        selected
          ? "border-blue-600 bg-white/[0.03]"
          : "border-transparent hover:border-zinc-700 hover:bg-white/[0.02]"
      }`}
    >
      {/* Status icon */}
      <span className="w-4 flex items-center justify-center flex-shrink-0">
        {STATUS_ICON[run.status] ?? <span className="w-2 h-2 rounded-full bg-zinc-600 inline-block" />}
      </span>

      {/* Run ID */}
      <span className="text-zinc-600 text-xs font-mono w-16 flex-shrink-0">{short}</span>

      {/* Criticité badge */}
      <span
        className={`text-xs border rounded px-1 py-0 flex-shrink-0 font-semibold ${crit}`}
      >
        {run.criticite}
      </span>

      {/* Agents */}
      <span className="flex-1 text-zinc-400 text-xs truncate min-w-0">
        {run.agents_involved.length > 0
          ? run.agents_involved.join(" · ")
          : run.instruction_excerpt.slice(0, 30)}
      </span>

      {/* Duration / time */}
      <span className="text-zinc-600 text-xs flex-shrink-0">
        {run.status === "running" ? relTime(run.started_at) : fmtDuration(run.duration_ms)}
      </span>

      {/* Veto indicator */}
      {run.veto_severity === "bloquant" && (
        <span className="text-red-500 text-xs flex-shrink-0">⊘</span>
      )}
    </div>
  );
}
