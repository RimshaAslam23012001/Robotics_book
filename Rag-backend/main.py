from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chapter, translation, chat, auth

app = FastAPI(
    title="Chapter Urdu Translation API",
    description="API for translating book chapters to Urdu based on user authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chapter.router, prefix="/api", tags=["chapter"])
app.include_router(translation.router, prefix="/api", tags=["translation"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(auth.router)  # Auth router has its own prefix

@app.get("/")
def read_root():
    return {"message": "Chapter Urdu Translation API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}