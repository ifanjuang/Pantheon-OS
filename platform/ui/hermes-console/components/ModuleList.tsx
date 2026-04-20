"use client";
import type { ModuleStatus } from "@/lib/types";

interface Props {
  modules: ModuleStatus[];
}

export default function ModuleList({ modules }: Props) {
  const loaded = modules.filter((m) => m.status === "loaded");
  const disabled = modules.filter((m) => m.status === "disabled");

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-3 py-2 border-b border-border">
        <span className="text-zinc-400 text-xs uppercase tracking-widest">Modules</span>
        <span className="text-zinc-500 text-xs">
          {loaded.length}/{modules.length}
        </span>
      </div>
      <div className="flex-1 overflow-y-auto">
        {loaded.map((m) => (
          <ModuleRow key={m.name} module={m} />
        ))}
        {disabled.length > 0 && (
          <>
            <div className="px-3 pt-3 pb-1 text-xs text-zinc-600 uppercase tracking-widest">
              Désactivés
            </div>
            {disabled.map((m) => (
              <ModuleRow key={m.name} module={m} />
            ))}
          </>
        )}
      </div>
    </div>
  );
}

function ModuleRow({ module: m }: { module: ModuleStatus }) {
  const active = m.status === "loaded";
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 hover:bg-white/[0.02] group">
      <span
        className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${
          active ? "bg-emerald-500" : "bg-zinc-700"
        }`}
      />
      <span
        className={`flex-1 truncate text-xs ${active ? "text-zinc-300" : "text-zinc-600"}`}
        title={m.description || m.name}
      >
        {m.name}
      </span>
      <span className="text-zinc-700 text-xs opacity-0 group-hover:opacity-100 transition-opacity">
        v{m.version}
      </span>
    </div>
  );
}
