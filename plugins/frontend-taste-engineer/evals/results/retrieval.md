# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.001 |
| static-skill | 0.638 | 0.572 | 0.350 | 0.689 | 0.000 | 0.419 | 1.000 | 1295 | 0.336 |
| lexical | 0.824 | 0.797 | 0.652 | 0.872 | 0.000 | 0.204 | 1.000 | 4075 | 2.732 |
| hybrid | 0.880 | 0.831 | 0.713 | 0.986 | 0.000 | 0.176 | 1.000 | 4107 | 5.471 |

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

## Post-retrieval candidate directions

Direction cases: 10
Diversity gate: PASS
Classifier styling fields: prohibited
Candidate count: two or three per case

## External source policy

Passed cases: 8 / 8

## Case status

- `b2b-landing` — hybrid quality 0.660
- `consumer-landing` — hybrid quality 0.795
- `developer-tool` — hybrid quality 0.823
- `enterprise-dashboard` — hybrid quality 0.851
- `mobile-onboarding` — hybrid quality 0.770
- `settings-interface` — hybrid quality 0.751
- `searchable-table` — hybrid quality 0.720
- `checkout-form` — hybrid quality 0.703
- `existing-redesign` — hybrid quality 0.890
- `existing-product-context-contract` — hybrid quality 0.980
- `anti-slop-remediation` — hybrid quality 0.963
- `screenshot-reconstruction` — hybrid quality 0.849
- `constrained-system` — hybrid quality 0.912
- `public-service` — hybrid quality 0.794
- `dark-mode-product` — hybrid quality 0.878
- `rtl-interface` — hybrid quality 0.743
- `animated-component` — hybrid quality 0.912
- `intentional-motion-system` — hybrid quality 1.000
- `motion-opportunity-gate` — hybrid quality 0.880
- `direct-manipulation-sheet` — hybrid quality 0.970
- `adaptive-material-type` — hybrid quality 0.798
- `minimalism-not-emptiness` — hybrid quality 0.959
- `subject-led-interface-language` — hybrid quality 1.000
- `rendered-state-browser-qa` — hybrid quality 0.897
- `performance-remediation` — hybrid quality 0.617
- `minimal-alex-message` — hybrid quality 0.934; classification PASS (autonomous-zero-brief-build)
- `minimal-robotics-team` — hybrid quality 0.948; classification PASS (autonomous-zero-brief-build)
- `minimal-ai-study-group` — hybrid quality 0.922; classification PASS (autonomous-zero-brief-build)
- `minimal-portfolio` — hybrid quality 0.878; classification PASS (autonomous-zero-brief-build)
- `minimal-machines-alive` — hybrid quality 0.883; classification PASS (autonomous-zero-brief-build)
- `minimal-funny-late-friend` — hybrid quality 0.934; classification PASS (autonomous-zero-brief-build)
- `minimal-premium-product` — hybrid quality 0.987; classification PASS (autonomous-zero-brief-build)
- `minimal-public-service` — hybrid quality 0.895; classification PASS (autonomous-zero-brief-build)
- `adaptive-personal-finance` — hybrid quality 0.935; classification PASS (autonomous-zero-brief-build)
- `adaptive-banking-onboarding` — hybrid quality 0.922; classification PASS (autonomous-zero-brief-build)
- `adaptive-investment-analytics` — hybrid quality 0.908; classification PASS (autonomous-zero-brief-build)
- `adaptive-enterprise-product` — hybrid quality 0.892; classification PASS (autonomous-zero-brief-build)
- `adaptive-developer-tool` — hybrid quality 0.921; classification PASS (autonomous-zero-brief-build)
- `adaptive-premium-ecommerce` — hybrid quality 0.961; classification PASS (autonomous-zero-brief-build)
- `continuous-narrative-unboxing` — hybrid quality 0.920
- `customer-copy-without-build-narration` — hybrid quality 0.964
- `route-backed-primary-navigation` — hybrid quality 0.919
- `concise-marketing-copy` — hybrid quality 1.000
