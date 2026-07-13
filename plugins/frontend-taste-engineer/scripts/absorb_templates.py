#!/usr/bin/env python3
"""Absorb template catalogs, starters, and UI kits into the seed library.

Adds discovery metadata only. Does not download, copy, or promote templates.
Paid marketplaces are tagged so agents treat them as entitlement-gated.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from enrich_source_cards import (
    SOURCE_CARDS,
    build_findability_index,
    enrich_knowledge_sources,
    enrich_seed,
)


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "seed-catalog.yml"
SOURCES_PATH = PLUGIN_ROOT / "knowledge" / "sources.json"
INDEX_PATH = PLUGIN_ROOT / "research" / "source-discovery" / "source-findability.md"
EXPANSION_ID = "2026-07-12-template-absorption"


def _s(
    source_id: str,
    name: str,
    url: str,
    *,
    summary: str,
    best_for: list[str],
    not_for: list[str] | None = None,
    keywords: list[str] | None = None,
    topics: list[str] | None = None,
    classification: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    seed: dict[str, Any] = {
        "id": source_id,
        "name": name,
        "canonical_url": url.rstrip("/"),
        "supplied_url": url if url.endswith("/") else url + "/",
    }
    # Keep GitHub and docs URLs exact when path matters.
    if "github.com" in url or "/docs/" in url or "/templates" in url or "/store" in url:
        seed["canonical_url"] = url
        seed["supplied_url"] = url
    if classification:
        seed["classification"] = classification
    card = {
        "display_name": name,
        "summary": summary,
        "best_for": best_for,
        "not_for": not_for or ["copying without license/entitlement review"],
        "keywords": keywords or [source_id.replace("-", " "), "templates"],
        "topics_contributed": topics or ["templates", "starter", "ui-kit"],
    }
    return seed, card


PAIRS: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = {
    "tailwind-blocks-templates": [
        _s("tailwindtemplates-io", "Tailwind Templates", "https://tailwindtemplates.io",
           summary="Directory of Tailwind CSS website and UI templates.",
           best_for=["Tailwind template discovery", "landing/admin starters"],
           keywords=["tailwind", "templates", "directory", "landing"]),
        _s("tailgrids", "Tailgrids", "https://tailgrids.com",
           summary="Tailwind UI components and website templates for marketing and apps.",
           best_for=["Tailwind sections", "marketing templates"],
           keywords=["tailgrids", "tailwind", "components", "templates"]),
        _s("graygrids", "GrayGrids", "https://www.graygrids.com",
           summary="Free and premium HTML/Tailwind templates for sites and dashboards.",
           best_for=["HTML/Tailwind template shopping"],
           keywords=["graygrids", "html", "tailwind", "templates"]),
        _s("wickedblocks", "Wicked Blocks", "https://wickedblocks.dev",
           summary="Copy-paste Tailwind blocks for landing and marketing layouts.",
           best_for=["Tailwind marketing blocks"],
           keywords=["wickedblocks", "tailwind", "blocks", "landing"]),
        _s("loopple", "Loopple", "https://www.loopple.com",
           summary="Drag-and-drop builder for Tailwind/Bootstrap dashboard and site kits.",
           best_for=["assembling dashboard/site kits"],
           keywords=["loopple", "builder", "tailwind", "dashboard"]),
        _s("tailwindflex", "TailwindFlex", "https://tailwindflex.com",
           summary="Community gallery of Tailwind component and section snippets.",
           best_for=["snippet inspiration", "section patterns"],
           keywords=["tailwindflex", "snippets", "tailwind", "gallery"]),
        _s("themewagon", "ThemeWagon", "https://themewagon.com",
           summary="Free Bootstrap/HTML and Tailwind website templates.",
           best_for=["free HTML template discovery"],
           keywords=["themewagon", "bootstrap", "html", "templates"]),
        _s("themefisher", "Themefisher", "https://themefisher.com",
           summary="Hugo/HTML/React-oriented themes and website templates.",
           best_for=["static-site and marketing templates"],
           keywords=["themefisher", "hugo", "templates", "themes"]),
        _s("statichunt", "Statichunt", "https://statichunt.com",
           summary="Jamstack theme directory across Astro, Hugo, Next, and more.",
           best_for=["Jamstack theme discovery"],
           keywords=["statichunt", "jamstack", "themes", "directory"]),
        _s("jamstackthemes", "Jamstack Themes", "https://jamstackthemes.dev",
           summary="Curated Jamstack themes sorted by SSG and CMS.",
           best_for=["SSG theme selection"],
           keywords=["jamstackthemes", "ssg", "themes"]),
        _s("astro-themes", "Astro Themes", "https://astro.build/themes",
           summary="Official Astro theme catalog for content and marketing sites.",
           best_for=["Astro starters", "content-site templates"],
           keywords=["astro", "themes", "starters"]),
        _s("nuxt-templates", "Nuxt Templates", "https://nuxt.com/templates",
           summary="Official Nuxt template gallery for apps and websites.",
           best_for=["Nuxt starters", "Vue app templates"],
           keywords=["nuxt", "templates", "vue"]),
        _s("flowbite-blocks", "Flowbite Blocks", "https://flowbite.com/blocks",
           summary="Tailwind section blocks spanning marketing, ecommerce, and app UI.",
           best_for=["Tailwind page sections", "block assembly"],
           keywords=["flowbite", "blocks", "tailwind", "sections"]),
        _s("htmlrev", "HTMLrev", "https://htmlrev.com",
           summary="Free HTML template directory with filters by stack and style.",
           best_for=["free HTML template browsing"],
           keywords=["htmlrev", "html", "templates", "free"]),
        _s("styleshout", "StyleShout", "https://www.styleshout.com",
           summary="Free website templates with classic marketing layouts.",
           best_for=["simple free site templates"],
           keywords=["styleshout", "html", "templates"]),
        _s("free-css", "Free CSS", "https://www.free-css.com",
           summary="Long-running free CSS/HTML template collection.",
           best_for=["legacy free template discovery"],
           not_for=["modern accessibility authority"],
           keywords=["free-css", "html", "templates"]),
        _s("bootstrapmade", "BootstrapMade", "https://bootstrapmade.com",
           summary="Bootstrap website templates for business, portfolio, and landing pages.",
           best_for=["Bootstrap marketing templates"],
           keywords=["bootstrapmade", "bootstrap", "templates"]),
        _s("startbootstrap", "Start Bootstrap", "https://startbootstrap.com",
           summary="Free Bootstrap themes and snippet templates for sites and admin UI.",
           best_for=["Bootstrap starters", "admin/site kits"],
           keywords=["startbootstrap", "bootstrap", "themes"]),
        _s("html5up", "HTML5 UP", "https://html5up.net",
           summary="Responsive HTML5/CSS3 site templates with distinctive visual styles.",
           best_for=["expressive HTML templates", "portfolio/landing starters"],
           keywords=["html5up", "html5", "templates", "responsive"]),
        _s("templatemo", "TemplateMo", "https://www.templatemo.com",
           summary="Free HTML CSS website templates for business and landing use.",
           best_for=["free HTML templates"],
           keywords=["templatemo", "html", "css", "templates"]),
        _s("tooplate", "Tooplate", "https://www.tooplate.com",
           summary="Free HTML templates with clean business and personal layouts.",
           best_for=["free HTML starters"],
           keywords=["tooplate", "html", "templates"]),
        _s("colorlib-templates", "Colorlib Templates", "https://colorlib.com/wp/templates/",
           summary="Large free Bootstrap template catalog from Colorlib.",
           best_for=["Bootstrap template discovery"],
           keywords=["colorlib", "bootstrap", "templates"]),
        _s("bootstrapious", "Bootstrapious", "https://bootstrapious.com",
           summary="Bootstrap themes and UI kits for websites and dashboards.",
           best_for=["Bootstrap theme shopping"],
           keywords=["bootstrapious", "bootstrap", "themes"]),
        _s("w3layouts", "W3Layouts", "https://w3layouts.com",
           summary="HTML website templates across many business categories.",
           best_for=["category-based HTML template search"],
           keywords=["w3layouts", "html", "templates"]),
        _s("zerotheme", "ZeroTheme", "https://www.zerotheme.com",
           summary="Free HTML5 templates and website kits.",
           best_for=["free HTML5 templates"],
           keywords=["zerotheme", "html5", "templates"]),
    ],
    "dashboard-data-app-ui": [
        _s("coreui", "CoreUI", "https://coreui.io",
           summary="Admin template and component system for Bootstrap/React/Vue/Angular dashboards.",
           best_for=["admin dashboards", "multi-framework admin kits"],
           keywords=["coreui", "admin", "dashboard", "bootstrap"]),
        _s("themeselection", "ThemeSelection", "https://themeselection.com",
           summary="Admin dashboard templates across Bootstrap, React, Vue, and Laravel.",
           best_for=["admin template shopping"],
           keywords=["themeselection", "admin", "dashboard", "templates"]),
        _s("adminmart", "AdminMart", "https://adminmart.com",
           summary="Admin dashboard templates for Bootstrap and modern JS stacks.",
           best_for=["admin UI kits"],
           keywords=["adminmart", "dashboard", "admin", "templates"]),
        _s("wrappixel", "WrapPixel", "https://www.wrappixel.com",
           summary="Admin and website templates for Bootstrap/React/Angular/Vue.",
           best_for=["admin/marketing templates"],
           keywords=["wrappixel", "admin", "templates"]),
        _s("pixelcave", "Pixelcave", "https://pixelcave.com",
           summary="Premium HTML admin and webapp templates.",
           best_for=["premium admin templates when entitled"],
           not_for=["copying without purchase"],
           keywords=["pixelcave", "admin", "premium", "html"]),
        _s("soft-ui-dashboard", "Soft UI Dashboard", "https://www.creative-tim.com/product/soft-ui-dashboard",
           summary="Creative Tim Soft UI admin dashboard template family.",
           best_for=["soft neumorphic admin starters"],
           keywords=["soft-ui", "creative-tim", "dashboard"]),
        _s("argon-dashboard", "Argon Dashboard", "https://www.creative-tim.com/product/argon-dashboard",
           summary="Creative Tim Argon admin dashboard templates.",
           best_for=["Bootstrap/React admin starters"],
           keywords=["argon", "dashboard", "creative-tim"]),
        _s("volt-dashboard", "Volt Dashboard", "https://demo.themesberg.com/volt-bootstrap-5-dashboard",
           summary="Themesberg Volt Bootstrap admin dashboard template.",
           best_for=["Bootstrap 5 admin starters"],
           keywords=["volt", "themesberg", "dashboard", "bootstrap"]),
        _s("berry-dashboard", "Berry Dashboard", "https://berrydashboard.io",
           summary="MUI React admin dashboard template suite.",
           best_for=["MUI admin apps", "React dashboard starters"],
           keywords=["berry", "mui", "dashboard", "react"]),
        _s("minimals-cc", "Minimals", "https://minimals.cc",
           summary="Premium React admin and website UI kit family.",
           best_for=["dense React admin kits when entitled"],
           not_for=["copying without entitlement"],
           keywords=["minimals", "react", "admin", "ui-kit"]),
        _s("mantine-ui-templates", "Mantine UI Templates", "https://ui.mantine.dev",
           summary="Mantine example templates and application UI compositions.",
           best_for=["Mantine app shells", "example layouts"],
           keywords=["mantine", "templates", "application-ui"]),
        _s("flowbite-admin-dashboard", "Flowbite Admin Dashboard", "https://github.com/themesberg/flowbite-admin-dashboard",
           summary="Open-source Tailwind admin dashboard built with Flowbite.",
           best_for=["Tailwind admin starter reference"],
           keywords=["flowbite", "admin", "tailwind", "github"]),
        _s("material-tailwind-dashboard", "Material Tailwind Dashboard", "https://www.material-tailwind.com/blocks/dashboard",
           summary="Material Tailwind dashboard blocks and admin layouts.",
           best_for=["Tailwind Material admin sections"],
           keywords=["material-tailwind", "dashboard", "blocks"]),
        _s("tabler-preview-templates", "Tabler Templates", "https://preview.tabler.io",
           summary="Tabler dashboard preview templates and page compositions.",
           best_for=["admin page composition ideas"],
           keywords=["tabler", "preview", "dashboard", "templates"]),
    ],
    "shadcn-ecosystem": [
        _s("shadcn-taxonomy", "Taxonomy", "https://tx.shadcn.com",
           summary="shadcn/ui example app combining content, auth, and marketing patterns.",
           best_for=["shadcn app architecture reference", "Next.js marketing+app hybrids"],
           keywords=["taxonomy", "shadcn", "nextjs", "starter"]),
        _s("shadcn-taxonomy-repo", "Taxonomy Repo", "https://github.com/shadcn-ui/taxonomy",
           summary="Source repository for the shadcn Taxonomy example application.",
           best_for=["inspecting shadcn starter structure"],
           keywords=["taxonomy", "shadcn", "github", "starter"]),
        _s("shadcn-next-template", "shadcn Next Template", "https://github.com/shadcn-ui/next-template",
           summary="Official-style Next.js starter wired for shadcn/ui.",
           best_for=["greenfield shadcn Next apps"],
           keywords=["shadcn", "next-template", "starter"]),
        _s("next-saas-stripe-starter", "Next SaaS Stripe Starter", "https://github.com/mickasmt/next-saas-stripe-starter",
           summary="Popular Next.js SaaS starter using shadcn-style UI and Stripe patterns.",
           best_for=["SaaS starter architecture", "billing UI shells"],
           keywords=["saas", "stripe", "nextjs", "shadcn", "starter"]),
        _s("skateshop", "Skateshop", "https://github.com/sadmann7/skateshop",
           summary="shadcn-based ecommerce storefront/example app.",
           best_for=["ecommerce UI with shadcn", "storefront patterns"],
           keywords=["skateshop", "ecommerce", "shadcn", "nextjs"]),
        _s("table-cn", "Table.cn", "https://table.cn",
           summary="Data-table patterns and examples in the shadcn ecosystem.",
           best_for=["shadcn data tables", "filter/sort table UX"],
           keywords=["table.cn", "datatable", "shadcn"]),
        _s("saas-ui", "SaaS UI", "https://saas-ui.dev",
           summary="React component kit and starter patterns for SaaS dashboards.",
           best_for=["SaaS app shells", "dashboard starters"],
           keywords=["saas-ui", "dashboard", "react", "starter"]),
        _s("shipfast", "ShipFast", "https://shipfa.st",
           summary="Paid Next.js boilerplate for shipping SaaS marketing + app quickly.",
           best_for=["SaaS boilerplate shopping when entitled"],
           not_for=["copying without purchase"],
           keywords=["shipfast", "saas", "boilerplate", "nextjs"]),
        _s("supastarter", "Supastarter", "https://supastarter.dev",
           summary="Production-oriented SaaS starter kits for Next.js and related stacks.",
           best_for=["SaaS starter kits when entitled"],
           not_for=["copying without entitlement"],
           keywords=["supastarter", "saas", "starter", "nextjs"]),
        _s("magicui-templates", "Magic UI Templates", "https://magicui.design/docs/templates",
           summary="Template offerings built around Magic UI animated components.",
           best_for=["animated marketing templates"],
           keywords=["magicui", "templates", "animated", "landing"]),
        _s("aceternity-templates", "Aceternity UI Templates", "https://ui.aceternity.com/templates",
           summary="Template packs using Aceternity animated section components.",
           best_for=["kinetic landing templates"],
           keywords=["aceternity", "templates", "landing", "animated"]),
    ],
    "component-catalogs": [
        _s("vercel-templates", "Vercel Templates", "https://vercel.com/templates",
           summary="Official Vercel deployment templates spanning Next.js apps and sites.",
           best_for=["Next.js starters", "deployable app templates"],
           keywords=["vercel", "templates", "nextjs", "starters"]),
        _s("nextjs-saas-starter", "Next.js SaaS Starter", "https://github.com/nextjs/saas-starter",
           summary="Vercel/Next.js SaaS starter with modern App Router patterns.",
           best_for=["SaaS architecture reference", "Next starters"],
           keywords=["nextjs", "saas", "starter", "github"]),
        _s("nextjs-subscription-payments", "Next.js Subscription Payments", "https://github.com/vercel/nextjs-subscription-payments",
           summary="Vercel subscription/payments starter for SaaS billing UIs.",
           best_for=["billing/settings UI patterns", "subscription apps"],
           keywords=["subscriptions", "stripe", "nextjs", "starter"]),
        _s("next-js-boilerplate", "Next.js Boilerplate", "https://github.com/ixartz/Next-js-Boilerplate",
           summary="Widely used Next.js boilerplate with testing and tooling defaults.",
           best_for=["production Next starter baseline"],
           keywords=["nextjs", "boilerplate", "starter"]),
        _s("saas-boilerplate", "SaaS Boilerplate", "https://github.com/ixartz/SaaS-Boilerplate",
           summary="Open-source SaaS boilerplate with auth, billing, and app shell patterns.",
           best_for=["SaaS app structure", "multi-tenant starter ideas"],
           keywords=["saas", "boilerplate", "auth", "billing"]),
        _s("next-enterprise", "Next Enterprise", "https://github.com/Blazity/next-enterprise",
           summary="Enterprise-oriented Next.js template with strict tooling defaults.",
           best_for=["enterprise Next baselines"],
           keywords=["next-enterprise", "nextjs", "enterprise", "starter"]),
        _s("vercel-commerce", "Vercel Commerce", "https://github.com/vercel/commerce",
           summary="Composable ecommerce storefront starter from Vercel.",
           best_for=["headless storefront templates"],
           keywords=["commerce", "ecommerce", "nextjs", "storefront"]),
        _s("relume", "Relume", "https://www.relume.io",
           summary="Webflow/Figma component and sitemap libraries for marketing sites.",
           best_for=["Webflow marketing systems", "sitemap-to-section planning"],
           keywords=["relume", "webflow", "figma", "components"]),
        _s("framer-templates", "Framer Templates", "https://www.framer.com/marketplace/templates/",
           summary="Framer marketplace templates for marketing and product sites.",
           best_for=["Framer site templates when entitled"],
           not_for=["code extraction assumptions"],
           keywords=["framer", "templates", "marketplace"]),
        _s("webflow-templates", "Webflow Templates", "https://webflow.com/templates",
           summary="Official Webflow template marketplace for marketing sites.",
           best_for=["Webflow template discovery"],
           not_for=["exporting as React without rebuild"],
           keywords=["webflow", "templates", "marketplace"]),
        _s("ui8", "UI8", "https://ui8.net",
           summary="Premium UI kit and template marketplace for product/marketing design.",
           best_for=["premium UI kit shopping when entitled"],
           not_for=["copying assets without license"],
           classification="inspiration-only",
           keywords=["ui8", "ui-kits", "marketplace", "premium"]),
        _s("craftwork", "Craftwork", "https://craftwork.design",
           summary="Design assets and UI kits for product and marketing interfaces.",
           best_for=["UI kit inspiration/shopping"],
           not_for=["unchecked asset redistribution"],
           classification="inspiration-only",
           keywords=["craftwork", "ui-kits", "assets"]),
        _s("primefaces-templates", "PrimeFaces Templates", "https://www.primefaces.org/templates/",
           summary="Premium templates for PrimeReact/PrimeVue/PrimeNG component suites.",
           best_for=["PrimeTek admin templates when entitled"],
           keywords=["primefaces", "primereact", "templates", "admin"]),
        _s("primereact", "PrimeReact", "https://primereact.org",
           summary="Rich React component library often used as an app/admin UI kit base.",
           best_for=["enterprise React component coverage"],
           keywords=["primereact", "components", "admin"]),
        _s("mui-store", "MUI Store", "https://mui.com/store/",
           summary="Official MUI template and theme store for React dashboards and sites.",
           best_for=["MUI templates when entitled"],
           not_for=["copying without purchase"],
           keywords=["mui-store", "templates", "dashboard", "react"]),
        _s("ant-design-pro", "Ant Design Pro", "https://pro.ant.design",
           summary="Enterprise React admin solution/templates built on Ant Design.",
           best_for=["Ant enterprise admin starters"],
           keywords=["ant-design-pro", "admin", "enterprise", "react"]),
    ],
    "landing-startup-references": [
        _s("landing-love", "Landing Love", "https://www.landing.love",
           summary="Curated landing-page inspiration and template-like references.",
           best_for=["landing direction", "section pattern scanning"],
           classification="inspiration-only",
           keywords=["landing-love", "landing", "inspiration"]),
        _s("saaspo", "SaaSPo", "https://saaspo.com",
           summary="SaaS landing-page and product-page inspiration gallery.",
           best_for=["SaaS landing structure"],
           classification="inspiration-only",
           keywords=["saaspo", "saas", "landing", "inspiration"]),
        _s("onepagelove-templates", "One Page Love Templates", "https://onepagelove.com/templates",
           summary="One-page website templates and theme listings.",
           best_for=["one-page template discovery"],
           keywords=["onepagelove", "templates", "one-page"]),
        _s("shipped-stories", "Shipped.club", "https://shipped.club",
           summary="Indie SaaS launch examples useful for landing and packaging patterns.",
           best_for=["indie SaaS landing examples"],
           classification="inspiration-only",
           keywords=["shipped", "saas", "launches", "landing"]),
        _s("landing-page-examples-lapa", "Lapa Landing Examples", "https://www.lapa.ninja/templates/",
           summary="Landing template/example listings adjacent to the Lapa gallery.",
           best_for=["landing template browsing"],
           classification="inspiration-only",
           keywords=["lapa", "landing", "templates"]),
        _s("dora", "Dora", "https://www.dora.run",
           summary="No-code site builder with expressive animated landing templates.",
           best_for=["animated landing inspiration"],
           not_for=["assuming exportable production React"],
           keywords=["dora", "no-code", "landing", "animation"]),
        _s("softr", "Softr", "https://www.softr.io",
           summary="No-code app/site builder with client-portal and landing templates.",
           best_for=["no-code app templates", "portal layouts"],
           keywords=["softr", "no-code", "templates", "portals"]),
    ],
    "portfolio-inspiration": [
        _s("html5up-portfolio", "HTML5 UP Portfolio", "https://html5up.net/uploads/demos/prologue/",
           summary="Representative HTML5 UP portfolio/personal demo templates.",
           best_for=["personal site starter inspiration"],
           keywords=["html5up", "portfolio", "personal"]),
        _s("readymag", "Readymag", "https://readymag.com",
           summary="Editorial website tool with portfolio and magazine-style templates.",
           best_for=["editorial portfolio inspiration"],
           classification="inspiration-only",
           keywords=["readymag", "portfolio", "editorial"]),
        _s("cargo-templates", "Cargo Marketplace", "https://cargo.site/Marketplace",
           summary="Cargo portfolio templates and marketplace layouts.",
           best_for=["creative portfolio templates"],
           classification="inspiration-only",
           keywords=["cargo", "portfolio", "marketplace"]),
        _s("notion-portfolio-templates", "Notion Portfolio Templates", "https://www.notion.com/templates/category/personal",
           summary="Notion personal/portfolio template category for content structure ideas.",
           best_for=["portfolio IA and content structure"],
           classification="inspiration-only",
           keywords=["notion", "portfolio", "templates"]),
    ],
    "ecommerce-product-ui": [
        _s("medusa-nextjs-starter", "Medusa Next.js Starter", "https://github.com/medusajs/nextjs-starter-medusa",
           summary="Official Medusa storefront starter for Next.js.",
           best_for=["headless commerce storefront starters"],
           keywords=["medusa", "nextjs", "storefront", "starter"]),
        _s("saleor-storefront", "Saleor Storefront", "https://github.com/saleor/storefront",
           summary="Saleor storefront reference implementation.",
           best_for=["composable commerce UI reference"],
           keywords=["saleor", "storefront", "ecommerce", "github"]),
        _s("shopify-skeleton-theme", "Shopify Skeleton Theme", "https://github.com/Shopify/skeleton-theme",
           summary="Minimal Shopify theme starter for custom storefronts.",
           best_for=["Shopify theme foundations"],
           keywords=["shopify", "theme", "skeleton", "liquid"]),
        _s("shopify-dawn", "Shopify Dawn", "https://github.com/Shopify/dawn",
           summary="Shopify's reference Online Store 2.0 theme.",
           best_for=["Shopify theme architecture", "storefront sections"],
           keywords=["dawn", "shopify", "theme", "os2"]),
        _s("spree-starter", "Spree Starter", "https://github.com/spree/spree_starter",
           summary="Spree commerce starter application.",
           best_for=["Spree storefront/admin starting points"],
           keywords=["spree", "ecommerce", "starter"]),
        _s("bagisto", "Bagisto", "https://bagisto.com",
           summary="Open-source Laravel ecommerce platform with storefront themes.",
           best_for=["Laravel ecommerce themes", "storefront kits"],
           keywords=["bagisto", "laravel", "ecommerce", "themes"]),
    ],
    "inspiration-catalogs": [
        _s("themeforest-site-templates", "ThemeForest Site Templates", "https://themeforest.net/category/site-templates",
           summary="Large paid marketplace of site templates across many niches.",
           best_for=["paid template discovery when entitled"],
           not_for=["copying without purchase", "treating demos as open source"],
           classification="inspiration-only",
           keywords=["themeforest", "marketplace", "templates", "paid"]),
        _s("themeforest-admin-templates", "ThemeForest Admin Templates", "https://themeforest.net/category/admin-templates",
           summary="Paid admin dashboard template marketplace.",
           best_for=["admin template shopping when entitled"],
           not_for=["copying without purchase"],
           classification="inspiration-only",
           keywords=["themeforest", "admin", "marketplace", "paid"]),
        _s("templatemonster", "TemplateMonster", "https://www.templatemonster.com",
           summary="Marketplace for website themes and templates across builders and stacks.",
           best_for=["commercial theme discovery"],
           not_for=["unchecked redistribution"],
           classification="inspiration-only",
           keywords=["templatemonster", "themes", "marketplace"]),
        _s("wrapbootstrap", "WrapBootstrap", "https://wrapbootstrap.com",
           summary="Bootstrap theme marketplace for sites and admin templates.",
           best_for=["Bootstrap premium themes when entitled"],
           not_for=["copying without purchase"],
           classification="inspiration-only",
           keywords=["wrapbootstrap", "bootstrap", "marketplace"]),
        _s("themes-getbootstrap", "Official Bootstrap Themes", "https://themes.getbootstrap.com",
           summary="Official Bootstrap themes and premium kits.",
           best_for=["official Bootstrap theme options"],
           keywords=["bootstrap-themes", "official", "premium"]),
        _s("cssdesignawards", "CSS Design Awards", "https://www.cssdesignawards.com",
           summary="Award gallery useful as high-craft template/direction inspiration.",
           best_for=["visual direction inspiration"],
           classification="inspiration-only",
           keywords=["cssda", "awards", "inspiration"]),
    ],
}


def apply() -> dict[str, Any]:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    existing_ids = {str(s.get("id")) for c in seed.get("categories") or [] for s in c.get("sources") or []}
    existing_urls = {str(s.get("canonical_url")) for c in seed.get("categories") or [] for s in c.get("sources") or []}

    cards: dict[str, dict[str, Any]] = {}
    added = 0
    for category in seed.get("categories") or []:
        category_id = str(category.get("id") or "")
        pairs = PAIRS.get(category_id) or []
        sources = list(category.get("sources") or [])
        for seed_item, card in pairs:
            source_id = str(seed_item["id"])
            url = str(seed_item["canonical_url"])
            if source_id in existing_ids or url in existing_urls:
                continue
            sources.append(seed_item)
            cards[source_id] = card
            existing_ids.add(source_id)
            existing_urls.add(url)
            added += 1
        category["sources"] = sources

    SOURCE_CARDS.update(cards)
    # Also persist cards onto imports for this process via enrich.
    for source_id, card in cards.items():
        SOURCE_CARDS[source_id] = card

    logs = list(seed.get("expansion_log") or [])
    if EXPANSION_ID not in logs:
        logs.append(EXPANSION_ID)
    seed["expansion_log"] = logs
    seed["catalog_revision"] = "2026-07-12"
    seed["template_absorption_added"] = added

    enriched = enrich_seed(seed)
    # Ensure newly added cards win even if fallback already ran somehow.
    for category in enriched.get("categories") or []:
        for source in category.get("sources") or []:
            card = cards.get(str(source.get("id")))
            if not card:
                continue
            source["name"] = card["display_name"]
            source["summary"] = card["summary"]
            source["best_for"] = card["best_for"]
            source["not_for"] = card["not_for"]
            source["keywords"] = card["keywords"]
            source["topics_contributed"] = card["topics_contributed"]
            source["findability_status"] = "discovery-card"

    total = sum(len(c["sources"]) for c in enriched["categories"])
    SEED_PATH.write_text(json.dumps(enriched, indent=2) + "\n", encoding="utf-8")
    knowledge = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    SOURCES_PATH.write_text(json.dumps(enrich_knowledge_sources(knowledge), indent=2) + "\n", encoding="utf-8")
    INDEX_PATH.write_text(build_findability_index(enriched), encoding="utf-8")
    return {"added": added, "total_sources": total, "cards": len(cards)}


if __name__ == "__main__":
    print(json.dumps(apply()))
