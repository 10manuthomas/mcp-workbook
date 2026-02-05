from mcp_tools.hotel_tools import HotelTools
from mcp_tools.time_conversion_tools import TimeConversionTools
from mcp_tools.user_info_tools import UserInfoTools

all_tool_cls = [
    HotelTools,
    UserInfoTools,
    TimeConversionTools
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
