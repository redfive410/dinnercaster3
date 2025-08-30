from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from mcp.server.fastmcp import FastMCP
import json

app = FastAPI(
    title="Dinnercaster3",
    description="Dinnercaster3 with MCP Server"
)

# Initialize MCP Server
mcp = FastMCP("dinnercaster3")

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dinnercaster3</title>
    </head>
    <body>
        <main>
            <div>Dinnercaster3</div>
        </main>
    </body>
    </html>
    """

# MCP Server Tools
@mcp.tool()
def echo(text: str) -> str:
    """Echo back the input text"""
    return f"Echo: {text}"

@mcp.tool()
def get_info() -> dict:
    """Get information about the Dinnercaster3 service"""
    return {
        "service": "Dinnercaster3",
        "description": "A FastAPI application with MCP server capabilities",
        "version": "1.0.0"
    }

# API Endpoints for FastAPI
@app.post("/echo")
async def api_echo(data: dict):
    """FastAPI echo endpoint"""
    text = data.get("text", "")
    return {"echo": text}

@app.get("/info")
async def api_info():
    """FastAPI info endpoint"""
    return {
        "service": "Dinnercaster3",
        "description": "A FastAPI application with MCP server capabilities",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/mcp-info")
async def mcp_info():
    """Provide information about the MCP server"""
    return {
        "mcp_server": "dinnercaster3",
        "version": "1.0.0",
        "available_tools": ["echo", "get_info"],
        "description": "MCP server with FastAPI web interface"
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        # Run as MCP server
        mcp.run()
    else:
        # Run as FastAPI server
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)