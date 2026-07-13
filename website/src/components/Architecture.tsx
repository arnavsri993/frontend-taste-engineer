import { SectionHeading } from "@/components/ui/SectionHeading";
import { ArrowDown } from "lucide-react";

const LAYERS = [
  {
    title: "Operating Skill",
    items: [
      "Classification",
      "Mandatory principles",
      "Workflow selection",
      "Completion gates",
    ],
    color: "border-teal bg-teal-muted/30",
  },
  {
    title: "Local MCP retrieval",
    items: [
      "Metadata filtering",
      "Exact matching",
      "Lexical retrieval",
      "Concept expansion",
      "Reranking",
      "Deduplication",
      "Context budgeting",
    ],
    color: "border-line bg-paper",
  },
  {
    title: "Canonical knowledge corpus",
    items: [
      "Product and UX",
      "Typography",
      "Composition",
      "Components",
      "Accessibility",
      "Motion",
      "Performance",
      "Responsive behavior",
      "Verification",
    ],
    color: "border-line bg-paper-elevated",
  },
  {
    title: "Safe external-source catalog",
    items: [
      "395 seed sources",
      "15 source families",
      "License gates",
      "Anti-copy rules",
      "Inspiration-only classification",
    ],
    color: "border-line bg-paper",
  },
  {
    title: "Verification",
    items: [
      "Runtime inspection",
      "Desktop and mobile screenshots",
      "Production build",
      "Accessibility checks",
      "Honest completion report",
    ],
    color: "border-teal/50 bg-teal-muted/20",
  },
];

export function Architecture() {
  return (
    <section id="architecture" className="section-padding grid-bg">
      <div className="container-main">
        <SectionHeading title="A compact operating skill backed by a deep system." />

        <div className="flex flex-col items-center gap-3 max-w-2xl mx-auto">
          {LAYERS.map((layer, i) => (
            <div key={layer.title} className="w-full">
              <article
                className={`border rounded-lg p-5 md:p-6 ${layer.color}`}
              >
                <h3 className="font-mono text-sm font-medium text-teal mb-3">
                  {i + 1}. {layer.title}
                </h3>
                <ul className="flex flex-wrap gap-2">
                  {layer.items.map((item) => (
                    <li
                      key={item}
                      className="px-2.5 py-1 bg-paper/80 border border-line rounded text-xs text-gray-600"
                    >
                      {item}
                    </li>
                  ))}
                </ul>
              </article>
              {i < LAYERS.length - 1 && (
                <div className="flex justify-center py-1" aria-hidden="true">
                  <ArrowDown className="w-4 h-4 text-gray-300" />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
