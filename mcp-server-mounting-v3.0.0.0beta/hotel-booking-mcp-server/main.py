import uvicorn
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.middleware import AuthMiddleware

from mcp_prompts.base_prompt_register import auto_prompt_register
from mcp_resources.base_resource_register import auto_resource_register
from mcp_tools.base_tool_register import auto_tool_register
from utils.custom_authorization import is_authorized


mcp = FastMCP("Hotel Booking MCP Server", mask_error_details=True,
                middleware=[AuthMiddleware(is_authorized("mcp.server.access.role"))],)

# Register all mcp_tools
auto_tool_register(mcp)

# Register all mcp_resources
auto_resource_register(mcp)

# Register all mcp_prompts
auto_prompt_register(mcp)

mcp_app = mcp.http_app(path="/hotel-booking-mcp")

if __name__ == "__main__":
    uvicorn.run("main:mcp_app", host="0.0.0.0", port=8092, log_level="info", reload=True)
