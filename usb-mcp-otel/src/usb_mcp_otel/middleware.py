import logging
from typing import TYPE_CHECKING, Any

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from fastmcp.server.middleware import Middleware, MiddlewareContext

try:
    from fastmcp.server.middleware import Middleware, MiddlewareContext

    HAS_FASTMCP = True
except ImportError:

    # Skipping OpenTelemetry middleware setup due to missing FastMCP version.
    # Please ensure you have FastMCP v3.0.0 or later installed.
    HAS_FASTMCP = False
    logger.warning(
        "Skipping OpenTelemetry middleware setup due to missing FastMCP. "
        "Please ensure you have FastMCP v3.0.0 or later installed if you intend to use the tracer middleware."
    )
    Middleware = Any
    MiddlewareContext = Any

from .decorator import otel_middleware_tracer


class OTELTracerMiddleware(Middleware):

    def __init__(self, *args, **kwargs):
        # Preventing the class from being used if the dependency is missing
        if not HAS_FASTMCP:
            raise RuntimeError(
                "OTELTracerMiddleware was initialized as FastMCP is not installed. "
                "Install it via: pip install 'usb-mcp-otel[fastmcp]' or 'usb-mcp-otel[all]'"
            )
        super().__init__(*args, **kwargs)

    @otel_middleware_tracer()
    async def on_initialize(self, context: MiddlewareContext, call_next):
        result = await call_next(context)
        return result

    @otel_middleware_tracer()
    async def on_call_tool(self, context: MiddlewareContext, call_next):
        result = await call_next(context)
        return result

    @otel_middleware_tracer()
    async def on_read_resource(self, context: MiddlewareContext, call_next):
        result = await call_next(context)
        return result

    @otel_middleware_tracer()
    async def on_get_prompt(self, context: MiddlewareContext, call_next):
        result = await call_next(context)
        return result
