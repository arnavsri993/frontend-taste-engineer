"use client";

import { CopyButton } from "@/components/ui/CopyButton";
import { INSTALL_COMMANDS } from "@/lib/demo-data";
import { REPO_URL } from "@/lib/plugin-version";

export function FinalCTA() {
  return (
    <section className="section-padding bg-teal text-white">
      <div className="container-main text-center max-w-2xl mx-auto">
        <h2 className="heading-display text-3xl md:text-4xl mb-4">
          A frontend should survive inspection, not just generate applause.
        </h2>
        <p className="text-lg text-white/80 mb-8 leading-relaxed">
          Give Codex a minimal prompt. Frontend Taste Engineer handles the brief, direction,
          implementation, refinement, and verification.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 min-h-[44px] px-5 py-2.5 bg-white text-teal font-medium rounded-md hover:bg-paper transition-colors"
          >
            View on GitHub
          </a>
          <CopyButton
            text={INSTALL_COMMANDS}
            label="Copy install commands"
            variant="inverse"
          />
        </div>
      </div>
    </section>
  );
}
