"""
Module containing the Container class.
Responsible for initializing and wiring together all RAG application components,
following hexagonal architecture principles.
"""
from src.application.use_cases.analyse_text_use_case import AnalyzeTextUseCase
from src.domain.services.text_analysis_service import TextAnalysisService
from src.insfrastructure.agents.contradiction_detector_agent import ContradictionDetector
from src.insfrastructure.agents.sentence_classifier_agent import SentenceClassifier
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class PromptProvider:
    pass


class Container:

    def __init__(self):
        self.azure_settings =AzureOpenAISettings()
        self.prompt_provider = PromptyLoader()
        self.classifier_agent = SentenceClassifier(self.azure_settings, self.prompt_provider)
        self.detector_agent = ContradictionDetector(self.azure_settings, self.prompt_provider)
        self.text_analysis_service = TextAnalysisService(self.classifier_agent, self.detector_agent)
        self.analyze_text_use_case = AnalyzeTextUseCase(self.text_analysis_service)
