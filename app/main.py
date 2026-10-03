from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router


load_dotenv()


app = FastAPI(
    title="DeployGuard AI",
    description="AI-powered deployment risk analyzer.",
    version="0.2.0"
)

app.include_router(router)