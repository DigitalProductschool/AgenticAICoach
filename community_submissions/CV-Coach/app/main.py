from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI()

# Include the upload router
app.include_router(upload_router)
