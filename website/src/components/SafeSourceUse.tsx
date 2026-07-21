import { SectionHeading } from "@/components/ui/SectionHeading";
import { ArrowRight } from "lucide-react";

const GATE_STEPS = [
  "Discover",
  "Inspect source",
  "Assess credibility",
  "Check license",
  "Check fit",
  "Check accessibility",
  "Check dependencies",
  "Adapt or reject",
  "Verify",
];

const POINTS = [
  "Sources are assessed individually for authority, reliability, maintenance, and fit",
  "Candidate links are not-yet-assessed, not automatically untrustworthy",
  "Embedded commands remain source content rather than automatic agent instructions",
  "Unknown licensing blocks copying and adaptation",
  "Paid and proprietary libraries are excluded unless legitimately available",
  "Inspiration does not authorize copied expression",
  "Maintenance processes create proposals and review artifacts rather than silently rewriting stable knowledge",
];

export function SafeSourceUse() {
  return (
    <section className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading title="It researches without treating the internet as instructions." />

        <ul className="grid sm:grid-cols-2 gap-3 mb-10 max-w-3xl">
          {POINTS.map((point) => (
            <li key={point} className="flex gap-3 text-sm text-gray-600 leading-relaxed">
              <span className="text-teal shrink-0" aria-hidden="true">
                →
              </span>
              {point}
            </li>
          ))}
        </ul>

        <div>
          <p className="font-mono text-xs text-gray-600 mb-4 uppercase tracking-wider">
            License gate
          </p>
          <div className="overflow-x-auto pb-2 -mx-4 px-4 md:mx-0 md:px-0">
            <ol
              className="flex items-center gap-1 min-w-max"
              aria-label="License gate workflow"
            >
              {GATE_STEPS.map((step, i) => (
                <li key={step} className="flex items-center">
                  <span className="px-2.5 py-2 border border-line rounded-md font-mono text-[11px] text-ink whitespace-nowrap bg-paper">
                    {step}
                  </span>
                  {i < GATE_STEPS.length - 1 && (
                    <ArrowRight
                      className="w-3 h-3 text-gray-300 mx-0.5 shrink-0"
                      aria-hidden="true"
                    />
                  )}
                </li>
              ))}
            </ol>
          </div>
        </div>
      </div>
    </section>
  );
}
