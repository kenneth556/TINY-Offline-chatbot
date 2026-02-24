"""
TinyllamaChatbot Core - Model Loading and Response Generation
"""

import os
import json
import logging
from typing import Optional
from ctransformers import AutoModelForCausalLM

from .prompt_manager import PromptManager
from .utils import clean_text

class TinyllamaChatbot:
    """Main chatbot class that handles model loading and response generation."""

    def __init__(self):
        self.model = None
        self.prompt_manager = PromptManager()
        self.config = self._load_config()
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> dict:
        """Load configuration from settings.json."""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config file not found, using defaults")
            return {
                "model_path": "C:\\Users\\Blakka\\Documents\\CHATBOT\\model\\Tinyllama-1B-miniguanaco.Q2_K.gguf",
                "model_type": "tinyllama",
                "temperature": 0.7,
                "max_tokens": 256,
                "gpu_layers": 0,
                "logging_enabled": True
            }

    def load_model(self) -> bool:
        """Public method to load the Tinyllama model using ctransformers."""
        try:
            model_path = self.config["model_path"]
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")

            self.logger.info(f"Loading model from: {model_path}")

            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                model_type=self.config["model_type"],
                gpu_layers=self.config["gpu_layers"],
                temperature=self.config["temperature"],
                max_new_tokens=self.config["max_tokens"],
                context_length=2048
            )

            self.logger.info("Model loaded successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load model: {str(e)}")
            return False

    def generate_response(self, user_input: str) -> str:
        """Generate a response to user input."""
        if not self.model:
            return "Error: Model not loaded"

        try:
            cleaned_input = clean_text(user_input)
            prompt = self.prompt_manager.format_prompt(cleaned_input)

            self.logger.info(f"Generating response for: {cleaned_input}")

            response = self.model(
                prompt,
                max_new_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"],
                stop=["Human:", "User:", "\n\n"]
            )

            cleaned_response = clean_text(response)

            if self.config.get("logging_enabled", True):
                self.prompt_manager.log_interaction(cleaned_input, cleaned_response)

            return cleaned_response

        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"

    def is_model_loaded(self) -> bool:
        """Check if the model is loaded and ready."""
        return self.model is not None

    def get_model_info(self) -> dict:
        """Return model configuration and status."""
        return {
            "model_path": self.config.get("model_path"),
            "model_type": self.config.get("model_type"),
            "temperature": self.config.get("temperature"),
            "max_tokens": self.config.get("max_tokens"),
            "gpu_layers": self.config.get("gpu_layers"),
            "is_loaded": self.is_model_loaded()
        }
