import { SectionHeading } from "@/components/ui/SectionHeading";

const INTENSITY_EXAMPLES = [
  { label: "Public service", level: 1, width: "20%" },
  { label: "Personal finance", level: 2, width: "40%" },
  { label: "Developer tool", level: 3, width: "60%" },
  { label: "Robotics team", level: 4, width: "80%" },
  { label: "Experimental personal page", level: 5, width: "100%" },
];

const FACTORS = [
  "Product type",
  "Audience",
  "Trust and risk",
  "Information density",
  "Frequency of use",
  "Seriousness",
  "Product maturity",
  "Accessibility",
  "Device context",
  "Experimental tolerance",
  "Familiarity requirements",
];

export function ContextAdaptiveTaste() {
  return (
    <section className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading
          title="Taste is contextual, not decorative."
          description={'“Premium,” “stunning,” and “world-class” do not automatically mean dark, cinematic, gradient-heavy, or highly animated. Visual intensity is inferred from product context — these examples are illustrative, not hardcoded rules.'}
        />

        <div className="grid lg:grid-cols-2 gap-10 lg:gap-16">
          <div>
            <p className="font-mono text-xs text-gray-600 mb-4 uppercase tracking-wider">
              Contextual intensity scale
            </p>
            <div className="space-y-4" role="img" aria-label="Intensity scale from 1 to 5">
              {INTENSITY_EXAMPLES.map((ex) => (
                <div key={ex.label}>
                  <div className="flex justify-between items-baseline mb-1.5">
                    <span className="text-sm text-ink">{ex.label}</span>
                    <span className="font-mono text-xs text-teal">{ex.level}</span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-teal rounded-full transition-all"
                      style={{ width: ex.width }}
                    />
                  </div>
                </div>
              ))}
            </div>
            <p className="mt-4 text-xs text-gray-400 font-mono">
              Illustrative examples — actual intensity is inferred per request.
            </p>
          </div>

          <div>
            <p className="font-mono text-xs text-gray-600 mb-4 uppercase tracking-wider">
              Factors considered
            </p>
            <ul className="grid grid-cols-2 gap-x-4 gap-y-2">
              {FACTORS.map((factor) => (
                <li
                  key={factor}
                  className="text-sm text-gray-600 flex items-center gap-2"
                >
                  <span className="w-1 h-1 rounded-full bg-mint shrink-0" aria-hidden="true" />
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
