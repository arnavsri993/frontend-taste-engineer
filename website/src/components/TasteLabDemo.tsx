"use client";

import { useCallback, useEffect, useRef, useState, useSyncExternalStore } from "react";
import { Monitor, Smartphone, Play, Pause } from "lucide-react";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { BrowserFrame } from "@/components/ui/BrowserFrame";
import {
  DEMO_EXAMPLES,
  STAGES,
  type DemoExample,
  type DemoStage,
} from "@/lib/demo-data";
import { cn } from "@/lib/utils";

function StageData({ data }: { data: Record<string, string> }) {
  return (
    <dl className="space-y-2.5">
      {Object.entries(data).map(([key, value]) => (
        <div key={key} className="grid grid-cols-1 sm:grid-cols-[9rem_1fr] gap-1 sm:gap-3">
          <dt className="font-mono text-xs text-teal shrink-0">{key}</dt>
          <dd className="text-sm text-gray-600 leading-relaxed">{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function PreviewPanel({
  example,
  viewport,
}: {
  example: DemoExample;
  viewport: "desktop" | "mobile";
}) {
  const { preview } = example;
  const isMobile = viewport === "mobile";

  return (
    <div
      className={cn(
        "transition-all duration-500 mx-auto overflow-hidden rounded-md",
        isMobile ? "w-[200px]" : "w-full"
      )}
      style={{
        background: preview.bg.includes("gradient") ? preview.bg : preview.bg,
        color: preview.text,
      }}
    >
      <div className={cn("p-4", isMobile && "p-3")}>
        <p
          className={cn(
            "text-[10px] font-mono mb-2 opacity-70",
            isMobile && "text-[8px]"
          )}
          style={{ color: preview.accent }}
        >
          {preview.subtitle}
        </p>
        <h3
          className={cn(
            "font-bold tracking-tight mb-4",
            preview.fontClass,
            isMobile ? "text-base" : "text-xl"
          )}
        >
          {preview.title}
        </h3>
        <div className="space-y-2">
          {preview.sections.map((section) => (
            <div
              key={section.label}
              className={cn(
                "border-t border-white/10 pt-2",
                isMobile && "pt-1.5"
              )}
            >
              <p
                className={cn(
                  "font-mono text-[10px] opacity-60 mb-0.5",
                  isMobile && "text-[8px]"
                )}
              >
                {section.label}
              </p>
              <p className={cn("text-xs leading-snug", isMobile && "text-[10px]")}>
                {section.content}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function subscribeReducedMotion(callback: () => void) {
  const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  mq.addEventListener("change", callback);
  return () => mq.removeEventListener("change", callback);
}

function getReducedMotionSnapshot() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function getReducedMotionServerSnapshot() {
  return false;
}

export function TasteLabDemo() {
  const [selectedId, setSelectedId] = useState(DEMO_EXAMPLES[0].id);
  const [customPrompt, setCustomPrompt] = useState("");
  const [activeStageIndex, setActiveStageIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [viewport, setViewport] = useState<"desktop" | "mobile">("desktop");
  const reducedMotion = useSyncExternalStore(
    subscribeReducedMotion,
    getReducedMotionSnapshot,
    getReducedMotionServerSnapshot
  );
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const example =
    DEMO_EXAMPLES.find((e) => e.id === selectedId) ?? DEMO_EXAMPLES[0];
  const activeStage = STAGES[activeStageIndex];
  const displayPrompt = customPrompt.trim() || example.prompt;

  const getStageData = useCallback(
    (stage: DemoStage): Record<string, string> => {
      switch (stage) {
        case "classify":
          return example.classify;
        case "brief":
          return example.brief;
        case "direct":
          return example.direct;
        case "build":
          return example.build;
        case "refine":
          return example.refine;
        case "verify":
          return example.verify;
      }
    },
    [example]
  );

  const resetStages = useCallback(() => {
    setActiveStageIndex(0);
  }, []);

  const selectExample = useCallback(
    (id: string) => {
      setSelectedId(id);
      setCustomPrompt("");
      resetStages();
      setIsPlaying(true);
    },
    [resetStages]
  );

  useEffect(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);

    if (!isPlaying || reducedMotion) return;

    intervalRef.current = setInterval(() => {
      setActiveStageIndex((prev) => {
        if (prev >= STAGES.length - 1) return prev;
        return prev + 1;
      });
    }, 2500);

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPlaying, reducedMotion, selectedId]);

  const handleStageClick = (index: number) => {
    setActiveStageIndex(index);
    setIsPlaying(false);
  };

  return (
    <section id="demo" className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading
          eyebrow="Interactive workflow preview"
          title="Taste Lab"
          description="Select a prompt and watch how Frontend Taste Engineer structures the work. This is an illustrative preview — no real generation occurs."
        />

        <div className="mb-6 flex items-center gap-2 px-3 py-2 bg-teal-muted/40 border border-teal/20 rounded-md">
          <span className="w-2 h-2 rounded-full bg-teal animate-pulse-subtle" aria-hidden="true" />
          <p className="text-sm font-mono text-teal-dark">
            Interactive workflow preview — illustrative only
          </p>
        </div>

        <div className="grid lg:grid-cols-[1fr_1.1fr] gap-8 lg:gap-10">
          <div className="space-y-6">
            <fieldset>
              <legend className="font-mono text-xs text-gray-600 mb-3 uppercase tracking-wider">
                Example prompts
              </legend>
              <div className="flex flex-col gap-2">
                {DEMO_EXAMPLES.map((ex) => (
                  <button
                    key={ex.id}
                    type="button"
                    onClick={() => selectExample(ex.id)}
                    className={cn(
                      "text-left px-4 py-3 rounded-md border text-sm transition-colors min-h-[44px]",
                      selectedId === ex.id && !customPrompt
                        ? "border-teal bg-teal-muted/50 text-ink"
                        : "border-line hover:border-gray-200 text-gray-600 hover:text-ink"
                    )}
                  >
                    {ex.prompt}
                  </button>
                ))}
              </div>
            </fieldset>

            <div>
              <label htmlFor="custom-prompt" className="font-mono text-xs text-gray-600 mb-2 block uppercase tracking-wider">
                Or type your own
              </label>
              <textarea
                id="custom-prompt"
                value={customPrompt}
                onChange={(e) => {
                  setCustomPrompt(e.target.value);
                  resetStages();
                }}
                placeholder="Enter a prompt to preview the workflow structure…"
                rows={2}
                className="w-full px-4 py-3 border border-line rounded-md text-sm bg-paper resize-y focus:border-teal transition-colors"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-3">
                <p className="font-mono text-xs text-gray-600 uppercase tracking-wider">
                  Workflow stages
                </p>
                <button
                  type="button"
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="inline-flex items-center gap-1.5 text-xs font-mono text-teal hover:text-teal-dark min-h-[44px] px-2"
                  aria-label={isPlaying ? "Pause stage progression" : "Play stage progression"}
                >
                  {isPlaying ? (
                    <>
                      <Pause className="w-3.5 h-3.5" /> Pause
                    </>
                  ) : (
                    <>
                      <Play className="w-3.5 h-3.5" /> Play
                    </>
                  )}
                </button>
              </div>

              <ol className="flex gap-2 mb-4 overflow-x-auto pb-2 -mx-1 px-1 md:flex-wrap md:overflow-visible" aria-label="Workflow stage progress">
                {STAGES.map((stage, i) => (
                  <li key={stage.id}>
                    <button
                      type="button"
                      onClick={() => handleStageClick(i)}
                      aria-current={i === activeStageIndex ? "step" : undefined}
                      className={cn(
                        "px-3 py-2 rounded-md border text-xs font-mono transition-colors min-h-[44px] shrink-0",
                        i === activeStageIndex && "stage-active font-medium",
                        i < activeStageIndex && "stage-complete text-teal",
                        i > activeStageIndex && "border-line text-gray-400"
                      )}
                    >
                      {i + 1}. {stage.label}
                    </button>
                  </li>
                ))}
              </ol>

              <div
                className="border border-line rounded-md p-4 md:p-5 bg-paper min-h-[200px]"
                aria-live="polite"
                aria-atomic="true"
              >
                <p className="font-mono text-xs text-teal mb-3">
                  Stage {activeStageIndex + 1}: {activeStage.label}
                </p>
                <StageData data={getStageData(activeStage.id)} key={`${selectedId}-${activeStage.id}`} />
              </div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <p className="font-mono text-xs text-gray-600">Preview surface</p>
              <div className="flex gap-1" role="group" aria-label="Viewport toggle">
                <button
                  type="button"
                  onClick={() => setViewport("desktop")}
                  aria-pressed={viewport === "desktop"}
                  className={cn(
                    "inline-flex items-center gap-1.5 px-3 py-2 rounded-md text-xs font-mono min-h-[44px] transition-colors",
                    viewport === "desktop"
                      ? "bg-teal text-white"
                      : "border border-line text-gray-600 hover:text-ink"
                  )}
                >
                  <Monitor className="w-3.5 h-3.5" aria-hidden="true" />
                  Desktop
                </button>
                <button
                  type="button"
                  onClick={() => setViewport("mobile")}
                  aria-pressed={viewport === "mobile"}
                  className={cn(
                    "inline-flex items-center gap-1.5 px-3 py-2 rounded-md text-xs font-mono min-h-[44px] transition-colors",
                    viewport === "mobile"
                      ? "bg-teal text-white"
                      : "border border-line text-gray-600 hover:text-ink"
                  )}
                >
                  <Smartphone className="w-3.5 h-3.5" aria-hidden="true" />
                  Mobile
                </button>
              </div>
            </div>

            <BrowserFrame url={`demo://${example.theme}`}>
              <div className="p-3 md:p-4">
                <div className="mb-3 px-3 py-2 bg-gray-100 rounded text-xs font-mono text-gray-600 truncate">
                  &ldquo;{displayPrompt}&rdquo;
                </div>
                <PreviewPanel example={example} viewport={viewport} />
              </div>
            </BrowserFrame>

            <p className="mt-3 text-xs text-gray-400 font-mono">
              Preview themes adapt to product context — not a single house style.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
