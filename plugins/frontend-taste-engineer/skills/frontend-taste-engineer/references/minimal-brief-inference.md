# Minimal brief inference

Infer only creative and reversible decisions. Preserve supplied wording exactly where it is the requested message.

## Profile contract

Record:

- Build mode.
- Domain and product type.
- Interface archetype: expressive, analytical, transactional, institutional, editorial, technical, or utilitarian.
- Purpose.
- Audience.
- Named recipient when present.
- Primary and secondary user tasks.
- Primary message.
- Supporting narrative.
- Emotional objective, tone, and seriousness.
- Trust and risk levels.
- Information density and frequency of use.
- Negative-space role.
- Content maturity.
- Brand and product maturity.
- Accessibility needs and expected devices.
- Visual ambition.
- Visual intensity from 1–5.
- Motion intensity.
- Motion grammar or coverage when the direction is non-static.
- Experimental tolerance and familiarity requirement.
- Interaction depth.
- Page type.
- Suggested composition.
- Hero treatment and component styling.
- Typography direction.
- Color/material direction.
- Imagery strategy.
- Motion stance.
- Required states.
- Retrieval topics.
- Verification priorities.

Also maintain two separate lists: `supplied_facts` and `inferred_assumptions`.

## Decision rules

- Treat quoted text, names, dates, teams, products, events, provided assets, and explicit constraints as supplied facts.
- Infer audience from who is addressed, who would share or act on the page, and the likely consequence of the task.
- Infer purpose as an outcome, not a visual adjective. “Premium” implies perceived craft and clarity, not invented exclusivity.
- Treat “stunning,” “world-class,” “beautiful,” “high quality,” and “distinctive” as quality targets. Do not raise visual or motion intensity merely because one appears.
- Raise trust and conservatism for public service, health, finance, identity, payment, or consequential forms.
- Raise visual ambition for expressive language such as “stunning,” “impossible to ignore,” a personal challenge, or a conceptual sentence.
- Keep interaction depth low when the content is primarily read; use moderate interaction only when it strengthens narrative, comparison, exploration, or task feedback.
- Choose the visual and motion intensity that fully expresses the product. Do not silently flatten an explicit kinetic, tactile, or narrative direction to low motion; calm work must still show authored type, spacing, density, states, and brand detail, while expressive work must still preserve task completion.
- For a sparse direction, state the role of major negative space and keep enough hierarchy, evidence, content, and affordance to make the primary task clear. Bare area is not automatically minimalist.
- When the direction is non-static, name two to four roles for focal/narrative, state-continuity, and direct-feedback motion plus their reduced-motion outcomes.
- Infer required states from reachable behavior. A static expressive page still needs link/button focus, active, responsive, and reduced-motion outcomes; a form additionally needs validation, error, loading, success, disabled, and recovery.

Do not infer customers, metrics, awards, integrations, testimonials, pricing, team history, event details, or product capabilities.

## Example reasoning

For “Make a website directed to Alex containing ‘You made it — Arnav’”:

- Supplied: Alex is the fictional recipient; the quoted sentence and Arnav attribution are exact content.
- Inferred: an expressive personal experience for Alex and share viewers; confident creative proof; bold, playful, editorial tone; high visual ambition; moderate narrative interaction.

For “Build a serious public-service application page”:

- Supplied: public-service, application page, serious.
- Inferred: consequential task completion; plain-language hierarchy; high trust; restrained visuals; minimal feedback motion; robust form and recovery states.

These directions must differ. Do not force both through the same hero/cards/gradient template.

For “Build a finance dashboard for tracking family investments” infer personal finance, high trust, medium-high risk, high information density, visual intensity 2, low motion, high familiarity, excellent numeric typography, truthful data views, explicit units and freshness, and calm professional direction. “Stunning” would improve execution, not turn this into a cinematic campaign.

## Verification

- Every supplied fact traces to the prompt or inspected project.
- Every unsupported choice is labeled as an assumption and remains reversible.
- The primary message is preserved exactly when quoted.
- The profile is specific enough to reject at least one plausible but wrong direction.
- No routine creative question remains necessary before implementation.
