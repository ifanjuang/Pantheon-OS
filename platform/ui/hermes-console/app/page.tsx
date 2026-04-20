"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import type { ErrorEntry, ModuleStatus, RunSummary, TraceEvent, WsMessage } from "@/lib/types";
import { API } from "@/lib/api";
import ModuleList from "@/components/ModuleList";
import RunList from "@/components/RunList";
import TraceViewer from "@/components/TraceViewer";
import ErrorStream from "@/components/ErrorStream";

type ConnStatus = "connecting" | "connected" | "disconnected";

export default function ControlPage() {
  const [modules, setModules] = useState<ModuleStatus[]>([]);
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [errors, setErrors] = useState<ErrorEntry[]>([]);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [trace, setTrace] = useState<TraceEvent[]>([]);
  const [traceLoading, setTraceLoading] = useState(false);
  const [connStatus, setConnStatus] = useState<ConnStatus>("connecting");
  const [uptime, setUptime] = useState(0);
  const [lastHeartbeat, setLastHeartbeat] = useState<string | null>(null);

  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const retryDelay = useRef(2000);
  const uptimeRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Uptime counter
  useEffect(() => {
    uptimeRef.current = setInterval(() => setUptime((t) => t + 1), 1000);
    return () => { if (uptimeRef.current) clearInterval(uptimeRef.current); };
  }, []);

  // WebSocket connection
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(API.wsUrl());
    wsRef.current = ws;
    setConnStatus("connecting");

    ws.onopen = () => {
      setConnStatus("connected");
      retryDelay.current = 2000;
    };

    ws.onmessage = (e) => {
      try {
        const msg = JSON.parse(e.data) as WsMessage;
        if (msg.type === "init") {
          setModules(msg.modules);
          setRuns(msg.runs);
          setErrors(msg.errors);
        } else if (msg.type === "run.update") {
          setRuns((prev) => {
            const idx = prev.findIndex((r) => r.run_id === msg.data.run_id);
            if (idx === -1) return [msg.data, ...prev].slice(0, 50);
            const next = [...prev];
            next[idx] = msg.data;
            return next;
          });
        } else if (msg.type === "errors.refresh") {
          setErrors(msg.errors);
        } else if (msg.type === "heartbeat") {
          setLastHeartbeat(msg.ts);
        }
      } catch {}
    };

    ws.onclose = () => {
      setConnStatus("disconnected");
      retryRef.current = setTimeout(() => {
        retryDelay.current = Math.min(retryDelay.current * 1.5, 30000);
        connect();
      }, retryDelay.current);
    };

    ws.onerror = () => ws.close();
  }, []);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
      if (retryRef.current) clearTimeout(retryRef.current);
    };
  }, [connect]);

  // Load trace when run is selected
  useEffect(() => {
    if (!selectedRunId) { setTrace([]); return; }
    setTraceLoading(true);
    API.trace(selectedRunId)
      .then(setTrace)
      .catch(() => setTrace([]))
      .finally(() => setTraceLoading(false));
  }, [selectedRunId]);

  const selectedRun = runs.find((r) => r.run_id === selectedRunId) ?? null;

  const fmtUptime = (s: number) => {
    const h = Math.floor(s / 3600).toString().padStart(2, "0");
    const m = Math.floor((s % 3600) / 60).toString().padStart(2, "0");
    const sec = (s % 60).toString().padStart(2, "0");
    return `${h}:${m}:${sec}`;
  };

  const connDot =
    connStatus === "connected" ? "bg-emerald-500" :
    connStatus === "connecting" ? "bg-amber-400 pulse-dot" : "bg-red-500";

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-surface">

      {/* ── Top bar ───────────────────────────────────────── */}
      <header className="flex items-center gap-4 px-4 py-2 border-b border-border flex-shrink-0 bg-panel">
        <span className="text-zinc-200 font-semibold tracking-tight">⬡ ARCEUS Control</span>
        <div className="flex-1" />
        <span className="text-zinc-700 text-xs">{fmtUptime(uptime)}</span>
        <div className="flex items-center gap-1.5">
          <span className={`w-2 h-2 rounded-full ${connDot}`} />
          <span className={`text-xs ${
            connStatus === "connected" ? "text-emerald-400" :
            connStatus === "connecting" ? "text-amber-400" : "text-red-400"
          }`}>
            {connStatus}
          </span>
        </div>
        {lastHeartbeat && (
          <span className="text-zinc-700 text-xs hidden xl:block">
            hb {new Date(lastHeartbeat).toLocaleTimeString("fr-FR")}
          </span>
        )}
      </header>

      {/* ── Main grid ─────────────────────────────────────── */}
      <div className="flex flex-1 min-h-0">

        {/* Modules — left column */}
        <aside className="w-44 flex-shrink-0 border-r border-border bg-panel">
          <ModuleList modules={modules} />
        </aside>

        {/* Runs — center column */}
        <div className="flex flex-col flex-1 min-w-0 border-r border-border">
          {/* Top half — runs */}
          <div className="h-1/2 border-b border-border bg-panel">
            <RunList
              runs={runs}
              selectedId={selectedRunId}
              onSelect={setSelectedRunId}
            />
          </div>
          {/* Bottom half — trace */}
          <div className="h-1/2 bg-surface">
            <TraceViewer
              run={selectedRun}
              events={trace}
              loading={traceLoading}
            />
          </div>
        </div>

        {/* Errors — right column */}
        <aside className="w-80 flex-shrink-0 bg-panel">
          <ErrorStream
            errors={errors}
            onSelectRun={setSelectedRunId}
          />
        </aside>
      </div>
    </div>
  );
}
