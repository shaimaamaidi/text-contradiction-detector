# Tests - text-contradiction-detector

## Structure des tests

La suite de tests est organisée en deux catégories principales :

### Tests unitaires (`tests/unit/`)
- `test_analyse_text_use_case.py` - Tests du use case d'analyse de texte
- `test_text_analysis_service.py` - Tests du service d'analyse
- `test_sentence_classifier_agent.py` - Tests de l'agent de classification
- `test_contradiction_detector_agent.py` - Tests de l'agent de détection de contradictions
- `test_dtos.py` - Tests des Data Transfer Objects
- `test_settings.py` - Tests de la configuration

### Tests d'intégration (`tests/integration/`)
- `test_main_api.py` - Tests de l'API principales

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

1. **Use Cases** - Logique métier principale d'analyse de texte
2. **Services** - Services de domaine et orchestration
3. **Agents** - Agents IA pour classification et détection
4. **DTOs** - Sérialisation et désérialisation des données
5. **Configuration** - Paramètres et configuration de l'application
6. **API** - Points de terminaison HTTP et intégration

## Notes

- Les tests utilisent des mocks et des fixtures pour isoler les composants
- Les données de test utilisent des phrases en arabe réelles avec des recommandations et avis
- Les tests sont conçus pour être exécutés rapidement et indépendamment
- La configuration pytest est définie dans `pytest.ini`
