from mcp_resources.cooking_resources import CookingResources

all_resource_cls = [
    CookingResources,
]


def auto_resource_register(mcp):
    for cls in all_resource_cls:
        instance = cls()

        # Look through all attributes of the created instance
        for name in dir(instance):
            attr = getattr(instance, name)

            # 1. Skip built-in attributes
            if name.startswith("__"):
                continue

            # 2. Check for the FastMCP resources
            if name.endswith("_resource"):
                mcp.add_resource(attr)
                print(f"Registered resource: {name} from {cls.__name__}")
