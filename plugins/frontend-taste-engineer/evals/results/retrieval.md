# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.001 |
| static-skill | 0.633 | 0.613 | 0.327 | 0.645 | 0.000 | 0.380 | 1.000 | 1183 | 0.307 |
| lexical | 0.768 | 0.735 | 0.544 | 0.822 | 0.000 | 0.265 | 1.000 | 3157 | 1.485 |
| hybrid | 0.868 | 0.810 | 0.730 | 0.950 | 0.000 | 0.189 | 1.000 | 3187 | 3.690 |

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

- `b2b-landing` — hybrid quality 0.660
- `consumer-landing` — hybrid quality 0.596
- `developer-tool` — hybrid quality 0.798
- `enterprise-dashboard` — hybrid quality 0.912
- `mobile-onboarding` — hybrid quality 0.753
- `settings-interface` — hybrid quality 0.744
- `searchable-table` — hybrid quality 0.722
- `checkout-form` — hybrid quality 0.629
- `existing-redesign` — hybrid quality 0.657
- `screenshot-reconstruction` — hybrid quality 0.789
- `constrained-system` — hybrid quality 0.934
- `public-service` — hybrid quality 0.765
- `dark-mode-product` — hybrid quality 0.934
- `rtl-interface` — hybrid quality 0.609
- `animated-component` — hybrid quality 0.934
- `performance-remediation` — hybrid quality 0.598
- `minimal-alex-message` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-robotics-team` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-ai-study-group` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-portfolio` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-machines-alive` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-funny-late-friend` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-premium-product` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-public-service` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-personal-finance` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-banking-onboarding` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-investment-analytics` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-enterprise-product` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-developer-tool` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-premium-ecommerce` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
