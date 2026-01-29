import dill as pickle

from deepdiff import DeepDiff
from fastmcp import Context
from fastmcp.prompts import prompt
from fastmcp.server.dependencies import get_context

from schemas.cooking_prompt_schemas import CookingPromptUserDataRequest


class CookingPrompts:

    # def serialize_ctx(self,ide:str):
    #     ctx = get_context()
    #     # Pickling to a file
    #     with open(f'{ide}.pkl', 'wb') as f:
    #         pickle.dump(ctx, f)
    #
    #     if ide =="vscode":
    #         with open('pycharm.pkl', 'rb') as f:
    #             loaded_v1 = pickle.load(f)
    #
    #         with open('vscode.pkl', 'rb') as f:
    #             loaded_v2 = pickle.load(f)
    #
    #         diff = DeepDiff(loaded_v1, loaded_v2)
    #         print("Differences found:")
    #         import pprint
    #         pprint.pprint(diff, indent=2)

    @prompt(name="TellMeCookingJokes", tags={"v1"})
    async def tell_me_cooking_joke_prompt(self, user_name: str, ctx: Context) -> str:

        # self.serialize_ctx("pycharm")

        result = await ctx.elicit(f"Hi {user_name}... Well I will need your details so, "
                                  f"do you approve this operation ?",
                                  response_type=None)

        if result.action == "accept":
            pass
        else:
            raise ValueError("Action rejected")

        """Collect user information through interactive prompts."""
        result = await ctx.elicit(
            message="Please provide your information",
            response_type=CookingPromptUserDataRequest
        )

        if result.action == "accept":
            user_data = result.data
            return (f"Hey {user_data.first_name} of {user_data.country},"
                    f" Cooking is fun and its a Joke, I wish I could cook any food, "
                    f"eat any thing as much as I want and stay healthy !!!")
        elif result.action == "decline":
            return "Information not provided"
        else:  # cancel
            return "Operation cancelled"
