import json
from typing import List, Dict, Any
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.domain.models.classification_result import ClassificationResult, Category
from src.domain.ports.input.classifier_agent_port import ClassifierAgentPort
from src.insfrastructure.config.settings import AzureOpenAISettings
from src.insfrastructure.prompts.prompt_loader import PromptyLoader


class SentenceClassifier(ClassifierAgentPort):
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


    def _classify_sentences(self, sentences: List[str]) -> str:
        # Créer une liste numérotée en chaîne de caractères
        numbered_sentences = "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))

        system_prompt = self.prompt_provider.get_system_prompt(
            prompt_name="prompt_classification"
        )
        user_prompt = self.prompt_provider.get_user_prompt(
            prompt_name="prompt_classification",
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

        # Retourner le contenu texte de la réponse
        return response.choices[0].message.content.strip()

    def classify_sentences(self, sentences: List[str]) -> ClassificationResult:
        """
        Transforme la sortie de classify_sentences en dictionnaire Python.
        Clé = catégorie
        Valeur = liste des phrases réelles
        """
        raw_output_str = self._classify_sentences(sentences)

        try:
            raw_output: Dict[str, Any] = json.loads(raw_output_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Impossible de parser la sortie JSON de l'agent : {e}\nSortie brute : {raw_output_str}")

        categories_list: List[Category] = []

        for category in raw_output.get("categories", []):
            name = category.get("name", "بدون اسم")
            phrase_indices = category.get("phrases", [])
            real_phrases = []

            for idx in phrase_indices:
                # idx peut être int ou dict
                if isinstance(idx, int):
                    if 0 < idx <= len(sentences):
                        real_phrases.append(sentences[idx - 1])
                elif isinstance(idx, dict) and "index" in idx:
                    i = idx["index"]
                    if 0 < i <= len(sentences):
                        real_phrases.append(sentences[i - 1])
                elif isinstance(idx, str):
                    # cas où le modèle renvoie directement les phrases
                    real_phrases.append(idx)

            categories_list.append(Category(name=name, phrases=real_phrases))

        return ClassificationResult(categories=categories_list)
