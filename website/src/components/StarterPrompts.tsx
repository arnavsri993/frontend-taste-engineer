import { SectionHeading } from "@/components/ui/SectionHeading";
import { CopyButton } from "@/components/ui/CopyButton";
import { STARTER_PROMPTS } from "@/lib/demo-data";

export function StarterPrompts() {
  return (
    <section className="section-padding bg-paper-elevated border-y border-line">
      <div className="container-main">
        <SectionHeading title="Start small. It handles the missing brief." />

        <ul className="space-y-3">
          {STARTER_PROMPTS.map((prompt) => (
            <li
              key={prompt}
              className="flex items-start gap-2 border border-line rounded-md bg-paper p-4"
            >
              <p className="flex-1 text-sm text-ink leading-relaxed font-mono">
                {prompt}
              </p>
              <CopyButton text={prompt} label="Copy" className="shrink-0" />
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
