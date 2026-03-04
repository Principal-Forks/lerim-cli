# OTEL Canvas: Maintain

The maintain operation is the "cold path" workflow that refines the memory library over time. While sync (hot path) extracts new memories from sessions, maintain processes existing memories to improve quality and relevance.

## Workflow Overview

```
maintain.started
    │
    ▼
maintain.scan.complete ────► maintain.error
    │
    ▼
maintain.actions.complete ─┬─► maintain.project.complete (per project)
    │                      │
    ▼                      │
maintain.complete ◄────────┘
```

## Events

### maintain.started
Emitted when the maintain operation begins.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `trigger` | string | yes | What triggered: `daemon`, `manual` |
| `input.projectCount` | number | yes | Number of registered projects to process |
| `input.dryRun` | boolean | no | Whether this is a dry run |

### maintain.scan.complete
Emitted after memories are scanned and analyzed for maintenance candidates.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.memoriesScanned` | number | yes | Total memories examined |
| `output.duplicatesFound` | number | yes | Duplicate memories identified |
| `output.lowValueFound` | number | yes | Low-value memories for archival |
| `output.decayCandidates` | number | yes | Memories eligible for confidence decay |

### maintain.actions.complete
Emitted after maintenance actions are applied.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.merged` | number | yes | Duplicate memories merged |
| `output.archived` | number | yes | Low-value memories archived |
| `output.consolidated` | number | yes | Related memories consolidated |
| `output.decayed` | number | yes | Memories with confidence decay applied |

### maintain.project.complete
Emitted after each project's maintenance completes.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `project.name` | string | yes | Project identifier |
| `project.path` | string | yes | Project filesystem path |
| `output.merged` | number | yes | Memories merged in this project |
| `output.archived` | number | yes | Memories archived in this project |
| `output.consolidated` | number | yes | Memories consolidated |
| `output.decayed` | number | yes | Decay applied count |
| `output.costUsd` | number | no | LLM cost for this project |

### maintain.complete
Emitted when the maintain operation finishes.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `output.status` | string | yes | `completed`, `partial`, or `failed` |
| `output.exitCode` | number | yes | Exit code (0=OK, 1=fatal, 3=partial, 4=lock_busy) |
| `output.projectsProcessed` | number | yes | Successfully processed project count |
| `output.projectsFailed` | number | yes | Failed project count |
| `output.costUsd` | number | no | Total LLM cost |
| `duration.ms` | number | yes | Total operation duration |

### maintain.error
Emitted when an error occurs.

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `error.type` | string | yes | Exception class name |
| `error.message` | string | yes | Error description |
| `error.stage` | string | no | Stage: `lock`, `scan`, `actions` |
| `error.project` | string | no | Project name if project-specific |

## Source Files

- `src/lerim/app/daemon.py` - Orchestration and lock handling
- `src/lerim/runtime/agent.py` - LerimAgent.maintain() implementation

## Maintenance Actions

The maintain workflow performs these refinement operations:

1. **Merge** - Combine duplicate or near-duplicate memories
2. **Archive** - Move low-value or obsolete memories to archive
3. **Consolidate** - Merge related memories into cohesive units
4. **Decay** - Apply time-based confidence reduction to stale memories

## Configuration

Decay behavior is controlled by these settings:

- `decay_days` - Days after which decay begins
- `decay_archive_threshold` - Confidence below which memories are archived
- `decay_min_confidence_floor` - Minimum confidence value
- `decay_recent_access_grace_days` - Grace period for recently accessed memories
