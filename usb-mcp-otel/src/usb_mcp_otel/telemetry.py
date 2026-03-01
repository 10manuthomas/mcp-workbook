import os
from typing import Optional, Dict, Any

from opentelemetry.trace import get_tracer

from .config import BasicMcpOtelConfig
from .metrics import McpOtelMetrics
from .traces import McpOtelTraces


class USBMcpOtel:
    _initialized = False

    @classmethod
    def get_tracer(cls, instrumentation_name: Optional[str] = None, version: Optional[str] = None):

        if not instrumentation_name:
            instrumentation_name = os.getenv("INSTRUMENTATION_NAME", "usb-mcp")

        if not version:
            version = os.getenv("INSTRUMENTATION_VERSION", None)

        otel_tracer = get_tracer(instrumentation_name, version)
        return otel_tracer

    @property
    def mcp_otel_traces(self):
        return self._mcp_otel_traces

    @property
    def mcp_otel_metrics(self):
        return self._mcp_otel_metrics

    def __init__(self, basic_config: Optional[BasicMcpOtelConfig] = None,
                 trace_provider_kwargs: Optional[Dict[str, Any]] = None,
                 trace_exporter_kwargs: Optional[Dict[str, Any]] = None,
                 trace_resource_attributes: Optional[Dict[str, Any]] = None,
                 trace_batch_processor_kwargs: Optional[Dict[str, Any]] = None,
                 metrics_provider_kwargs: Optional[Dict[str, Any]] = None,
                 metrics_exporter_kwargs: Optional[Dict[str, Any]] = None,
                 metrics_resource_attributes: Optional[Dict[str, Any]] = None
                 ):

        if USBMcpOtel._initialized:
            return
        self._basic_config = basic_config
        self._trace_provider_kwargs = trace_provider_kwargs
        self._trace_exporter_kwargs = trace_exporter_kwargs
        self._trace_resource_attributes = trace_resource_attributes
        self._trace_batch_processor_kwargs = trace_batch_processor_kwargs
        self._metrics_provider_kwargs = metrics_provider_kwargs
        self._metrics_exporter_kwargs = metrics_exporter_kwargs
        self._metrics_resource_attributes = metrics_resource_attributes

        self._mcp_otel_traces = McpOtelTraces(
            basic_config=self._basic_config,
            provider_kwargs=self._trace_provider_kwargs,
            exporter_kwargs=self._trace_exporter_kwargs,
            resource_attributes=self._trace_resource_attributes,
            batch_processor_kwargs=self._trace_batch_processor_kwargs
        )

        self._mcp_otel_metrics = McpOtelMetrics(
            basic_config=basic_config,
            provider_kwargs=metrics_provider_kwargs,
            exporter_kwargs=metrics_exporter_kwargs,
            resource_attributes=metrics_resource_attributes
        )
        USBMcpOtel._initialized = True
