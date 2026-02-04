"""
Module: container
Description:
    Defines the Container class responsible for initializing and wiring together
    all core components of the application, following hexagonal architecture
    and dependency injection principles.
"""

from src.application.use_cases.analyse_text_use_case import AnalyzeTextUseCase
from src.domain.services.text_analysis_service import TextAnalysisService
from src.insfrastructure.agents.contradiction_detector_agent import ContradictionDetector
from src.insfrastructure.agents.sentence_classifier_agent import SentenceClassifier
from src.insfrastructure.config.app_settings import AppSettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class Container:
    """
    Dependency injection container for the application.

    This class initializes all core components, including configuration, prompts,
    agents, domain services, and use cases, and wires them together.
    """

    def __init__(self):
        """
        Initializes the container and all dependent services, agents, and use cases.

        Attributes:
            app_settings (AppSettings): Application configuration and environment variables.
            prompt_provider (PromptyLoader): Provides prompts to agents.
            classifier_agent (SentenceClassifier): Agent responsible for sentence classification.
            detector_agent (ContradictionDetector): Agent responsible for contradiction detection.
            text_analysis_service (TextAnalysisService): Domain service orchestrating classification and detection.
            analyze_text_use_case (AnalyzeTextUseCase): Application use case for text analysis.
        """
        # Load application configuration
        self.app_settings = AppSettings()

        # Initialize prompt provider
        self.prompt_provider = PromptyLoader()

        # Initialize agents
        self.classifier_agent = SentenceClassifier(self.app_settings, self.prompt_provider)
        self.detector_agent = ContradictionDetector(self.app_settings, self.prompt_provider)

        # Initialize domain service
        self.text_analysis_service = TextAnalysisService(self.classifier_agent, self.detector_agent)

        # Initialize use case
        self.analyze_text_use_case = AnalyzeTextUseCase(self.text_analysis_service)
