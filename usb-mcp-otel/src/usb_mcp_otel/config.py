from dataclasses import dataclass


@dataclass
class BasicMcpOtelConfig:
    """
    OpenTelemetryConfig is a dataclass that holds the configuration for OpenTelemetry.
    """

    service_name: str
    otel_exporter_endpoint: str

    @classmethod
    def load_from_env(cls) -> "BasicMcpOtelConfig":
        """
        Load the OpenTelemetry configuration from environment variables.

        Returns:
            An instance of OpenTelemetryConfig with values loaded from environment variables.
        """
        import os
        service_name = os.getenv("OTEL_SERVICE_NAME", "mcp-server")
        otel_exporter_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

        return cls(
            service_name=service_name,
            otel_exporter_endpoint=otel_exporter_endpoint
        )
