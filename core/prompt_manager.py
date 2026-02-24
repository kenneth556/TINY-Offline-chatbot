"""
TinyllamaChatbot - Prompt Management and Logging
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Tuple

class PromptManager:
    """Manages prompt formatting and conversation logging."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.conversation_history: List[Tuple[str, str]] = []
        self.log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'chat_history.txt')
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Ensure the logs directory exists."""
        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)

    def format_prompt(self, user_input: str) -> str:
        """Format the user input into a proper prompt for the model."""
        return f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{user_input}

### Response:
"""

    def add_to_history(self, user_input: str, bot_response: str):
        """Add interaction to in-memory history."""
        self.conversation_history.append((user_input, bot_response))
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]

    def log_interaction(self, user_input: str, bot_response: str):
        """Log the conversation to file and memory."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add to memory
        self.add_to_history(user_input, bot_response)

        # Write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n[{timestamp}]\n")
                f.write(f"User: {user_input}\n")
                f.write(f"Bot: {bot_response}\n")
                f.write("-" * 50 + "\n")
        except Exception as e:
            self.logger.error(f"Failed to write to log file: {str(e)}")

    def get_conversation_history(self) -> List[Tuple[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()

    def clear_history(self):
        """Clear the conversation history from memory."""
        self.conversation_history.clear()
        self.logger.info("Conversation history cleared")

    def export_history(self, filename: str) -> bool:
        """Export conversation history to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Tinyllama Chatbot - Conversation Export\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")

                for i, (user_msg, bot_msg) in enumerate(self.conversation_history, 1):
                    f.write(f"Conversation {i}:\n")
                    f.write(f"User: {user_msg}\n")
                    f.write(f"Bot: {bot_msg}\n")
                    f.write("-" * 30 + "\n\n")

            self.logger.info(f"History exported to: {filename}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to export history: {str(e)}")
            return False
