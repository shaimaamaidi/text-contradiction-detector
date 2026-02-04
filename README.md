# AI Text Analysis and Contradiction Detection System

A sophisticated AI-powered system for analyzing Arabic text, classifying recommendations, and detecting contradictions between statements using Azure OpenAI and clean architecture principles.

## Overview

This application processes Arabic text documents containing recommendations and opinions, performing:
- **Sentence Classification**: Categorizes each sentence as support, reject, or neutral
- **Contradiction Detection**: Identifies contradictory statements within the analyzed text
- **RESTful API**: Exposes analysis capabilities through FastAPI endpoints

## Architecture

The project follows **Clean Architecture** principles with clear separation of concerns:

```
src/
├── application/          # Use Cases & DTOs
│   ├── dto/             # Data Transfer Objects
│   └── use_cases/       # Application business logic
├── domain/              # Domain Models & Business Logic
│   ├── models/          # Domain entities
│   ├── services/        # Domain services
│   └── ports/           # Interfaces (Input/Output ports)
├── insfrastructure/     # Infrastructure & External Services
│   ├── agents/          # LLM agents (Classifier, Detector)
│   ├── config/          # Configuration management
│   ├── di/              # Dependency injection
│   └── prompts/         # Prompt templates and loaders
└── presentation/        # API Layer
    └── api/             # FastAPI application & endpoints
```

## Key Components

### 1. **Sentence Classifier Agent**
Classifies Arabic sentences using Azure OpenAI:
- Analyzes sentiment and recommendations
- Outputs: Support, Reject, or Neutral
- Uses `.prompty` templates for consistency

### 2. **Contradiction Detector Agent**
Detects logical contradictions:
- Compares classified sentences within categories
- Identifies conflicting recommendations
- Provides explanations for detected contradictions

### 3. **Text Analysis Service**
Orchestrates analysis workflow:
- Calls classifier agent for each sentence
- Runs contradiction detection
- Aggregates results into response

### 4. **FastAPI Application**
RESTful API with endpoints:
- `POST /analyze` - Analyze text and detect contradictions
- `GET /health` - Health check endpoint

## Installation

### Prerequisites
- Python 3.10+
- Azure OpenAI API credentials
- Virtual environment

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd text-contradiction-detector
```

2. **Create virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
AZURE_OPENAI_ENDPOINT=https://<your-instance>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=<your-api-version>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-model>
```

## Usage

### Running the API Server

```bash
python src/presentation/api/main_api.py
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### API Endpoints

#### Analyze Text
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "sentences": [
      "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري",
      "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة"
    ]
  }'
```

#### Response Format
```json
{
  "categories": [
    {
      "category_name": "إدارة المشاريع",
      "statements": [
        "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري، حيث أن المشروع جاهز من الناحية الفنية، وتأخير القرار قد يؤدي إلى خسارة فرص استراتيجية مهمة.",
        "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة الإجمالية والمخاطر التشغيلية، وأقترح إعادة الدراسة قبل اتخاذ أي قرار.",
        "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود لمدة 3 أشهر لقياس الأثر قبل التوسع الكامل.",
        "أؤيد الموافقة على المقترح ولكن أرى أن تكون مدة التجربة سنة كاملة لضمان الحصول على نتائج دقيقة وشاملة."
      ],
      "contradictions": [
        {
          "statements": [
            "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري، حيث أن المشروع جاهز من الناحية الفنية، وتأخير القرار قد يؤدي إلى خسارة فرص استراتيجية مهمة.",
            "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة الإجمالية والمخاطر التشغيلية، وأقترح إعادة الدراسة قبل اتخاذ أي قرار."
          ],
          "severity": "حاد",
          "comment": "الإفادة 1 توصي بالبدء الفوري في التنفيذ، بينما الإفادة 2 تقترح رفض المقترح وإعادة الدراسة، مما يشير إلى تعارض جذري في التوصيات."
        },
        {
          "statements": [
            "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري، حيث أن المشروع جاهز من الناحية الفنية، وتأخير القرار قد يؤدي إلى خسارة فرص استراتيجية مهمة.",
            "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود لمدة 3 أشهر لقياس الأثر قبل التوسع الكامل."
          ],
          "severity": "متوسط",
          "comment": "الإفادة 1 توصي بالتنفيذ الفوري الكامل، بينما الإفادة 3 تقترح تطبيقًا محدودًا لمدة 3 أشهر، مما يعكس اختلافًا في نطاق التنفيذ."
        }
      ]
    },
    {
      "category_name": "الطاقة",
      "statements": [
        "أوصي بالاستثمار في الطاقة الشمسية لتقليل التكاليف وزيادة الاستدامة.",
        "أرى أن التركيز على الوقود الأحفوري أكثر أمانًا وموثوقية لتلبية احتياجات الطاقة الحالية."
      ],
      "contradictions": [
        {
          "statements": [
            "أوصي بالاستثمار في الطاقة الشمسية لتقليل التكاليف وزيادة الاستدامة.",
            "أرى أن التركيز على الوقود الأحفوري أكثر أمانًا وموثوقية لتلبية احتياجات الطاقة الحالية."
          ],
          "severity": "حاد",
          "comment": "الإفادة 1 تدعو للاستثمار في الطاقة الشمسية كوسيلة مستدامة، بينما الإفادة 2 تفضل الوقود الأحفوري كخيار أكثر أمانًا، مما يعكس تناقضًا في التوجهات."
        }
      ]
    }
  ]
}
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
```

