#!/usr/bin/env python3
"""Expand the seed catalog with additional discovery sources and cards.

New entries remain unresolved/inspiration-only seeds. This does not inspect
upstream sites, grant licenses, or promote stable knowledge.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from enrich_source_cards import SOURCE_CARDS, enrich_seed, enrich_knowledge_sources, build_findability_index


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "seed-catalog.yml"
SOURCES_PATH = PLUGIN_ROOT / "knowledge" / "sources.json"
INDEX_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "source-findability.md"


# category_id -> list of seed dicts
EXPANSIONS: dict[str, list[dict[str, Any]]] = {
    "agent-mcp-ai-ui": [
        {"id": "assistant-ui", "name": "Assistant UI", "canonical_url": "https://www.assistant-ui.com", "supplied_url": "https://www.assistant-ui.com/"},
        {"id": "copilotkit", "name": "CopilotKit", "canonical_url": "https://www.copilotkit.ai", "supplied_url": "https://www.copilotkit.ai/"},
        {"id": "langui", "name": "LangUI", "canonical_url": "https://www.langui.dev", "supplied_url": "https://www.langui.dev/"},
        {"id": "vercel-ai-chatbot", "name": "Vercel AI Chatbot", "canonical_url": "https://github.com/vercel/ai-chatbot", "supplied_url": "https://github.com/vercel/ai-chatbot"},
    ],
    "component-catalogs": [
        {"id": "untitled-ui", "name": "Untitled UI", "canonical_url": "https://www.untitledui.com", "supplied_url": "https://www.untitledui.com/"},
        {"id": "farm-ui", "name": "Farm UI", "canonical_url": "https://farmui.com", "supplied_url": "https://farmui.com/"},
        {"id": "react-email", "name": "React Email", "canonical_url": "https://react.email", "supplied_url": "https://react.email/"},
        {"id": "component-gallery", "name": "Component Gallery", "canonical_url": "https://component.gallery", "supplied_url": "https://component.gallery/"},
        {"id": "semantic-ui-react", "name": "Semantic UI React", "canonical_url": "https://react.semantic-ui.com", "supplied_url": "https://react.semantic-ui.com/"},
    ],
    "shadcn-ecosystem": [
        {"id": "platejs", "name": "Plate", "canonical_url": "https://platejs.org", "supplied_url": "https://platejs.org/"},
        {"id": "novel", "name": "Novel", "canonical_url": "https://novel.sh", "supplied_url": "https://novel.sh/"},
        {"id": "shadcn-ui-directory", "name": "shadcn Directory", "canonical_url": "https://www.shadcn.io", "supplied_url": "https://www.shadcn.io/"},
    ],
    "tailwind-blocks-templates": [
        {"id": "flyonui", "name": "FlyonUI", "canonical_url": "https://flyonui.com", "supplied_url": "https://flyonui.com/"},
        {"id": "sailboatui", "name": "Sailboat UI", "canonical_url": "https://sailboatui.com", "supplied_url": "https://sailboatui.com/"},
        {"id": "ripple-ui", "name": "Ripple UI", "canonical_url": "https://www.ripple-ui.com", "supplied_url": "https://www.ripple-ui.com/"},
        {"id": "flowbite-react", "name": "Flowbite React", "canonical_url": "https://flowbite-react.com", "supplied_url": "https://flowbite-react.com/"},
    ],
    "accessible-primitives": [
        {"id": "bits-ui", "name": "Bits UI", "canonical_url": "https://bits-ui.com", "supplied_url": "https://bits-ui.com/"},
        {"id": "base-ui", "name": "Base UI", "canonical_url": "https://base-ui.com", "supplied_url": "https://base-ui.com/"},
        {"id": "tanstack-form-latest", "name": "TanStack Form", "canonical_url": "https://tanstack.com/form/latest", "supplied_url": "https://tanstack.com/form/latest"},
        {"id": "tanstack-virtual-latest", "name": "TanStack Virtual", "canonical_url": "https://tanstack.com/virtual/latest", "supplied_url": "https://tanstack.com/virtual/latest"},
        {"id": "react-aria-components", "name": "React Aria Components", "canonical_url": "https://react-spectrum.adobe.com/react-aria/components.html", "supplied_url": "https://react-spectrum.adobe.com/react-aria/components.html"},
    ],
    "dashboard-data-app-ui": [
        {"id": "ag-grid", "name": "AG Grid", "canonical_url": "https://www.ag-grid.com", "supplied_url": "https://www.ag-grid.com/"},
        {"id": "apache-echarts", "name": "Apache ECharts", "canonical_url": "https://echarts.apache.org", "supplied_url": "https://echarts.apache.org/"},
        {"id": "plotly-javascript", "name": "Plotly.js", "canonical_url": "https://plotly.com/javascript/", "supplied_url": "https://plotly.com/javascript/"},
        {"id": "handsontable", "name": "Handsontable", "canonical_url": "https://handsontable.com", "supplied_url": "https://handsontable.com/"},
    ],
    "design-systems-product-ui": [
        {"id": "ant-design", "name": "Ant Design", "canonical_url": "https://ant.design", "supplied_url": "https://ant.design/"},
        {"id": "mui", "name": "MUI", "canonical_url": "https://mui.com", "supplied_url": "https://mui.com/"},
        {"id": "bootstrap", "name": "Bootstrap", "canonical_url": "https://getbootstrap.com", "supplied_url": "https://getbootstrap.com/"},
        {"id": "shoelace", "name": "Shoelace", "canonical_url": "https://shoelace.style", "supplied_url": "https://shoelace.style/"},
        {"id": "open-props", "name": "Open Props", "canonical_url": "https://open-props.style", "supplied_url": "https://open-props.style/"},
        {"id": "bulma", "name": "Bulma", "canonical_url": "https://bulma.io", "supplied_url": "https://bulma.io/"},
    ],
    "motion-animation": [
        {"id": "lenis", "name": "Lenis", "canonical_url": "https://lenis.darkroom.engineering", "supplied_url": "https://lenis.darkroom.engineering/"},
        {"id": "theatrejs", "name": "Theatre.js", "canonical_url": "https://www.theatrejs.com", "supplied_url": "https://www.theatrejs.com/"},
        {"id": "view-transitions-chrome", "name": "View Transitions API", "canonical_url": "https://developer.chrome.com/docs/web-platform/view-transitions", "supplied_url": "https://developer.chrome.com/docs/web-platform/view-transitions"},
        {"id": "barba-js", "name": "Barba.js", "canonical_url": "https://barba.js.org", "supplied_url": "https://barba.js.org/"},
    ],
    "icons-illustrations-backgrounds": [
        {"id": "remixicon", "name": "Remix Icon", "canonical_url": "https://remixicon.com", "supplied_url": "https://remixicon.com/"},
        {"id": "feathericons", "name": "Feather Icons", "canonical_url": "https://feathericons.com", "supplied_url": "https://feathericons.com/"},
        {"id": "bootstrap-icons", "name": "Bootstrap Icons", "canonical_url": "https://icons.getbootstrap.com", "supplied_url": "https://icons.getbootstrap.com/"},
        {"id": "fontawesome", "name": "Font Awesome", "canonical_url": "https://fontawesome.com", "supplied_url": "https://fontawesome.com/"},
        {"id": "ionicons", "name": "Ionicons", "canonical_url": "https://ionic.io/ionicons", "supplied_url": "https://ionic.io/ionicons"},
    ],
    "fonts-typography": [
        {"id": "fontsquirrel", "name": "Font Squirrel", "canonical_url": "https://www.fontsquirrel.com", "supplied_url": "https://www.fontsquirrel.com/"},
        {"id": "adobe-fonts", "name": "Adobe Fonts", "canonical_url": "https://fonts.adobe.com", "supplied_url": "https://fonts.adobe.com/"},
        {"id": "recursive-design", "name": "Recursive", "canonical_url": "https://www.recursive.design", "supplied_url": "https://www.recursive.design/"},
    ],
    "color-theme-tools": [
        {"id": "whocanuse", "name": "Who Can Use", "canonical_url": "https://www.whocanuse.com", "supplied_url": "https://www.whocanuse.com/"},
        {"id": "colorable", "name": "Colorable", "canonical_url": "https://colorable.jxnblk.com", "supplied_url": "https://colorable.jxnblk.com/"},
        {"id": "contrast-ratio", "name": "Contrast Ratio", "canonical_url": "https://contrast-ratio.com", "supplied_url": "https://contrast-ratio.com/"},
        {"id": "huetone", "name": "Huetone", "canonical_url": "https://huetone.ardov.me", "supplied_url": "https://huetone.ardov.me/"},
    ],
    "inspiration-catalogs": [
        {"id": "saasframe", "name": "SaaSframe", "canonical_url": "https://www.saasframe.io", "supplied_url": "https://www.saasframe.io/", "classification": "inspiration-only"},
        {"id": "growth-design", "name": "Growth.Design", "canonical_url": "https://growth.design", "supplied_url": "https://growth.design/", "classification": "inspiration-only"},
        {"id": "laws-of-ux", "name": "Laws of UX", "canonical_url": "https://lawsofux.com", "supplied_url": "https://lawsofux.com/", "classification": "inspiration-only"},
        {"id": "screenshot-club", "name": "Screenshot Club", "canonical_url": "https://screenshot.club", "supplied_url": "https://screenshot.club/", "classification": "inspiration-only"},
    ],
    "portfolio-inspiration": [
        {"id": "read-cv", "name": "Read.cv", "canonical_url": "https://read.cv", "supplied_url": "https://read.cv/", "classification": "inspiration-only"},
        {"id": "bento-me", "name": "Bento", "canonical_url": "https://bento.me", "supplied_url": "https://bento.me/", "classification": "inspiration-only"},
        {"id": "cargo-site", "name": "Cargo", "canonical_url": "https://cargo.site", "supplied_url": "https://cargo.site/", "classification": "inspiration-only"},
        {"id": "tonik", "name": "Tonik", "canonical_url": "https://www.tonik.com", "supplied_url": "https://www.tonik.com/", "classification": "inspiration-only"},
    ],
    "landing-startup-references": [
        {"id": "copyhackers", "name": "Copyhackers", "canonical_url": "https://copyhackers.com", "supplied_url": "https://copyhackers.com/"},
        {"id": "refined-so", "name": "Refined", "canonical_url": "https://www.refined.site", "supplied_url": "https://www.refined.site/", "classification": "inspiration-only"},
        {"id": "landing-page-checklist", "name": "Landing Page Checklist", "canonical_url": "https://www.checklist.design", "supplied_url": "https://www.checklist.design/"},
    ],
    "ecommerce-product-ui": [
        {"id": "medusa", "name": "Medusa", "canonical_url": "https://medusajs.com", "supplied_url": "https://medusajs.com/"},
        {"id": "saleor", "name": "Saleor", "canonical_url": "https://saleor.io", "supplied_url": "https://saleor.io/"},
        {"id": "snipcart", "name": "Snipcart", "canonical_url": "https://snipcart.com", "supplied_url": "https://snipcart.com/"},
        {"id": "commercejs", "name": "Commerce.js", "canonical_url": "https://commercejs.com", "supplied_url": "https://commercejs.com/"},
    ],
}


EXPANSION_CARDS: dict[str, dict[str, Any]] = {
    "assistant-ui": {
        "display_name": "Assistant UI",
        "summary": "React components and primitives for AI chat and assistant interfaces.",
        "best_for": ["chat UIs", "assistant threads", "tool-call presentation"],
        "not_for": ["generic marketing landings"],
        "keywords": ["assistant-ui", "chat", "ai", "react", "threads"],
        "topics_contributed": ["ai-ui", "chat", "assistant", "components"],
    },
    "copilotkit": {
        "display_name": "CopilotKit",
        "summary": "Framework for in-app AI copilots and generative UI hooks.",
        "best_for": ["product copilots", "in-app AI assistance"],
        "not_for": ["static brochure sites"],
        "keywords": ["copilotkit", "copilot", "ai", "generative-ui"],
    },
    "langui": {
        "display_name": "LangUI",
        "summary": "Open-source Tailwind components oriented to AI/chat product UI.",
        "best_for": ["AI product UI blocks", "chat layouts"],
        "not_for": ["accessibility proof"],
        "keywords": ["langui", "ai", "tailwind", "chat"],
    },
    "vercel-ai-chatbot": {
        "display_name": "Vercel AI Chatbot",
        "summary": "Reference Next.js chatbot template built on the AI SDK.",
        "best_for": ["AI chatbot starters", "streaming UI patterns"],
        "not_for": ["design-system authority"],
        "keywords": ["ai-chatbot", "vercel", "nextjs", "streaming"],
    },
    "untitled-ui": {
        "display_name": "Untitled UI",
        "summary": "Large Figma/React UI kit with extensive product and marketing components.",
        "best_for": ["product UI kits", "design-to-code component coverage"],
        "not_for": ["copying without entitlement"],
        "keywords": ["untitled-ui", "figma", "react", "ui-kit"],
    },
    "farm-ui": {
        "display_name": "Farm UI",
        "summary": "Animated React/Tailwind components and landing sections.",
        "best_for": ["marketing sections", "animated components"],
        "not_for": ["enterprise form systems"],
        "keywords": ["farm-ui", "animated", "tailwind", "landing"],
    },
    "react-email": {
        "display_name": "React Email",
        "summary": "React components and tooling for building HTML emails.",
        "best_for": ["transactional email templates", "email component systems"],
        "not_for": ["web app shells"],
        "keywords": ["react-email", "email", "templates", "react"],
    },
    "component-gallery": {
        "display_name": "Component Gallery",
        "summary": "Directory comparing design-system components across major systems.",
        "best_for": ["cross-system component comparison", "pattern research"],
        "not_for": ["drop-in implementation"],
        "keywords": ["component-gallery", "design-systems", "comparison"],
    },
    "semantic-ui-react": {
        "display_name": "Semantic UI React",
        "summary": "React integration of Semantic UI's component vocabulary.",
        "best_for": ["legacy Semantic UI React apps"],
        "not_for": ["new greenfield defaults"],
        "keywords": ["semantic-ui", "react", "components"],
    },
    "platejs": {
        "display_name": "Plate",
        "summary": "Plugin-based rich text editor framework commonly paired with shadcn stacks.",
        "best_for": ["rich text editors", "document editing UIs"],
        "not_for": ["simple textareas"],
        "keywords": ["plate", "rich-text", "editor", "shadcn"],
    },
    "novel": {
        "display_name": "Novel",
        "summary": "Notion-style WYSIWYG editor built on modern React editor primitives.",
        "best_for": ["document editors", "WYSIWYG experiences"],
        "not_for": ["data grids"],
        "keywords": ["novel", "editor", "wysiwyg", "notion-style"],
    },
    "shadcn-ui-directory": {
        "display_name": "shadcn Directory",
        "summary": "Community directory surface for shadcn-related resources and blocks.",
        "best_for": ["discovering shadcn ecosystem resources"],
        "not_for": ["official API docs"],
        "keywords": ["shadcn", "directory", "blocks", "resources"],
    },
    "flyonui": {
        "display_name": "FlyonUI",
        "summary": "Tailwind component library with semantic classes and themes.",
        "best_for": ["Tailwind component kits", "themed UI assembly"],
        "not_for": ["headless accessibility research"],
        "keywords": ["flyonui", "tailwind", "components", "themes"],
    },
    "sailboatui": {
        "display_name": "Sailboat UI",
        "summary": "Modern Tailwind CSS component collection for product/marketing pages.",
        "best_for": ["Tailwind sections", "product UI blocks"],
        "not_for": ["framework-agnostic primitives"],
        "keywords": ["sailboatui", "tailwind", "components"],
    },
    "ripple-ui": {
        "display_name": "Ripple UI",
        "summary": "Tailwind component kit with utility-first component classes.",
        "best_for": ["Tailwind UI building"],
        "not_for": ["design-system governance"],
        "keywords": ["ripple-ui", "tailwind", "components"],
    },
    "flowbite-react": {
        "display_name": "Flowbite React",
        "summary": "React components built on the Flowbite Tailwind design system.",
        "best_for": ["React + Flowbite apps", "Tailwind React components"],
        "not_for": ["non-Tailwind stacks"],
        "keywords": ["flowbite-react", "tailwind", "react", "components"],
    },
    "bits-ui": {
        "display_name": "Bits UI",
        "summary": "Headless accessible component primitives for Svelte.",
        "best_for": ["Svelte accessible widgets", "headless Svelte UI"],
        "not_for": ["React-only projects"],
        "keywords": ["bits-ui", "svelte", "headless", "accessible"],
        "topics_contributed": ["accessibility", "primitives", "svelte", "keyboard"],
    },
    "base-ui": {
        "display_name": "Base UI",
        "summary": "Unstyled accessible React primitives from the MUI team.",
        "best_for": ["headless React widgets", "custom-styled accessible components"],
        "not_for": ["Material look-and-feel alone"],
        "keywords": ["base-ui", "mui", "headless", "accessible", "react"],
        "topics_contributed": ["accessibility", "primitives", "keyboard", "components"],
    },
    "tanstack-form-latest": {
        "display_name": "TanStack Form",
        "summary": "Headless form state library with framework adapters.",
        "best_for": ["complex forms", "validation orchestration"],
        "not_for": ["visual form kits"],
        "keywords": ["tanstack-form", "forms", "validation", "headless"],
    },
    "tanstack-virtual-latest": {
        "display_name": "TanStack Virtual",
        "summary": "Headless virtualization utilities for large lists and grids.",
        "best_for": ["virtualized lists", "performance for long collections"],
        "not_for": ["small static lists"],
        "keywords": ["tanstack-virtual", "virtualization", "lists", "performance"],
    },
    "react-aria-components": {
        "display_name": "React Aria Components",
        "summary": "Styled-optional accessible React components built on React Aria behaviors.",
        "best_for": ["accessible component building", "behavior + structure together"],
        "not_for": ["non-React stacks"],
        "keywords": ["react-aria-components", "accessibility", "components", "adobe"],
        "topics_contributed": ["accessibility", "primitives", "components", "keyboard"],
    },
    "ag-grid": {
        "display_name": "AG Grid",
        "summary": "High-performance data grid for complex enterprise table use cases.",
        "best_for": ["enterprise grids", "filtering/sorting at scale"],
        "not_for": ["simple marketing tables", "license-blind commercial use"],
        "keywords": ["ag-grid", "datagrid", "enterprise", "table"],
    },
    "apache-echarts": {
        "display_name": "Apache ECharts",
        "summary": "Feature-rich charting library for interactive data visualization.",
        "best_for": ["complex charts", "dashboard visualization"],
        "not_for": ["tiny decorative sparklines without need"],
        "keywords": ["echarts", "charts", "dataviz", "apache"],
    },
    "plotly-javascript": {
        "display_name": "Plotly.js",
        "summary": "High-level charting library for scientific and analytical visuals.",
        "best_for": ["analytical charts", "interactive scientific plots"],
        "not_for": ["lightweight icon charts"],
        "keywords": ["plotly", "charts", "dataviz", "javascript"],
    },
    "handsontable": {
        "display_name": "Handsontable",
        "summary": "Spreadsheet-like data grid component for web applications.",
        "best_for": ["spreadsheet UX", "editable grids"],
        "not_for": ["read-only simple tables"],
        "keywords": ["handsontable", "spreadsheet", "datagrid"],
    },
    "ant-design": {
        "display_name": "Ant Design",
        "summary": "Enterprise React design system with extensive components and patterns.",
        "best_for": ["enterprise React apps", "admin interfaces", "form-heavy products"],
        "not_for": ["Ant brand cloning on unrelated products"],
        "keywords": ["antd", "ant-design", "enterprise", "react", "design-system"],
        "topics_contributed": ["design-system", "enterprise", "components", "forms"],
    },
    "mui": {
        "display_name": "MUI",
        "summary": "Material UI React component library and related MUI tooling.",
        "best_for": ["Material-based React apps", "dense product UI"],
        "not_for": ["non-Material brands without adaptation"],
        "keywords": ["mui", "material-ui", "react", "design-system"],
        "topics_contributed": ["design-system", "material", "components", "react"],
    },
    "bootstrap": {
        "display_name": "Bootstrap",
        "summary": "Widely used CSS/component framework for responsive page scaffolding.",
        "best_for": ["rapid responsive scaffolding", "familiar component vocabulary"],
        "not_for": ["distinctive brand-first experiences without heavy customization"],
        "keywords": ["bootstrap", "css", "components", "responsive"],
    },
    "shoelace": {
        "display_name": "Shoelace",
        "summary": "Framework-agnostic web component library with accessible defaults.",
        "best_for": ["web components", "framework-agnostic UI"],
        "not_for": ["React-only ecosystems seeking JSX primitives"],
        "keywords": ["shoelace", "web-components", "accessible"],
    },
    "open-props": {
        "display_name": "Open Props",
        "summary": "CSS custom-property design tokens for spacing, color, shadows, and more.",
        "best_for": ["token foundations", "CSS-first design systems"],
        "not_for": ["component behavior"],
        "keywords": ["open-props", "tokens", "css", "design-tokens"],
    },
    "bulma": {
        "display_name": "Bulma",
        "summary": "CSS-only Flexbox component framework.",
        "best_for": ["CSS-only layouts", "simple responsive scaffolds"],
        "not_for": ["JS widget behavior"],
        "keywords": ["bulma", "css", "flexbox", "components"],
    },
    "lenis": {
        "display_name": "Lenis",
        "summary": "Smooth-scroll library used in expressive marketing sites.",
        "best_for": ["smooth scrolling experiences"],
        "not_for": ["accessibility-critical reading flows without careful testing"],
        "keywords": ["lenis", "smooth-scroll", "motion"],
    },
    "theatrejs": {
        "display_name": "Theatre.js",
        "summary": "Animation sequencing toolkit with visual timeline editing.",
        "best_for": ["complex sequenced motion", "timeline-driven UI"],
        "not_for": ["simple hover states"],
        "keywords": ["theatrejs", "timeline", "animation", "sequencing"],
    },
    "view-transitions-chrome": {
        "display_name": "View Transitions API",
        "summary": "Platform documentation for native view transitions between UI states/pages.",
        "best_for": ["page/state transitions", "native motion progressive enhancement"],
        "not_for": ["assuming universal browser support without fallbacks"],
        "keywords": ["view-transitions", "chrome", "animation", "navigation"],
    },
    "barba-js": {
        "display_name": "Barba.js",
        "summary": "Library for fluid page-transition experiences in multi-page sites.",
        "best_for": ["MPA page transitions"],
        "not_for": ["SPA frameworks with their own routers unless carefully integrated"],
        "keywords": ["barba", "page-transitions", "pjax"],
    },
    "remixicon": {
        "display_name": "Remix Icon",
        "summary": "Open-source neutral-style icon set for interface use.",
        "best_for": ["UI icons", "consistent iconography"],
        "not_for": ["brand logos"],
        "keywords": ["remixicon", "icons", "svg"],
    },
    "feathericons": {
        "display_name": "Feather",
        "summary": "Simple open-source line icons popular in product UI.",
        "best_for": ["minimal UI icons"],
        "not_for": ["filled illustration systems"],
        "keywords": ["feather", "icons", "svg"],
    },
    "bootstrap-icons": {
        "display_name": "Bootstrap Icons",
        "summary": "Official icon library for Bootstrap-based interfaces.",
        "best_for": ["Bootstrap projects", "general UI icons"],
        "not_for": ["exclusive brand identity"],
        "keywords": ["bootstrap-icons", "icons"],
    },
    "fontawesome": {
        "display_name": "Font Awesome",
        "summary": "Large icon family with free and Pro tiers; license boundaries matter.",
        "best_for": ["broad icon coverage when licensed appropriately"],
        "not_for": ["assuming Pro icons are free"],
        "keywords": ["fontawesome", "icons", "pro"],
    },
    "ionicons": {
        "display_name": "Ionicons",
        "summary": "Icon set from the Ionic ecosystem for web and mobile UIs.",
        "best_for": ["mobile/web iconography"],
        "not_for": ["custom brand marks"],
        "keywords": ["ionicons", "icons", "ionic"],
    },
    "fontsquirrel": {
        "display_name": "Font Squirrel",
        "summary": "Font finding/hosting resource with licensing filters for web use.",
        "best_for": ["finding web-safe licensed fonts"],
        "not_for": ["skipping per-font license checks"],
        "keywords": ["fontsquirrel", "fonts", "licensing"],
    },
    "adobe-fonts": {
        "display_name": "Adobe Fonts",
        "summary": "Subscription font service integrated with Adobe Creative Cloud.",
        "best_for": ["premium type discovery when entitled"],
        "not_for": ["self-host assumptions without entitlement"],
        "keywords": ["adobe-fonts", "typekit", "fonts"],
    },
    "recursive-design": {
        "display_name": "Recursive",
        "summary": "Variable font designed for code and UI with broad stylistic range.",
        "best_for": ["variable UI/code typography"],
        "not_for": ["ornamental script needs"],
        "keywords": ["recursive", "variable-font", "typography"],
    },
    "whocanuse": {
        "display_name": "Who Can Use",
        "summary": "Contrast tool that visualizes vision-condition impact for color pairs.",
        "best_for": ["inclusive contrast review", "vision-condition awareness"],
        "not_for": ["palette fashion browsing"],
        "keywords": ["whocanuse", "contrast", "accessibility", "vision"],
    },
    "colorable": {
        "display_name": "Colorable",
        "summary": "Tool for testing contrast across combinations in a palette.",
        "best_for": ["palette contrast matrices"],
        "not_for": ["motion guidance"],
        "keywords": ["colorable", "contrast", "palette"],
    },
    "contrast-ratio": {
        "display_name": "Contrast Ratio",
        "summary": "Simple WCAG contrast-ratio calculator by Lea Verou.",
        "best_for": ["quick contrast checks"],
        "not_for": ["full palette systems"],
        "keywords": ["contrast-ratio", "wcag", "accessibility"],
    },
    "huetone": {
        "display_name": "Huetone",
        "summary": "Perceptually-oriented color scale editor for design tokens.",
        "best_for": ["LCH-ish ramps", "token palette crafting"],
        "not_for": ["illustration gradients only"],
        "keywords": ["huetone", "color-scales", "tokens", "lch"],
    },
    "saasframe": {
        "display_name": "SaaSframe",
        "summary": "SaaS product and landing-page screenshot inspiration library.",
        "best_for": ["SaaS UI inspiration", "marketing page research"],
        "not_for": ["code copy"],
        "keywords": ["saasframe", "saas", "inspiration", "screenshots"],
    },
    "growth-design": {
        "display_name": "Growth.Design",
        "summary": "Case-study style product psychology and UX storytelling references.",
        "best_for": ["UX case-study inspiration", "growth-product patterns"],
        "not_for": ["implementation snippets"],
        "keywords": ["growth-design", "ux", "case-study", "psychology"],
    },
    "laws-of-ux": {
        "display_name": "Laws of UX",
        "summary": "Illustrated collection of UX heuristics and cognitive principles.",
        "best_for": ["heuristic reminders", "design rationale language"],
        "not_for": ["visual asset reuse"],
        "keywords": ["laws-of-ux", "heuristics", "ux", "psychology"],
    },
    "screenshot-club": {
        "display_name": "Screenshot Club",
        "summary": "Curated product screenshot inspiration.",
        "best_for": ["product UI browsing"],
        "not_for": ["copying UI chrome"],
        "keywords": ["screenshot-club", "screenshots", "inspiration"],
    },
    "read-cv": {
        "display_name": "Read.cv",
        "summary": "Professional profile/CV pages often used as portfolio references.",
        "best_for": ["personal profile layout inspiration"],
        "not_for": ["cloning profiles"],
        "keywords": ["read-cv", "portfolio", "cv", "profile"],
    },
    "bento-me": {
        "display_name": "Bento",
        "summary": "Link-in-bio / personal page product with bento-style layouts.",
        "best_for": ["personal page layout inspiration"],
        "not_for": ["enterprise app shells"],
        "keywords": ["bento", "personal", "link-in-bio"],
    },
    "cargo-site": {
        "display_name": "Cargo",
        "summary": "Creative portfolio website platform used by designers/artists.",
        "best_for": ["creative portfolio direction"],
        "not_for": ["SaaS admin UI"],
        "keywords": ["cargo", "portfolio", "creative"],
    },
    "tonik": {
        "display_name": "Tonik",
        "summary": "Portfolio and personal-site inspiration resource.",
        "best_for": ["portfolio browsing"],
        "not_for": ["component APIs"],
        "keywords": ["tonik", "portfolio", "inspiration"],
    },
    "copyhackers": {
        "display_name": "Copyhackers",
        "summary": "Conversion-oriented copywriting education and examples.",
        "best_for": ["landing copy craft", "conversion messaging"],
        "not_for": ["visual component libraries"],
        "keywords": ["copyhackers", "copywriting", "conversion"],
    },
    "refined-so": {
        "display_name": "Refined",
        "summary": "Curated website/product inspiration references.",
        "best_for": ["visual direction browsing"],
        "not_for": ["code extraction"],
        "keywords": ["refined", "inspiration", "websites"],
    },
    "landing-page-checklist": {
        "display_name": "Checklist Design",
        "summary": "UI checklist resource for interface quality and landing-page completeness.",
        "best_for": ["landing QA checklists", "UI completeness review"],
        "not_for": ["visual asset packs"],
        "keywords": ["checklist", "landing", "qa", "ui"],
    },
    "medusa": {
        "display_name": "Medusa",
        "summary": "Open-source commerce platform with storefront/admin UI surfaces.",
        "best_for": ["headless commerce architecture", "storefront patterns"],
        "not_for": ["non-commerce marketing sites"],
        "keywords": ["medusa", "ecommerce", "headless", "storefront"],
    },
    "saleor": {
        "display_name": "Saleor",
        "summary": "Open-source composable commerce platform and storefront examples.",
        "best_for": ["composable commerce UI", "storefront references"],
        "not_for": ["unrelated SaaS dashboards"],
        "keywords": ["saleor", "ecommerce", "storefront"],
    },
    "snipcart": {
        "display_name": "Snipcart",
        "summary": "Cart platform for adding ecommerce to existing sites.",
        "best_for": ["lightweight cart integration patterns"],
        "not_for": ["full marketplace architecture"],
        "keywords": ["snipcart", "cart", "ecommerce"],
    },
    "commercejs": {
        "display_name": "Commerce.js",
        "summary": "Headless ecommerce API/platform with storefront integration patterns.",
        "best_for": ["headless commerce frontends"],
        "not_for": ["design-system tokens"],
        "keywords": ["commercejs", "headless", "ecommerce"],
    },
}


def merge_expansions(seed: dict[str, Any]) -> dict[str, Any]:
    categories = []
    existing_ids: set[str] = set()
    existing_urls: set[str] = set()
    for category in seed.get("categories") or []:
        for source in category.get("sources") or []:
            existing_ids.add(str(source.get("id")))
            existing_urls.add(str(source.get("canonical_url")))
        categories.append(category)

    added = 0
    for category in categories:
        category_id = str(category.get("id") or "")
        extras = EXPANSIONS.get(category_id) or []
        sources = list(category.get("sources") or [])
        for item in extras:
            source_id = str(item["id"])
            url = str(item["canonical_url"])
            if source_id in existing_ids or url in existing_urls:
                continue
            sources.append(dict(item))
            existing_ids.add(source_id)
            existing_urls.add(url)
            added += 1
        category["sources"] = sources
    updated = dict(seed)
    updated["categories"] = categories
    updated["catalog_revision"] = "2026-07-12"
    updated.setdefault("expansion_log", [])
    if "2026-07-12-library-expansion" not in updated["expansion_log"]:
        updated["expansion_log"].append("2026-07-12-library-expansion")
    updated["expansion_added"] = added
    return updated


def main() -> int:
    # Ensure cards are available to enrich_source_cards import path by mutating SOURCE_CARDS.
    SOURCE_CARDS.update(EXPANSION_CARDS)

    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    # If already expanded, avoid duplicating; still refresh cards/index.
    already = set(seed.get("expansion_log") or [])
    if "2026-07-12-library-expansion" not in already:
        seed = merge_expansions(seed)
    else:
        # Still merge in case file was partially edited.
        seed = merge_expansions(seed)

    enriched = enrich_seed(seed)
    total = sum(len(c["sources"]) for c in enriched["categories"])
    SEED_PATH.write_text(json.dumps(enriched, indent=2) + "\n", encoding="utf-8")

    knowledge = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    SOURCES_PATH.write_text(json.dumps(enrich_knowledge_sources(knowledge), indent=2) + "\n", encoding="utf-8")
    INDEX_PATH.write_text(build_findability_index(enriched), encoding="utf-8")

    print(json.dumps({
        "total_sources": total,
        "added_this_run": seed.get("expansion_added", 0),
        "expansion_cards": len(EXPANSION_CARDS),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
