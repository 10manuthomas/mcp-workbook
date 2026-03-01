"""
USB-MCP-OTEL: US Bank Enterprise OpenTelemetry wrapper for FastMCP.
"""

from .config import BasicMcpOtelConfig
from .telemetry import USBMcpOtel
from .middleware import OTELTracerMiddleware

__version__ = "0.0.1"
__author__ = "USB Enterprise Team"

__all__ = [
    "BasicMcpOtelConfig",
    "USBMcpOtel",
    "OTELTracerMiddleware",
]