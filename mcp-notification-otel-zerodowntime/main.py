
from usb_mcp_otel import BasicMcpOtelConfig, USBMcpOtel, OTELTracerMiddleware

base_mcp_otel_config = BasicMcpOtelConfig(service_name="base-mcp-gateway", otel_exporter_endpoint="http://localhost:4317")
usb_mcp_otel = USBMcpOtel(basic_config=base_mcp_otel_config)

import mcp.types
import uvicorn
from cryptography.fernet import Fernet
from fastmcp import FastMCP, Context
from fastmcp.client import StreamableHttpTransport
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.middleware import MiddlewareContext, Middleware
from fastmcp.server.middleware.caching import ResponseCachingMiddleware
from fastmcp.server.middleware.logging import LoggingMiddleware, StructuredLoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.server.providers.proxy import FastMCPProxy
from key_value.aio.stores.redis import RedisStore
from key_value.aio.wrappers.encryption import FernetEncryptionWrapper

redis_store = RedisStore(host="localhost", port=6379)
# redis_store = RedisStore(host="host.docker.internal", port=6379)

# The AzureProvider handles Azure's token format and validation
auth_provider = AzureProvider(
    client_id="",  # Your Azure App Client ID
    client_secret="",  # Your Azure App Client Secret
    tenant_id="",  # Your Azure Tenant ID (REQUIRED)
    base_url="http://localhost:8090",  # Must match your App registration
    # base_url="http://localhost:30090",  # Must match your App registration
    required_scopes=["mcp.tool.access"],  # At least one scope REQUIRED - name of scope from your App
    # identifier_uri defaults to api://{client_id}
    identifier_uri="",
    # Optional: request additional upstream scopes in the authorize request
    additional_authorize_scopes=["User.Read", "offline_access", "openid", "email"],
    redirect_path="/auth/callback",  # Default value, customize if needed
    # base_authority="login.microsoftonline.us"      # For Azure Government (default: login.microsoftonline.com)
    client_storage=FernetEncryptionWrapper(
        key_value=redis_store,
        fernet=Fernet("")
    )
)
print("Base URl is http://localhost:30090")

redis_cache_middleware = ResponseCachingMiddleware(
    cache_storage=redis_store
)

mcp_app = FastMCP("Base Gateway MCP Server", mask_error_details=True,
                  auth=auth_provider,
                  session_state_store=redis_store,
                  # stateless_http=True,
                  # middleware=[redis_cache_middleware]
                  )

from fastmcp.server.dependencies import get_access_token


class SessionManager:
    def __init__(self):
        self.sessions = set()

    def register(self, session):
        self.sessions.add(session)

    def unregister(self, session):
        self.sessions.discard(session)

    async def broadcast(self, notification_type):
        for session in list(self.sessions):
            try:
                await session.send_notification(notification_type)
            except Exception as e:
                print(e)
                # Remove dead sessions
                self.sessions.discard(session)


session_manager = SessionManager()


@mcp_app.tool
# @bridge_mcp_context
async def base_server_get_user_info(ctx: Context) -> dict:
    token = get_access_token()

    if token is None:
        return {"authenticated": False}
    print("Calling base_server_get_user_info  tool")
    access_tk = await ctx.get_state("access_token")
    print("access_tk:::", access_tk)
    # Access client-provided metadata
    meta = ctx.request_context.meta
    print("Request meta:", meta)

    return {"authenticated": True, "user": token.claims}


@mcp_app.tool
async def base_server_get_user_info_2(ctx: Context) -> dict:
    token = get_access_token()
    if token is None:
        return {"authenticated": False}
    print("Calling base_server_get_user_info  tool")
    access_tk = await ctx.get_state("access_token")
    print("access_tk:::", access_tk)
    # Access client-provided metadata
    meta = ctx.request_context.meta
    print("Request meta:", meta)

    return {"authenticated": True, "user": token.claims}


@mcp_app.tool
async def force_notification(ctx: Context) -> str:
    await session_manager.broadcast(mcp.types.ToolListChangedNotification())
    await session_manager.broadcast(mcp.types.ResourceListChangedNotification())
    await session_manager.broadcast(mcp.types.PromptListChangedNotification())
    print("Notifications sent to all sessions")
    return "Notifications sent"


from fastmcp.server.providers.proxy import ProxyClient


def make_client_factory(mcp_server_url: str):
    def client_factory():
        print(f"Client factory invoked for {mcp_server_url}")
        access_token = get_access_token()
        headers = {"access_token": access_token.token} if access_token else {}

        transport = StreamableHttpTransport(
            url=mcp_server_url,
            headers=headers
        )
        return ProxyClient(transport)

    return client_factory


subservers = {
    "flight-booking": "http://localhost:8091/flight-booking-mcp",
    # "flight-booking": "http://host.docker.internal:8091/flight-booking-mcp",
}

dynamic_subservers = {
    "hotel-booking": "http://localhost:8092/hotel-booking-mcp",
    # "hotel-booking": "http://host.docker.internal:8092/hotel-booking-mcp",
}


@mcp_app.tool
async def dynamic_server_mounting(ctx: Context) -> str:
    for sub_namespace, sub_url in dynamic_subservers.items():
        sub_proxy = FastMCPProxy(
            client_factory=make_client_factory(sub_url),
            name=sub_namespace,
            auth=None  # or a per-subserver auth strategy
        )
        mcp_app.mount(sub_proxy, namespace=sub_namespace)
        print(f"Dynamic Mounted proxy: {sub_namespace} -> {sub_url}")

    return "Dynamic subservers mounted"


for namespace, url in subservers.items():
    proxy = FastMCPProxy(
        client_factory=make_client_factory(url),
        name=namespace,
        auth=None  # or a per-subserver auth strategy
    )
    mcp_app.mount(proxy, namespace=namespace)
    print(f"Mounted proxy: {namespace} -> {url}")


class NotificationBroadcastRegistrationMiddleware(Middleware):
    async def on_list_tools(self, context: MiddlewareContext, call_next):

        session_manager.register(context.fastmcp_context.session)

        tools = await call_next(context)
        return tools




mcp_app.add_middleware(OTELTracerMiddleware())
mcp_app.add_middleware(NotificationBroadcastRegistrationMiddleware())
mcp_app.add_middleware(TimingMiddleware())
mcp_app.add_middleware(LoggingMiddleware())
mcp_app.add_middleware(StructuredLoggingMiddleware())

mcp_http_app = mcp_app.http_app(path="/base-mcp-gateway", )

# mcp_app.add_middleware(ForwardAuthTokenMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:mcp_http_app", host="0.0.0.0", port=8090, log_level="info", reload=False)
