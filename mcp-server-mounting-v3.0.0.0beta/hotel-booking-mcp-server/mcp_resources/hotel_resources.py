from fastmcp import Context
from fastmcp.resources import resource


class HotelResources:

    @resource(uri="hotel://hotel-booking-checklist",
              name="HotelBookingChecklist", tags={"v1"})
    async def get_hotel_booking_checklist_resource(self, ctx: Context) -> str:
        await ctx.info(f"Processing: Hotel Booking Checklist")
        file_path = 'mcp_resources/resource_files/hotel_booking_checklist.md'
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        return markdown_text
