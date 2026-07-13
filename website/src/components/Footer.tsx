import { PLUGIN_VERSION, REPO_URL } from "@/lib/plugin-version";

export function Footer() {
  return (
    <footer className="border-t border-line bg-paper py-10 px-4">
      <div className="container-main">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 text-sm text-gray-600">
          <div>
            <p className="font-medium text-ink">Frontend Taste Engineer</p>
            <p className="mt-1">
              Created by{" "}
              <a
                href="https://github.com/arnavsri993"
                className="text-teal hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                arnavsri993
              </a>
            </p>
          </div>
          <ul className="flex flex-wrap gap-x-6 gap-y-2">
            <li>
              <a href={`${REPO_URL}/blob/main/LICENSE`} className="hover:text-ink transition-colors">
                MIT License
              </a>
            </li>
            <li>
              <a href={REPO_URL} className="hover:text-ink transition-colors">
                GitHub repository
              </a>
            </li>
            <li>
              <span className="text-gray-400">No analytics or telemetry</span>
            </li>
            <li>
              <span className="font-mono text-xs text-gray-400">v{PLUGIN_VERSION}</span>
            </li>
          </ul>
        </div>
      </div>
    </footer>
  );
}
