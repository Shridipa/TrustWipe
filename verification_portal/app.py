from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import route modules
from routes.home import router as home_router
from routes.verify import router as verify_router

app = FastAPI(title="Trustwipe Verification Portal")

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Register route blueprints
app.include_router(home_router)
app.include_router(verify_router)

# Optional: Template engine setup (if needed globally)
templates = Jinja2Templates(directory="templates")

# Optional: Root health check or metadata
@app.get("/health")
def health_check():
    return {"status": "ok", "app": "Trustwipe Verification Portal"}