### Test Structure

```
tests/
├── conftest.py                          # Shared fixtures
├── unit/                                # Unit tests
│   ├── test_analyse_text_use_case.py
│   ├── test_text_analysis_service.py
│   ├── test_sentence_classifier_agent.py
│   ├── test_contradiction_detector_agent.py
│   ├── test_dtos.py
│   └── test_settings.py
└── integration/
    └── test_main_api.py
```

### Test Statistics
- **Total Tests**: 76
- **Unit Tests**: 63
- **Integration Tests**: 13

### Test Fixtures

Shared fixtures in `conftest.py`:
- `sample_sentences` - 10 Arabic test sentences
- `sample_single_sentence` - Single test sentence
- `contradictory_sentences` - Contradictory pairs
- `non_contradictory_sentences` - Compatible sentences
- `empty_sentences` - Edge case fixture
- `analysis_request_data` - Formatted request data

## Dependencies

### Core Dependencies
```
fastapi          # Web framework
uvicorn          # ASGI server
pydantic         # Data validation
openai           # Azure OpenAI client
python-dotenv    # Environment configuration
pyyaml           # YAML parsing
jinja2           # Template engine
```

### Testing Dependencies
```
pytest           # Testing framework
pytest-cov       # Coverage reporting
pytest-asyncio   # Async test support
pytest-mock      # Mocking utilities
```

## Configuration

### Application Settings

Located in `src/insfrastructure/config/app_settings.py`:

```python
class AppSettings:
    cors_origins: list         # CORS allowed origins (e.g., ["http://localhost:3000"])
    endpoint: str              # Azure OpenAI endpoint URL
    api_key: str               # API authentication key
    api_version: str           # API version (e.g., "2024-08-01-preview")
    model: str                 # Deployment name (e.g., "gpt-4o")
```

**Environment Variables:**
```env
CORS_ORIGINS=<your-cors-1>,<your-cors-2>
AZURE_OPENAI_ENDPOINT=https://<your-instance>.openai.azure.com/
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_API_VERSION=<your-api-version>
AZURE_OPENAI_DEPLOYMENT_NAME=<your-deployment-model>
```

### Prompt Templates

Located in `src/insfrastructure/prompts/templates/`:

- `prompt_classification.prompty` - Sentence classification prompt
- `prompt_contradiction.prompty` - Contradiction detection prompt

## Project Structure Details

### DTOs (Data Transfer Objects)
- `AnalysisRequest` - Input for text analysis
- `AnalysisResponse` - Output with classifications and contradictions

### Domain Models
- `ClassificationResult` - Classification output
- `Category` - Support/Reject/Neutral enum
- `ContradictionResult` - Contradiction details
- `ClassificationLLMResponse` - LLM response mapping
- `ContradictionLLMResponse` - LLM response mapping

### Ports (Interfaces)
- `ClassifierAgentPort` - Sentence classification interface
- `DetectorAgentPort` - Contradiction detection interface
- `PromptProviderPort` - Prompt template interface
- `AnalyzeTextPort` - Text analysis interface

## Development Workflow

### Code Style & Quality

Follow these principles:
- Clean Architecture with clear separation of concerns
- Dependency Injection for testability
- Comprehensive unit and integration tests
- Type hints for all functions
- Docstrings in English for all modules

## Docker Support

### Docker Compose

```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## Git Workflow

### Branch Strategy
- `master` - Production-ready code
- `dev` - Development branch

## Project Status

🚀 **Active Development**

- ✅ Core functionality complete
- ✅ Test coverage: 76 tests (63 unit + 13 integration)
- ✅ API endpoints operational

