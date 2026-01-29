from fastmcp import Context
from fastmcp.server.dependencies import get_access_token
from fastmcp.tools import tool

from schemas.unit_conversion_schemas import UnitConversionRequest, UnitConversionResponse
from utils.custom_authorization import is_authorized


class UnitConversionTools:

    @tool(
        name="UnitConversionTool",
        description="A tool to convert units from one measurement to another.",
        tags={"v1"},
        auth=is_authorized("mcp.server.access.role.admin")
    )
    async def unit_conversion_tool(self, unit_conversion_request: UnitConversionRequest, ctx:Context) -> UnitConversionResponse:
        await ctx.info(f"Processing: Unit Conversion Tool!!!!")
        token = get_access_token()
        print("token:::",token)
        print({
            "client_id": token.client_id,
            "scopes": token.scopes,
            "claims": token.claims,
        })
        return UnitConversionResponse(converted_value=12.0, input=unit_conversion_request)

