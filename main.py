#!/usr/bin/env python3
"""
TinyllamaChatbot - Main Entry Point
A fully offline AI chatbot powered by Tinyllama 1B GGUF model
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import threading

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.interface import ChatbotGUI
from core.chatbot import TinyllamaChatbot
from core.utils import setup_logging

def main():
    """Main entry point for the TinyllamaChatbot application."""
    try:
        # Setup logging
        setup_logging()
        
        # Create root window
        root = tk.Tk()
        root.title("Tinyllama Chatbot (Offline)")
        root.geometry("800x600")
        root.minsize(600, 400)
        
        # Initialize chatbot
        chatbot = TinyllamaChatbot()
        
        # Create GUI
        gui = ChatbotGUI(root, chatbot)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()