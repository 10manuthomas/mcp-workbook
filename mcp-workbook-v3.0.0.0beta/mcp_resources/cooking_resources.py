from fastmcp import Context
from fastmcp.resources import resource


class CookingResources:

    @resource(uri="cooking://knife-skills",
              name="KnifeSkills", tags={"v1"})
    async def get_knife_skills_resource(self,ctx:Context) -> str:
        await ctx.info(f"Processing: Reading knife skills resource")
        file_path = 'mcp_resources/resource_files/knife-skills.md'
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        return markdown_text
