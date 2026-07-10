# Frontend evidence manifests

Frontend-output scores are accepted only after a real task has been executed.
Create `<case-id>.json` here with all 16 rubric criteria. Each criterion requires
a `score` from 0–5 and at least one evidence item:

```json
{
  "rubric": {
    "accessibility": {
      "score": 4,
      "evidence": [
        {
          "status": "pass",
          "observation": "Primary flow completed by keyboard with visible focus.",
          "artifact": "artifacts/b2b-landing/keyboard-check.md",
          "command": "documented command or manual protocol"
        }
      ]
    }
  }
}
```

The evaluator intentionally leaves missing cases unscored. It does not infer
frontend quality from retrieval quality or file existence.
