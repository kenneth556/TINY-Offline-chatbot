
"""
TinyllamaChatbot - Utility Functions
"""

import os
import re
import logging
from typing import Optional

def clean_text(text: str) -> str:
    """Clean and normalize text input/output."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove control characters except newlines and tabs
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Limit length to prevent extremely long responses
    if len(text) > 1000:
        text = text[:1000] + "..."
    
    return text

def setup_logging():
    """Setup logging configuration."""
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'application.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def validate_model_file(model_path: str) -> bool:
    """Validate that the model file exists and is accessible."""
    if not os.path.exists(model_path):
        return False
    
    if not os.path.isfile(model_path):
        return False
    
    # Check if file has .gguf extension
    if not model_path.lower().endswith('.gguf'):
        return False
    
    # Check if file is readable
    try:
        with open(model_path, 'rb') as f:
            # Read first few bytes to ensure it's accessible
            f.read(4)
        return True
    except (IOError, OSError):
        return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"

def get_model_info(model_path: str) -> dict:
    """Get information about the model file."""
    if not os.path.exists(model_path):
        return {"exists": False}
    
    stat = os.stat(model_path)
    return {
        "exists": True,
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "modified": stat.st_mtime,
        "path": model_path
    }

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def is_valid_input(text: str) -> bool:
    """Validate user input."""
    if not text or not text.strip():
        return False
    
    # Check for minimum length
    if len(text.strip()) < 1:
        return False
    
    # Check for maximum length
    if len(text) > 500:
        return False
    
    return True
