# OTEL Canvas: Extract Pipeline

The extract pipeline uses DSPy ChainOfThought to extract memory candidates from session transcripts. It supports windowing for long transcripts and automatic deduplication.

## Workflow Overview

```
extract.started
    │
    ▼
extract.window.complete ────► extract.error
    │ (per window)
    ▼
extract.merge.complete
    │ (if multi-window)
    ▼
extract.complete
```

## Events

### extract.started
Emitted when extraction begins.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `input.transcriptLength` | number | yes | Character length of transcript |
| `input.windowCount` | number | yes | Number of windows to process |
| `input.hasGuidance` | boolean | yes | Whether lead agent provided guidance |

### extract.window.complete
Emitted after each window is processed.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `window.index` | number | yes | Zero-based window index |
| `window.candidateCount` | number | yes | Candidates from this window |

### extract.merge.complete
Emitted after multi-window deduplication (skipped for single-window).

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.beforeCount` | number | yes | Candidates before merge |
| `output.afterCount` | number | yes | Candidates after dedupe |

### extract.complete
Emitted when extraction finishes.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.candidateCount` | number | yes | Final candidate count |
| `output.decisionCount` | number | yes | Decision primitives extracted |
| `output.learningCount` | number | yes | Learning primitives extracted |
| `duration.ms` | number | yes | Total extraction duration |

### extract.error
Emitted when extraction fails.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `error.type` | string | yes | Exception class name |
| `error.message` | string | yes | Error description |
| `error.windowIndex` | number | no | Window index if failed during extraction |
| `duration.ms` | number | yes | Duration until failure |

## Source Files

- `src/lerim/memory/extract_pipeline.py` - DSPy extraction with windowing

## Memory Types

The pipeline extracts two primitive types:
- **decisions** - Explicit choices, policies, or architectural decisions
- **learnings** - Insights, procedures, friction points, pitfalls, preferences
