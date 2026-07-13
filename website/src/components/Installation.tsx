import { SectionHeading } from "@/components/ui/SectionHeading";
import { CopyButton } from "@/components/ui/CopyButton";
import { INSTALL_COMMANDS, VALIDATION_COMMANDS } from "@/lib/demo-data";

export function Installation() {
  return (
    <section id="install" className="section-padding">
      <div className="container-main">
        <SectionHeading title="Install it locally." />

        <div className="space-y-8 max-w-3xl">
          <div>
            <div className="flex items-center justify-between mb-2">
              <p className="font-mono text-xs text-gray-600 uppercase tracking-wider">
                Installation
              </p>
              <CopyButton text={INSTALL_COMMANDS} label="Copy" />
            </div>
            <div className="terminal-block">
              <code>{INSTALL_COMMANDS}</code>
            </div>
          </div>

          <ol className="space-y-2 text-sm text-gray-600 list-decimal list-inside">
            <li>Clone the repository first</li>
            <li>Add the repository marketplace once</li>
            <li>Install the plugin</li>
            <li>
              Start a new Codex task so bundled Skills and MCP tools are discovered
            </li>
            <li>Review and trust the plugin hook through <code className="font-mono text-xs bg-gray-100 px-1 rounded">/hooks</code></li>
            <li>Installed plugins do not automatically trust command hooks</li>
          </ol>

          <div>
            <div className="flex items-center justify-between mb-2">
              <p className="font-mono text-xs text-gray-600 uppercase tracking-wider">
                Validation
              </p>
              <CopyButton text={VALIDATION_COMMANDS} label="Copy" />
            </div>
            <div className="terminal-block">
              <code>{VALIDATION_COMMANDS}</code>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
