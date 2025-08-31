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

@app.post("/mcp")
async def mcp_post_endpoint(request: dict):
    """Handle MCP protocol requests"""
    try:
        # Handle different MCP request types
        method = request.get("method")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "dinnercaster3",
                        "version": "1.0.0"
                    }
                },
                "id": request.get("id", 1)
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "result": {
                    "tools": [
                        {
                            "name": "echo",
                            "description": "Echo back the input text",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string"}
                                },
                                "required": ["text"]
                            }
                        },
                        {
                            "name": "get_info",
                            "description": "Get information about the Dinnercaster3 service",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                },
                "id": request.get("id", 1)
            }
        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            arguments = request.get("params", {}).get("arguments", {})

            if tool_name == "echo":
                result = echo(arguments.get("text", ""))
            elif tool_name == "get_info":
                result = get_info()
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": "Method not found"
                    },
                    "id": request.get("id", 1)
                }

            return {
                "jsonrpc": "2.0",
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result)
                        }
                    ]
                },
                "id": request.get("id", 1)
            }
        else:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Method not found"
                },
                "id": request.get("id", 1)
            }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            },
            "id": request.get("id", 1)
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