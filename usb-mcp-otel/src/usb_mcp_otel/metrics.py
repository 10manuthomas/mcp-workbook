from typing import Optional, Dict, Any

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

from .config import BasicMcpOtelConfig


class McpOtelMetrics:
    def __init__(self, basic_config: Optional[BasicMcpOtelConfig] = None, provider_kwargs: Optional[Dict[str, Any]] = None,
                 exporter_kwargs: Optional[Dict[str, Any]] = None,
                 resource_attributes: Optional[Dict[str, Any]] = None):
        self._basic_config = basic_config
        self._provider_kwargs = provider_kwargs
        self._exporter_kwargs = exporter_kwargs
        self._resource_attributes = resource_attributes

        if self._basic_config is None:
            self._basic_config = BasicMcpOtelConfig.load_from_env()

        self._setup_metrics()

    def _setup_metrics(self) -> None:

        attributes = {
            SERVICE_NAME: self._basic_config.service_name
        }

        if self._resource_attributes:
            attributes.update(self._resource_attributes)

        exporter_kwargs = self._exporter_kwargs or {}
        provider_kwargs = self._provider_kwargs or {}
        if self._basic_config.otel_exporter_endpoint:
            exporter_kwargs.setdefault("endpoint", self._basic_config.otel_exporter_endpoint)

        resource = Resource.create(attributes)
        otlp_metric_exporter = OTLPMetricExporter(**exporter_kwargs)
        metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
        metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader], **provider_kwargs)
        metrics.set_meter_provider(metrics_provider)
