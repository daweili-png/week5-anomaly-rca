import json
import time

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
    SpanExportResult,
)


class JSONFileSpanExporter(SpanExporter):
    """
    Custom exporter that writes finished spans to a JSON file.
    """

    def __init__(self, filename="output/spans_sample.json"):
        self.filename = filename

    def export(self, spans):
        records = []

        for span in spans:
            record = {
                "name": span.name,
                "trace_id": format(span.context.trace_id, "032x"),
                "span_id": format(span.context.span_id, "016x"),
                "attributes": dict(span.attributes),
                "start_time": span.start_time,
                "end_time": span.end_time,
            }

            records.append(record)

        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                for record in records:
                    f.write(json.dumps(record) + "\n")

            return SpanExportResult.SUCCESS

        except Exception:
            return SpanExportResult.FAILURE

    def shutdown(self):
        pass


def setup_tracer():
    """
    Configure OpenTelemetry tracing.
    """

    provider = TracerProvider()

    console_exporter = ConsoleSpanExporter()
    file_exporter = JSONFileSpanExporter()

    provider.add_span_processor(
        BatchSpanProcessor(console_exporter)
    )

    provider.add_span_processor(
        BatchSpanProcessor(file_exporter)
    )

    trace.set_tracer_provider(provider)

    return trace.get_tracer("week5-rca-agent")


def run_instrumented_agent(
    tracer,
    agent_function,
    metrics_file,
    log_file,
    start_time,
    end_time
):
    """
    Run RCA agent inside an OpenTelemetry GenAI span.
    """

    start = time.perf_counter()

    with tracer.start_as_current_span(
        "gen_ai.rca_agent"
    ) as span:

        # Simulated GenAI attributes
        span.set_attribute(
            "gen_ai.system",
            "simulated"
        )

        span.set_attribute(
            "gen_ai.request.model",
            "simulated-rca-agent"
        )

        # Approximate token values for demonstration
        input_tokens = 420
        output_tokens = 120

        span.set_attribute(
            "gen_ai.usage.input_tokens",
            input_tokens
        )

        span.set_attribute(
            "gen_ai.usage.output_tokens",
            output_tokens
        )

        result = agent_function(
            metrics_file,
            log_file,
            start_time,
            end_time
        )

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        span.set_attribute(
            "agent.latency_ms",
            round(latency_ms, 2)
        )

        # Zero cost because this run uses a simulated agent
        span.set_attribute(
            "agent.estimated_cost_usd",
            0.0
        )

        return result