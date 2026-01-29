import uvicorn
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider

from mcp_prompts.base_prompt_register import auto_prompt_register
from mcp_resources.base_resource_register import auto_resource_register
from mcp_tools.base_tool_register import auto_tool_register


# The AzureProvider handles Azure's token format and validation
auth_provider = AzureProvider(
    client_id="",  # Your Azure App Client ID
    client_secret="",                 # Your Azure App Client Secret
    tenant_id="", # Your Azure Tenant ID (REQUIRED)
    base_url="http://localhost:8090",                   # Must match your App registration
    required_scopes=["mcp.tool.access"],                 # At least one scope REQUIRED - name of scope from your App
    # identifier_uri defaults to api://{client_id}
     identifier_uri="",
    # Optional: request additional upstream scopes in the authorize request
     additional_authorize_scopes=["User.Read", "offline_access", "openid", "email"],
     redirect_path="/auth/callback"                  # Default value, customize if needed
    # base_authority="login.microsoftonline.us"      # For Azure Government (default: login.microsoftonline.com)
)

mcp = FastMCP("Recipe MCP Server", mask_error_details=True, auth=auth_provider)


# Register all mcp_tools
auto_tool_register(mcp)

# Register all mcp_resources
auto_resource_register(mcp)

# Register all mcp_prompts
auto_prompt_register(mcp)

mcp_app = mcp.http_app(path="/mcp-workbook-server")
# mcp_app = mcp.http_app()

if __name__ == "__main__":
    uvicorn.run("main:mcp_app", host="0.0.0.0", port=8090, log_level="info", reload=True)
