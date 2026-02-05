from fastmcp import Context
from fastmcp.tools import tool

from schemas.hotel_tool_schemas import HotelSuggestionRequest, WhatAndWhereToEatRequest


class HotelTools:

    @tool(
        name="HotelSuggestions",
        tags={"v1"}
    )
    async def get_hotel_suggestions_tool(self, hotel_suggestion_request: HotelSuggestionRequest,
                                         ctx: Context) -> str:
        """Generate Hotel suggestions with the provided content."""
        result = await ctx.elicit("Hey, To complete this operation,"
                                  " I will need to use external Hotel API .. Do you Approve this action?",
                                  response_type=None)
        if result.action == "accept":
            print("Accepted")
        elif result.action == "decline":
            print("Rejected")
            raise ValueError("Action decline")
        elif result.action == "cancel":
            print("User canceled the operation")
            # raise ValueError("Action cancel")
        return f"Oh So you can stay at the Grand Hotel in {hotel_suggestion_request.location} "

    @tool(
        name="WhatAndWhereToEatIdeas",
        tags={"v1"}
    )
    async def get_what_and_where_to_eat_ideas_tool(self, what_and_where_to_eat_request: WhatAndWhereToEatRequest,
                                                   ctx: Context) -> str:
        """Get what and where to eat ideas with the provided content, to make the most of your travel."""
        result = await ctx.elicit("Hey, To complete this operation,"
                                  " I will need to use your LLM .. Do you Approve this action?",
                                  response_type=None)
        if result.action == "accept":
            print("Accepted")
        elif result.action == "decline":
            print("Rejected")
            raise ValueError("Action decline")
        elif result.action == "cancel":
            print("User canceled the operation")
            # raise ValueError("Action cancel")

        result = await ctx.sample(f"Please generate a what and where to eat "
                                  f"suggestion for a trip to {what_and_where_to_eat_request.place_of_visit} ")
        return (f"Here is your amazing what and where to eat idea, "
                f" this will help you make the most of your travel :: {result.text}")
