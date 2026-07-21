# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.001 |
| static-skill | 0.640 | 0.559 | 0.349 | 0.712 | 0.000 | 0.431 | 1.000 | 1292 | 0.389 |
| lexical | 0.816 | 0.781 | 0.655 | 0.857 | 0.000 | 0.217 | 1.000 | 3681 | 2.484 |
| hybrid | 0.867 | 0.818 | 0.698 | 0.966 | 0.000 | 0.183 | 1.000 | 3674 | 4.326 |

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

- `b2b-landing` — hybrid quality 0.664
- `consumer-landing` — hybrid quality 0.659
- `developer-tool` — hybrid quality 0.826
- `enterprise-dashboard` — hybrid quality 0.850
- `mobile-onboarding` — hybrid quality 0.772
- `settings-interface` — hybrid quality 0.751
- `searchable-table` — hybrid quality 0.720
- `checkout-form` — hybrid quality 0.703
- `existing-redesign` — hybrid quality 0.728
- `anti-slop-remediation` — hybrid quality 0.963
- `screenshot-reconstruction` — hybrid quality 0.843
- `constrained-system` — hybrid quality 0.912
- `public-service` — hybrid quality 0.763
- `dark-mode-product` — hybrid quality 0.934
- `rtl-interface` — hybrid quality 0.831
- `animated-component` — hybrid quality 0.912
- `intentional-motion-system` — hybrid quality 1.000
- `motion-opportunity-gate` — hybrid quality 0.849
- `direct-manipulation-sheet` — hybrid quality 0.970
- `adaptive-material-type` — hybrid quality 0.798
- `minimalism-not-emptiness` — hybrid quality 1.000
- `subject-led-interface-language` — hybrid quality 0.950
- `rendered-state-browser-qa` — hybrid quality 0.896
- `performance-remediation` — hybrid quality 0.618
- `minimal-alex-message` — hybrid quality 0.921; classification PASS (autonomous-zero-brief-build)
- `minimal-robotics-team` — hybrid quality 0.922; classification PASS (autonomous-zero-brief-build)
- `minimal-ai-study-group` — hybrid quality 0.948; classification PASS (autonomous-zero-brief-build)
- `minimal-portfolio` — hybrid quality 0.918; classification PASS (autonomous-zero-brief-build)
- `minimal-machines-alive` — hybrid quality 0.882; classification PASS (autonomous-zero-brief-build)
- `minimal-funny-late-friend` — hybrid quality 0.934; classification PASS (autonomous-zero-brief-build)
- `minimal-premium-product` — hybrid quality 0.904; classification PASS (autonomous-zero-brief-build)
- `minimal-public-service` — hybrid quality 0.894; classification PASS (autonomous-zero-brief-build)
- `adaptive-personal-finance` — hybrid quality 0.961; classification PASS (autonomous-zero-brief-build)
- `adaptive-banking-onboarding` — hybrid quality 0.935; classification PASS (autonomous-zero-brief-build)
- `adaptive-investment-analytics` — hybrid quality 0.908; classification PASS (autonomous-zero-brief-build)
- `adaptive-enterprise-product` — hybrid quality 0.935; classification PASS (autonomous-zero-brief-build)
- `adaptive-developer-tool` — hybrid quality 0.907; classification PASS (autonomous-zero-brief-build)
- `adaptive-premium-ecommerce` — hybrid quality 0.948; classification PASS (autonomous-zero-brief-build)
- `concise-marketing-copy` — hybrid quality 1.000
