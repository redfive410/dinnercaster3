from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="FastAPI on Google Cloud Run",
    description="Deploy your FastAPI application to Google Cloud Run"
)

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI on Google Cloud Run</title>
    </head>
    <body>
        <main>
            <div>FastAPI on Google Cloud Run</div>
        </main>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    return {"status": "healthy"}