# Retrieval evaluation

**Result:** PASS

| Variant | Quality | Precision | Recall | Mandatory recall | Duplicates | Irrelevant tokens | Provenance | Context tokens | p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0 | 0.004 |
| static-skill | 0.656 | 0.500 | 0.325 | 0.854 | 0.000 | 0.498 | 1.000 | 972 | 1.979 |
| lexical | 0.737 | 0.650 | 0.469 | 0.865 | 0.000 | 0.348 | 1.000 | 3013 | 6.552 |
| hybrid | 0.751 | 0.650 | 0.481 | 0.906 | 0.000 | 0.349 | 1.000 | 3055 | 4.655 |

## Gates

- PASS — mandatory_rule_recall
- PASS — duplicate_rate
- PASS — context_budget
- PASS — provenance_correctness
- PASS — hybrid_not_below_lexical
- PASS — latency

## Case status

- `b2b-landing` — hybrid quality 0.659
- `consumer-landing` — hybrid quality 0.605
- `developer-tool` — hybrid quality 0.798
- `enterprise-dashboard` — hybrid quality 0.912
- `mobile-onboarding` — hybrid quality 0.753
- `settings-interface` — hybrid quality 0.692
- `searchable-table` — hybrid quality 0.775
- `checkout-form` — hybrid quality 0.629
- `existing-redesign` — hybrid quality 0.657
- `screenshot-reconstruction` — hybrid quality 0.789
- `constrained-system` — hybrid quality 0.934
- `public-service` — hybrid quality 0.765
- `dark-mode-product` — hybrid quality 0.934
- `rtl-interface` — hybrid quality 0.609
- `animated-component` — hybrid quality 0.912
- `performance-remediation` — hybrid quality 0.598
