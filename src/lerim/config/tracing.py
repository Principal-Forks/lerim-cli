"""OpenTelemetry tracing for PydanticAI agent instrumentation.

Sends spans to Logfire cloud (free tier) and/or a local OTLP collector.
Activated by ``tracing.enabled = true`` in config or ``LERIM_TRACING=1``.
"""

from __future__ import annotations

import logfire
from loguru import logger

from lerim.config.settings import Config


def _make_otlp_processor(endpoint: str):
    """Create an OTLP span processor that sends protobuf to the given endpoint.

    Uses the standard OTLPSpanExporter which sends protobuf format.
    Returns None if the opentelemetry exporter is not installed.
    """
    try:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor

        # OTLPSpanExporter sends protobuf by default with Content-Type: application/x-protobuf
        exporter = OTLPSpanExporter(endpoint=endpoint)
        return SimpleSpanProcessor(exporter)
    except ImportError:
        logger.warning(
            "opentelemetry-exporter-otlp-proto-http not installed, "
            "skipping OTLP export. Install with: pip install lerim[test]"
        )
        return None


def configure_tracing(config: Config) -> None:
    """Activate OpenTelemetry tracing if enabled in config or via LERIM_TRACING env var.

    Sends traces to Logfire cloud via the token in ``.logfire/`` directory.
    If ``tracing.otlp_endpoint`` is set, also exports to a local OTLP collector.
    Must be called once at startup before any LerimAgent is constructed.
    """
    if not config.tracing_enabled:
        return

    # Build additional span processors for local OTLP export
    additional_processors = []
    if config.tracing_otlp_endpoint:
        processor = _make_otlp_processor(config.tracing_otlp_endpoint)
        if processor:
            additional_processors.append(processor)

    logfire.configure(
        send_to_logfire="if-token-present" if config.tracing_send_to_logfire else False,
        service_name="lerim",
        console=False,
        additional_span_processors=additional_processors if additional_processors else None,
    )
    logfire.instrument_pydantic_ai(include_content=config.tracing_include_content)
    logfire.instrument_dspy()
    if config.tracing_include_httpx:
        logfire.instrument_httpx(capture_all=True)

    destinations = []
    if config.tracing_send_to_logfire:
        destinations.append("Logfire")
    if config.tracing_otlp_endpoint:
        destinations.append(config.tracing_otlp_endpoint)
    logger.info(f"OTel tracing enabled → {', '.join(destinations) or 'no destinations'}")


if __name__ == "__main__":
    """Minimal self-test: configure_tracing runs without error."""
    from lerim.config.settings import load_config

    cfg = load_config()
    configure_tracing(cfg)
    state = "enabled" if cfg.tracing_enabled else "disabled"
    print(f"tracing.py self-test passed (tracing {state})")
