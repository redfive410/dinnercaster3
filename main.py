from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

# Constants
SERVICE_NAME = "dinnercaster3"
SERVICE_VERSION = "1.0.0"
SERVICE_DESCRIPTION = "A FastAPI application with MCP server capabilities"
PROTOCOL_VERSION = "2024-11-05"

SERVICE_INFO = {
    "service": "Dinnercaster3",
    "description": SERVICE_DESCRIPTION,
    "version": SERVICE_VERSION
}

MCP_SERVER_INFO = {
    "name": SERVICE_NAME,
    "version": SERVICE_VERSION
}

TOOL_DEFINITIONS = [
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
mcp = FastMCP(SERVICE_NAME)

# Helper functions for MCP responses
def create_mcp_response(result, request_id=1):
    """Create a standard MCP response"""
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }

def create_mcp_error(code, message, request_id=1):
    """Create a standard MCP error response"""
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": request_id
    }

def get_capabilities():
    """Get MCP server capabilities"""
    return {
        "protocolVersion": PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": MCP_SERVER_INFO
    }

def handle_initialize(request_id):
    """Handle MCP initialize request"""
    return create_mcp_response(get_capabilities(), request_id)

def handle_tools_list(request_id):
    """Handle MCP tools/list request"""
    result = {"tools": TOOL_DEFINITIONS}
    return create_mcp_response(result, request_id)

def handle_tools_call(tool_name, arguments, request_id):
    """Handle MCP tools/call request"""
    if tool_name == "echo":
        result = echo(arguments.get("text", ""))
    elif tool_name == "get_info":
        result = get_info()
    else:
        return create_mcp_error(-32601, "Method not found", request_id)
    
    return create_mcp_response({
        "content": [{"type": "text", "text": str(result)}]
    }, request_id)

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
    return SERVICE_INFO

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/mcp-info")
async def mcp_info():
    """Provide information about the MCP server"""
    return {
        "mcp_server": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "available_tools": [tool["name"] for tool in TOOL_DEFINITIONS],
        "description": "MCP server with FastAPI web interface"
    }

@app.get("/mcp")
async def mcp_get_endpoint():
    """Get MCP server information and capabilities"""
    result = get_capabilities()
    result["available_tools"] = [
        {"name": tool["name"], "description": tool["description"]} 
        for tool in TOOL_DEFINITIONS
    ]
    return create_mcp_response(result)

@app.post("/mcp")
async def mcp_post_endpoint(request: dict):
    """Handle MCP protocol requests"""
    try:
        method = request.get("method")
        request_id = request.get("id", 1)

        if method == "initialize":
            return handle_initialize(request_id)
        elif method == "tools/list":
            return handle_tools_list(request_id)
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            return handle_tools_call(tool_name, arguments, request_id)
        else:
            return create_mcp_error(-32601, "Method not found", request_id)
    except Exception as e:
        return create_mcp_error(-32603, f"Internal error: {str(e)}", request.get("id", 1))

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
