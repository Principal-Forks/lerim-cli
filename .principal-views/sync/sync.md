# Sync Operation

The sync operation is the primary mechanism for extracting learnings from coding agent sessions and storing them as persistent memories.

## What Problem Does This Solve?

Coding agents (Claude, Codex, Cursor, etc.) accumulate valuable knowledge during sessions - decisions made, patterns learned, mistakes avoided. Without lerim, this knowledge is lost when sessions end. The sync operation captures and preserves this knowledge.

## How It Works

1. **Index** - Discover new sessions from connected agent platforms
2. **Enqueue** - Queue sessions for processing, matching them to registered projects
3. **Extract** - Process each session through the extraction pipeline to identify learnings
4. **Store** - Save extracted memories to the project's `.lerim/memory/` directory

## Operations

### Full Sync (`lerim sync`)

Runs the complete sync pipeline:
- Indexes sessions within the configured time window (default: 7 days)
- Filters by agent type if specified
- Extracts memories from queued sessions
- Records results in the service run database

### Single Session Sync (`lerim sync --run-id <id>`)

Processes a specific session by run ID:
- Skips indexing phase
- Forces re-extraction even if previously processed
- Useful for debugging or re-processing failed sessions

## Design Choices

### Sequential Job Processing

Jobs are processed sequentially (oldest-first) rather than in parallel. This ensures:
- Later sessions can correctly update memories from earlier sessions
- Consistent ordering of memory updates
- Predictable memory state after sync

### Project-Based Memory Routing

Each session is matched to a registered project. Memories are stored in the project's local `.lerim/memory/` directory rather than a global location. This:
- Keeps project context isolated
- Enables project-specific memory search
- Supports multi-project workflows

### Lock-Based Concurrency Control

A filesystem lock prevents concurrent sync/maintain operations:
- Avoids race conditions in memory updates
- Supports distributed deployments (Docker, multiple hosts)
- Auto-recovers from stale locks (dead processes)

## Error Scenarios

### Lock Busy
Another sync or maintain operation is running. The operation exits with code 4.

### Partial Failure
Some sessions extracted successfully, others failed. Exit code 3 indicates partial success - review failed sessions for retry.

### No Sessions
No new sessions found in the time window. This is normal for quiet periods - not an error.

## Triggers

- **daemon** - Automated background sync from the daemon loop
- **manual** - User-initiated via `lerim sync` CLI command
- **api** - Triggered via HTTP API endpoint
