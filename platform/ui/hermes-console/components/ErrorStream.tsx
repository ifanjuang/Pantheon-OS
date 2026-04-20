"use client";
import type { ErrorEntry } from "@/lib/types";
import { fmtTime } from "@/lib/api";

const SEV_STYLE: Record<string, { label: string; color: string; dot: string }> = {
  error:   { label: "ERR",  color: "text-red-400",    dot: "bg-red-500" },
  warning: { label: "WARN", color: "text-amber-400",  dot: "bg-amber-400" },
  info:    { label: "INFO", color: "text-blue-400",   dot: "bg-blue-500" },
};

interface Props {
  errors: ErrorEntry[];
  onSelectRun?: (id: string) => void;
}

export default function ErrorStream({ errors, onSelectRun }: Props) {
  const errCount = errors.filter((e) => e.severity === "error").length;
  const warnCount = errors.filter((e) => e.severity === "warning").length;

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-3 py-2 border-b border-border flex-shrink-0">
        <span className="text-zinc-400 text-xs uppercase tracking-widest">Errors</span>
        {errCount > 0 && (
          <span className="text-red-400 text-xs">{errCount} error{errCount > 1 ? "s" : ""}</span>
        )}
        {warnCount > 0 && (
          <span className="text-amber-400 text-xs">{warnCount} warn{warnCount > 1 ? "s" : ""}</span>
        )}
        {errors.length === 0 && (
          <span className="text-emerald-500 text-xs ml-auto">✓ clear</span>
        )}
      </div>
      <div className="flex-1 overflow-y-auto">
        {errors.length === 0 && (
          <div className="px-3 py-4 text-zinc-700 text-xs">Aucune erreur récente</div>
        )}
        {errors.map((err, i) => (
          <ErrorRow key={i} err={err} onSelectRun={onSelectRun} />
        ))}
      </div>
    </div>
  );
}

function ErrorRow({
  err,
  onSelectRun,
}: {
  err: ErrorEntry;
  onSelectRun?: (id: string) => void;
}) {
  const s = SEV_STYLE[err.severity] ?? SEV_STYLE.info;
  return (
    <div
      className={`flex items-start gap-2 px-3 py-1.5 hover:bg-white/[0.02] ${
        err.run_id ? "cursor-pointer" : ""
      }`}
      onClick={() => err.run_id && onSelectRun?.(err.run_id)}
    >
      <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 mt-1.5 ${s.dot}`} />
      <span className="text-zinc-700 text-xs flex-shrink-0 w-14">{fmtTime(err.timestamp)}</span>
      <span className={`text-xs font-semibold flex-shrink-0 w-8 ${s.color}`}>{s.label}</span>
      <span className="text-zinc-400 text-xs flex-shrink-0 w-16 truncate">{err.source}</span>
      <span className="text-zinc-300 text-xs truncate flex-1">{err.message}</span>
      {err.run_id && (
        <span className="text-zinc-700 text-xs flex-shrink-0 font-mono">
          {err.run_id.split("-")[0]}
        </span>
      )}
    </div>
  );
}
