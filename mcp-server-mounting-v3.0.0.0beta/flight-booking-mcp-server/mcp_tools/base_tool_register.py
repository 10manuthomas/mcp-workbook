from mcp_tools.currency_conversion_tools import CurrencyConversionTools
from mcp_tools.flight_tools import FlightTools
from mcp_tools.user_info_tools import UserInfoTools

all_tool_cls = [
    CurrencyConversionTools,
    UserInfoTools,
    FlightTools
]


def auto_tool_register(mcp):
    for cls in all_tool_cls:
        instance = cls()

        # Look through all attributes of the created instance
        for name in dir(instance):
            attr = getattr(instance, name)

            # 1. Skip built-in attributes
            if name.startswith("__"):
                continue

            # 2. Check for the FastMCP tool marker
            if name.endswith("_tool"):
                mcp.add_tool(attr)
                print(f"Registered tool: {name} from {cls.__name__}")
