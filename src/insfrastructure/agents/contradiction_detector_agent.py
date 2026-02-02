import json
from typing import List
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.domain.models.classification_result import ClassificationResult
from src.domain.models.contradiction_result import ContradictionResult, Contradiction
from src.domain.ports.input.detector_agent_port import DetectorAgentPort
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class ContradictionDetector(DetectorAgentPort):
    """
    Agent pour analyser un ensemble de phrases dans une catégorie
    et détecter les contradictions entre elles.
    Retourne :
        - La liste des numéros des phrases contradictoires
        - Une petite explication pour chaque contradiction
    """

    def __init__(self, azure_settings: AzureOpenAISettings, prompt_provider: PromptyLoader):
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

    def _detect_contradictions_per_category(self, sentences: List[str]) -> str:
        """
        Analyse les phrases et retourne les contradictions détectées.
        """
        numbered_sentences = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))

        system_prompt = self.prompt_provider.get_system_prompt(
            prompt_name="prompt_contradiction"
        )
        user_prompt = self.prompt_provider.get_user_prompt(
            prompt_name="prompt_contradiction",
            numbered_sentences=numbered_sentences
        )
        messages = [
            ChatCompletionSystemMessageParam(
                role="system",
                content=system_prompt),
            ChatCompletionUserMessageParam(
                role="user",
                content=user_prompt)
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1024,
            temperature=0,
        )

        return response.choices[0].message.content.strip()

    def detect_contradiction(self, classification_result: ClassificationResult) -> List[ContradictionResult]:
        """
        Parcourt un dictionnaire de catégories et de phrases,
        détecte les contradictions pour chaque catégorie.

        Args:
            categories (Dict[str, List[str]]):
                Clé = nom de la catégorie
                Valeur = liste de phrases

        Returns:
            Dict[str, str]: clé = catégorie, valeur = résultat du détecteur
            :param classification_result:
        """
        all_responses: List[ContradictionResult] = []
        # Parcourir les catégories
        for category in classification_result.categories:

            raw_output_str = self._detect_contradictions_per_category(category.phrases)
            try:
                raw_output = json.loads(raw_output_str)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Impossible de parser la sortie JSON pour la catégorie {category.name}: {e}\nSortie brute: {raw_output_str}"
                )
            contradictions_data = raw_output.get("التناقضات", [])
            if not contradictions_data:
                # Aucune contradiction détectée, on ignore cette catégorie
                continue

            contradictions_list: List[Contradiction] = []
            for contradiction in contradictions_data:
                sentences_numbers = contradiction.get("إفادات", [])

                # convertir les indices en phrases réelles
                sentences_texts = [
                    category.phrases[i - 1]  # -1 car JSON est 1-based, liste Python est 0-based
                    for i in sentences_numbers
                    if 0 < i <= len(category.phrases)
                ]

                contradictions_list.append(
                    Contradiction(
                        sentences=sentences_texts,
                        severity=contradiction.get("مستوى_التعارض", ""),
                        comment=contradiction.get("تعليق", "")
                    )
                )

            all_responses.append(
                ContradictionResult(
                    contradictions=contradictions_list
                )
            )

        return all_responses
