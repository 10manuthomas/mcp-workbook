from functools import wraps
from typing import Optional, Any

from opentelemetry.trace import Status, StatusCode

from .telemetry import USBMcpOtel


def _get_client_info(ctx: Any) -> Any:

    # 1. Try standard message params
    try:
        return ctx.message.params.clientInfo
    except AttributeError:
        pass

    # 2. Try session params
    try:
        return ctx.fastmcp_context.session.client_params.clientInfo
    except AttributeError:
        return None


def otel_middleware_tracer(instrumentation_name: Optional[str] = None, version: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            ctx = args[1]
            fastmcp_context = getattr(ctx, 'fastmcp_context', None)
            client_id = getattr(fastmcp_context, 'client_id', "unknown")
            session_id = getattr(fastmcp_context, 'session_id', "unknown")
            fastmcp_obj = getattr(fastmcp_context, 'fastmcp', None)
            mcp_server_name = getattr(fastmcp_obj, 'name', "unknown")

            client_info = _get_client_info(ctx)
            client_name = getattr(client_info, 'name', "unknown") or "unknown"
            client_version = getattr(client_info, 'version', "unknown") or "unknown"

            span_name = "mcp_unknown_operation"
            mcp_primitive_type = None
            mcp_primitive_key = None

            msg = getattr(ctx, 'message', None)

            if func.__name__ == "on_initialize":
                span_name = f"mcp_client_initialize_{client_name}"
            elif func.__name__ == "on_call_tool":
                tool_name = getattr(msg, 'name', 'unknown')
                span_name = f"complete_mcp_tool_call_{tool_name}"
                mcp_primitive_type = "tool"
                mcp_primitive_key = tool_name
            elif func.__name__ == "on_read_resource":
                resource_uri = getattr(msg, 'uri', 'unknown')
                span_name = f"complete_mcp_resource_read_{resource_uri}"
                mcp_primitive_type = "resource"
                mcp_primitive_key = resource_uri
            elif func.__name__ == "on_get_prompt":
                prompt_name = getattr(msg, 'name', 'unknown')
                span_name = f"complete_mcp_get_prompt_{prompt_name}"
                mcp_primitive_type = "prompt"
                mcp_primitive_key = prompt_name

            tracer = USBMcpOtel.get_tracer(instrumentation_name, version)

            with tracer.start_as_current_span(span_name) as span:
                try:
                    span.set_attribute("client_name", client_name)
                    span.set_attribute("client_id", client_id)
                    span.set_attribute("session_id", session_id)
                    span.set_attribute("client_version", client_version)
                    span.set_attribute("mcp_server_name", mcp_server_name)
                    span.set_attribute("mcp_primitive_type", mcp_primitive_type)
                    span.set_attribute("mcp_primitive_key", mcp_primitive_key)
                    result = await func(*args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise e

        return wrapper

    return decorator
