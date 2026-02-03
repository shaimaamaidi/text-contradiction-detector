"""
Module: container
Description:
    Contains the Container class responsible for initializing and wiring together
    all components of the RAG application, following hexagonal architecture principles.
"""

from src.application.use_cases.analyse_text_use_case import AnalyzeTextUseCase
from src.domain.services.text_analysis_service import TextAnalysisService
from src.insfrastructure.agents.contradiction_detector_agent import ContradictionDetector
from src.insfrastructure.agents.sentence_classifier_agent import SentenceClassifier
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class Container:
    """
    Dependency injection container for the RAG application.
    Initializes all core components and wires them together.
    """

    def __init__(self):
        """
        Initializes the container and all dependent services, agents, and use cases.
        """
        # Load Azure OpenAI configuration
        self.azure_settings = AzureOpenAISettings()

        # Initialize prompt provider
        self.prompt_provider = PromptyLoader()

        # Initialize agents
        self.classifier_agent = SentenceClassifier(self.azure_settings, self.prompt_provider)
        self.detector_agent = ContradictionDetector(self.azure_settings, self.prompt_provider)

        # Initialize domain service
        self.text_analysis_service = TextAnalysisService(self.classifier_agent, self.detector_agent)

        # Initialize use case
        self.analyze_text_use_case = AnalyzeTextUseCase(self.text_analysis_service)
