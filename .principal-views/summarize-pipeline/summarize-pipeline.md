# OTEL Canvas: Summarize Pipeline

The summarize pipeline uses DSPy ChainOfThought to create structured summaries from session transcripts. It captures user intent and session narrative for each coding session.

## Workflow Overview

```
summarize.started
    │
    ├─► summarize.skip_merge (single window)
    │         │
    │         ▼
    │   summarize.complete
    │
    └─► summarize.window.complete (per window)
              │
              ▼
        summarize.merge.complete
              │
              ▼
        summarize.complete
```

## Events

### summarize.started
Emitted when summarization begins.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `input.transcriptLength` | number | yes | Character length of transcript |
| `input.windowCount` | number | yes | Number of windows |
| `input.hasGuidance` | boolean | yes | Whether guidance was provided |

### summarize.window.complete
Emitted after each partial summary (multi-window only).

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `window.index` | number | yes | Zero-based window index |
| `window.totalWindows` | number | yes | Total window count |

### summarize.skip_merge
Emitted for single-window direct summarization.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.mode` | string | yes | Always "direct" |

### summarize.merge.complete
Emitted after partial summaries are merged.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.partialCount` | number | yes | Number of partials merged |

### summarize.complete
Emitted when summarization finishes.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.titleLength` | number | yes | Title character length |
| `output.intentWords` | number | yes | User intent word count |
| `output.narrativeWords` | number | yes | Narrative word count |
| `output.tagCount` | number | yes | Number of tags |
| `duration.ms` | number | yes | Total duration |

### summarize.error
Emitted on failure.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `error.type` | string | yes | Exception class |
| `error.message` | string | yes | Error description |
| `duration.ms` | number | yes | Duration until failure |

## Source Files

- `src/lerim/memory/summarization_pipeline.py`
