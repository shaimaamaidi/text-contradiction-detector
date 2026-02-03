"""
Module: main_api
Description:
    FastAPI application exposing endpoints for text analysis and contradiction detection.
    Provides:
        - POST /analyze: Analyze sentences, classify them, and detect contradictions.
        - GET /health: Health check endpoint.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse
from src.insfrastructure.di.container import Container

# === FASTAPI INITIALIZATION ===
app = FastAPI(title="Text Contradiction API")

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === INIT AGENTS AND SERVICES ===
container = Container()

# === POST ENDPOINT FOR TEXT ANALYSIS ===
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    """
    Analyze a set of sentences:
        - Classification
        - Contradiction detection
    Returns the list of detected contradictions.

    Args:
        request (AnalysisRequest): Request containing sentences to analyze.

    Returns:
        AnalysisResponse: DTO containing detected contradictions.
    """
    if not request.sentences:
        raise HTTPException(status_code=400, detail="The list of sentences is empty.")

    try:
        response: AnalysisResponse = container.analyze_text_use_case.execute(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === HEALTH CHECK ENDPOINT ===
@app.get("/health")
async def health():
    """
    Health check endpoint.

    Returns:
        dict: {"status": "ok"} if service is running.
    """
    return {"status": "ok"}
