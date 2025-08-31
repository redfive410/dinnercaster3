from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP
import json

app = FastAPI(
    title="Dinnercaster3",
    description="Dinnercaster3 with MCP Server"
)

# Add CORS middleware for web browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://claude.ai", "https://*.claude.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/mcp")
async def mcp_endpoint():
    """MCP server endpoint for claude.ai"""
    return {
        "mcp_server": "dinnercaster3",
        "status": "available",
        "endpoints": {
            "echo": "/echo",
            "info": "/info",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import sys
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))

    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        # Run as MCP server (stdio) - for Claude Desktop
        mcp.run()
    else:
        # Run FastAPI app for Cloud Run
        uvicorn.run(app, host="0.0.0.0", port=port)