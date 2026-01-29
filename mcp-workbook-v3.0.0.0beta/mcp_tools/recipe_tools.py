from fastmcp import Context
from fastmcp.tools import tool

from schemas.recipe_schemas import RecipeSuggestionRequest


class RecipeTools:

    @tool(
        name="RecipeSuggestions",
        tags={"v1"}
    )
    async def get_recipe_suggestions_tool(self, recipe_suggestion_request: RecipeSuggestionRequest,
                                          ctx: Context) -> str:
        """Generate a recipe suggestion with the provided content."""
        all_ingredients = ','.join(recipe_suggestion_request.ingredients)
        result = await ctx.elicit("Hey .. I will need to use your LLM .. Do you Approve this action?",
                                  response_type=None)
        if result.action == "accept":
            print("Accepted")
        elif result.action == "decline":
            print("Rejected")
            raise ValueError("Action decline")
        elif result.action == "cancel":
            print("User canceled the operation")
            # raise ValueError("Action cancel")
        result = await ctx.sample(f"Please generate a recipe suggestion using these ingredients:\n\n{all_ingredients}")
        return f"Drum Roll !!! So you can make :: {result.text}"
