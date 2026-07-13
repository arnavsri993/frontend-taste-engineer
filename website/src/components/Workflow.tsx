import { SectionHeading } from "@/components/ui/SectionHeading";
import { ArrowRight } from "lucide-react";

const STEPS = [
  "Inspect",
  "Classify",
  "Brief",
  "Direct",
  "Build",
  "Run",
  "Capture",
  "Critique",
  "Fix",
  "Verify",
];

const DETAILS = [
  "Inspects the existing project first",
  "Separates supplied facts from reversible assumptions",
  "Writes a product brief and design thesis",
  "Retrieves only stage-relevant guidance",
  "Implements complete content and behavior",
  "Captures meaningful desktop and mobile screenshots",
  "Fixes the three highest-impact weaknesses",
  "Runs the production build and applicable checks",
  "Reports evidence and unresolved limits",
];

export function Workflow() {
  return (
    <section id="workflow" className="section-padding measure-marks">
      <div className="container-main">
        <SectionHeading title="From seven words to a verified implementation." />

        <div className="overflow-x-auto pb-4 -mx-4 px-4 md:mx-0 md:px-0">
          <ol
            className="flex items-center gap-1 min-w-max md:min-w-0 md:flex-wrap md:justify-center mb-10"
            aria-label="Workflow steps"
          >
            {STEPS.map((step, i) => (
              <li key={step} className="flex items-center">
                <span className="px-3 py-2 bg-paper border border-line rounded-md font-mono text-xs text-ink whitespace-nowrap">
                  {step}
                </span>
                {i < STEPS.length - 1 && (
                  <ArrowRight
                    className="w-3.5 h-3.5 text-gray-300 mx-0.5 shrink-0 hidden sm:block"
                    aria-hidden="true"
                  />
                )}
              </li>
            ))}
          </ol>
        </div>

        <ul className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl">
          {DETAILS.map((detail) => (
            <li
              key={detail}
              className="flex gap-3 text-sm text-gray-600 leading-relaxed"
            >
              <span className="w-1.5 h-1.5 rounded-full bg-teal shrink-0 mt-2" aria-hidden="true" />
              {detail}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
