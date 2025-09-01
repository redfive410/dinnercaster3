# Deploy FastAPI to Google Cloud Run

This is a FastAPI template which can be deployed to [Google Cloud Run](https://cloud.google.com/run/docs).

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

3. Open [http://localhost:8000](http://localhost:8000) to view the application.
4. API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Deploying to Google Cloud Run

This template can be used to deploy your FastAPI application as a Docker container.

1. Deploy to Cloud Run: `gcloud run deploy dinnercaster3 --source=. --allow-unauthenticated --region=us-west1`.

## Learn More

To learn more about FastAPI, take a look at the following resources:

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - learn about FastAPI features and API.
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - an interactive FastAPI tutorial.

You can check out [the FastAPI GitHub repository](https://github.com/tiangolo/fastapi) - your feedback and contributions are welcome!

## Use MCP servers in Claude Desktop
```
{
    "mcpServers": {
      "weather": {
        "command": "HARDCODED_PATH_HERE/uv",
        "args": ["--directory", "HARDCODED_PATH_HERE/weather-server-python", "run", "weather.py"]
      },
      "dinnercaster3-npx": {
        "command": "npx",
        "args": [
          "-y",
          "mcp-remote",
          "https://dinnercaster3-mcp-000000000000.us-west1.run.app/mcp"
        ]
      }
    }
  }
```
