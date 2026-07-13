"use client";

import { useState } from "react";
import Image from "next/image";
import { Menu, X } from "lucide-react";
import { GitHubIcon } from "@/components/ui/GitHubIcon";
import { REPO_URL } from "@/lib/plugin-version";

const NAV_ITEMS = [
  { label: "Product", href: "#product" },
  { label: "Live Demo", href: "#demo" },
  { label: "How It Works", href: "#workflow" },
  { label: "Architecture", href: "#architecture" },
  { label: "Install", href: "#install" },
];

export function Navigation() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-line bg-paper/95 backdrop-blur-sm shadow-sm">
      <nav aria-label="Main navigation">
        <div className="container-main flex items-center justify-between h-14 md:h-16 px-4 md:px-8">
          <a href="#" className="flex items-center gap-2.5 shrink-0">
            <Image
              src="/assets/icon.svg"
              alt=""
              width={32}
              height={32}
              className="rounded-md"
              aria-hidden="true"
            />
            <span className="font-mono text-sm font-medium tracking-tight hidden sm:inline">
              Frontend Taste Engineer
            </span>
          </a>

          <ul className="hidden lg:flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  className="px-3 py-2 text-sm text-gray-600 hover:text-ink rounded transition-colors"
                >
                  {item.label}
                </a>
              </li>
            ))}
            <li>
              <a
                href={REPO_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-2 btn-primary text-sm !min-h-[2.25rem] !py-1.5"
              >
                <GitHubIcon className="w-4 h-4" />
                GitHub
              </a>
            </li>
          </ul>

          <button
            type="button"
            className="lg:hidden min-h-[44px] min-w-[44px] flex items-center justify-center rounded"
            aria-expanded={mobileOpen}
            aria-controls="mobile-nav"
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {mobileOpen && (
          <div id="mobile-nav" className="lg:hidden border-t border-line bg-paper px-4 pb-4">
            <ul className="flex flex-col gap-1 pt-2">
              {NAV_ITEMS.map((item) => (
                <li key={item.href}>
                  <a
                    href={item.href}
                    className="block px-3 py-3 text-sm text-gray-600 hover:text-ink rounded min-h-[44px]"
                    onClick={() => setMobileOpen(false)}
                  >
                    {item.label}
                  </a>
                </li>
              ))}
              <li>
                <a
                  href={REPO_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-3 py-3 text-sm font-medium text-teal min-h-[44px]"
                >
                  <GitHubIcon className="w-4 h-4" />
                  GitHub
                </a>
              </li>
            </ul>
          </div>
        )}
      </nav>
    </header>
  );
}
