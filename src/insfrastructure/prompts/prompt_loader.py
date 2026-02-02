from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from jinja2 import Template

from src.domain.ports.input.prompt_provider_port import PromptProviderPort


class PromptyLoader(PromptProviderPort):
    """Implémentation du chargeur de fichiers .prompty au format YAML avec sections system/user."""

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initialise le loader.

        Args:
            templates_dir: Chemin vers le répertoire des templates
        """
        if templates_dir is None:
            current_dir = Path(__file__).parent
            self.templates_dir = current_dir / "templates"
        else:
            self.templates_dir = Path(templates_dir)

        if not self.templates_dir.exists():
            raise ValueError(f"Templates directory not found: {self.templates_dir}")

    @staticmethod
    def _parse_prompty_file(file_path: Path) -> Dict[str, Any]:
        """
        Parse un fichier .prompty avec frontmatter YAML.

        Args:
            file_path: Chemin vers le fichier .prompty

        Returns:
            Dict contenant les métadonnées et les sections (system, user)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Séparer le frontmatter YAML (entre ---)
        parts = content.split('---')
        if len(parts) < 3:
            raise ValueError(f"Invalid .prompty file format: {file_path}")

        # Parser le YAML du frontmatter
        metadata = yaml.safe_load(parts[1])

        # Récupérer le contenu du prompt après le frontmatter
        prompt_content = '---'.join(parts[2:]).strip()
        # Parser le contenu YAML interne s'il existe (system/user)
        content_dict = yaml.safe_load(prompt_content)

        if not content_dict or 'system' not in content_dict or 'user' not in content_dict:
            raise ValueError(f"The .prompty file must contain 'system' and 'user' sections: {file_path}")

        return {
            'metadata': metadata,
            'content': content_dict
        }

    def _load_prompt(self, prompt_name: str, section: str = "system", **kwargs: Any) -> str:
        """
        Charge et formate un prompt pour une section donnée.

        Args:
            prompt_name: Nom du fichier (sans extension)
            section: Section du prompt à récupérer ("system" ou "user")
            **kwargs: Variables pour le template Jinja2

        Returns:
            str: Le prompt formaté
        """
        file_path = self.templates_dir / f"{prompt_name}.prompty"

        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        prompty_data = self._parse_prompty_file(file_path)
        prompt_sections = prompty_data['content']

        if section not in prompt_sections:
            raise ValueError(f"Section '{section}' not found in prompt '{prompt_name}'")

        prompt_content = prompt_sections[section]

        # Valider les inputs si définis dans les métadonnées
        metadata = prompty_data['metadata']
        if 'inputs' in metadata:
            required_inputs = set(metadata['inputs'].keys())
            provided_inputs = set(kwargs.keys())
            missing_inputs = required_inputs - provided_inputs

            if missing_inputs:
                raise ValueError(
                    f"Missing required inputs for {prompt_name}: {missing_inputs}"
                )

        # Formatter avec Jinja2
        template = Template(prompt_content)
        formatted_prompt = template.render(**kwargs)

        return formatted_prompt

    def get_system_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """Récupère le prompt système formaté."""
        return self._load_prompt(prompt_name, section="system", **kwargs)

    def get_user_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """Récupère le prompt user formaté."""
        return self._load_prompt(prompt_name, section="user", **kwargs)
