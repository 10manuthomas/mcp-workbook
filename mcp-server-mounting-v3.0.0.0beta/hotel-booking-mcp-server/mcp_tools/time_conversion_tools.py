from fastmcp import Context
from fastmcp.tools import tool

from schemas.time_conversion_schemas import TimeConversionRequest, TimeConversionResponse
from utils.custom_authorization import is_authorized


class TimeConversionTools:

    @tool(
        name="TimeConversionTool",
        description="A tool to convert one Timezone to another.",
        tags={"v1"},
        auth=is_authorized("mcp.server.access.role.admin")
    )
    async def time_conversion_tool(self, time_conversion_request: TimeConversionRequest,
                                   ctx: Context) -> TimeConversionResponse:
        await ctx.info(f"Processing: Time Conversion Tool!!!!")
        return TimeConversionResponse(converted_value=14.54, input=time_conversion_request)
