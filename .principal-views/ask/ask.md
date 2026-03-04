# OTEL Canvas: Ask

The ask operation queries accumulated memories using natural language. It's the primary way users interact with their memory library.

## Workflow Overview

```
ask.started
    │
    ▼
ask.inference.complete ────► ask.error
    │
    ▼
ask.complete
```

## Events

### ask.started
Emitted when a query is received.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `input.questionLength` | number | yes | Character length of the question |
| `input.memoryRoot` | string | yes | Memory directory being queried |

### ask.inference.complete
Emitted after the LLM generates a response.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.responseLength` | number | yes | Character length of response |
| `output.sessionId` | string | yes | Agent session identifier |
| `output.costUsd` | number | yes | LLM inference cost |

### ask.complete
Emitted when the query completes.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.hasError` | boolean | yes | Whether response indicates an error (e.g., auth failure) |
| `duration.ms` | number | yes | Total operation duration |

### ask.error
Emitted when the query fails.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `error.type` | string | yes | Exception class name |
| `error.message` | string | yes | Error description |
| `duration.ms` | number | yes | Duration until failure |

## Source Files

- `src/lerim/app/api.py` - `api_ask()` entry point
- `src/lerim/runtime/agent.py` - `LerimAgent.ask()` implementation
