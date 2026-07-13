import { SectionHeading } from "@/components/ui/SectionHeading";

const FRAMEWORKS = [
  "HTML/CSS/JavaScript",
  "React",
  "Next.js",
  "Vue",
  "Nuxt",
  "Svelte",
  "SvelteKit",
  "Astro",
  "Web Components",
];

const WORK_TYPES = [
  "Landing pages",
  "Product surfaces",
  "Application frontends",
  "Existing redesigns",
  "Screenshot reconstruction",
  "Component systems",
  "Design systems",
  "Accessibility repair",
  "Performance repair",
  "Motion refinement",
  "Visual audits",
];

export function SupportedWork() {
  return (
    <section className="section-padding">
      <div className="container-main">
        <SectionHeading
          title="Supported work"
          description="Framework support varies by project context. Not every framework has identical tooling or guaranteed output."
        />

        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <h3 className="font-mono text-xs text-gray-600 mb-4 uppercase tracking-wider">
              Frameworks
            </h3>
            <div className="border border-line rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <tbody>
                  {FRAMEWORKS.map((fw, i) => (
                    <tr
                      key={fw}
                      className={i > 0 ? "border-t border-line" : ""}
                    >
                      <td className="px-4 py-3 text-ink">{fw}</td>
                      <td className="px-4 py-3 text-right">
                        <span className="inline-block w-2 h-2 rounded-full bg-teal" aria-label="Supported" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div>
            <h3 className="font-mono text-xs text-gray-600 mb-4 uppercase tracking-wider">
              Work types
            </h3>
            <div className="border border-line rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <tbody>
                  {WORK_TYPES.map((wt, i) => (
                    <tr
                      key={wt}
                      className={i > 0 ? "border-t border-line" : ""}
                    >
                      <td className="px-4 py-3 text-ink">{wt}</td>
                      <td className="px-4 py-3 text-right">
                        <span className="inline-block w-2 h-2 rounded-full bg-teal" aria-label="Supported" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
