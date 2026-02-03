"""
Module: prompty_loader
Description:
    Implementation of a YAML-based .prompty file loader.
    Supports system and user sections and renders prompts using Jinja2 templates.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from jinja2 import Template

from src.domain.ports.input.prompt_provider_port import PromptProviderPort


class PromptyLoader(PromptProviderPort):
    """
    Loader for .prompty files in YAML format, supporting 'system' and 'user' sections.
    Provides methods to fetch and render prompts using Jinja2 templates.
    """

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Initializes the prompt loader.

        Args:
            templates_dir (Optional[str]): Path to the directory containing prompt templates.
                                           Defaults to a 'templates' folder next to this file.
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
        Parses a .prompty file with YAML frontmatter.

        Args:
            file_path (Path): Path to the .prompty file.

        Returns:
            Dict[str, Any]: Dictionary containing metadata and prompt sections ('system', 'user').
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split YAML frontmatter (between ---)
        parts = content.split('---')
        if len(parts) < 3:
            raise ValueError(f"Invalid .prompty file format: {file_path}")

        # Parse YAML metadata from frontmatter
        metadata = yaml.safe_load(parts[1])

        # Parse remaining content YAML for 'system' and 'user' sections
        prompt_content = '---'.join(parts[2:]).strip()
        content_dict = yaml.safe_load(prompt_content)

        if not content_dict or 'system' not in content_dict or 'user' not in content_dict:
            raise ValueError(f"The .prompty file must contain 'system' and 'user' sections: {file_path}")

        return {
            'metadata': metadata,
            'content': content_dict
        }

    def _load_prompt(self, prompt_name: str, section: str = "system", **kwargs: Any) -> str:
        """
        Loads and renders a prompt for a given section using Jinja2.

        Args:
            prompt_name (str): Name of the prompt file (without extension).
            section (str): Section of the prompt to fetch ('system' or 'user').
            **kwargs: Variables to render in the Jinja2 template.

        Returns:
            str: The formatted prompt.
        """
        file_path = self.templates_dir / f"{prompt_name}.prompty"

        if not file_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        prompty_data = self._parse_prompty_file(file_path)
        prompt_sections = prompty_data['content']

        if section not in prompt_sections:
            raise ValueError(f"Section '{section}' not found in prompt '{prompt_name}'")

        prompt_content = prompt_sections[section]

        # Validate inputs defined in metadata
        metadata = prompty_data['metadata']
        if 'inputs' in metadata:
            required_inputs = set(metadata['inputs'].keys())
            provided_inputs = set(kwargs.keys())
            missing_inputs = required_inputs - provided_inputs

            if missing_inputs:
                raise ValueError(
                    f"Missing required inputs for {prompt_name}: {missing_inputs}"
                )

        # Render the template with Jinja2
        template = Template(prompt_content)
        formatted_prompt = template.render(**kwargs)

        return formatted_prompt

    def get_system_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """
        Retrieves the formatted system prompt.

        Args:
            prompt_name (str): Name of the prompt.
            **kwargs: Variables to render in the template.

        Returns:
            str: Formatted system prompt.
        """
        return self._load_prompt(prompt_name, section="system", **kwargs)

    def get_user_prompt(self, prompt_name: str, **kwargs: Any) -> str:
        """
        Retrieves the formatted user prompt.

        Args:
            prompt_name (str): Name of the prompt.
            **kwargs: Variables to render in the template.

        Returns:
            str: Formatted user prompt.
        """
        return self._load_prompt(prompt_name, section="user", **kwargs)
