from mcp_prompts.flight_booking_prompts import FlightBookingPrompts

all_prompt_cls = [
    FlightBookingPrompts,
]


def auto_prompt_register(mcp):
    for cls in all_prompt_cls:
        instance = cls()

        # Look through all attributes of the created instance
        for name in dir(instance):
            attr = getattr(instance, name)

            # 1. Skip built-in attributes
            if name.startswith("__"):
                continue

            # 2. Check for the FastMCP prompts
            if name.endswith("_prompt"):
                mcp.add_prompt(attr)
                print(f"Registered prompt: {name} from {cls.__name__}")
