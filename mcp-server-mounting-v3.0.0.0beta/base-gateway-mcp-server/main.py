import uvicorn
from fastmcp import FastMCP, Context, Client
from fastmcp.client import StreamableHttpTransport
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.middleware import MiddlewareContext, Middleware
from fastmcp.server.providers import ProxyProvider
from fastmcp.server.providers.proxy import FastMCPProxy
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# The AzureProvider handles Azure's token format and validation
auth_provider = AzureProvider(
    client_id="",  # Your Azure App Client ID
    client_secret="",  # Your Azure App Client Secret
    tenant_id="",  # Your Azure Tenant ID (REQUIRED)
    base_url="http://localhost:8090",  # Must match your App registration
    required_scopes=["mcp.tool.access"],  # At least one scope REQUIRED - name of scope from your App
    # identifier_uri defaults to api://{client_id}
    identifier_uri="",
    # Optional: request additional upstream scopes in the authorize request
    additional_authorize_scopes=["User.Read", "offline_access", "openid", "email"],
    redirect_path="/auth/callback"  # Default value, customize if needed
    # base_authority="login.microsoftonline.us"      # For Azure Government (default: login.microsoftonline.com)
)

mcp = FastMCP("Base Gateway MCP Server", mask_error_details=True,
              auth=auth_provider, )

from fastmcp.server.dependencies import get_access_token, get_http_request


@mcp.tool
async def base_server_get_user_info(ctx: Context) -> dict:
    token = get_access_token()
    if token is None:
        return {"authenticated": False}

    access_tk = await ctx.get_state("access_token")
    print("access_tk:::", access_tk)

    return {"authenticated": True, "user": token.claims}


class ForwardAuthTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("authorization")
        print("Token from incoming request:", token)
        if token:
            request.state.forwarded_token = token
        return await call_next(request)

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
    "hotel-booking": "http://localhost:8092/hotel-booking-mcp",
}

for namespace, url in subservers.items():
    proxy = FastMCPProxy(
        client_factory=make_client_factory(url),
        name=namespace,
        auth=None  # or a per-subserver auth strategy
    )
    mcp.mount(proxy, namespace=namespace)
    print(f"Mounted proxy: {namespace} -> {url}")


mcp_app = mcp.http_app(path="/base-mcp",)

if __name__ == "__main__":
    uvicorn.run("main:mcp_app", host="0.0.0.0", port=8090, log_level="info", reload=True)
