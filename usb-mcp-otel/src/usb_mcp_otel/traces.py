from typing import Any, Optional, Dict

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .config import BasicMcpOtelConfig


class McpOtelTraces:

    def __init__(self, basic_config: Optional[BasicMcpOtelConfig] = None, provider_kwargs: Optional[Dict[str, Any]] = None,
                 exporter_kwargs: Optional[Dict[str, Any]] = None, resource_attributes: Optional[Dict[str, Any]] = None,
                 batch_processor_kwargs: Optional[Dict[str, Any]] = None):
        self._basic_config = basic_config
        self._provider_kwargs = provider_kwargs
        self._exporter_kwargs = exporter_kwargs
        self._resource_attributes = resource_attributes
        self._batch_processor_kwargs = batch_processor_kwargs

        if self._basic_config is None:
            self._basic_config = BasicMcpOtelConfig.load_from_env()

        self._setup_traces()

    def _setup_traces(self):

        attributes = {
            SERVICE_NAME: self._basic_config.service_name
        }

        if self._resource_attributes:
            attributes.update(self._resource_attributes)

        exporter_kwargs = self._exporter_kwargs or {}
        provider_kwargs = self._provider_kwargs or {}
        batch_processor_kwargs = self._batch_processor_kwargs or {}

        if self._basic_config.otel_exporter_endpoint:
            exporter_kwargs.setdefault("endpoint", self._basic_config.otel_exporter_endpoint)

        resource = Resource.create(attributes)
        span_exporter = OTLPSpanExporter(**exporter_kwargs)
        traces_provider = TracerProvider(resource=resource, **provider_kwargs)
        batch_span_processor = BatchSpanProcessor(span_exporter, **batch_processor_kwargs)
        traces_provider.add_span_processor(batch_span_processor)
        trace.set_tracer_provider(traces_provider)
