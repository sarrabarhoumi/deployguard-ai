from fastapi        import FastAPI

from app.api.routes import router

app = FastAPI(
    title="DeployGuard AI",
    description="AI-powered deployment risk analyzer.",
    version="0.1.0"
)

app.include_router(router)