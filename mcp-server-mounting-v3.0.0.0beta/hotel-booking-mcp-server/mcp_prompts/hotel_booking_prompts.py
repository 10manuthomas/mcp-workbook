from fastmcp import Context
from fastmcp.prompts import prompt

from schemas.hotel_prompt_schemas import HotelBookingIdeaPromptRequest


class HotelPrompts:

    @prompt(name="HotelBookingIdeas", tags={"v1"})
    async def get_hotel_booking_idea_prompt(self, user_name: str, ctx: Context) -> str:
        """Prompt to get hotel booking ideas based on user input."""

        result = await ctx.elicit(f"Hi {user_name}... Well I will need your travel details to proceed, "
                                  f"do you approve this operation ?",
                                  response_type=None)

        if result.action == "accept":
            pass
        else:
            raise ValueError("Action rejected")

        """Collect user information through interactive prompts."""
        result = await ctx.elicit(
            message="Please provide your information",
            response_type=HotelBookingIdeaPromptRequest
        )

        if result.action == "accept":
            user_data = result.data
            return (f"I am visiting {user_data.place_of_visit} from {user_data.from_date} "
                    f"till {user_data.to_date} with {user_data.number_of_people} people. "
                    f"Prepare some hotel booking ideas for me !!!")
        elif result.action == "decline":
            return "Information not provided"
        else:  # cancel
            return "Operation cancelled"
