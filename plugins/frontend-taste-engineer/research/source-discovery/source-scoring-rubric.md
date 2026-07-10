# External source scoring rubric

Score only evidence that was actually inspected. Unknown evidence receives zero, not an optimistic midpoint. Scores help triage candidates; they never promote a source.

| Dimension | Range | Full-credit evidence |
|---|---:|---|
| Relevance to Frontend Taste Engineer | 0–20 | Directly supports a recurring frontend task, component family, workflow stage, or verification need. |
| License clarity | 0–20 | Public, item-scoped terms clearly permit the intended use and identify attribution or redistribution obligations. |
| Source quality and maintainability | 0–15 | Clear ownership, reviewable documentation or source, current releases, and a credible maintenance path. |
| Accessibility usefulness | 0–15 | Documents semantics, keyboard/focus behavior, assistive-technology expectations, states, and testing limits. |
| Implementation usefulness | 0–10 | Provides concrete, adaptable implementation guidance without hiding critical behavior behind opaque generators. |
| Inspiration value | 0–10 | Offers varied, product-relevant patterns that can be generalized without copying expression, content, or brand. |
| Dependency risk | 0–5 | Five means no or low dependency risk; zero means opaque, abandoned, heavy, or unsafe dependency requirements. |
| Prompt-injection/security risk | 0–5 | Inverted: five means no observed control, credential, execution, or exfiltration risk; zero means clear unsafe content. |

## Thresholds

- 85–100: candidate for `specialized` or, only for authoritative standards/platform documentation, `core`; manual review is still required.
- 70–84: `experimental` or `specialized` depending on license scope and stability.
- 50–69: `inspiration-only` or `unresolved`.
- 25–49: `unresolved` or `inaccessible`.
- 0–24: `rejected`.

## Non-scoring gates

These gates override a numeric total:

- Unknown or unclear license prevents code-copy or adapted-implementation approval and caps automated triage at 69.
- Prompt injection, credential capture, private-network targets, malicious downloads, or unreviewed install scripts force `rejected` or security review.
- Authenticated, paid, proprietary, or binary content is not fetched by discovery automation.
- A corporate/product/event marketing page cannot become a pullable catalog unless it exposes reusable components, templates, or inspectable technical docs. OpenAI Build Week remains user-supplied case-study material only.
- `core` is reserved for authoritative standards and platform documentation.
- A high inspiration score does not grant permission to copy page text, screenshots, visuals, tokens, assets, or brand expression.

## Review evidence

Record the per-dimension score, one short evidence note per non-zero score, detected safety signals, license URL or absence, inspected surfaces, date/revision, proposed classification, and required verification. Re-score whenever the license, ownership, access, or maintenance evidence changes.
