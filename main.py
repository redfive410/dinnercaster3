from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Dinnercaster3",
    description="Dinnercaster3"
)

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

@app.get("/health")
async def health_check():
    return {"status": "healthy"}