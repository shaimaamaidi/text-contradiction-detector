"""
Module: contradiction_detector
Description:
    Agent that analyzes a set of sentences within a category and detects contradictions between them.
    Provides:
        - A list of sentences involved in each contradiction
        - A brief explanation for each contradiction
"""

from typing import List
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.domain.models.classification_result import ClassificationResult
from src.domain.models.contradiction_llm_response import ContradictionLLMResponse
from src.domain.models.contradiction_result import ContradictionResult, Contradiction
from src.domain.ports.input.detector_agent_port import DetectorAgentPort
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class ContradictionDetector(DetectorAgentPort):
    """
    Agent for analyzing a set of sentences within a category
    and detecting contradictions between them.
    """

    def __init__(self, azure_settings: AzureOpenAISettings, prompt_provider: PromptyLoader):
        """
        Initializes the contradiction detector agent.

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

    def detect_contradiction(
            self,
            classification_result: ClassificationResult
    ) -> List[ContradictionResult]:
        """
        Detects contradictions across all categories in a classification result.

        Args:
            classification_result (ClassificationResult): Categories with sentences.

        Returns:
            List[ContradictionResult]: List of contradiction results per category.
        """
        all_results: List[ContradictionResult] = []

        for category in classification_result.categories:
            # Skip categories with fewer than 2 sentences
            if len(category.phrases) < 2:
                continue

            # Get LLM response
            llm_response = self._detect_contradictions_per_category(category.phrases)

            # Map to domain model
            contradiction_result = ContradictionDetector._map_llm_to_domain(llm_response, category.phrases)

            all_results.append(contradiction_result)

        return all_results

    def _detect_contradictions_per_category(self, sentences: List[str]) -> ContradictionLLMResponse:
        """
        Analyzes sentences in a category and returns the detected contradictions as a structured LLM response.

        Args:
            sentences (List[str]): List of sentences in the category.

        Returns:
            ContradictionLLMResponse: Parsed LLM response with detected contradictions.
        """
        # Number sentences for clarity in prompts
        numbered_sentences = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))

        system_prompt = self.prompt_provider.get_system_prompt(
            prompt_name="prompt_contradiction"
        )
        user_prompt = self.prompt_provider.get_user_prompt(
            prompt_name="prompt_contradiction",
            numbered_sentences=numbered_sentences
        )

        messages = [
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
            ChatCompletionUserMessageParam(role="user", content=user_prompt)
        ]

        completion = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=messages,
            response_format=ContradictionLLMResponse,
            max_tokens=1024,
            temperature=0,
        )

        return completion.choices[0].message.parsed

    @staticmethod
    def _map_llm_to_domain(
            llm_response: ContradictionLLMResponse,
            sentences: List[str]
    ) -> ContradictionResult:
        """
        Maps the LLM contradiction response to the domain model.

        Args:
            llm_response (ContradictionLLMResponse): LLM output with sentence indices.
            sentences (List[str]): Original sentences in the category.

        Returns:
            ContradictionResult: Domain object containing contradictions with full sentences.
        """
        contradictions_list: List[Contradiction] = []

        for c in llm_response.contradictions:
            sentences_texts = [
                sentences[i - 1]
                for i in c.statements
                if 0 < i <= len(sentences)
            ]

            contradictions_list.append(
                Contradiction(
                    statements=sentences_texts,
                    severity=c.severity_level,
                    comment=c.comment
                )
            )

        return ContradictionResult(contradictions=contradictions_list)
