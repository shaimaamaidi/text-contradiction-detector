"""
Module: sentence_classifier
Description:
    Agent responsible for classifying sentences using Azure OpenAI.
    It converts the LLM output into domain-level classification results.
"""

from typing import List
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.domain.models.classification_llm_response import ClassificationLLMResponse
from src.domain.models.classification_result import ClassificationResult, Category
from src.domain.ports.input.classifier_agent_port import ClassifierAgentPort
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class SentenceClassifier(ClassifierAgentPort):
    """
    Agent for classifying sentences using an LLM (Azure OpenAI).
    Converts the LLM response into domain-level ClassificationResult objects.
    """

    def __init__(self, azure_settings: AzureOpenAISettings, prompt_provider: PromptyLoader):
        """
        Initializes the sentence classifier agent.

        Args:
            azure_settings (AzureOpenAISettings): Azure OpenAI configuration.
            prompt_provider (PromptyLoader): Provider for system and user prompts.
        """
        self.endpoint = azure_settings.endpoint
        self.api_key = azure_settings.api_key
        self.api_version = azure_settings.api_version
        self.model = azure_settings.model

        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version
        )
        self.prompt_provider = prompt_provider

    def classify_sentences(self, sentences: List[str]) -> ClassificationResult:
        """
        Classifies sentences and maps the LLM response to the domain model.

        Args:
            sentences (List[str]): Sentences to classify.

        Returns:
            ClassificationResult: Domain-level classification result.
        """
        llm_response = self._classify_sentences(sentences)
        return SentenceClassifier._map_llm_to_domain(llm_response, sentences)

    def _classify_sentences(self, sentences: List[str]) -> ClassificationLLMResponse:
        """
        Sends sentences to the LLM for classification and parses the response.

        Args:
            sentences (List[str]): Sentences to classify.

        Returns:
            ClassificationLLMResponse: Parsed LLM response.
        """
        # Number sentences for clarity in prompts
        numbered_sentences = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))

        system_prompt = self.prompt_provider.get_system_prompt(
            prompt_name="prompt_classification"
        )
        user_prompt = self.prompt_provider.get_user_prompt(
            prompt_name="prompt_classification",
            numbered_sentences=numbered_sentences
        )

        messages = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt)
        ]

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=ClassificationLLMResponse,
            temperature=0,
            max_tokens=1024,
        )

        return completion.choices[0].message.parsed

    @staticmethod
    def _map_llm_to_domain(
        llm_response: ClassificationLLMResponse,
        sentences: List[str]
    ) -> ClassificationResult:
        """
        Maps the LLM classification response to the domain ClassificationResult object.

        Args:
            llm_response (ClassificationLLMResponse): The parsed LLM response.
            sentences (List[str]): Original list of sentences.

        Returns:
            ClassificationResult: Domain classification result.
        """
        categories: List[Category] = []

        for cat in llm_response.categories:
            phrases: List[str] = []

            for i in cat.phrases:
                index: int = int(i)
                if 0 < index <= len(sentences):
                    phrases.append(sentences[index - 1])

            categories.append(
                Category(
                    name=cat.name,
                    phrases=phrases
                )
            )

        return ClassificationResult(categories=categories)
