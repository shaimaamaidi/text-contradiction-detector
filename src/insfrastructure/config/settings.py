# infrastructure/config/settings.py
import os
from dotenv import load_dotenv

# Charger automatiquement les variables d'environnement depuis le fichier .env
load_dotenv()


class AzureOpenAISettings:
    """
    Configuration centralisée pour Azure OpenAI.
    Lit les variables depuis le fichier .env et fournit une validation.
    """

    def __init__(self):
        self.endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")
        self.model: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

        self._validate()

    def _validate(self):
        """Vérifie que toutes les variables essentielles sont présentes"""
        if not all([self.endpoint, self.api_key, self.api_version, self.model]):
            missing = [
                name
                for name, value in [
                    ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                    ("AZURE_OPENAI_API_KEY", self.api_key),
                    ("AZURE_OPENAI_API_VERSION", self.api_version),
                    ("AZURE_OPENAI_DEPLOYMENT_NAME", self.model),
                ]
                if not value
            ]
            raise ValueError(
                f"Les variables d'environnement suivantes sont manquantes : {', '.join(missing)}"
            )


