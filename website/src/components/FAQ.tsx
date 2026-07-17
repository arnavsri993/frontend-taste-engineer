"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { cn } from "@/lib/utils";

const FAQ_ITEMS = [
  {
    q: "What is Frontend Taste Engineer?",
    a: "An installable Codex plugin that expands minimal frontend requests into complete, context-aware, responsive, accessible, screenshot-refined, deployment-ready implementations. It combines a compact operating Skill, local MCP retrieval, a knowledge corpus, and a safely gated source catalog.",
  },
  {
    q: "Is this a standalone application?",
    a: "No. It is a Codex plugin that runs within Codex tasks. The optional local review UI is a separate inspection tool, not a standalone product.",
  },
  {
    q: "Does it work without network access?",
    a: "Yes, for core operation. The local MCP server reads local plugin data and does not require credentials or network access. External source research is optional and gated.",
  },
  {
    q: "Can it redesign an existing frontend?",
    a: "Yes. The existing-product redesign mode inspects the current product, records evidence-backed defects, and makes targeted changes without needless rewrites.",
  },
  {
    q: "Can it rebuild a supplied screenshot?",
    a: "Yes. Screenshot reconstruction mode analyzes visual evidence, implements section by section, and preserves semantics and keyboard operation even when the screenshot does not expose them.",
  },
  {
    q: "Does it support accessibility work?",
    a: "Yes. Accessibility is built into implementation, not treated as cleanup. Dedicated accessibility remediation mode repairs semantic, keyboard, focus, and contrast failures.",
  },
  {
    q: "Does it automatically copy components from external sites?",
    a: "No. Sources are assessed individually: reviewed sources report scoped credibility, reliability evidence, and license status, while candidate links remain not-yet-assessed. Embedded commands stay source content rather than agent instructions. Unknown licensing still blocks copying and adaptation.",
  },
  {
    q: "Which frontend frameworks are supported?",
    a: "HTML/CSS/JavaScript, React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Astro, Web Components, and common styling systems. Support varies by project context.",
  },
  {
    q: "Does the interactive website demo run the actual plugin?",
    a: "No. The Taste Lab demo is an illustrative workflow preview. It shows how the plugin structures work but does not call the plugin or any API.",
  },
  {
    q: "How do I install it?",
    a: 'Clone the repository, run `codex plugin marketplace add "$(pwd)"`, then `codex plugin add frontend-taste-engineer@personal`. Start a new Codex task and review hooks through /hooks.',
  },
];

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="section-padding">
      <div className="container-main">
        <SectionHeading title="FAQ" />

        <div className="max-w-3xl divide-y divide-line border border-line rounded-lg overflow-hidden">
          {FAQ_ITEMS.map((item, i) => {
            const isOpen = openIndex === i;
            return (
              <div key={item.q}>
                <h3>
                  <button
                    type="button"
                    id={`faq-trigger-${i}`}
                    aria-expanded={isOpen}
                    aria-controls={`faq-panel-${i}`}
                    onClick={() => setOpenIndex(isOpen ? null : i)}
                    className="flex items-center justify-between w-full px-5 py-4 text-left text-sm font-medium text-ink hover:bg-gray-100/50 transition-colors min-h-[44px]"
                  >
                    {item.q}
                    <ChevronDown
                      className={cn(
                        "w-4 h-4 text-gray-400 shrink-0 ml-4 transition-transform",
                        isOpen && "rotate-180"
                      )}
                      aria-hidden="true"
                    />
                  </button>
                </h3>
                {isOpen && (
                  <div
                    id={`faq-panel-${i}`}
                    role="region"
                    aria-labelledby={`faq-trigger-${i}`}
                    className="px-5 pb-4"
                  >
                    <p className="text-sm text-gray-600 leading-relaxed">{item.a}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
