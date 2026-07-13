import { SectionHeading } from "@/components/ui/SectionHeading";

const MODES = [
  {
    id: "autonomous",
    name: "Autonomous zero-brief build",
    description:
      "Default for minimal requests. Infers a product brief, design thesis, and complete implementation from a short prompt without routine creative questions.",
    highlight: true,
  },
  {
    id: "greenfield",
    name: "Greenfield build",
    description:
      "New page, product surface, or application when the user supplies a substantive brief.",
  },
  {
    id: "redesign",
    name: "Existing-product redesign",
    description:
      "Improve an existing interface with evidence-backed changes, preserving working architecture.",
  },
  {
    id: "screenshot",
    name: "Screenshot reconstruction",
    description:
      "Reproduce supplied visual evidence responsively while preserving semantics and keyboard operation.",
  },
  {
    id: "component",
    name: "Component build",
    description:
      "Implement one reusable, stateful component with a complete state matrix and keyboard behavior.",
  },
  {
    id: "design-system",
    name: "Design-system work",
    description:
      "Create, extend, audit, or migrate tokens and components with migration planning.",
  },
  {
    id: "visual-audit",
    name: "Visual audit",
    description:
      "Diagnose quality issues with severity, evidence, and specific corrections ranked by impact.",
  },
  {
    id: "motion",
    name: "Motion refinement",
    description:
      "Improve transition and interaction behavior at runtime, including reduced-motion support.",
  },
  {
    id: "a11y",
    name: "Accessibility remediation",
    description:
      "Repair semantic, keyboard, focus, contrast, or assistive-technology failures.",
  },
  {
    id: "perf",
    name: "Performance remediation",
    description:
      "Improve measured delivery, rendering, or interaction cost with proportionate budgets.",
  },
];

export function CapabilitySystem() {
  return (
    <section className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading title="One plugin, several operating modes." />

        <div className="space-y-0 border border-line rounded-lg overflow-hidden">
          {MODES.map((mode, i) => (
            <article
              key={mode.id}
              className={`grid md:grid-cols-[14rem_1fr] gap-2 md:gap-6 px-5 py-4 md:py-5 ${
                i > 0 ? "border-t border-line" : ""
              } ${mode.highlight ? "bg-teal-muted/30" : "bg-paper"}`}
            >
              <h3
                className={`font-mono text-sm font-medium ${
                  mode.highlight ? "text-teal" : "text-ink"
                }`}
              >
                {mode.name}
                {mode.highlight && (
                  <span className="ml-2 text-[10px] uppercase tracking-wider text-teal/70 font-normal">
                    default
                  </span>
                )}
              </h3>
              <p className="text-sm text-gray-600 leading-relaxed">{mode.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
