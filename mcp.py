from fastapi import APIRouter

def tool(name):
    def decorator(func):
        func._tool_name = name
        return func
    return decorator

class MCPServer:
    def __init__(self, app):
        self.app = app
        self.router = APIRouter()

    def include_tool(self, func):
        endpoint = f"/mcp/{func._tool_name}"
        self.router.post(endpoint)(func)
        self.app.include_router(self.router)
