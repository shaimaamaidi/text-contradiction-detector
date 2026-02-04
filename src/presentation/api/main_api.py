"""
Module: main_api
Description:
    FastAPI application exposing endpoints for text analysis and contradiction detection.
    Provides:
        - POST /analyze: Analyze sentences, classify them, and detect contradictions.
        - GET /health: Health check endpoint.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse
from src.domain.exceptions.app_exception import AppException
from src.insfrastructure.di.container import Container
from src.insfrastructure.handlers.exception_handler import FastAPIExceptionHandler

# === FASTAPI INITIALIZATION ===
app = FastAPI(title="Text Contradiction API")

# === INIT AGENTS AND SERVICES AND APP CONFIGURATION ===
container = Container()

# Enable CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=container.app_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handlers
app.add_exception_handler(AppException, FastAPIExceptionHandler.handle_app_exception)
app.add_exception_handler(RequestValidationError, FastAPIExceptionHandler.handle_validation_exception)
app.add_exception_handler(Exception, FastAPIExceptionHandler.handle_generic_exception)


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
        raise AppException("The list of sentences is empty.", code="EMPTY_TEXT")

    return container.analyze_text_use_case.execute(request)


# === HEALTH CHECK ENDPOINT ===
@app.get("/health")
async def health():
    """
    Health check endpoint.

    Returns:
        dict: {"status": "ok"} if service is running.
    """
    return {"status": "ok"}
