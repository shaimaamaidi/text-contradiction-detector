"""
Module: prompt_provider_port
Description:
    This module defines the abstract interface (port) for loading prompts.
    It specifies methods to retrieve system and user prompts for the application.
"""

from abc import ABC, abstractmethod


class PromptProviderPort(ABC):
    """
    Port for loading prompts.
    Defines the abstract methods to retrieve system and user prompts.
    """

    @abstractmethod
    def get_system_prompt(self, prompt_type: str) -> str:
        """
        Retrieves a system prompt.

        Args:
            prompt_type (str): Type of system prompt (e.g., "prompt_classification", "prompt_contradiction").

        Returns:
            str: The system prompt.
        """
        pass

    @abstractmethod
    def get_user_prompt(self, context: str, question: str) -> str:
        """
        Retrieves and formats the user prompt.

        Args:
            context (str): Context used to answer the question.
            question (str): The user's question.

        Returns:
            str: The formatted user prompt.
        """
        pass
