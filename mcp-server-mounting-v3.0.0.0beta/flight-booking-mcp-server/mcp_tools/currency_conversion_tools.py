from fastmcp import Context
from fastmcp.server.dependencies import get_http_headers
from fastmcp.tools import tool

from schemas.currency_conversion_schemas import CurrencyConversionRequest, CurrencyConversionResponse
from utils.custom_authorization import is_authorized


class CurrencyConversionTools:

    @tool(
        name="CurrencyConversionTool",
        description="A tool to convert one currency to another.",
        tags={"v1"},
        auth=is_authorized("mcp.server.access.role")
    )
    async def currency_conversion_tool(self, currency_conversion_request: CurrencyConversionRequest,
                                       ctx: Context) -> CurrencyConversionResponse:
        await ctx.info(f"Processing: Currency Conversion Tool!!!!")
        access_tk = await ctx.get_state("access_token")
        print("access_tk:::", access_tk)
        headers = get_http_headers()
        print("headers::", headers)
        return CurrencyConversionResponse(converted_value=100.0, input=currency_conversion_request)
