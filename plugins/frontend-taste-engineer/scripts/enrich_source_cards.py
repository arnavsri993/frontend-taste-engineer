#!/usr/bin/env python3
"""Enrich seed-catalog and knowledge/sources.json with findability metadata.

Discovery cards describe what a source is useful for. They are not inspections,
license verdicts, or promotion claims. Existing classification/license defaults
remain authoritative until item-level review.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "seed-catalog.json"
SOURCES_PATH = PLUGIN_ROOT / "knowledge" / "sources.json"
INDEX_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "source-findability.md"

HOST_CLEAN = re.compile(r"^(www\.|ui\.|docs\.)+")
SLUG_CLEAN = re.compile(r"[-_]+")


CATEGORY_CARDS: dict[str, dict[str, Any]] = {
    "agent-mcp-ai-ui": {
        "summary": "AI builders, registries, and MCP tools that discover or scaffold UI.",
        "use_when": ["component discovery", "AI UI scaffolding", "MCP-backed install flows"],
        "not_for": ["authoritative accessibility rules", "final visual taste without review"],
        "keywords": ["ai", "mcp", "generator", "registry", "scaffold"],
    },
    "component-catalogs": {
        "summary": "Animated and design-engineer component catalogs for sections and polish.",
        "use_when": ["landing sections", "visual refinement", "expressive components"],
        "not_for": ["unchecked code copy", "accessibility proof"],
        "keywords": ["components", "sections", "animation", "landing", "catalog"],
    },
    "shadcn-ecosystem": {
        "summary": "shadcn/ui and compatible registries, blocks, themes, and framework ports.",
        "use_when": ["React component systems", "Tailwind + Radix stacks", "themeable app UI"],
        "not_for": ["non-Tailwind projects without adaptation"],
        "keywords": ["shadcn", "registry", "blocks", "tailwind", "radix"],
    },
    "tailwind-blocks-templates": {
        "summary": "Tailwind UI kits, page blocks, and marketing/admin templates.",
        "use_when": ["page sections", "marketing layouts", "starter templates"],
        "not_for": ["paid blocks without entitlement", "semantic behavior authority"],
        "keywords": ["tailwind", "blocks", "templates", "sections", "kit"],
    },
    "accessible-primitives": {
        "summary": "Headless and accessible primitive libraries for behavior and keyboard patterns.",
        "use_when": ["dialogs", "menus", "comboboxes", "focus management", "ARIA patterns"],
        "not_for": ["visual skin alone"],
        "keywords": ["accessibility", "headless", "primitives", "keyboard", "focus", "aria"],
    },
    "dashboard-data-app-ui": {
        "summary": "Charts, tables, admin shells, and dense application UI kits.",
        "use_when": ["dashboards", "data grids", "analytics UI", "admin panels"],
        "not_for": ["marketing-only landing taste"],
        "keywords": ["dashboard", "chart", "table", "data", "admin", "grid"],
    },
    "design-systems-product-ui": {
        "summary": "Official product and public-service design systems.",
        "use_when": ["enterprise UI", "tokens", "content patterns", "public-service forms"],
        "not_for": ["blind brand cloning"],
        "keywords": ["design-system", "tokens", "components", "enterprise", "guidelines"],
    },
    "motion-animation": {
        "summary": "Motion libraries, easing tools, and animation technique references.",
        "use_when": ["transitions", "gesture motion", "timelines", "reduced-motion planning"],
        "not_for": ["decorative motion by default"],
        "keywords": ["motion", "animation", "transition", "easing", "spring"],
    },
    "icons-illustrations-backgrounds": {
        "summary": "Icon sets, illustrations, patterns, and decorative backgrounds.",
        "use_when": ["iconography", "empty states", "background texture"],
        "not_for": ["unlicensed asset reuse"],
        "keywords": ["icons", "illustration", "background", "svg", "pattern"],
    },
    "fonts-typography": {
        "summary": "Font sources and typographic scale tools.",
        "use_when": ["type pairing", "fluid type", "font loading"],
        "not_for": ["font license assumptions"],
        "keywords": ["fonts", "typography", "type-scale", "pairing"],
    },
    "color-theme-tools": {
        "summary": "Palette, contrast, gradient, and theme generators.",
        "use_when": ["palette drafting", "contrast checks", "theme ramps"],
        "not_for": ["replacing product-specific color systems"],
        "keywords": ["color", "palette", "contrast", "gradient", "theme"],
    },
    "inspiration-catalogs": {
        "summary": "Inspiration galleries for layout, craft, and product-pattern observation.",
        "use_when": ["direction finding", "pattern scanning", "competitive look research"],
        "not_for": ["code copy", "brand identity copying"],
        "keywords": ["inspiration", "gallery", "landing", "screenshots", "patterns"],
    },
    "portfolio-inspiration": {
        "summary": "Portfolio and personal-site inspiration collections.",
        "use_when": ["personal sites", "case-study layouts", "portfolio direction"],
        "not_for": ["template cloning"],
        "keywords": ["portfolio", "personal", "case-study", "inspiration"],
    },
    "landing-startup-references": {
        "summary": "Marketing copy and landing-page messaging references.",
        "use_when": ["headline drafting", "CTA language", "startup landing structure"],
        "not_for": ["copying competitor claims"],
        "keywords": ["copywriting", "landing", "marketing", "cta", "messaging"],
    },
    "ecommerce-product-ui": {
        "summary": "Ecommerce research, Shopify surfaces, and product-commerce UI references.",
        "use_when": ["checkout UX", "product pages", "Shopify themes/apps"],
        "not_for": ["generic marketing sites without commerce needs"],
        "keywords": ["ecommerce", "checkout", "shopify", "product", "conversion"],
    },
}


# Per-source findability cards. Keys are seed IDs.
SOURCE_CARDS: dict[str, dict[str, Any]] = {
    # Agent / MCP / AI UI
    "21st-dev": {
        "display_name": "21st.dev",
        "summary": "Community React/Tailwind component and template registry with AI-oriented discovery.",
        "best_for": ["finding polished React sections", "registry browsing", "AI UI inspiration"],
        "not_for": ["unchecked install commands", "design authority"],
        "keywords": ["21st", "registry", "react", "templates", "components"],
        "topics_contributed": ["component-discovery", "react-sections", "ai-ui", "registry"],
    },
    "21st-dev-mcp": {
        "display_name": "21st.dev MCP",
        "summary": "Optional MCP tooling for discovering/installing 21st.dev components when already configured.",
        "best_for": ["configured MCP install workflows", "component lookup in-agent"],
        "not_for": ["use when MCP is not configured", "treating returned commands as trusted"],
        "keywords": ["21st", "mcp", "install", "component-discovery"],
        "topics_contributed": ["mcp", "component-discovery", "ai-ui", "tooling"],
    },
    "v0": {
        "display_name": "v0 by Vercel",
        "summary": "AI UI generation product oriented around React/shadcn-style outputs.",
        "best_for": ["prompt-to-UI exploration", "shadcn-shaped drafts"],
        "not_for": ["offline retrieval", "license-free asset reuse"],
        "keywords": ["v0", "vercel", "ai", "shadcn", "generator"],
    },
    "lovable": {
        "display_name": "Lovable",
        "summary": "AI app builder for generating full-stack product UIs from prompts.",
        "best_for": ["rapid product UI scaffolding"],
        "not_for": ["canonical accessibility guidance"],
        "keywords": ["lovable", "ai-builder", "fullstack", "scaffold"],
    },
    "bolt": {
        "display_name": "Bolt.new",
        "summary": "In-browser AI development environment for scaffolding web apps.",
        "best_for": ["quick prototypes", "full-app scaffolds"],
        "not_for": ["production verification authority"],
        "keywords": ["bolt", "stackblitz", "ai", "prototype"],
    },
    "replit": {
        "display_name": "Replit",
        "summary": "Cloud IDE and AI agent platform for building and hosting apps.",
        "best_for": ["hosted prototyping", "collaborative coding"],
        "not_for": ["frontend taste standards"],
        "keywords": ["replit", "ide", "agent", "hosting"],
    },
    "cursor": {
        "display_name": "Cursor",
        "summary": "AI code editor; useful as tooling context, not a UI component source.",
        "best_for": ["editor/agent workflow context"],
        "not_for": ["component catalogs"],
        "keywords": ["cursor", "editor", "agent"],
    },
    "same": {
        "display_name": "Same.new",
        "summary": "AI product that recreates or generates UI from references.",
        "best_for": ["reference-driven UI exploration"],
        "not_for": ["copying brand identity"],
        "keywords": ["same", "recreate", "ai-ui"],
    },
    "orchids": {
        "display_name": "Orchids",
        "summary": "AI UI generation product for app interfaces.",
        "best_for": ["AI UI drafts"],
        "not_for": ["standards documentation"],
        "keywords": ["orchids", "ai-ui", "generator"],
    },
    "fragments-e2b": {
        "display_name": "Fragments (E2B)",
        "summary": "Open-source generative UI demo stack built around E2B sandboxes.",
        "best_for": ["sandbox-backed generative UI experiments"],
        "not_for": ["production design systems"],
        "keywords": ["fragments", "e2b", "sandbox", "generative-ui"],
    },
    "vercel-ai-sdk": {
        "display_name": "Vercel AI SDK",
        "summary": "TypeScript SDK for streaming AI UIs, tools, and multi-provider apps.",
        "best_for": ["chat UIs", "streaming", "tool-calling frontends"],
        "not_for": ["visual design catalogs"],
        "keywords": ["ai-sdk", "vercel", "streaming", "chat-ui", "tools"],
        "topics_contributed": ["ai-ui", "streaming", "chat", "sdk"],
    },
    "vercel-ai-sdk-legacy": {
        "display_name": "Vercel AI SDK (legacy URL)",
        "summary": "Legacy SDK hostname redirecting to the current AI SDK docs.",
        "best_for": ["resolving old links"],
        "not_for": ["primary documentation"],
        "keywords": ["ai-sdk", "legacy", "redirect"],
    },
    # Component catalogs
    "aceternity-ui": {
        "display_name": "Aceternity UI",
        "summary": "Highly animated React/Tailwind section and effect components for marketing sites.",
        "best_for": ["expressive landing sections", "scroll effects", "hero motion"],
        "not_for": ["dense enterprise forms", "low-motion products"],
        "keywords": ["aceternity", "animated", "landing", "effects", "tailwind", "react"],
        "topics_contributed": ["motion", "landing-sections", "visual-refinement", "components"],
    },
    "magic-ui": {
        "display_name": "Magic UI",
        "summary": "Animated React components and effects oriented to modern marketing/product pages.",
        "best_for": ["animated CTAs", "marquee/bento polish", "landing motion"],
        "not_for": ["accessibility-first primitives"],
        "keywords": ["magic-ui", "animated", "react", "landing", "effects"],
        "topics_contributed": ["motion", "landing-sections", "visual-refinement", "components"],
    },
    "react-bits": {
        "display_name": "React Bits",
        "summary": "Collection of creative React UI bits and animated interactions.",
        "best_for": ["interaction polish", "creative micro-UI"],
        "not_for": ["headless accessibility baselines"],
        "keywords": ["react-bits", "creative", "animation", "components"],
    },
    "animate-ui": {
        "display_name": "Animate UI",
        "summary": "Animated component library focused on motion-forward React UI.",
        "best_for": ["motion components", "animated interactions"],
        "not_for": ["static content sites needing minimal JS"],
        "keywords": ["animate-ui", "motion", "react", "components"],
    },
    "originui": {
        "display_name": "Origin UI",
        "summary": "Copy-friendly React/Tailwind component patterns in a shadcn-adjacent style.",
        "best_for": ["app UI building blocks", "form and layout patterns"],
        "not_for": ["spectacle animation catalogs"],
        "keywords": ["origin-ui", "tailwind", "react", "patterns"],
    },
    "cult-ui": {
        "display_name": "Cult UI",
        "summary": "Design-engineer component experiments and distinctive UI patterns.",
        "best_for": ["distinctive component ideas", "visual exploration"],
        "not_for": ["enterprise defaults"],
        "keywords": ["cult-ui", "experimental", "components"],
    },
    "kibo-ui": {
        "display_name": "Kibo UI",
        "summary": "Composable React components and blocks extending the shadcn ecosystem.",
        "best_for": ["shadcn expansions", "app blocks"],
        "not_for": ["non-React stacks"],
        "keywords": ["kibo", "shadcn", "blocks", "react"],
    },
    "kokonutui": {
        "display_name": "KokonutUI",
        "summary": "Modern React UI components with a polished marketing aesthetic.",
        "best_for": ["marketing components", "visual polish"],
        "not_for": ["accessibility proof"],
        "keywords": ["kokonut", "react", "components", "marketing"],
    },
    "eldoraui-site": {
        "display_name": "Eldora UI",
        "summary": "Animated React UI components for landing-page effects.",
        "best_for": ["animated sections", "landing effects"],
        "not_for": ["data-dense admin UI"],
        "keywords": ["eldora", "animated", "landing", "react"],
    },
    "uilayouts": {
        "display_name": "UI Layouts",
        "summary": "Layout and section patterns for modern product/marketing pages.",
        "best_for": ["section composition", "layout ideas"],
        "not_for": ["behavior primitives"],
        "keywords": ["layouts", "sections", "composition"],
    },
    "hover": {
        "display_name": "Hover.dev",
        "summary": "Interactive UI animation examples and hover/transition techniques.",
        "best_for": ["hover states", "micro-interaction ideas"],
        "not_for": ["full design systems"],
        "keywords": ["hover", "micro-interaction", "animation"],
    },
    "motion-primitives": {
        "display_name": "Motion Primitives",
        "summary": "Composable motion-oriented React UI primitives and patterns.",
        "best_for": ["reusable motion components", "animated UI building blocks"],
        "not_for": ["CSS-only projects"],
        "keywords": ["motion-primitives", "react", "animation", "components"],
    },
    "inspira-ui": {
        "display_name": "Inspira UI",
        "summary": "Inspiration-heavy React component collection for modern interfaces.",
        "best_for": ["visual component ideas"],
        "not_for": ["license-blind copying"],
        "keywords": ["inspira", "react", "components", "inspiration"],
    },
    "fancycomponents": {
        "display_name": "Fancy Components",
        "summary": "Fancy animated React components for expressive interfaces.",
        "best_for": ["expressive UI flourishes"],
        "not_for": ["austere enterprise UIs"],
        "keywords": ["fancy", "animated", "react"],
    },
    "serafimcloud-github-21st": {
        "display_name": "21st.dev GitHub Pages mirror",
        "summary": "GitHub Pages surface related to 21st.dev component discovery.",
        "best_for": ["alternate discovery entrypoint"],
        "not_for": ["canonical docs"],
        "keywords": ["21st", "github-pages", "components"],
    },
    "nyxbui": {
        "display_name": "Nyxb UI",
        "summary": "Design-oriented UI component collection.",
        "best_for": ["component browsing", "visual ideas"],
        "not_for": ["standards reference"],
        "keywords": ["nyxb", "components", "ui"],
    },
    "ui-jln": {
        "display_name": "JLN UI",
        "summary": "Personal/curated UI component and pattern gallery.",
        "best_for": ["pattern inspiration"],
        "not_for": ["maintained design system"],
        "keywords": ["jln", "ui", "patterns"],
    },
    "hyperui": {
        "display_name": "HyperUI",
        "summary": "Free Tailwind CSS components for marketing and application pages.",
        "best_for": ["Tailwind sections", "free marketing blocks"],
        "not_for": ["complex accessible widgets"],
        "keywords": ["hyperui", "tailwind", "free", "components"],
    },
    "launchuicomponents": {
        "display_name": "Launch UI Components",
        "summary": "Launch-oriented UI components and marketing building blocks.",
        "best_for": ["startup landing components"],
        "not_for": ["enterprise data grids"],
        "keywords": ["launch", "startup", "components"],
    },
    "precedent": {
        "display_name": "Precedent",
        "summary": "Opinionated Next.js starter with polished UI conventions.",
        "best_for": ["Next.js starter patterns"],
        "not_for": ["framework-agnostic guidance"],
        "keywords": ["precedent", "nextjs", "starter"],
    },
    "ui-mantine": {
        "display_name": "Mantine UI",
        "summary": "Mantine component library docs and ready application UI examples.",
        "best_for": ["React app components", "hooks-driven UI"],
        "not_for": ["Tailwind-only stacks"],
        "keywords": ["mantine", "react", "components", "hooks"],
    },
    "chakra-ui": {
        "display_name": "Chakra UI",
        "summary": "Accessible React component library with style-props theming.",
        "best_for": ["accessible React apps", "themeable component systems"],
        "not_for": ["raw HTML-only projects"],
        "keywords": ["chakra", "react", "accessible", "theming"],
    },
    "heroui": {
        "display_name": "HeroUI",
        "summary": "Modern React UI library (formerly NextUI) with polished components.",
        "best_for": ["React product UI", "themed components"],
        "not_for": ["headless-only needs"],
        "keywords": ["heroui", "nextui", "react", "components"],
    },
    "material-tailwind": {
        "display_name": "Material Tailwind",
        "summary": "Material-inspired components built with Tailwind CSS.",
        "best_for": ["Material-looking Tailwind UI"],
        "not_for": ["official Material Design authority"],
        "keywords": ["material", "tailwind", "components"],
    },
    "nextui": {
        "display_name": "NextUI (legacy name)",
        "summary": "Legacy NextUI hostname; product continues as HeroUI.",
        "best_for": ["resolving older NextUI references"],
        "not_for": ["primary current docs"],
        "keywords": ["nextui", "heroui", "legacy"],
    },
    # shadcn ecosystem
    "shadcn-ui": {
        "display_name": "shadcn/ui",
        "summary": "Copy-in React components built on Radix primitives and Tailwind.",
        "best_for": ["app component systems", "accessible baseline widgets", "themeable UI"],
        "not_for": ["npm-package lock-in expectations", "non-React without ports"],
        "keywords": ["shadcn", "radix", "tailwind", "components", "registry"],
        "topics_contributed": ["components", "radix", "tailwind", "theming", "app-ui"],
    },
    "shadcnblocks": {
        "display_name": "shadcnblocks",
        "summary": "Ready-made page/section blocks for shadcn/ui projects.",
        "best_for": ["marketing/app sections on shadcn stacks"],
        "not_for": ["headless primitive research"],
        "keywords": ["shadcn", "blocks", "sections"],
    },
    "shadcnui-expansions-typeart-cc": {
        "display_name": "shadcn UI Expansions",
        "summary": "Community expansions and extra components around shadcn/ui.",
        "best_for": ["missing shadcn patterns"],
        "not_for": ["official API guarantees"],
        "keywords": ["shadcn", "expansions", "community"],
    },
    "shadcn-form": {
        "display_name": "shadcn Form",
        "summary": "Form builders and patterns targeting shadcn/ui + React Hook Form style stacks.",
        "best_for": ["form UX on shadcn", "validation UI"],
        "not_for": ["non-form product surfaces"],
        "keywords": ["shadcn", "forms", "validation"],
    },
    "shadcn-extension-vercel": {
        "display_name": "shadcn Extension",
        "summary": "Extended component set and utilities for shadcn-based apps.",
        "best_for": ["extra shadcn components"],
        "not_for": ["canonical shadcn docs"],
        "keywords": ["shadcn", "extension", "components"],
    },
    "shadcnui-blocks": {
        "display_name": "shadcnui Blocks",
        "summary": "Block/section marketplace-style resources for shadcn UI.",
        "best_for": ["page blocks", "section starters"],
        "not_for": ["primitive keyboard behavior"],
        "keywords": ["shadcn", "blocks", "sections"],
    },
    "blocks-tremor-so": {
        "display_name": "Tremor Blocks",
        "summary": "Dashboard and analytics blocks from the Tremor ecosystem.",
        "best_for": ["dashboard sections", "KPI layouts"],
        "not_for": ["marketing hero spectacle"],
        "keywords": ["tremor", "blocks", "dashboard", "charts"],
        "topics_contributed": ["dashboard", "charts", "blocks", "data-ui"],
    },
    "tweakcn": {
        "display_name": "tweakcn",
        "summary": "Visual theme tuner for shadcn/ui color and style tokens.",
        "best_for": ["theme exploration", "token tweaking"],
        "not_for": ["component behavior"],
        "keywords": ["tweakcn", "theme", "shadcn", "tokens"],
    },
    "shadcn-svelte": {
        "display_name": "shadcn-svelte",
        "summary": "Svelte port of the shadcn/ui component approach.",
        "best_for": ["Svelte component systems"],
        "not_for": ["React-only projects"],
        "keywords": ["shadcn", "svelte", "components"],
    },
    "shadcn-vue": {
        "display_name": "shadcn-vue",
        "summary": "Vue port of shadcn-style components.",
        "best_for": ["Vue component systems"],
        "not_for": ["React-only projects"],
        "keywords": ["shadcn", "vue", "components"],
    },
    "registry-build": {
        "display_name": "registry.build",
        "summary": "Registry tooling/hosting related to distributable component registries.",
        "best_for": ["registry packaging", "component distribution"],
        "not_for": ["visual inspiration"],
        "keywords": ["registry", "components", "distribution"],
    },
    "builtatlightspeed": {
        "display_name": "Built at Lightspeed",
        "summary": "Directory of Tailwind templates and UI kits.",
        "best_for": ["finding Tailwind templates quickly"],
        "not_for": ["accessibility standards"],
        "keywords": ["tailwind", "templates", "directory"],
    },
    "awesome-shadcn-ui-vercel": {
        "display_name": "Awesome shadcn/ui",
        "summary": "Curated index of shadcn-related resources, registries, and tools.",
        "best_for": ["discovering shadcn ecosystem tools"],
        "not_for": ["single-library API docs"],
        "keywords": ["awesome", "shadcn", "directory", "registry"],
    },
    # Tailwind blocks
    "tailwind-plus-ui-blocks": {
        "display_name": "Tailwind Plus UI Blocks",
        "summary": "Official paid Tailwind UI block catalog (formerly Tailwind UI Plus).",
        "best_for": ["high-quality Tailwind sections when entitled"],
        "not_for": ["copying without purchase/license"],
        "keywords": ["tailwind-plus", "ui-blocks", "paid", "official"],
    },
    "tailwind-ui": {
        "display_name": "Tailwind UI",
        "summary": "Official Tailwind component/template product (legacy hostname still used).",
        "best_for": ["official Tailwind kits when entitled"],
        "not_for": ["free unrestricted copying"],
        "keywords": ["tailwind-ui", "templates", "official"],
    },
    "preline": {
        "display_name": "Preline UI",
        "summary": "Tailwind component library with extensive marketing and app sections.",
        "best_for": ["Tailwind page sections", "plugin-based components"],
        "not_for": ["framework-agnostic accessibility primitives"],
        "keywords": ["preline", "tailwind", "components"],
    },
    "flowbite": {
        "display_name": "Flowbite",
        "summary": "Tailwind component library spanning marketing and dashboard UI.",
        "best_for": ["Tailwind components", "Figma-linked kits"],
        "not_for": ["headless behavior authority"],
        "keywords": ["flowbite", "tailwind", "components", "dashboard"],
    },
    "daisyui": {
        "display_name": "daisyUI",
        "summary": "Tailwind plugin that provides semantic component classes and themes.",
        "best_for": ["fast themed Tailwind UI", "class-based components"],
        "not_for": ["deep accessible widget behavior"],
        "keywords": ["daisyui", "tailwind", "themes", "plugin"],
    },
    "mambaui": {
        "display_name": "Mamba UI",
        "summary": "Free Tailwind components and sections.",
        "best_for": ["free Tailwind starters"],
        "not_for": ["enterprise design systems"],
        "keywords": ["mamba", "tailwind", "free"],
    },
    "merakiui": {
        "display_name": "Meraki UI",
        "summary": "Tailwind components with dark-mode-friendly marketing patterns.",
        "best_for": ["Tailwind marketing components"],
        "not_for": ["data-grid solutions"],
        "keywords": ["meraki", "tailwind", "components"],
    },
    "tailblocks-cc": {
        "display_name": "Tailblocks",
        "summary": "Ready Tailwind blocks for common landing sections.",
        "best_for": ["landing section starters"],
        "not_for": ["complex app widgets"],
        "keywords": ["tailblocks", "landing", "tailwind"],
    },
    "floatui": {
        "display_name": "Float UI",
        "summary": "Tailwind UI components and templates for modern sites.",
        "best_for": ["Tailwind site sections"],
        "not_for": ["accessibility specs"],
        "keywords": ["floatui", "tailwind", "templates"],
    },
    "cruip": {
        "display_name": "Cruip",
        "summary": "Polished Tailwind templates for SaaS and marketing sites.",
        "best_for": ["SaaS landing templates"],
        "not_for": ["free unrestricted reuse without checking terms"],
        "keywords": ["cruip", "saas", "templates", "tailwind"],
    },
    "tailawesome": {
        "display_name": "Tailawesome",
        "summary": "Directory of Tailwind resources and templates.",
        "best_for": ["discovering Tailwind kits"],
        "not_for": ["single-source implementation docs"],
        "keywords": ["tailawesome", "directory", "tailwind"],
    },
    "tailwindtoolbox": {
        "display_name": "Tailwind Toolbox",
        "summary": "Older Tailwind templates and starter resources.",
        "best_for": ["simple Tailwind starters"],
        "not_for": ["current best-practice authority"],
        "keywords": ["tailwindtoolbox", "templates", "starters"],
    },
    "kitwind-products-kometa-components": {
        "display_name": "Kitwind Kometa Components",
        "summary": "Kometa Tailwind component/product kit from Kitwind.",
        "best_for": ["Tailwind marketing kits"],
        "not_for": ["headless primitives"],
        "keywords": ["kitwind", "kometa", "tailwind"],
    },
    "creative-tim-templates-tailwind": {
        "display_name": "Creative Tim Tailwind Templates",
        "summary": "Commercial Tailwind templates from Creative Tim.",
        "best_for": ["admin/marketing template shopping"],
        "not_for": ["open-license assumptions"],
        "keywords": ["creative-tim", "templates", "tailwind"],
    },
    "tailwind-kit": {
        "display_name": "Tailwind Kit",
        "summary": "Tailwind UI kit and component collection.",
        "best_for": ["Tailwind UI assembly"],
        "not_for": ["standards docs"],
        "keywords": ["tailwind-kit", "components"],
    },
    "tailwindcomponents": {
        "display_name": "Tailwind Components",
        "summary": "Community gallery of Tailwind snippets and components.",
        "best_for": ["snippet inspiration", "community patterns"],
        "not_for": ["vetted accessibility"],
        "keywords": ["tailwindcomponents", "gallery", "snippets"],
    },
    "windstatic": {
        "display_name": "Windstatic",
        "summary": "Static Tailwind components and sections.",
        "best_for": ["static marketing sections"],
        "not_for": ["complex stateful widgets"],
        "keywords": ["windstatic", "tailwind", "static"],
    },
    "postsrc-components": {
        "display_name": "PostSrc Components",
        "summary": "Component snippets and UI examples including Tailwind-oriented pieces.",
        "best_for": ["snippet lookup"],
        "not_for": ["design-system completeness"],
        "keywords": ["postsrc", "snippets", "components"],
    },
    "pagedone": {
        "display_name": "Pagedone",
        "summary": "UI blocks and page sections for product/marketing sites.",
        "best_for": ["page section kits"],
        "not_for": ["primitive behavior docs"],
        "keywords": ["pagedone", "blocks", "sections"],
    },
    "shuffle": {
        "display_name": "Shuffle",
        "summary": "Visual editor/marketplace for assembling Tailwind UI pages.",
        "best_for": ["assembling marketing pages quickly"],
        "not_for": ["offline knowledge retrieval"],
        "keywords": ["shuffle", "editor", "tailwind"],
    },
    "tailtemplate": {
        "display_name": "Tailtemplate",
        "summary": "Tailwind template collection for sites and apps.",
        "best_for": ["template discovery"],
        "not_for": ["accessibility audits"],
        "keywords": ["tailtemplate", "templates"],
    },
    "creative-tim-learning-lab-tailwind-starter-kit-presentation": {
        "display_name": "Creative Tim Tailwind Starter Kit",
        "summary": "Learning-lab presentation for Creative Tim's Tailwind starter kit.",
        "best_for": ["starter-kit overview"],
        "not_for": ["deep API reference"],
        "keywords": ["creative-tim", "starter-kit", "tailwind"],
    },
    "notusjs": {
        "display_name": "Notus JS",
        "summary": "Tailwind UI kit historically popular for admin/landing starters.",
        "best_for": ["older Tailwind kit reference"],
        "not_for": ["modern accessibility baseline"],
        "keywords": ["notus", "tailwind", "kit"],
    },
    "tailwindawesome": {
        "display_name": "Tailwind Awesome",
        "summary": "Curated Tailwind templates and UI resources.",
        "best_for": ["template discovery"],
        "not_for": ["implementation authority"],
        "keywords": ["tailwindawesome", "templates", "directory"],
    },
    # Accessible primitives
    "radix-primitives": {
        "display_name": "Radix Primitives",
        "summary": "Unstyled accessible React primitives for dialogs, menus, tabs, and more.",
        "best_for": ["accessible widget behavior", "focus management", "composable primitives"],
        "not_for": ["styled design-system look"],
        "keywords": ["radix", "primitives", "dialog", "menu", "focus", "accessible"],
        "topics_contributed": ["accessibility", "primitives", "keyboard", "focus", "components"],
    },
    "radix-ui-themes": {
        "display_name": "Radix Themes",
        "summary": "Styled design system built on Radix primitives.",
        "best_for": ["quick styled Radix apps"],
        "not_for": ["fully custom visual languages without overrides"],
        "keywords": ["radix-themes", "design-system", "react"],
    },
    "react-aria": {
        "display_name": "React Aria",
        "summary": "Adobe's accessible React hook/component behaviors across mouse, touch, and keyboard.",
        "best_for": ["complex accessible widgets", "internationalized interactions", "behavior without styling"],
        "not_for": ["visual skin libraries"],
        "keywords": ["react-aria", "accessibility", "hooks", "i18n", "keyboard"],
        "topics_contributed": ["accessibility", "primitives", "i18n", "keyboard", "components"],
    },
    "ariakit": {
        "display_name": "Ariakit",
        "summary": "Lower-level accessible React toolkit for building custom widgets.",
        "best_for": ["custom accessible components", "combobox/dialog patterns"],
        "not_for": ["drop-in styled kits"],
        "keywords": ["ariakit", "accessibility", "combobox", "dialog", "react"],
        "topics_contributed": ["accessibility", "primitives", "keyboard", "components"],
    },
    "headless-ui": {
        "display_name": "Headless UI",
        "summary": "Unstyled accessible components from the Tailwind Labs team for React and Vue.",
        "best_for": ["Tailwind + headless widgets", "menus/dialogs/listboxes"],
        "not_for": ["CSS-framework-agnostic deep i18n suites"],
        "keywords": ["headless-ui", "tailwind", "accessible", "react", "vue"],
    },
    "ark-ui": {
        "display_name": "Ark UI",
        "summary": "Headless component library powered by Zag.js across frameworks.",
        "best_for": ["multi-framework accessible primitives"],
        "not_for": ["visual templates"],
        "keywords": ["ark-ui", "zag", "headless", "primitives"],
    },
    "park-ui": {
        "display_name": "Park UI",
        "summary": "Styled components built on Ark UI with design-token theming.",
        "best_for": ["Ark-based styled systems"],
        "not_for": ["raw primitive-only research"],
        "keywords": ["park-ui", "ark", "theming", "components"],
    },
    "zagjs": {
        "display_name": "Zag.js",
        "summary": "Framework-agnostic state machines for accessible UI components.",
        "best_for": ["portable component state machines"],
        "not_for": ["ready-made visual UI"],
        "keywords": ["zag", "state-machine", "accessible", "headless"],
    },
    "react-spectrum-adobe": {
        "display_name": "React Spectrum",
        "summary": "Adobe's styled React implementation of Spectrum components.",
        "best_for": ["Spectrum-styled React apps", "accessible product UI"],
        "not_for": ["brand-neutral headless-only needs"],
        "keywords": ["react-spectrum", "adobe", "spectrum", "accessible"],
    },
    "reach-tech": {
        "display_name": "Reach UI",
        "summary": "Older accessible React component foundation; many patterns superseded by newer libraries.",
        "best_for": ["historical accessible pattern reference"],
        "not_for": ["new greenfield defaults"],
        "keywords": ["reach-ui", "legacy", "accessible"],
    },
    "downshift-js": {
        "display_name": "Downshift",
        "summary": "Primitive builders for accessible autocomplete/combobox/select experiences.",
        "best_for": ["custom comboboxes", "typeahead selects"],
        "not_for": ["general design systems"],
        "keywords": ["downshift", "combobox", "autocomplete", "select"],
    },
    "floating-ui": {
        "display_name": "Floating UI",
        "summary": "Positioning engine for popovers, tooltips, menus, and floating elements.",
        "best_for": ["anchored overlays", "collision-aware positioning"],
        "not_for": ["full component styling"],
        "keywords": ["floating-ui", "popover", "tooltip", "positioning"],
        "topics_contributed": ["overlays", "positioning", "popover", "tooltip"],
    },
    "radix-ui-colors": {
        "display_name": "Radix Colors",
        "summary": "Accessible color scales designed for UI surfaces and text contrast.",
        "best_for": ["palette scales", "dark/light tokens"],
        "not_for": ["illustration palettes"],
        "keywords": ["radix-colors", "palette", "contrast", "tokens"],
    },
    "radix-ui-icons": {
        "display_name": "Radix Icons",
        "summary": "Clean icon set from the Radix ecosystem.",
        "best_for": ["UI iconography with Radix apps"],
        "not_for": ["brand logo replacement"],
        "keywords": ["radix-icons", "icons", "svg"],
    },
    "vaul-emilkowal-ski": {
        "display_name": "Vaul",
        "summary": "Accessible drawer component for React, popular in mobile/sheet patterns.",
        "best_for": ["mobile drawers", "bottom sheets"],
        "not_for": ["desktop-only dialog needs without adaptation"],
        "keywords": ["vaul", "drawer", "sheet", "react"],
    },
    "cmdk-paco-me": {
        "display_name": "cmdk",
        "summary": "Fast, accessible command-menu primitive for React.",
        "best_for": ["command palettes", "keyboard-first search menus"],
        "not_for": ["general navigation systems"],
        "keywords": ["cmdk", "command-palette", "menu", "keyboard"],
    },
    "sonner-emilkowal-ski": {
        "display_name": "Sonner",
        "summary": "Opinionated toast component with strong defaults for React apps.",
        "best_for": ["toast notifications", "async feedback"],
        "not_for": ["modal dialogs"],
        "keywords": ["sonner", "toast", "notifications", "react"],
    },
    # Dashboard / data
    "tremor-so": {
        "display_name": "Tremor",
        "summary": "React components for dashboards and charts on Tailwind stacks.",
        "best_for": ["KPI cards", "dashboard charts", "analytics UI"],
        "not_for": ["marketing animation catalogs"],
        "keywords": ["tremor", "dashboard", "charts", "tailwind"],
        "topics_contributed": ["dashboard", "charts", "data-ui", "analytics"],
    },
    "reui": {
        "display_name": "ReUI",
        "summary": "Modern UI components oriented to application interfaces.",
        "best_for": ["app UI kits"],
        "not_for": ["normative a11y specs"],
        "keywords": ["reui", "application", "components"],
    },
    "tanstack-table-latest": {
        "display_name": "TanStack Table",
        "summary": "Headless table utilities for sorting, filtering, pagination, and virtualization.",
        "best_for": ["data tables", "grid logic without imposed styles"],
        "not_for": ["charting"],
        "keywords": ["tanstack-table", "datagrid", "sorting", "filtering", "pagination"],
        "topics_contributed": ["tables", "datagrid", "filtering", "pagination"],
    },
    "recharts": {
        "display_name": "Recharts",
        "summary": "Composable charting library for React based on SVG.",
        "best_for": ["React charts", "dashboard visuals"],
        "not_for": ["canvas-level custom WebGL viz"],
        "keywords": ["recharts", "charts", "react", "svg"],
    },
    "chartjs": {
        "display_name": "Chart.js",
        "summary": "Widely used canvas charting library for the web.",
        "best_for": ["simple charts", "framework-agnostic charting"],
        "not_for": ["highly custom React composition models"],
        "keywords": ["chartjs", "charts", "canvas"],
    },
    "nivo": {
        "display_name": "Nivo",
        "summary": "Rich React dataviz components built on D3.",
        "best_for": ["beautiful React dataviz", "server-friendly SVG charts"],
        "not_for": ["tiny bundle absolute priority without review"],
        "keywords": ["nivo", "dataviz", "d3", "react"],
    },
    "visx-airbnb": {
        "display_name": "visx",
        "summary": "Low-level React visualization primitives from Airbnb.",
        "best_for": ["custom React dataviz systems"],
        "not_for": ["drop-in dashboard kits"],
        "keywords": ["visx", "dataviz", "react", "d3"],
    },
    "mui-x-react-data-grid": {
        "display_name": "MUI X Data Grid",
        "summary": "Feature-rich React data grid from MUI X.",
        "best_for": ["enterprise tables", "dense data operations"],
        "not_for": ["lightweight marketing tables"],
        "keywords": ["mui", "data-grid", "table", "enterprise"],
    },
    "ui-mantine-category-application": {
        "display_name": "Mantine Application UI",
        "summary": "Mantine examples category focused on application shells and patterns.",
        "best_for": ["app shell inspiration", "Mantine app layouts"],
        "not_for": ["Tailwind-only stacks"],
        "keywords": ["mantine", "application", "shell", "examples"],
    },
    "creative-tim-templates-dashboard": {
        "display_name": "Creative Tim Dashboards",
        "summary": "Commercial dashboard templates from Creative Tim.",
        "best_for": ["admin template shopping"],
        "not_for": ["open-license assumptions"],
        "keywords": ["creative-tim", "dashboard", "templates"],
    },
    "flatlogic-templates": {
        "display_name": "Flatlogic Templates",
        "summary": "Admin and SaaS templates across several stacks.",
        "best_for": ["admin starters"],
        "not_for": ["accessibility standards"],
        "keywords": ["flatlogic", "admin", "templates"],
    },
    "tabler": {
        "display_name": "Tabler",
        "summary": "Free HTML dashboard UI kit with practical admin patterns.",
        "best_for": ["admin dashboards", "operational UI"],
        "not_for": ["highly branded marketing sites"],
        "keywords": ["tabler", "dashboard", "admin", "html"],
    },
    "adminlte": {
        "display_name": "AdminLTE",
        "summary": "Classic open-source admin dashboard template.",
        "best_for": ["traditional admin shells"],
        "not_for": ["modern design-system authority"],
        "keywords": ["adminlte", "admin", "dashboard"],
    },
    "keenthemes-metronic": {
        "display_name": "Metronic",
        "summary": "Popular commercial admin dashboard theme suite.",
        "best_for": ["feature-rich admin templates when licensed"],
        "not_for": ["copying without entitlement"],
        "keywords": ["metronic", "admin", "theme", "paid"],
    },
    "devias": {
        "display_name": "Devias Kit",
        "summary": "React admin templates and dashboard kits.",
        "best_for": ["React admin starters"],
        "not_for": ["primitive accessibility docs"],
        "keywords": ["devias", "admin", "react", "dashboard"],
    },
    "mantine-react-table": {
        "display_name": "Mantine React Table",
        "summary": "Data-table library built to integrate with Mantine.",
        "best_for": ["Mantine data tables"],
        "not_for": ["non-Mantine design systems without adaptation"],
        "keywords": ["mantine", "table", "datagrid"],
    },
    "material-react-table": {
        "display_name": "Material React Table",
        "summary": "Data-table library built around Material UI conventions.",
        "best_for": ["MUI data tables"],
        "not_for": ["headless-only table needs"],
        "keywords": ["material", "table", "mui", "datagrid"],
    },
    # Design systems
    "m3-material": {
        "display_name": "Material Design 3",
        "summary": "Google's Material 3 design system guidance and patterns.",
        "best_for": ["Material theming", "component anatomy", "adaptive design"],
        "not_for": ["non-Material brand systems without translation"],
        "keywords": ["material", "m3", "design-system", "tokens"],
    },
    "developer-apple-design-human-interface-guidelines": {
        "display_name": "Apple Human Interface Guidelines",
        "summary": "Apple platform design guidance for clarity, deference, and accessibility.",
        "best_for": ["craft quality", "platform-aware motion/typography thinking"],
        "not_for": ["direct web measurement copying"],
        "keywords": ["apple", "hig", "guidelines", "accessibility"],
    },
    "carbondesignsystem": {
        "display_name": "Carbon Design System",
        "summary": "IBM's enterprise design system for dense, data-heavy products.",
        "best_for": ["enterprise data UI", "tokens", "content/guidelines"],
        "not_for": ["playful consumer marketing defaults"],
        "keywords": ["carbon", "ibm", "enterprise", "design-system"],
    },
    "atlassian": {
        "display_name": "Atlassian Design System",
        "summary": "Atlassian product design system for content, accessibility, and tools UI.",
        "best_for": ["product content patterns", "enterprise app UI"],
        "not_for": ["consumer landing spectacle"],
        "keywords": ["atlassian", "design-system", "content", "accessibility"],
    },
    "polaris-shopify": {
        "display_name": "Shopify Polaris",
        "summary": "Shopify's commerce/admin design system and guidance.",
        "best_for": ["commerce admin UI", "forms", "merchant workflows"],
        "not_for": ["non-commerce brand cloning"],
        "keywords": ["polaris", "shopify", "commerce", "admin"],
    },
    "primer-style": {
        "display_name": "Primer",
        "summary": "GitHub's design system for developer-tool interfaces.",
        "best_for": ["developer tools UI", "practical accessibility patterns"],
        "not_for": ["consumer ecommerce look"],
        "keywords": ["primer", "github", "developer-tools", "design-system"],
    },
    "spectrum-adobe": {
        "display_name": "Adobe Spectrum",
        "summary": "Adobe's design system emphasizing color, accessibility, and cross-product UI.",
        "best_for": ["adaptive color", "product design-system structure"],
        "not_for": ["copying Adobe brand assets"],
        "keywords": ["spectrum", "adobe", "design-system", "color"],
    },
    "design-system-service-gov-uk": {
        "display_name": "GOV.UK Design System",
        "summary": "Public-service design system focused on clarity, forms, and accessibility evidence.",
        "best_for": ["forms", "error messaging", "public-service UX"],
        "not_for": ["decorative brand expression"],
        "keywords": ["govuk", "forms", "accessibility", "public-service"],
    },
    "designsystem-digital-gov": {
        "display_name": "U.S. Web Design System",
        "summary": "U.S. federal design system for accessible public-facing services.",
        "best_for": ["government/public services", "accessible components", "trust cues"],
        "not_for": ["implying government affiliation"],
        "keywords": ["uswds", "federal", "accessibility", "public-service"],
    },
    "gestalt-pinterest-systems": {
        "display_name": "Pinterest Gestalt",
        "summary": "Pinterest's product design system.",
        "best_for": ["product component patterns", "design-system structure"],
        "not_for": ["Pinterest brand cloning"],
        "keywords": ["gestalt", "pinterest", "design-system"],
    },
    "base-uber": {
        "display_name": "Uber Base",
        "summary": "Uber's Base design system for product interfaces.",
        "best_for": ["product UI systems", "mobile-aware components"],
        "not_for": ["Uber brand imitation"],
        "keywords": ["base", "uber", "design-system"],
    },
    "orbit-kiwi": {
        "display_name": "Kiwi.com Orbit",
        "summary": "Orbit design system from Kiwi.com for travel product UI.",
        "best_for": ["travel/product UI patterns"],
        "not_for": ["generic marketing templates"],
        "keywords": ["orbit", "kiwi", "design-system"],
    },
    "lightningdesignsystem": {
        "display_name": "Salesforce Lightning Design System",
        "summary": "Salesforce SLDS for enterprise CRM-style interfaces.",
        "best_for": ["enterprise CRM patterns", "blueprints"],
        "not_for": ["consumer lifestyle branding"],
        "keywords": ["slds", "salesforce", "lightning", "enterprise"],
    },
    "fluent2-microsoft": {
        "display_name": "Fluent 2",
        "summary": "Microsoft Fluent 2 design system for cross-platform product UI.",
        "best_for": ["enterprise theming", "high contrast", "semantic tokens"],
        "not_for": ["Fluent asset misuse"],
        "keywords": ["fluent", "microsoft", "design-system", "tokens"],
    },
    "garden-zendesk": {
        "display_name": "Zendesk Garden",
        "summary": "Zendesk's Garden design system for support/product UI.",
        "best_for": ["support-product interfaces"],
        "not_for": ["marketing landing kits"],
        "keywords": ["garden", "zendesk", "design-system"],
    },
    "design-gitlab": {
        "display_name": "GitLab Design System",
        "summary": "Pajamas/GitLab design-system guidance for product UI.",
        "best_for": ["developer-tool product patterns"],
        "not_for": ["GitLab brand cloning"],
        "keywords": ["gitlab", "pajamas", "design-system"],
    },
    "paste-twilio": {
        "display_name": "Twilio Paste",
        "summary": "Twilio's Paste design system for product interfaces.",
        "best_for": ["product design-system structure", "inclusive components"],
        "not_for": ["Twilio brand copying"],
        "keywords": ["paste", "twilio", "design-system"],
    },
    "vercel-geist": {
        "display_name": "Vercel Geist",
        "summary": "Vercel's Geist design system, typography, and UI foundations.",
        "best_for": ["developer-product aesthetics", "Geist typography/UI"],
        "not_for": ["non-Vercel brand imitation"],
        "keywords": ["geist", "vercel", "design-system", "typography"],
    },
    "linear": {
        "display_name": "Linear",
        "summary": "Linear product site/app as a craft reference for dense productivity UI.",
        "best_for": ["productivity UI inspiration", "dense elegant layouts"],
        "not_for": ["copying Linear brand/UI expression"],
        "keywords": ["linear", "inspiration", "product-ui", "craft"],
    },
    # Motion
    "motion": {
        "display_name": "Motion",
        "summary": "Modern Motion library (Framer Motion lineage) for React animation and gestures.",
        "best_for": ["React motion", "layout animations", "gesture-driven UI"],
        "not_for": ["CSS-only constraints without JS"],
        "keywords": ["motion", "framer-motion", "react", "animation", "gestures"],
        "topics_contributed": ["motion", "animation", "gestures", "transitions"],
    },
    "framer-motion": {
        "display_name": "Framer Motion docs",
        "summary": "Framer-hosted Motion documentation and examples.",
        "best_for": ["Motion API examples", "React animation patterns"],
        "not_for": ["Framer site-builder cloning"],
        "keywords": ["framer-motion", "motion", "react", "docs"],
    },
    "gsap": {
        "display_name": "GSAP",
        "summary": "Professional animation platform for complex timelines and sequencing.",
        "best_for": ["complex timelines", "sequenced storytelling motion"],
        "not_for": ["simple state toggles", "license-blind commercial use"],
        "keywords": ["gsap", "timeline", "animation", "sequencing"],
    },
    "animejs": {
        "display_name": "Anime.js",
        "summary": "Lightweight JavaScript animation library for timelines and SVG.",
        "best_for": ["JS timelines", "SVG animation"],
        "not_for": ["React lifecycle-first systems without wrappers"],
        "keywords": ["animejs", "animation", "svg", "timeline"],
    },
    "react-spring": {
        "display_name": "React Spring",
        "summary": "Spring-physics animation library for React.",
        "best_for": ["interruptible spring motion", "gesture-friendly animation"],
        "not_for": ["strict CSS-only delivery"],
        "keywords": ["react-spring", "spring", "physics", "animation"],
    },
    "auto-animate-formkit": {
        "display_name": "AutoAnimate",
        "summary": "Drop-in automatic animations for layout changes with tiny setup.",
        "best_for": ["list/layout transitions", "low-ceremony motion"],
        "not_for": ["narrative cinematic sequences"],
        "keywords": ["auto-animate", "layout", "transitions"],
    },
    "lottiefiles": {
        "display_name": "LottieFiles",
        "summary": "Lottie animation hosting, editors, and asset marketplace.",
        "best_for": ["vector animation assets", "micro-illustration motion"],
        "not_for": ["unlicensed asset use", "motion-as-status alone"],
        "keywords": ["lottie", "animation", "assets"],
    },
    "rive": {
        "display_name": "Rive",
        "summary": "State-machine-driven interactive animation runtime and editor.",
        "best_for": ["interactive animated graphics", "runtime state machines"],
        "not_for": ["simple CSS hover states"],
        "keywords": ["rive", "interactive", "animation", "state-machine"],
    },
    "transitions": {
        "display_name": "Transitions.dev",
        "summary": "Transition showcase, vocabulary, and refinement tooling for UI motion.",
        "best_for": ["transition vocabulary", "motion inspection concepts"],
        "not_for": ["blind snippet vendoring without license clarity"],
        "keywords": ["transitions", "motion", "css", "refine"],
    },
    "easings": {
        "display_name": "Easings.net",
        "summary": "Visual reference for common easing curves.",
        "best_for": ["choosing easing curves", "motion language"],
        "not_for": ["full animation systems"],
        "keywords": ["easing", "curves", "timing"],
    },
    "cubic-bezier": {
        "display_name": "cubic-bezier.com",
        "summary": "Interactive cubic-bezier curve editor for CSS timing functions.",
        "best_for": ["custom CSS easings"],
        "not_for": ["spring physics models"],
        "keywords": ["cubic-bezier", "css", "easing"],
    },
    "animista": {
        "display_name": "Animista",
        "summary": "CSS animation playground for generating keyframe snippets.",
        "best_for": ["CSS keyframe ideas"],
        "not_for": ["accessibility-complete motion systems"],
        "keywords": ["animista", "css", "keyframes"],
    },
    "cssanimation": {
        "display_name": "CSS Animation Rocks",
        "summary": "Educational CSS animation articles and examples.",
        "best_for": ["learning CSS animation techniques"],
        "not_for": ["component libraries"],
        "keywords": ["css", "animation", "education"],
    },
    "tympanus-codrops": {
        "display_name": "Codrops",
        "summary": "Experimental frontend UI techniques and creative demos.",
        "best_for": ["creative technique inspiration"],
        "not_for": ["production defaults without adaptation"],
        "keywords": ["codrops", "experimental", "ui", "demos"],
    },
    "codepen": {
        "display_name": "CodePen",
        "summary": "Front-end sandbox community full of UI/motion demos.",
        "best_for": ["prototype inspiration", "isolated technique demos"],
        "not_for": ["unvetted production dependencies"],
        "keywords": ["codepen", "demos", "sandbox", "inspiration"],
    },
    "threejs": {
        "display_name": "Three.js",
        "summary": "WebGL 3D library for expressive/spatial web experiences.",
        "best_for": ["3D/WebGL experiences when product-justified"],
        "not_for": ["ordinary marketing pages", "accessibility-critical flows without fallback"],
        "keywords": ["threejs", "webgl", "3d"],
    },
    "react-three-fiber-docs-pmnd-rs": {
        "display_name": "React Three Fiber",
        "summary": "React renderer for Three.js scenes.",
        "best_for": ["React-managed 3D scenes"],
        "not_for": ["simple 2D UI motion"],
        "keywords": ["react-three-fiber", "r3f", "threejs", "react"],
    },
    "github-pmndrs-drei": {
        "display_name": "Drei",
        "summary": "Useful helpers and abstractions for React Three Fiber.",
        "best_for": ["R3F helpers", "common 3D UI building blocks"],
        "not_for": ["2D design systems"],
        "keywords": ["drei", "r3f", "threejs", "helpers"],
    },
    "shadergradient": {
        "display_name": "Shader Gradient",
        "summary": "Tool for generating animated shader gradients.",
        "best_for": ["decorative gradient backdrops"],
        "not_for": ["content readability surfaces without contrast checks"],
        "keywords": ["shader", "gradient", "background"],
    },
    "shadertoy": {
        "display_name": "Shadertoy",
        "summary": "Community platform for exploring fragment shaders.",
        "best_for": ["shader experimentation"],
        "not_for": ["direct production drop-in without performance review"],
        "keywords": ["shadertoy", "glsl", "shaders"],
    },
    # Icons / backgrounds
    "lucide": {
        "display_name": "Lucide",
        "summary": "Open-source consistent SVG icon set popular with modern app UI.",
        "best_for": ["app icons", "UI iconography"],
        "not_for": ["brand logos"],
        "keywords": ["lucide", "icons", "svg"],
    },
    "heroicons": {
        "display_name": "Heroicons",
        "summary": "SVG icons by the Tailwind Labs team.",
        "best_for": ["Tailwind-era UI icons"],
        "not_for": ["pictogram illustration systems"],
        "keywords": ["heroicons", "icons", "tailwind"],
    },
    "phosphoricons": {
        "display_name": "Phosphor Icons",
        "summary": "Flexible icon family with multiple weights.",
        "best_for": ["multi-weight icon systems"],
        "not_for": ["photo assets"],
        "keywords": ["phosphor", "icons", "weights"],
    },
    "tabler-icons": {
        "display_name": "Tabler Icons",
        "summary": "Large free SVG icon set paired with the Tabler ecosystem.",
        "best_for": ["admin/app icon coverage"],
        "not_for": ["custom brand marks"],
        "keywords": ["tabler-icons", "icons", "svg"],
    },
    "iconoir": {
        "display_name": "Iconoir",
        "summary": "Open-source icon library with a distinctive line style.",
        "best_for": ["alternative icon aesthetic"],
        "not_for": ["logo replacement"],
        "keywords": ["iconoir", "icons"],
    },
    "icons8": {
        "display_name": "Icons8",
        "summary": "Commercial icon/illustration marketplace and generators.",
        "best_for": ["asset shopping when licensed"],
        "not_for": ["assuming free commercial reuse"],
        "keywords": ["icons8", "icons", "illustrations", "marketplace"],
    },
    "simpleicons": {
        "display_name": "Simple Icons",
        "summary": "SVG icons for popular brands and tools.",
        "best_for": ["tech brand icons with trademark care"],
        "not_for": ["implying endorsement"],
        "keywords": ["simpleicons", "brand-icons", "svg"],
    },
    "svgl": {
        "display_name": "SVGL",
        "summary": "Collection of SVG brand/tool logos for developers.",
        "best_for": ["devtool logo SVGs with trademark care"],
        "not_for": ["unreviewed trademark use"],
        "keywords": ["svgl", "logos", "svg"],
    },
    "svgbackgrounds": {
        "display_name": "SVG Backgrounds",
        "summary": "Configurable SVG background patterns.",
        "best_for": ["decorative page backgrounds"],
        "not_for": ["content-bearing imagery"],
        "keywords": ["svg", "backgrounds", "patterns"],
    },
    "heropatterns": {
        "display_name": "Hero Patterns",
        "summary": "Repeatable SVG background patterns.",
        "best_for": ["subtle texture backgrounds"],
        "not_for": ["illustration storytelling"],
        "keywords": ["heropatterns", "svg", "patterns"],
    },
    "haikei": {
        "display_name": "Haikei",
        "summary": "Generator for SVG shapes, waves, and blob backgrounds.",
        "best_for": ["hero backgrounds", "abstract shapes"],
        "not_for": ["icon systems"],
        "keywords": ["haikei", "svg", "blobs", "waves"],
    },
    "fffuel": {
        "display_name": "fffuel",
        "summary": "Suite of color/SVG utility generators for designers.",
        "best_for": ["quick SVG/color utilities"],
        "not_for": ["full design systems"],
        "keywords": ["fffuel", "generators", "svg", "color"],
    },
    "patterncraft": {
        "display_name": "Pattern Craft",
        "summary": "Pattern generation tool for decorative backgrounds.",
        "best_for": ["pattern textures"],
        "not_for": ["semantic icons"],
        "keywords": ["patterncraft", "patterns", "backgrounds"],
    },
    "bg-ibelick": {
        "display_name": "BG by ibelick",
        "summary": "Curated CSS/SVG background snippets for modern sites.",
        "best_for": ["decorative backgrounds", "hero atmospheres"],
        "not_for": ["content images"],
        "keywords": ["backgrounds", "css", "snippets", "hero"],
    },
    "meshgradient-in": {
        "display_name": "Mesh Gradient",
        "summary": "Mesh gradient generator for soft colorful backgrounds.",
        "best_for": ["gradient atmospheres"],
        "not_for": ["text contrast finalization without checks"],
        "keywords": ["mesh-gradient", "background", "color"],
    },
    "blobmaker": {
        "display_name": "Blobmaker",
        "summary": "SVG blob shape generator.",
        "best_for": ["organic decorative shapes"],
        "not_for": ["UI icons"],
        "keywords": ["blobmaker", "svg", "shapes"],
    },
    "undraw": {
        "display_name": "unDraw",
        "summary": "Open-style illustration set for empty states and onboarding.",
        "best_for": ["empty states", "onboarding illustrations"],
        "not_for": ["custom brand illustration systems without review"],
        "keywords": ["undraw", "illustrations", "empty-state"],
    },
    "manypixels-gallery": {
        "display_name": "ManyPixels Gallery",
        "summary": "Illustration gallery/resources for product visuals.",
        "best_for": ["illustration shopping"],
        "not_for": ["license-free assumptions"],
        "keywords": ["manypixels", "illustrations"],
    },
    "storyset": {
        "display_name": "Storyset",
        "summary": "Customizable illustrations for product storytelling.",
        "best_for": ["onboarding/marketing illustrations"],
        "not_for": ["unchecked license reuse"],
        "keywords": ["storyset", "illustrations", "customizable"],
    },
    "openpeeps": {
        "display_name": "Open Peeps",
        "summary": "Hand-drawn people illustration library.",
        "best_for": ["friendly human illustrations"],
        "not_for": ["corporate iconography"],
        "keywords": ["open-peeps", "illustrations", "people"],
    },
    "ls-graphics-free-mockups": {
        "display_name": "LS Graphics Free Mockups",
        "summary": "Free device/mockup graphics for presentations.",
        "best_for": ["marketing mockups"],
        "not_for": ["UI component behavior"],
        "keywords": ["mockups", "devices", "graphics"],
    },
    "shapes-framer": {
        "display_name": "Framer Shapes",
        "summary": "Shape/graphic resources associated with Framer ecosystems.",
        "best_for": ["decorative shapes"],
        "not_for": ["accessibility primitives"],
        "keywords": ["shapes", "framer", "graphics"],
    },
    # Fonts
    "fonts-google": {
        "display_name": "Google Fonts",
        "summary": "Large hosted font catalog for web typography.",
        "best_for": ["web font selection", "quick pairing"],
        "not_for": ["privacy-sensitive self-host mandates without review"],
        "keywords": ["google-fonts", "typography", "webfonts"],
    },
    "rsms-me-inter": {
        "display_name": "Inter",
        "summary": "Widely used UI sans typeface designed for screens.",
        "best_for": ["product UI type", "dense interfaces"],
        "not_for": ["distinctive brand display needs"],
        "keywords": ["inter", "ui-font", "sans"],
    },
    "vercel-font": {
        "display_name": "Geist Font",
        "summary": "Vercel's Geist font family for product/developer interfaces.",
        "best_for": ["developer-product typography"],
        "not_for": ["ornamental display typography"],
        "keywords": ["geist", "vercel", "font"],
    },
    "fontsource": {
        "display_name": "Fontsource",
        "summary": "Self-hostable font packages for npm/ bundler workflows.",
        "best_for": ["self-hosted fonts", "privacy-conscious delivery"],
        "not_for": ["font discovery inspiration alone"],
        "keywords": ["fontsource", "self-host", "webfonts"],
    },
    "fontshare": {
        "display_name": "Fontshare",
        "summary": "Quality free font library from Indian Type Foundry.",
        "best_for": ["distinctive free fonts", "pairing ideas"],
        "not_for": ["ignoring per-font licenses"],
        "keywords": ["fontshare", "fonts", "free"],
    },
    "futurefonts-xyz": {
        "display_name": "Future Fonts",
        "summary": "Marketplace for experimental and in-progress typefaces.",
        "best_for": ["expressive display type"],
        "not_for": ["assuming free licensing"],
        "keywords": ["futurefonts", "experimental", "type"],
    },
    "typescale": {
        "display_name": "Type Scale",
        "summary": "Visualizer for modular typographic scales.",
        "best_for": ["type-scale planning"],
        "not_for": ["font licensing"],
        "keywords": ["typescale", "modular-scale", "typography"],
    },
    "utopia-fyi": {
        "display_name": "Utopia",
        "summary": "Fluid responsive type and space scale calculator.",
        "best_for": ["fluid type", "responsive spacing systems"],
        "not_for": ["font file hosting"],
        "keywords": ["utopia", "fluid-type", "responsive", "spacing"],
    },
    "fluid-style": {
        "display_name": "Fluid Style",
        "summary": "Tools/guidance around fluid CSS sizing.",
        "best_for": ["fluid clamp-based sizing"],
        "not_for": ["component kits"],
        "keywords": ["fluid", "css", "clamp", "sizing"],
    },
    "modernfontstacks": {
        "display_name": "Modern Font Stacks",
        "summary": "System font stack presets that avoid webfont loading.",
        "best_for": ["performance-first typography", "system fonts"],
        "not_for": ["custom brand typefaces"],
        "keywords": ["system-fonts", "font-stacks", "performance"],
    },
    "fontpair": {
        "display_name": "FontPair",
        "summary": "Font pairing inspiration gallery.",
        "best_for": ["pairing exploration"],
        "not_for": ["license verification"],
        "keywords": ["fontpair", "pairing", "typography"],
    },
    "typewolf": {
        "display_name": "Typewolf",
        "summary": "Typography inspiration and font recommendations from real sites.",
        "best_for": ["type inspiration", "pairing research"],
        "not_for": ["implementation snippets"],
        "keywords": ["typewolf", "typography", "inspiration"],
    },
    # Color tools
    "coolors": {
        "display_name": "Coolors",
        "summary": "Fast palette generator and color scheme explorer.",
        "best_for": ["palette drafting"],
        "not_for": ["final contrast certification"],
        "keywords": ["coolors", "palette", "generator"],
    },
    "colorhunt": {
        "display_name": "Color Hunt",
        "summary": "Curated color palette gallery.",
        "best_for": ["palette inspiration"],
        "not_for": ["accessible ramp generation"],
        "keywords": ["colorhunt", "palette", "gallery"],
    },
    "realtimecolors": {
        "display_name": "Realtime Colors",
        "summary": "Live preview tool for testing palettes on UI layouts.",
        "best_for": ["seeing colors on UI structure"],
        "not_for": ["token architecture docs"],
        "keywords": ["realtimecolors", "palette", "preview"],
    },
    "tints": {
        "display_name": "Tints.dev",
        "summary": "Tailwind-oriented color ramp generator.",
        "best_for": ["Tailwind palette ramps"],
        "not_for": ["illustration palettes"],
        "keywords": ["tints", "tailwind", "ramps", "palette"],
    },
    "uicolors-create": {
        "display_name": "UI Colors",
        "summary": "UI color scale generator for design tokens.",
        "best_for": ["token ramps", "UI scales"],
        "not_for": ["random aesthetic gradients"],
        "keywords": ["uicolors", "scales", "tokens"],
    },
    "huemint": {
        "display_name": "Huemint",
        "summary": "ML-assisted palette generator with product-aware modes.",
        "best_for": ["unusual but coherent palettes"],
        "not_for": ["WCAG proof alone"],
        "keywords": ["huemint", "palette", "ml"],
    },
    "gradient-style": {
        "display_name": "Gradient Style",
        "summary": "Gradient creation and exploration tool.",
        "best_for": ["CSS gradients"],
        "not_for": ["semantic token systems"],
        "keywords": ["gradient", "css", "generator"],
    },
    "grabient": {
        "display_name": "Grabient",
        "summary": "Beautiful CSS gradient presets and editor.",
        "best_for": ["hero gradients"],
        "not_for": ["contrast-checked text colors"],
        "keywords": ["grabient", "gradient", "css"],
    },
    "cssgradient": {
        "display_name": "CSS Gradient",
        "summary": "Simple CSS gradient generator.",
        "best_for": ["quick gradient CSS"],
        "not_for": ["design-token governance"],
        "keywords": ["cssgradient", "gradient"],
    },
    "hypercolor": {
        "display_name": "Hypercolor",
        "summary": "Tailwind-oriented gradient presets.",
        "best_for": ["Tailwind gradients"],
        "not_for": ["accessible text color systems"],
        "keywords": ["hypercolor", "tailwind", "gradient"],
    },
    "eggradients": {
        "display_name": "eggradients",
        "summary": "Gradient inspiration gallery.",
        "best_for": ["gradient mood boards"],
        "not_for": ["implementation standards"],
        "keywords": ["eggradients", "gradient", "inspiration"],
    },
    "colorbox": {
        "display_name": "ColorBox",
        "summary": "Lyft ColorBox tool for generating systematic color ramps.",
        "best_for": ["design-system color ramps"],
        "not_for": ["random trendy palettes"],
        "keywords": ["colorbox", "ramps", "design-system"],
    },
    "leonardocolor": {
        "display_name": "Leonardo",
        "summary": "Adobe tool for contrast-aware generative color palettes.",
        "best_for": ["accessible color systems", "contrast targets"],
        "not_for": ["illustration-only palettes"],
        "keywords": ["leonardo", "contrast", "accessible-color"],
    },
    "accessiblepalette": {
        "display_name": "Accessible Palette",
        "summary": "Palette generator focused on WCAG-oriented contrast relationships.",
        "best_for": ["accessible ramps", "contrast planning"],
        "not_for": ["decorative gradient browsing"],
        "keywords": ["accessible-palette", "wcag", "contrast"],
    },
    "webaim-resources-contrastchecker": {
        "display_name": "WebAIM Contrast Checker",
        "summary": "Authoritative practical contrast checking utility.",
        "best_for": ["text/background contrast checks"],
        "not_for": ["palette fashion inspiration"],
        "keywords": ["webaim", "contrast", "wcag", "checker"],
        "topics_contributed": ["contrast", "accessibility", "color"],
    },
    # Inspiration catalogs
    "awwwards": {
        "display_name": "Awwwards",
        "summary": "Curated award-winning website inspiration gallery.",
        "best_for": ["high-craft direction finding", "interactive site inspiration"],
        "not_for": ["code copy", "accessibility proof"],
        "keywords": ["awwwards", "inspiration", "awards", "websites"],
    },
    "godly": {
        "display_name": "Godly",
        "summary": "Hand-picked unusual/high-quality website inspiration.",
        "best_for": ["distinctive landing inspiration"],
        "not_for": ["implementation snippets"],
        "keywords": ["godly", "inspiration", "landing"],
    },
    "land-book": {
        "display_name": "Land-book",
        "summary": "Landing-page gallery organized for marketing-site research.",
        "best_for": ["landing structure inspiration"],
        "not_for": ["copying brand assets"],
        "keywords": ["land-book", "landing", "gallery"],
    },
    "lapa-ninja": {
        "display_name": "Lapa Ninja",
        "summary": "Landing-page design gallery.",
        "best_for": ["landing page pattern scanning"],
        "not_for": ["component APIs"],
        "keywords": ["lapa", "landing", "inspiration"],
    },
    "landingfolio": {
        "display_name": "Landingfolio",
        "summary": "Landing-page component and section inspiration library.",
        "best_for": ["section-level landing research"],
        "not_for": ["code entitlements without review"],
        "keywords": ["landingfolio", "sections", "landing"],
    },
    "onepagelove": {
        "display_name": "One Page Love",
        "summary": "One-page website inspiration and resources.",
        "best_for": ["single-page site direction"],
        "not_for": ["app-shell patterns"],
        "keywords": ["onepagelove", "one-page", "inspiration"],
    },
    "mobbin": {
        "display_name": "Mobbin",
        "summary": "Mobile and web app screenshot library for product-pattern research.",
        "best_for": ["flows", "app UI patterns", "screen inventories"],
        "not_for": ["copying UI chrome/brand"],
        "keywords": ["mobbin", "screenshots", "mobile", "flows"],
    },
    "page-flows": {
        "display_name": "Page Flows",
        "summary": "User-flow screenshot library for product UX research.",
        "best_for": ["onboarding/checkout flow research"],
        "not_for": ["visual asset reuse"],
        "keywords": ["page-flows", "flows", "ux", "screenshots"],
    },
    "saaslandingpage": {
        "display_name": "SaaS Landing Page",
        "summary": "Gallery of SaaS marketing landing pages.",
        "best_for": ["SaaS landing structure"],
        "not_for": ["app UI components"],
        "keywords": ["saas", "landing", "gallery"],
    },
    "refero": {
        "display_name": "Refero",
        "summary": "Product UI reference library with searchable screens.",
        "best_for": ["product UI references", "pattern search"],
        "not_for": ["code extraction"],
        "keywords": ["refero", "product-ui", "screens"],
    },
    "screenlane": {
        "display_name": "Screenlane",
        "summary": "App screenshot inspiration for modern product UI.",
        "best_for": ["mobile/product screen inspiration"],
        "not_for": ["implementation licenses"],
        "keywords": ["screenlane", "screenshots", "apps"],
    },
    "siteinspire": {
        "display_name": "SiteInspire",
        "summary": "CSS/design gallery of noteworthy websites.",
        "best_for": ["web design inspiration"],
        "not_for": ["component docs"],
        "keywords": ["siteinspire", "gallery", "css"],
    },
    "httpster": {
        "display_name": "Httpster",
        "summary": "Curated website design inspiration feed.",
        "best_for": ["visual browsing"],
        "not_for": ["technical references"],
        "keywords": ["httpster", "inspiration"],
    },
    "maxibestof-one": {
        "display_name": "MaxiBestOf",
        "summary": "Design inspiration collection.",
        "best_for": ["mood/direction browsing"],
        "not_for": ["code samples"],
        "keywords": ["maxibestof", "inspiration"],
    },
    "minimal-gallery": {
        "display_name": "Minimal Gallery",
        "summary": "Minimalist website inspiration gallery.",
        "best_for": ["restrained visual direction"],
        "not_for": ["loud kinetic styles"],
        "keywords": ["minimal", "gallery", "inspiration"],
    },
    "dark": {
        "display_name": "Dark Design",
        "summary": "Dark-mode website inspiration gallery.",
        "best_for": ["dark UI direction"],
        "not_for": ["forcing dark mode by default"],
        "keywords": ["dark", "inspiration", "gallery"],
    },
    "curated": {
        "display_name": "Curated Design",
        "summary": "Curated interface/design inspiration site.",
        "best_for": ["general UI inspiration"],
        "not_for": ["implementation details"],
        "keywords": ["curated", "inspiration"],
    },
    "footer": {
        "display_name": "Footer Design",
        "summary": "Gallery focused on website footer patterns.",
        "best_for": ["footer IA and layout ideas"],
        "not_for": ["full-site systems"],
        "keywords": ["footer", "gallery", "patterns"],
    },
    "navbar-gallery": {
        "display_name": "Navbar Gallery",
        "summary": "Gallery of navigation-bar patterns.",
        "best_for": ["nav layout inspiration"],
        "not_for": ["accessible menu behavior docs"],
        "keywords": ["navbar", "navigation", "gallery"],
    },
    "calltoinspiration": {
        "display_name": "CallToInspiration",
        "summary": "Category-based UI inspiration (buttons, forms, etc.).",
        "best_for": ["element-level inspiration"],
        "not_for": ["code reuse"],
        "keywords": ["calltoinspiration", "elements", "gallery"],
    },
    "darkmodedesign": {
        "display_name": "Dark Mode Design",
        "summary": "Inspiration specifically for dark interfaces.",
        "best_for": ["dark theme direction"],
        "not_for": ["contrast validation"],
        "keywords": ["dark-mode", "inspiration"],
    },
    "webframe-xyz": {
        "display_name": "Webframe",
        "summary": "Screenshot gallery of web app UI.",
        "best_for": ["app UI screenshots"],
        "not_for": ["copying product chrome"],
        "keywords": ["webframe", "screenshots", "app-ui"],
    },
    "lookup": {
        "display_name": "Lookup Design",
        "summary": "Design inspiration lookup/gallery.",
        "best_for": ["quick visual references"],
        "not_for": ["technical docs"],
        "keywords": ["lookup", "inspiration"],
    },
    "nicelydone-club": {
        "display_name": "Nicely Done",
        "summary": "Product UI reference club/gallery.",
        "best_for": ["SaaS UI references"],
        "not_for": ["asset extraction"],
        "keywords": ["nicelydone", "saas", "references"],
    },
    "appshots": {
        "display_name": "Appshots",
        "summary": "App screenshot inspiration library.",
        "best_for": ["mobile app visual research"],
        "not_for": ["web component APIs"],
        "keywords": ["appshots", "mobile", "screenshots"],
    },
    "interfaces-pro": {
        "display_name": "Interfaces.pro",
        "summary": "Interface inspiration collection.",
        "best_for": ["UI browsing"],
        "not_for": ["implementation guidance"],
        "keywords": ["interfaces", "inspiration"],
    },
    "designspells": {
        "display_name": "Design Spells",
        "summary": "Small delightful UI details and micro-interaction inspiration.",
        "best_for": ["micro-detail inspiration"],
        "not_for": ["system-wide architecture"],
        "keywords": ["designspells", "details", "micro-interaction"],
    },
    "bento-grids": {
        "display_name": "Bento Grids",
        "summary": "Inspiration focused on bento-style layout compositions.",
        "best_for": ["bento layout ideas"],
        "not_for": ["forcing bento everywhere"],
        "keywords": ["bento", "grids", "layout"],
    },
    "producthunt": {
        "display_name": "Product Hunt",
        "summary": "Product discovery feed useful for launch-page and positioning research.",
        "best_for": ["positioning inspiration", "launch tropes"],
        "not_for": ["design-system guidance"],
        "keywords": ["producthunt", "launches", "positioning"],
    },
    "dribbble": {
        "display_name": "Dribbble",
        "summary": "Designer community shots for visual exploration.",
        "best_for": ["visual moodboards"],
        "not_for": ["production-ready accessible implementations"],
        "keywords": ["dribbble", "shots", "inspiration"],
    },
    "behance": {
        "display_name": "Behance",
        "summary": "Portfolio case-study network for design inspiration.",
        "best_for": ["case-study storytelling inspiration"],
        "not_for": ["code samples"],
        "keywords": ["behance", "portfolio", "case-study"],
    },
    # Portfolio
    "pafolios": {
        "display_name": "Pafolios",
        "summary": "Portfolio inspiration directory.",
        "best_for": ["portfolio direction"],
        "not_for": ["template cloning"],
        "keywords": ["pafolios", "portfolio", "inspiration"],
    },
    "awwwards-portfolio": {
        "display_name": "Awwwards Portfolios",
        "summary": "Awwwards collection filtered to portfolio sites.",
        "best_for": ["high-craft portfolio inspiration"],
        "not_for": ["accessibility evidence"],
        "keywords": ["awwwards", "portfolio"],
    },
    "bestfolios": {
        "display_name": "Bestfolios",
        "summary": "Curated portfolio examples.",
        "best_for": ["portfolio structure ideas"],
        "not_for": ["implementation kits"],
        "keywords": ["bestfolios", "portfolio"],
    },
    "minimal-gallery-categories-portfolio": {
        "display_name": "Minimal Gallery — Portfolio",
        "summary": "Minimal Gallery category for portfolios.",
        "best_for": ["restrained portfolio direction"],
        "not_for": ["maximalist motion references"],
        "keywords": ["minimal", "portfolio"],
    },
    "siteinspire-websites": {
        "display_name": "SiteInspire Websites",
        "summary": "SiteInspire website index for browsing inspiration.",
        "best_for": ["broad site inspiration"],
        "not_for": ["docs"],
        "keywords": ["siteinspire", "websites"],
    },
    "onepagelove-gallery-personal": {
        "display_name": "One Page Love — Personal",
        "summary": "Personal/one-page site inspiration subset.",
        "best_for": ["personal sites"],
        "not_for": ["enterprise apps"],
        "keywords": ["personal", "one-page", "portfolio"],
    },
    # Landing / copy
    "marketing-examples": {
        "display_name": "Marketing Examples",
        "summary": "Real marketing examples across channels and page types.",
        "best_for": ["campaign structure", "positioning examples"],
        "not_for": ["copying competitor claims"],
        "keywords": ["marketing", "examples", "campaigns"],
    },
    "swipefiles": {
        "display_name": "Swipe Files",
        "summary": "Swipe-file style marketing inspiration library.",
        "best_for": ["landing/email swipe research"],
        "not_for": ["verbatim reuse"],
        "keywords": ["swipefiles", "marketing", "copy"],
    },
    "goodemailcopy": {
        "display_name": "Good Email Copy",
        "summary": "Collection of strong email copy examples.",
        "best_for": ["email messaging tone"],
        "not_for": ["visual UI systems"],
        "keywords": ["email", "copywriting"],
    },
    "really-good-emails": {
        "display_name": "Really Good Emails",
        "summary": "Curated email design and copy gallery.",
        "best_for": ["email layout + copy inspiration"],
        "not_for": ["web app components"],
        "keywords": ["email", "design", "copy"],
    },
    "copywritingexamples": {
        "display_name": "Copywriting Examples",
        "summary": "Library of copywriting samples for product and marketing pages.",
        "best_for": ["headline/CTA drafting"],
        "not_for": ["plagiarizing claims"],
        "keywords": ["copywriting", "headlines", "cta"],
    },
    # Ecommerce
    "baymard": {
        "display_name": "Baymard Institute",
        "summary": "Research-backed ecommerce UX guidelines and benchmark studies.",
        "best_for": ["checkout UX", "product-page research", "ecommerce usability"],
        "not_for": ["free full guideline assumptions without access"],
        "keywords": ["baymard", "ecommerce", "ux-research", "checkout"],
        "topics_contributed": ["ecommerce", "checkout", "usability", "research"],
    },
    "rebuyengine": {
        "display_name": "Rebuy Engine",
        "summary": "Shopify-oriented merchandising/personalization product; useful as commerce-UI context.",
        "best_for": ["commerce merchandising UI context"],
        "not_for": ["generic design systems"],
        "keywords": ["rebuy", "shopify", "merchandising"],
    },
    "shopify-partners-blog": {
        "display_name": "Shopify Partners Blog",
        "summary": "Shopify partner articles on commerce UX, apps, and themes.",
        "best_for": ["Shopify ecosystem guidance"],
        "not_for": ["non-Shopify generic UI rules"],
        "keywords": ["shopify", "partners", "commerce", "blog"],
    },
    "ecommercefuel": {
        "display_name": "EcommerceFuel",
        "summary": "Ecommerce operator community/content.",
        "best_for": ["operator perspective on store UX"],
        "not_for": ["component libraries"],
        "keywords": ["ecommercefuel", "operators", "commerce"],
    },
    "builtfor-shopify": {
        "display_name": "Built for Shopify",
        "summary": "Shopify quality/program surface for apps meeting higher standards.",
        "best_for": ["Shopify app UX expectations"],
        "not_for": ["non-Shopify products"],
        "keywords": ["built-for-shopify", "apps", "quality"],
    },
    "themealley": {
        "display_name": "ThemeAlley",
        "summary": "Theme marketplace/directory style resource for store themes.",
        "best_for": ["theme discovery"],
        "not_for": ["accessibility certification"],
        "keywords": ["themes", "marketplace", "ecommerce"],
    },
    "themes-shopify": {
        "display_name": "Shopify Theme Store",
        "summary": "Official Shopify theme store for storefront templates.",
        "best_for": ["storefront theme research"],
        "not_for": ["copying theme code without license"],
        "keywords": ["shopify", "themes", "storefront"],
    },
}


REGISTERED_SOURCE_CARDS: dict[str, dict[str, Any]] = {
    "wcag-22": {
        "summary": "Normative accessibility success criteria and conformance model.",
        "best_for": ["accessibility requirements", "completion gates", "audit baselines"],
        "when_to_use": ["Any interface that must be perceivable, operable, understandable, or robust."],
        "keywords": ["wcag", "accessibility", "conformance", "a11y"],
    },
    "wai-aria-apg": {
        "summary": "Authoring practices for ARIA patterns, keyboard interaction, and widget structure.",
        "best_for": ["dialogs", "tabs", "menus", "comboboxes", "landmarks"],
        "when_to_use": ["Building or auditing complex widgets and keyboard UX."],
        "keywords": ["aria", "apg", "keyboard", "patterns", "widgets"],
    },
    "mdn-web-docs": {
        "summary": "Platform reference for HTML/CSS/JS behavior, accessibility, and compatibility.",
        "best_for": ["browser APIs", "element semantics", "compat checks"],
        "when_to_use": ["Need authoritative platform behavior rather than framework opinion."],
        "keywords": ["mdn", "html", "css", "javascript", "compat"],
    },
    "webdev": {
        "summary": "Chrome-team guidance on performance, responsive design, forms, and web quality.",
        "best_for": ["Core Web Vitals", "performance", "responsive techniques"],
        "when_to_use": ["Optimizing delivery, rendering, and modern web quality."],
        "keywords": ["web.dev", "performance", "vitals", "responsive"],
    },
    "react-docs": {
        "summary": "Official React documentation for component architecture and state behavior.",
        "best_for": ["React state", "effects", "composition"],
        "when_to_use": ["React-specific implementation decisions."],
        "keywords": ["react", "hooks", "state", "docs"],
    },
    "nextjs-docs": {
        "summary": "Official Next.js docs for App Router, rendering, metadata, and deployment patterns.",
        "best_for": ["routing", "SSR/SSG", "metadata", "Next-specific architecture"],
        "when_to_use": ["Working in a Next.js codebase."],
        "keywords": ["nextjs", "app-router", "vercel", "docs"],
    },
    "material-3": {
        "summary": "Material Design 3 system guidance and related implementation references.",
        "best_for": ["Material theming", "component anatomy"],
        "when_to_use": ["Product already committed to Material language."],
        "keywords": ["material", "m3", "design-system"],
    },
    "apple-hig": {
        "summary": "Apple HIG for clarity, accessibility, motion restraint, and platform craft.",
        "best_for": ["quality of craft", "motion etiquette", "accessibility mindset"],
        "when_to_use": ["Need platform-grade interaction principles, not Apple asset copying."],
        "keywords": ["apple", "hig", "craft", "accessibility"],
    },
    "fluent-2": {
        "summary": "Microsoft Fluent 2 design system for enterprise product UI and tokens.",
        "best_for": ["enterprise theming", "semantic tokens", "high contrast"],
        "when_to_use": ["Building Fluent-aligned or enterprise Windows-adjacent experiences."],
        "keywords": ["fluent", "microsoft", "tokens"],
    },
    "carbon-design-system": {
        "summary": "IBM Carbon design system for dense enterprise and data products.",
        "best_for": ["data-heavy UI", "enterprise components", "content guidelines"],
        "when_to_use": ["Complex operational interfaces needing structured systems."],
        "keywords": ["carbon", "ibm", "enterprise", "data"],
    },
    "polaris": {
        "summary": "Shopify Polaris guidance for commerce admin and merchant workflows.",
        "best_for": ["commerce admin", "forms", "merchant UX"],
        "when_to_use": ["Shopify admin/commerce product surfaces."],
        "keywords": ["polaris", "shopify", "commerce"],
    },
    "primer-design-system": {
        "summary": "GitHub Primer system for developer-tool interfaces and practical a11y patterns.",
        "best_for": ["developer tools", " pragmatic accessibility"],
        "when_to_use": ["Building tools for technical audiences."],
        "keywords": ["primer", "github", "developer-tools"],
    },
    "govuk-design-system": {
        "summary": "GOV.UK system focused on clear public-service forms and evidenced accessibility.",
        "best_for": ["forms", "errors", "public-service content"],
        "when_to_use": ["High-stakes informational or government-like services."],
        "keywords": ["govuk", "forms", "public-service"],
    },
    "uswds": {
        "summary": "U.S. Web Design System for accessible federal/public services.",
        "best_for": ["public services", "trust", "accessible components"],
        "when_to_use": ["Civic/public-facing experiences needing clarity and trust."],
        "keywords": ["uswds", "federal", "accessibility"],
    },
    "spectrum-design-system": {
        "summary": "Adobe Spectrum system with strong color and adaptive design guidance.",
        "best_for": ["color systems", "adaptive UI", "product design-system structure"],
        "when_to_use": ["Designing resilient cross-product component systems."],
        "keywords": ["spectrum", "adobe", "color"],
    },
    "react-aria": {
        "summary": "Accessible React behavior hooks/components across modalities and locales.",
        "best_for": ["complex widgets", "keyboard/touch parity", "i18n interactions"],
        "when_to_use": ["Need behavior correctness more than styling."],
        "keywords": ["react-aria", "accessibility", "hooks", "i18n"],
    },
    "radix-primitives": {
        "summary": "Unstyled accessible React primitives used widely under design systems like shadcn.",
        "best_for": ["dialogs", "menus", "tabs", "focus management"],
        "when_to_use": ["Need composable accessible behavior with custom visuals."],
        "keywords": ["radix", "primitives", "accessible", "focus"],
    },
    "transitions-dev-repo": {
        "summary": "Motion transition showcase and generator-oriented repository.",
        "best_for": ["transition vocabulary", "motion pattern study"],
        "when_to_use": ["Refining motion language; verify license before copying code."],
        "keywords": ["transitions", "motion", "css"],
    },
    "emil-design-skills": {
        "summary": "Credible practitioner skills for motion opportunity selection, animation review and planning, direct manipulation, gesture physics, animation vocabulary, typography, materials, and design craft.",
        "best_for": ["animation review", "motion opportunity filtering", "gesture and direct-manipulation design", "system-level motion audits", "interaction polish"],
        "when_to_use": ["Need implementation-oriented motion craft heuristics with explicit frequency, accessibility, interruption, and runtime verification context."],
        "keywords": ["emil", "motion", "animation-review", "gesture", "direct-manipulation", "velocity", "motion-audit", "skills"],
    },
    "taste-skill-repo": {
        "summary": "Anti-slop frontend skill collection emphasizing brief inference and completion checks.",
        "best_for": ["anti-slop review", "direction selection workflows"],
        "when_to_use": ["Need experimental workflow ideas; do not treat aesthetic bans as universal law."],
        "keywords": ["taste-skill", "anti-slop", "skills"],
    },
    "kill-ai-slop": {
        "summary": "Field guide/scanner taxonomy for detecting AI-slop visual and copy signals.",
        "best_for": ["slop triage categories", "audit method inspiration"],
        "when_to_use": ["Inspiration only while license remains unresolved; synthesize, do not copy."],
        "keywords": ["anti-slop", "taxonomy", "audit"],
    },
    "amicro-micro-transitions": {
        "summary": "React micro-interaction showcase for control-state feedback ideas.",
        "best_for": ["button/hover micro-interaction catalogs"],
        "when_to_use": ["Inspiration only; license claim lacked LICENSE file at inspection."],
        "keywords": ["micro-interactions", "motion", "react"],
    },
}


def _title_from_id(source_id: str, fallback_name: str) -> str:
    if fallback_name and fallback_name.lower() not in {"ui", "bg", "fonts", "design", "blocks", "themes", "registry"}:
        if any(ch.isupper() for ch in fallback_name[1:]) or " " in fallback_name:
            return fallback_name
    cleaned = SLUG_CLEAN.sub(" ", source_id).strip()
    return cleaned.title() if cleaned else fallback_name or source_id


def _fallback_card(source: dict[str, Any], category_id: str) -> dict[str, Any]:
    cat = CATEGORY_CARDS.get(category_id, {})
    name = _title_from_id(str(source.get("id") or ""), str(source.get("name") or ""))
    host = ""
    url = str(source.get("canonical_url") or "")
    if "://" in url:
        host = HOST_CLEAN.sub("", url.split("://", 1)[1].split("/", 1)[0])
    return {
        "display_name": name,
        "summary": f"{name} — {cat.get('summary', 'Frontend discovery source.')}",
        "best_for": list(cat.get("use_when") or ["discovery"]),
        "not_for": list(cat.get("not_for") or ["unchecked copying"]),
        "keywords": sorted(set([*(cat.get("keywords") or []), *(source.get("id", "").split("-")), *host.split(".")[:2]])),
    }


def enrich_seed(seed: dict[str, Any]) -> dict[str, Any]:
    categories = []
    for category in seed.get("categories") or []:
        category_id = str(category.get("id") or "")
        cat_card = CATEGORY_CARDS.get(category_id, {})
        defaults = dict(category.get("defaults") or {})
        if cat_card:
            defaults.setdefault("category_summary", cat_card.get("summary"))
            defaults.setdefault("category_use_when", cat_card.get("use_when"))
            defaults.setdefault("category_not_for", cat_card.get("not_for"))
            # Keep existing topics, but ensure keywords exist at category level for inheritance.
            defaults.setdefault("keywords", cat_card.get("keywords"))
        sources = []
        for source in category.get("sources") or []:
            item = dict(source)
            source_id = str(item.get("id") or "")
            card = SOURCE_CARDS.get(source_id)
            if card is None and item.get("summary") and item.get("keywords"):
                # Preserve previously baked discovery cards (e.g. library expansions).
                card = {
                    "display_name": item.get("name"),
                    "summary": item.get("summary"),
                    "best_for": item.get("best_for") or [],
                    "not_for": item.get("not_for") or [],
                    "keywords": item.get("keywords") or [],
                    "topics_contributed": item.get("topics_contributed"),
                }
            if card is None:
                card = _fallback_card(item, category_id)
            # Prefer curated card fields; do not invent license/classification.
            item["name"] = card.get("display_name") or item.get("name")
            item["summary"] = card["summary"]
            item["best_for"] = card.get("best_for") or []
            item["not_for"] = card.get("not_for") or []
            item["keywords"] = card.get("keywords") or []
            if card.get("topics_contributed"):
                item["topics_contributed"] = card["topics_contributed"]
            item["findability_status"] = "discovery-card"
            sources.append(item)
        categories.append({**category, "defaults": defaults, "sources": sources})
    updated = dict(seed)
    updated["categories"] = categories
    updated["findability"] = {
        "schema": "source-discovery-card/0.1",
        "note": (
            "summary/best_for/not_for/keywords are discovery findability aids. "
            "They are not inspections, license grants, or promotion decisions."
        ),
        "last_enriched": "2026-07-12",
    }
    return updated


def enrich_knowledge_sources(payload: dict[str, Any]) -> dict[str, Any]:
    sources = []
    for source in payload.get("sources") or []:
        item = dict(source)
        card = REGISTERED_SOURCE_CARDS.get(str(item.get("id") or ""), {})
        if card:
            item["summary"] = card["summary"]
            item["best_for"] = card.get("best_for") or []
            item["when_to_use"] = card.get("when_to_use") or []
            item["keywords"] = card.get("keywords") or []
        sources.append(item)
    updated = dict(payload)
    updated["sources"] = sources
    updated["findability"] = {
        "schema": "registered-source-card/0.1",
        "note": "Findability fields help retrieval choose registered evidence sources; provenance remains in the registry.",
        "last_enriched": "2026-07-12",
    }
    return updated


def build_findability_index(seed: dict[str, Any]) -> str:
    lines = [
        "# Source findability index",
        "",
        "Generated discovery cards for the seed catalog. Use this to route tasks to the right source family.",
        "These cards do not grant copy permission and do not replace item-level license review.",
        "",
    ]
    need_map: list[tuple[str, list[str]]] = [
        ("Website / admin / SaaS templates", ["vercel-templates", "tailwindtemplates-io", "themewagon", "html5up", "startbootstrap", "shadcn-taxonomy", "next-saas-stripe-starter", "coreui", "shipfast"]),
        ("Accessible dialogs, menus, comboboxes, focus", ["react-aria", "react-aria-components", "radix-primitives", "ariakit", "base-ui", "bits-ui", "headless-ui", "floating-ui", "cmdk-paco-me"]),
        ("Animated marketing sections / kinetic polish", ["magic-ui", "aceternity-ui", "react-bits", "animate-ui", "motion-primitives", "farm-ui", "eldoraui-site"]),
        ("shadcn / Tailwind app component systems", ["shadcn-ui", "kibo-ui", "originui", "tweakcn", "awesome-shadcn-ui-vercel", "platejs"]),
        ("Enterprise design systems", ["ant-design", "mui", "carbondesignsystem", "fluent2-microsoft", "primer-style", "polaris-shopify"]),
        ("Dashboards, charts, data tables", ["tremor-so", "tanstack-table-latest", "ag-grid", "recharts", "apache-echarts", "nivo", "tabler"]),
        ("Official design-system guidance", ["m3-material", "carbondesignsystem", "primer-style", "polaris-shopify", "fluent2-microsoft", "design-system-service-gov-uk", "open-props"]),
        ("Motion libraries and easing tools", ["motion", "react-spring", "gsap", "lenis", "theatrejs", "view-transitions-chrome", "auto-animate-formkit", "easings"]),
        ("Icons, illustrations, backgrounds", ["lucide", "heroicons", "remixicon", "feathericons", "undraw", "haikei", "bg-ibelick"]),
        ("Typography and fluid type", ["fonts-google", "utopia-fyi", "fontsource", "recursive-design", "modernfontstacks", "typewolf"]),
        ("Color ramps and contrast", ["leonardocolor", "accessiblepalette", "webaim-resources-contrastchecker", "whocanuse", "huetone", "tints"]),
        ("Inspiration-only galleries", ["awwwards", "mobbin", "page-flows", "godly", "refero", "saasframe", "growth-design"]),
        ("Landing copy and messaging", ["marketing-examples", "copywritingexamples", "copyhackers", "really-good-emails", "goodemailcopy"]),
        ("Ecommerce UX", ["baymard", "polaris-shopify", "medusa", "saleor", "themes-shopify", "builtfor-shopify"]),
        ("AI/MCP component discovery", ["21st-dev-mcp", "21st-dev", "assistant-ui", "copilotkit", "vercel-ai-sdk", "v0"]),
    ]
    by_id = {}
    for category in seed.get("categories") or []:
        for source in category.get("sources") or []:
            by_id[str(source.get("id"))] = source
    lines.append("## Route by need")
    lines.append("")
    for title, ids in need_map:
        lines.append(f"### {title}")
        lines.append("")
        for source_id in ids:
            source = by_id.get(source_id)
            if not source:
                continue
            lines.append(
                f"- `{source_id}` — **{source.get('name')}**: {source.get('summary')}"
            )
        lines.append("")
    lines.append("## Categories")
    lines.append("")
    for category in seed.get("categories") or []:
        lines.append(f"### {category.get('label')} (`{category.get('id')}`)")
        lines.append("")
        summary = (category.get("defaults") or {}).get("category_summary")
        if summary:
            lines.append(summary)
            lines.append("")
        for source in category.get("sources") or []:
            best = ", ".join((source.get("best_for") or [])[:3])
            lines.append(f"- `{source.get('id')}` — {source.get('name')}: {source.get('summary')} _Best for:_ {best}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate enrichment coverage without writing.")
    args = parser.parse_args(argv)

    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    enriched_seed = enrich_seed(seed)
    missing = []
    for category in enriched_seed["categories"]:
        for source in category["sources"]:
            if not source.get("summary") or not source.get("keywords"):
                missing.append(source.get("id"))
    if missing:
        raise SystemExit(f"Missing findability fields for: {', '.join(missing)}")

    knowledge = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    enriched_knowledge = enrich_knowledge_sources(knowledge)
    for source in enriched_knowledge["sources"]:
        if source["id"] in REGISTERED_SOURCE_CARDS and not source.get("summary"):
            raise SystemExit(f"Registered source missing summary: {source['id']}")

    if args.check:
        print(json.dumps({
            "seed_sources": sum(len(c["sources"]) for c in enriched_seed["categories"]),
            "curated_source_cards": len(SOURCE_CARDS),
            "registered_source_cards": len(REGISTERED_SOURCE_CARDS),
            "ok": True,
        }))
        return 0

    SEED_PATH.write_text(json.dumps(enriched_seed, indent=2) + "\n", encoding="utf-8")
    SOURCES_PATH.write_text(json.dumps(enriched_knowledge, indent=2) + "\n", encoding="utf-8")
    INDEX_PATH.write_text(build_findability_index(enriched_seed), encoding="utf-8")
    print(f"Wrote {SEED_PATH}")
    print(f"Wrote {SOURCES_PATH}")
    print(f"Wrote {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
