export type DemoStage =
  | "classify"
  | "brief"
  | "direct"
  | "build"
  | "refine"
  | "verify";

export const STAGES: { id: DemoStage; label: string }[] = [
  { id: "classify", label: "Classify" },
  { id: "brief", label: "Brief" },
  { id: "direct", label: "Direct" },
  { id: "build", label: "Build" },
  { id: "refine", label: "Refine" },
  { id: "verify", label: "Verify" },
];

export type PreviewTheme = "robotics" | "alive" | "finance" | "audit";

export interface DemoExample {
  id: string;
  prompt: string;
  theme: PreviewTheme;
  classify: Record<string, string>;
  brief: Record<string, string>;
  direct: Record<string, string>;
  build: Record<string, string>;
  refine: Record<string, string>;
  verify: Record<string, string>;
  preview: {
    title: string;
    subtitle: string;
    accent: string;
    bg: string;
    text: string;
    fontClass: string;
    sections: { label: string; content: string }[];
  };
}

export const DEMO_EXAMPLES: DemoExample[] = [
  {
    id: "robotics",
    prompt: "Make a website for my robotics team.",
    theme: "robotics",
    classify: {
      "Task mode": "Autonomous zero-brief build",
      "Product type": "Team landing page",
      Audience: "Students, mentors, sponsors",
      "Trust level": "Medium — credibility without enterprise formality",
      "Visual intensity": "4 — energetic, mechanical, confident",
    },
    brief: {
      "Product goal": "Recruit members, showcase projects, communicate meeting schedule",
      "Main user": "Prospective team member or sponsor visiting for the first time",
      "Required sections": "Hero, project gallery, team roster, schedule, join CTA",
      "Content assumptions": "Synthetic team names; no fabricated competition wins",
    },
    direct: {
      "Design thesis":
        "Precision engineering expressed through bold geometry, monospace data labels, and kinetic accent motion.",
      "Typography stance": "Condensed sans headlines with mono labels for specs and dates",
      "Composition stance": "Asymmetric grid with visible measurement marks and offset panels",
      "Color/material stance": "Dark steel base, teal signal accents, high-contrast CTAs",
      "Motion stance": "Subtle mechanical transitions; reduced-motion static layout",
    },
    build: {
      Content: "Original copy for hero, three project cards, roster, and schedule",
      Components: "Navigation, project cards with status badges, roster grid, join form states",
      "Responsive behavior": "Stacked gallery on mobile; sticky nav collapses to menu",
      "Functional states": "Form validation, empty roster fallback, loading project images",
      Accessibility: "Semantic landmarks, keyboard nav, focus rings, alt text on images",
    },
    refine: {
      "Desktop screenshot review": "Hero CTA competes with project gallery hierarchy",
      "Mobile screenshot review": "Schedule table overflows horizontally at 390px",
      "Three highest-impact weaknesses":
        "1. Mobile schedule overflow 2. Weak project card hierarchy 3. Join form missing error state",
      Corrections: "Responsive schedule cards, stronger card titles, form error messaging",
    },
    verify: {
      "Production build": "Pass — static export compatible",
      "Keyboard and focus": "Pass — all interactive elements reachable",
      "Reduced motion": "Pass — animations respect prefers-reduced-motion",
      Overflow: "Pass after schedule refactor",
      "Routes and assets": "Pass — all links resolve",
      "Remaining limitations": "Screen-reader behavior not fully verified on real devices",
    },
    preview: {
      title: "ROBOTICS TEAM",
      subtitle: "Building machines that compete",
      accent: "#FFCF70",
      bg: "#1A2424",
      text: "#E8EDEB",
      fontClass: "font-mono",
      sections: [
        { label: "Projects", content: "Autonomous Rover · Line Follower · Arm Control" },
        { label: "Next meet", content: "Thu 6pm · Lab 204" },
        { label: "Join", content: "Open to all skill levels" },
      ],
    },
  },
  {
    id: "alive",
    prompt: "Turn this sentence into a website: machines should feel alive.",
    theme: "alive",
    classify: {
      "Task mode": "Autonomous zero-brief build",
      "Product type": "Expressive personal/experimental page",
      Audience: "Creative technologists, portfolio visitors",
      "Trust level": "Low — artistic expression, not product claims",
      "Visual intensity": "5 — experimental, expressive, motion-forward",
    },
    brief: {
      "Product goal": "Translate a philosophical sentence into an experiential web surface",
      "Main user": "Visitor seeking an evocative, memorable interaction",
      "Required sections": "Immersive hero, manifesto text, generative visual element, credits",
      "Content assumptions": "No fabricated product metrics or testimonials",
    },
    direct: {
      "Design thesis":
        "Organic motion and layered depth suggest sentience without literal robot imagery.",
      "Typography stance": "Variable-weight display type with generous tracking shifts",
      "Composition stance": "Full-bleed sections with overlapping translucent layers",
      "Color/material stance": "Deep indigo-black with bioluminescent teal and mint pulses",
      "Motion stance": "Breathing animations on load; interruptible on interaction",
    },
    build: {
      Content: "Manifesto paragraphs derived from the core sentence; no placeholder lorem",
      Components: "Animated gradient field, text reveal sequence, minimal nav",
      "Responsive behavior": "Motion scales down on mobile; text reflows at 320px",
      "Functional states": "Pause animation control, reduced-motion static gradient",
      Accessibility: "Motion toggle, sufficient contrast on text overlays, skip link",
    },
    refine: {
      "Desktop screenshot review": "Text contrast drops on animated background mid-cycle",
      "Mobile screenshot review": "Manifesto paragraphs too wide for comfortable reading",
      "Three highest-impact weaknesses":
        "1. Contrast fluctuation 2. Mobile line length 3. No pause control for motion",
      Corrections: "Stable text backdrop, narrower measure, visible pause button",
    },
    verify: {
      "Production build": "Pass",
      "Keyboard and focus": "Pass — pause control and skip link reachable",
      "Reduced motion": "Pass — static fallback verified",
      Overflow: "Pass — no horizontal scroll at 320px",
      "Routes and assets": "Pass",
      "Remaining limitations": "Canvas performance on low-end devices not measured",
    },
    preview: {
      title: "feel alive",
      subtitle: "machines should",
      accent: "#C8F0A0",
      bg: "linear-gradient(135deg, #0F1A2A 0%, #1A3A3A 50%, #0B6E69 100%)",
      text: "#F7F5F0",
      fontClass: "font-serif italic",
      sections: [
        { label: "Manifesto", content: "Not imitation of life — presence in motion" },
        { label: "Signal", content: "Pulse · breathe · respond" },
      ],
    },
  },
  {
    id: "finance",
    prompt: "Design a landing page for a calm personal-finance product.",
    theme: "finance",
    classify: {
      "Task mode": "Autonomous zero-brief build",
      "Product type": "Personal finance landing page",
      Audience: "Budget-conscious adults seeking clarity",
      "Trust level": "High — financial data requires credibility",
      "Visual intensity": "2 — calm, precise, trustworthy",
    },
    brief: {
      "Product goal": "Explain value proposition and drive sign-up without pressure tactics",
      "Main user": "Person overwhelmed by existing finance apps",
      "Required sections": "Hero, feature overview, security note, pricing, FAQ, sign-up",
      "Content assumptions": "No fabricated user counts, ratings, or bank partnerships",
    },
    direct: {
      "Design thesis":
        "Clarity through restrained typography, generous whitespace, and numeric precision.",
      "Typography stance": "Humanist sans with tabular figures for any numbers shown",
      "Composition stance": "Single-column flow with clear section breaks and left-aligned text",
      "Color/material stance": "Warm paper background, teal accents, no gradients",
      "Motion stance": "Minimal — subtle fade on section entry only",
    },
    build: {
      Content: "Complete feature descriptions, security copy, and FAQ answers",
      Components: "Feature list, pricing table, accordion FAQ, sign-up form with states",
      "Responsive behavior": "Pricing cards stack; FAQ full-width on mobile",
      "Functional states": "Form validation, accordion expand/collapse, empty pricing tier",
      Accessibility: "Accordion ARIA, form labels, 4.5:1 contrast, focus management",
    },
    refine: {
      "Desktop screenshot review": "Pricing section lacks visual separation from FAQ",
      "Mobile screenshot review": "Sign-up form fields too narrow for comfortable input",
      "Three highest-impact weaknesses":
        "1. Section separation 2. Mobile form width 3. FAQ heading hierarchy",
      Corrections: "Section dividers, full-width inputs, corrected heading levels",
    },
    verify: {
      "Production build": "Pass",
      "Keyboard and focus": "Pass — accordion and form fully operable",
      "Reduced motion": "Pass — no essential information in motion",
      Overflow: "Pass at 320px and 200% zoom",
      "Routes and assets": "Pass",
      "Remaining limitations": "No real payment integration tested",
    },
    preview: {
      title: "ClearBudget",
      subtitle: "Personal finance, simplified",
      accent: "#0B6E69",
      bg: "#F7F5F0",
      text: "#0F1A1A",
      fontClass: "font-sans",
      sections: [
        { label: "Track", content: "See where every dollar goes" },
        { label: "Plan", content: "Set goals without spreadsheets" },
        { label: "Secure", content: "Your data stays on your device" },
      ],
    },
  },
  {
    id: "audit",
    prompt: "Audit this frontend and fix its three highest-impact problems.",
    theme: "audit",
    classify: {
      "Task mode": "Visual audit + remediation",
      "Product type": "Existing frontend under review",
      Audience: "End users of the product being audited",
      "Trust level": "High — audit findings must be evidence-backed",
      "Visual intensity": "Inferred from existing product context",
    },
    brief: {
      "Product goal": "Identify and fix the three highest-impact design and usability defects",
      "Main user": "Current product user affected by the defects",
      "Required sections": "Evidence inventory, severity-ranked findings, corrections, verification",
      "Content assumptions": "Defects backed by screenshot or runtime evidence",
    },
    direct: {
      "Design thesis": "Preserve working architecture; correct defects without wholesale restyle",
      "Typography stance": "Match existing scale; fix hierarchy gaps only where evidenced",
      "Composition stance": "Targeted layout fixes at affected viewports",
      "Color/material stance": "Fix contrast failures; do not introduce new palette",
      "Motion stance": "Add reduced-motion support where motion causes accessibility failure",
    },
    build: {
      Content: "Finding descriptions with severity, evidence, and specific corrections",
      Components: "Corrected components at affected states and viewports",
      "Responsive behavior": "Fix mobile overflow and breakpoint failures found in audit",
      "Functional states": "Implement missing error, empty, and focus states identified",
      Accessibility: "Repair semantic, keyboard, and contrast failures from audit rubric",
    },
    refine: {
      "Desktop screenshot review": "Before/after comparison at matching viewport",
      "Mobile screenshot review": "Verify overflow and tap target fixes at 390px",
      "Three highest-impact weaknesses":
        "1. Missing focus indicators 2. Mobile nav unreachable by keyboard 3. Placeholder copy in production",
      Corrections: "Focus-visible styles, keyboard-trapped mobile menu, finished copy",
    },
    verify: {
      "Production build": "Pass after corrections",
      "Keyboard and focus": "Pass — previously failing paths now reachable",
      "Reduced motion": "Pass — motion respects user preference",
      Overflow: "Pass — horizontal scroll eliminated at 320px",
      "Routes and assets": "Pass",
      "Remaining limitations": "Screen-reader testing recommended on real assistive technology",
    },
    preview: {
      title: "Audit Report",
      subtitle: "3 findings · 3 corrections",
      accent: "#FFCF70",
      bg: "#FEFDFB",
      text: "#0F1A1A",
      fontClass: "font-mono",
      sections: [
        { label: "Critical", content: "Missing focus indicators on all interactive elements" },
        { label: "High", content: "Mobile navigation unreachable by keyboard" },
        { label: "High", content: "Placeholder copy visible in production hero" },
      ],
    },
  },
];

export const STARTER_PROMPTS = [
  "Make a website for my robotics team.",
  "Turn this sentence into a website: machines should feel alive.",
  "Design and build a distinctive production-ready landing page for this product.",
  "Audit this frontend and fix its highest-impact design and usability problems.",
  "Rebuild this screenshot responsively while preserving accessibility.",
  "Create an accessible, polished component system for this application.",
  "Refine the motion and interaction quality of this interface.",
  "Turn this rough frontend into a coherent product experience.",
];

export const INSTALL_COMMANDS = `codex plugin marketplace add "$(pwd)"
codex plugin add frontend-taste-engineer@personal`;

export const VALIDATION_COMMANDS = `python3 plugins/frontend-taste-engineer/scripts/validate_all.py
python3 -m unittest discover -s plugins/frontend-taste-engineer/mcp-server/tests -v
python3 plugins/frontend-taste-engineer/evals/run_retrieval_evals.py
python3 plugins/frontend-taste-engineer/evals/run_frontend_evals.py`;
