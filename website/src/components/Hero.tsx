import { BrowserFrame } from "@/components/ui/BrowserFrame";
import { REPO_URL } from "@/lib/plugin-version";

const PROOF_ITEMS = [
  "Responsive by default",
  "Accessibility built into implementation",
  "Screenshot refinement loop",
  "Production verification",
  "MIT licensed",
];

export function Hero() {
  return (
    <section id="product" className="section-padding grid-bg relative overflow-hidden">
      <div className="container-main relative">
        <div className="grid lg:grid-cols-2 gap-10 lg:gap-16 items-center">
          <div>
            <p className="eyebrow mb-4">Codex plugin · Open source · MIT licensed</p>
            <h1 className="heading-display text-4xl sm:text-5xl lg:text-[3.25rem] text-ink mb-6">
              Give it one sentence. Get a frontend with taste.
            </h1>
            <p className="text-lg text-gray-600 leading-relaxed mb-8 max-w-xl">
              Frontend Taste Engineer turns minimal requests into complete, context-aware web
              experiences. It plans, writes, builds, audits, screenshot-refines, and verifies the
              result instead of stopping at an attractive first draft.
            </p>
            <div className="flex flex-wrap gap-3 mb-10">
              <a href="#demo" className="btn-primary">
                Try the interactive demo
              </a>
              <a
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary"
              >
                View the repository
              </a>
            </div>
            <ul className="flex flex-wrap gap-x-4 gap-y-2" aria-label="Key capabilities">
              {PROOF_ITEMS.map((item) => (
                <li
                  key={item}
                  className="text-xs font-mono text-gray-600 flex items-center gap-1.5"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-teal shrink-0" aria-hidden="true" />
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div aria-label="Workflow inspection preview" role="img">
            <BrowserFrame url="inspect://frontend-taste-engineer">
              <div className="p-4 md:p-5 space-y-4 text-sm">
                <div className="border border-line rounded-md p-3 bg-teal-muted/30">
                  <p className="font-mono text-xs text-gray-600 mb-1">User prompt</p>
                  <p className="text-ink">&ldquo;Make a website for my robotics team.&rdquo;</p>
                </div>

                <div className="grid sm:grid-cols-2 gap-3">
                  <div className="border border-line rounded-md p-3">
                    <p className="font-mono text-xs text-teal mb-1">Product brief</p>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Team landing page for recruiting members and showcasing projects.
                    </p>
                  </div>
                  <div className="border border-line rounded-md p-3">
                    <p className="font-mono text-xs text-teal mb-1">Design thesis</p>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Precision engineering through bold geometry and kinetic accents.
                    </p>
                  </div>
                </div>

                <div className="relative border border-line rounded-md overflow-hidden">
                  <div className="bg-[#1A2424] p-4 text-[#E8EDEB]">
                    <p className="font-mono text-[10px] text-[#FFCF70] mb-1">PREVIEW</p>
                    <p className="font-mono text-sm font-bold tracking-wide">ROBOTICS TEAM</p>
                    <p className="text-xs text-gray-400 mt-1">Building machines that compete</p>
                  </div>
                  <div
                    className="absolute top-2 right-2 flex items-center gap-1"
                    aria-hidden="true"
                  >
                    <span className="w-2 h-2 rounded-full border border-teal bg-teal/20" />
                    <span className="text-[10px] font-mono text-teal">refine</span>
                  </div>
                  <div
                    className="absolute bottom-2 left-2 flex items-center gap-1"
                    aria-hidden="true"
                  >
                    <span className="w-2 h-2 rounded-full border border-gold bg-gold/20" />
                    <span className="text-[10px] font-mono text-gold">mobile overflow</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 border border-teal/30 bg-teal-muted/20 rounded-md px-3 py-2">
                  <span className="font-mono text-xs text-teal shrink-0">Verification</span>
                  <span className="text-xs text-gray-600 leading-snug">
                    Build pass · Keyboard pass · 1 limitation noted
                  </span>
                </div>
              </div>
            </BrowserFrame>
          </div>
        </div>
      </div>
    </section>
  );
}
