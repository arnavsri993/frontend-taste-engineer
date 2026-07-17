# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.002 |
| static-skill | 0.650 | 0.568 | 0.351 | 0.737 | 0.000 | 0.418 | 1.000 | 1291 | 0.453 |
| lexical | 0.816 | 0.782 | 0.637 | 0.867 | 0.000 | 0.215 | 1.000 | 3511 | 2.785 |
| hybrid | 0.875 | 0.816 | 0.744 | 0.959 | 0.000 | 0.188 | 1.000 | 3469 | 4.911 |

## Gates

- PASS — mandatory_rule_recall
- PASS — duplicate_rate
- PASS — irrelevant_token_rate
- PASS — context_budget
- PASS — provenance_correctness
- PASS — hybrid_not_below_lexical
- PASS — latency
- PASS — minimal_prompt_skill_activation
- PASS — minimal_prompt_classification
- PASS — context_adaptive_direction_diversity
- PASS — external_source_policy
- PASS — required_record_ids

## Minimal-prompt classification

Passed cases: 14 / 14
Skill activation: PASS

## Context-adaptive direction

Direction cases: 10
Diversity gate: PASS
Visual intensity levels: 1, 2, 3, 4, 5
Overly similar pairs: 0

## External source policy

Passed cases: 8 / 8

## Case status

- `b2b-landing` — hybrid quality 0.547
- `consumer-landing` — hybrid quality 0.658
- `developer-tool` — hybrid quality 0.828
- `enterprise-dashboard` — hybrid quality 0.849
- `mobile-onboarding` — hybrid quality 0.741
- `settings-interface` — hybrid quality 0.720
- `searchable-table` — hybrid quality 0.722
- `checkout-form` — hybrid quality 0.704
- `existing-redesign` — hybrid quality 0.890
- `anti-slop-remediation` — hybrid quality 0.963
- `screenshot-reconstruction` — hybrid quality 0.811
- `constrained-system` — hybrid quality 0.912
- `public-service` — hybrid quality 0.693
- `dark-mode-product` — hybrid quality 0.904
- `rtl-interface` — hybrid quality 0.746
- `animated-component` — hybrid quality 0.912
- `intentional-motion-system` — hybrid quality 1.000
- `motion-opportunity-gate` — hybrid quality 0.911
- `direct-manipulation-sheet` — hybrid quality 0.970
- `adaptive-material-type` — hybrid quality 0.797
- `minimalism-not-emptiness` — hybrid quality 1.000
- `performance-remediation` — hybrid quality 0.705
- `minimal-alex-message` — hybrid quality 0.877; classification PASS (autonomous-zero-brief-build)
- `minimal-robotics-team` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-ai-study-group` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `minimal-portfolio` — hybrid quality 0.877; classification PASS (autonomous-zero-brief-build)
- `minimal-machines-alive` — hybrid quality 0.876; classification PASS (autonomous-zero-brief-build)
- `minimal-funny-late-friend` — hybrid quality 0.877; classification PASS (autonomous-zero-brief-build)
- `minimal-premium-product` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `minimal-public-service` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `adaptive-personal-finance` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-banking-onboarding` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-investment-analytics` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `adaptive-enterprise-product` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-developer-tool` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-premium-ecommerce` — hybrid quality 0.987; classification PASS (autonomous-zero-brief-build)
- `concise-marketing-copy` — hybrid quality 1.000
