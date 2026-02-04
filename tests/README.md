# Tests - text-contradiction-detector

## Statistiques des tests

- **Total Tests**: 76
- **Tests Unitaires**: 63
- **Tests d'Intégration**: 13

## Structure des tests

La suite de tests est organisée en deux catégories principales :

### Tests unitaires (`tests/unit/`)
- `test_analyse_text_use_case.py` - Tests du use case d'analyse de texte (6 tests)
- `test_text_analysis_service.py` - Tests du service d'analyse (7 tests)
- `test_sentence_classifier_agent.py` - Tests de l'agent de classification (8 tests)
- `test_contradiction_detector_agent.py` - Tests de l'agent de détection de contradictions (9 tests)
- `test_contradiction_llm_response.py` - Tests des réponses LLM (10 tests)
- `test_dtos.py` - Tests des Data Transfer Objects (9 tests)
- `test_settings.py` - Tests de la configuration (10 tests : 7 initiaux + 3 tests CORS)

**Total tests unitaires: 63**

### Tests d'intégration (`tests/integration/`)
- `test_main_api.py` - Tests de l'API principales (13 tests : 10 initiaux + 3 tests exceptions/CORS)

**Total tests d'intégration: 13**

## Fixtures disponibles

Le fichier `conftest.py` fournit les fixtures réutilisables suivantes :

### Données de test
- `sample_sentences` - Liste de 10 phrases en arabe avec recommandations et avis
- `analysis_request_data` - Requête d'analyse avec les phrases de test
- `sample_single_sentence` - Une phrase unique
- `contradictory_sentences` - Paire de phrases contradictoires
- `non_contradictory_sentences` - Paire de phrases compatibles
- `empty_sentences` - Liste vide pour les cas limites

## Exécution des tests

### Exécuter tous les tests
```bash
pytest tests/
```

### Exécuter les tests unitaires uniquement
```bash
pytest tests/unit/
```

### Exécuter les tests d'intégration uniquement
```bash
pytest tests/integration/
```

### Exécuter un fichier de test spécifique
```bash
pytest tests/unit/test_analyse_text_use_case.py
```

### Exécuter un test spécifique
```bash
pytest tests/unit/test_analyse_text_use_case.py::TestAnalyseTextUseCase::test_execute_with_valid_sentences
```

### Exécuter avec couverture de code
```bash
pytest tests/ --cov=src --cov-report=html
```

### Exécuter les tests en mode verbose
```bash
pytest tests/ -v
```

## Couverture des tests

Les tests couvrent les domaines suivants :

1. **Use Cases** - Logique métier principale d'analyse de texte (6 tests)
2. **Services** - Services de domaine et orchestration (7 tests)
3. **Agents** - Agents IA pour classification et détection (17 tests)
4. **LLM Response** - Mapping et traitement des réponses LLM (10 tests)
5. **DTOs** - Sérialisation et désérialisation des données (9 tests)
6. **Configuration** - Paramètres et configuration de l'application avec CORS (10 tests)
7. **API** - Points de terminaison HTTP et intégration + exception handling (13 tests)

## Notes

- Les tests utilisent des mocks et des fixtures pour isoler les composants
- Les données de test utilisent des phrases en arabe réelles avec des recommandations et avis
- Les tests sont conçus pour être exécutés rapidement et indépendamment
- La configuration pytest est définie dans `pytest.ini`
