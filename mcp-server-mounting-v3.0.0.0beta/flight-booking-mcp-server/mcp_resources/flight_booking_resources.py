from fastmcp import Context
from fastmcp.resources import resource


class FlightBookingResources:

    @resource(uri="flight-booking://layover-tips",
              name="LayoverTips", tags={"v1"})
    async def get_layover_tips_resource(self, ctx: Context) -> str:
        await ctx.info(f"Processing: Reading Layover tips resource")
        file_path = 'mcp_resources/resource_files/layover_tips.md'
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        return markdown_text
