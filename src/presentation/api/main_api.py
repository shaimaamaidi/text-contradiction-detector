from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse
from src.insfrastructure.di.container import Container

# === INITIALISATION DE FASTAPI ===
app = FastAPI(title="Text Contradiction API")

# Autoriser le CORS si nécessaire
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === INIT AGENTS ET SERVICES ===
container = Container()
# === ENDPOINT POST POUR ANALYSE DE TEXTE ===
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    """
    Analyse un ensemble de phrases :
    - Classification
    - Détection des contradictions
    Retourne la liste des contradictions détectées.
    """
    if not request.sentences:
        raise HTTPException(status_code=400, detail="La liste de phrases est vide.")

    try:
        response: AnalysisResponse = container.analyze_text_use_case.execute(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === ENDPOINT HEALTH CHECK ===
@app.get("/health")
async def health():
    return {"status": "ok"}
