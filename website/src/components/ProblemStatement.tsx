import { SectionHeading } from "@/components/ui/SectionHeading";
import { X, Check } from "lucide-react";

const TYPICAL = [
  "Produces a hero and several cards",
  "Reuses a fashionable visual formula",
  "Leaves incomplete states",
  "Treats accessibility as cleanup",
  "Stops before runtime inspection",
  "Reports success without evidence",
];

const FTE = [
  "Builds from a product and UX brief",
  "Selects a context-specific visual direction",
  "Writes finished original copy",
  "Implements behavior and relevant states",
  "Reviews desktop and mobile screenshots",
  "Runs production verification",
  "Reports remaining limitations honestly",
];

export function ProblemStatement() {
  return (
    <section className="section-padding">
      <div className="container-main">
        <SectionHeading
          title="Most frontend agents stop when the page looks plausible."
          description="A convincing screenshot is not the same as a complete product. Dead controls, placeholder copy, inaccessible interactions, broken mobile layouts, fabricated proof, unnecessary JavaScript, and unverified claims still count as failure."
        />

        <div className="grid md:grid-cols-2 gap-6 md:gap-8">
          <div className="border border-line rounded-lg p-6 md:p-8 bg-paper-elevated">
            <div className="flex items-center gap-2 mb-6">
              <span className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
                <X className="w-4 h-4 text-gray-400" aria-hidden="true" />
              </span>
              <h3 className="font-mono text-sm font-medium text-gray-600">
                Typical generator
              </h3>
            </div>
            <ul className="space-y-3">
              {TYPICAL.map((item) => (
                <li key={item} className="flex gap-3 text-sm text-gray-600">
                  <span className="text-gray-300 shrink-0 mt-0.5" aria-hidden="true">
                    —
                  </span>
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div className="border-2 border-teal/30 rounded-lg p-6 md:p-8 bg-teal-muted/20">
            <div className="flex items-center gap-2 mb-6">
              <span className="w-8 h-8 rounded-full bg-teal/10 flex items-center justify-center">
                <Check className="w-4 h-4 text-teal" aria-hidden="true" />
              </span>
              <h3 className="font-mono text-sm font-medium text-teal">
                Frontend Taste Engineer
              </h3>
            </div>
            <ul className="space-y-3">
              {FTE.map((item) => (
                <li key={item} className="flex gap-3 text-sm text-ink">
                  <span className="text-teal shrink-0 mt-0.5" aria-hidden="true">
                    ✓
                  </span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
