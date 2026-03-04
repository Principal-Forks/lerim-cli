# OTEL Canvas: LLM Internals

This canvas documents the **auto-instrumented** LLM operations captured by Logfire. These spans are created automatically when tracing is enabled - no manual instrumentation required.

## Instrumentation Setup

Configured in `src/lerim/config/tracing.py`:

```python
logfire.instrument_pydantic_ai()  # Agent runs, model requests, tool calls
logfire.instrument_dspy()          # ChainOfThought, Predict
logfire.instrument_httpx()         # HTTP requests (optional)
```

## Span Hierarchy

```
sync.operation (manual - our canvas)
│
├── pydantic_ai.agent.run          ← AUTO: Full agent execution
│   │
│   ├── pydantic_ai.model.request  ← AUTO: LLM API call
│   │   └── httpx.request          ← AUTO: HTTP to provider
│   │
│   ├── pydantic_ai.tool.call      ← AUTO: Tool execution
│   │
│   └── pydantic_ai.model.request  ← AUTO: Follow-up call
│
├── extract.started (manual - our canvas)
│
├── dspy.ChainOfThought            ← AUTO: DSPy reasoning
│   └── dspy.Predict               ← AUTO: Prediction step
│       └── httpx.request          ← AUTO: HTTP to provider
│
└── sync.complete (manual - our canvas)
```

## PydanticAI Spans (Cyan)

### pydantic_ai.agent.run
Top-level span for a full agent execution.

| Attribute | Description |
|-----------|-------------|
| `agent.name` | Agent identifier |
| `agent.model` | LLM model name |
| `run.prompt_length` | Input prompt length |

### pydantic_ai.model.request
Individual LLM API call.

| Attribute | Description |
|-----------|-------------|
| `model.name` | Model identifier |
| `model.provider` | openai, anthropic, openrouter, etc. |
| `tokens.input` | Input token count |
| `tokens.output` | Output token count |
| `duration.ms` | Request latency |

### pydantic_ai.tool.call
Agent tool invocation.

| Attribute | Description |
|-----------|-------------|
| `tool.name` | read_file, write_memory, glob, grep, etc. |
| `tool.success` | Whether tool succeeded |
| `duration.ms` | Tool execution time |

## DSPy Spans (Purple)

### dspy.ChainOfThought
DSPy reasoning step execution.

| Attribute | Description |
|-----------|-------------|
| `signature.name` | MemoryExtractSignature, TraceSummarySignature |
| `signature.inputs` | Input field names |
| `signature.outputs` | Output field names |

### dspy.Predict
Individual DSPy prediction.

| Attribute | Description |
|-----------|-------------|
| `model.name` | LLM model used |
| `tokens.input` | Input tokens |
| `tokens.output` | Output tokens |

## HTTP Spans (Orange)

### httpx.request
Outbound HTTP API call.

| Attribute | Description |
|-----------|-------------|
| `http.method` | GET, POST, etc. |
| `http.url` | Target URL |
| `http.status_code` | Response status |
| `duration.ms` | Request latency |

## Enabling Tracing

Set in `~/.lerim/config.toml`:

```toml
[tracing]
enabled = true
otlp_endpoint = "http://localhost:4318/v1/traces"  # Optional local collector
```

Or via environment:

```bash
LERIM_TRACING=1 lerim sync
```
