# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.004 |
| static-skill | 0.619 | 0.594 | 0.315 | 0.623 | 0.000 | 0.384 | 1.000 | 1239 | 0.840 |
| lexical | 0.752 | 0.710 | 0.545 | 0.792 | 0.000 | 0.287 | 1.000 | 3346 | 2.125 |
| hybrid | 0.850 | 0.781 | 0.701 | 0.941 | 0.000 | 0.222 | 1.000 | 3355 | 5.749 |

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

- `b2b-landing` — hybrid quality 0.658
- `consumer-landing` — hybrid quality 0.411
- `developer-tool` — hybrid quality 0.827
- `enterprise-dashboard` — hybrid quality 0.934
- `mobile-onboarding` — hybrid quality 0.720
- `settings-interface` — hybrid quality 0.744
- `searchable-table` — hybrid quality 0.722
- `checkout-form` — hybrid quality 0.629
- `existing-redesign` — hybrid quality 0.658
- `anti-slop-remediation` — hybrid quality 0.963
- `screenshot-reconstruction` — hybrid quality 0.790
- `constrained-system` — hybrid quality 0.912
- `public-service` — hybrid quality 0.689
- `dark-mode-product` — hybrid quality 0.881
- `rtl-interface` — hybrid quality 0.606
- `animated-component` — hybrid quality 0.934
- `intentional-motion-system` — hybrid quality 0.887
- `minimalism-not-emptiness` — hybrid quality 0.898
- `performance-remediation` — hybrid quality 0.567
- `minimal-alex-message` — hybrid quality 0.903; classification PASS (autonomous-zero-brief-build)
- `minimal-robotics-team` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `minimal-ai-study-group` — hybrid quality 0.987; classification PASS (autonomous-zero-brief-build)
- `minimal-portfolio` — hybrid quality 0.877; classification PASS (autonomous-zero-brief-build)
- `minimal-machines-alive` — hybrid quality 0.877; classification PASS (autonomous-zero-brief-build)
- `minimal-funny-late-friend` — hybrid quality 0.903; classification PASS (autonomous-zero-brief-build)
- `minimal-premium-product` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `minimal-public-service` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `adaptive-personal-finance` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-banking-onboarding` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-investment-analytics` — hybrid quality 0.974; classification PASS (autonomous-zero-brief-build)
- `adaptive-enterprise-product` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-developer-tool` — hybrid quality 1.000; classification PASS (autonomous-zero-brief-build)
- `adaptive-premium-ecommerce` — hybrid quality 0.987; classification PASS (autonomous-zero-brief-build)
- `concise-marketing-copy` — hybrid quality 1.000
