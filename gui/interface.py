"""
Tkinter GUI Interface for TinyllamaChatbot
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import logging
from datetime import datetime
from typing import Optional

from core.prompt_manager import PromptManager
from core.utils import clean_text

class ChatbotGUI:
    """Main GUI class for the TinyllamaChatbot"""

    def __init__(self, root: tk.Tk, chatbot):
        self.root = root
        self.chatbot = chatbot
        self.prompt_manager = PromptManager()
        self.is_generating = False

        self.setup_gui()
        self.load_model_async()

    def setup_gui(self):
        """Setup the main GUI components"""
        self.root.title("Tinyllama Chatbot (Offline)")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Status section
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)

        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky="w")
        self.status_var = tk.StringVar(value="Loading model...")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, foreground="orange")
        self.status_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

        self.info_button = ttk.Button(status_frame, text="Model Info", command=self.show_model_info)
        self.info_button.grid(row=0, column=2, sticky="e")

        # Chat display
        chat_frame = ttk.LabelFrame(main_frame, text="Chat History", padding="5")
        chat_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, width=70, height=20,
            state=tk.DISABLED, font=('Consolas', 10)
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew")

        self.chat_display.tag_configure("user", foreground="blue", font=('Consolas', 10, 'bold'))
        self.chat_display.tag_configure("assistant", foreground="green", font=('Consolas', 10))
        self.chat_display.tag_configure("system", foreground="red", font=('Consolas', 9, 'italic'))
        self.chat_display.tag_configure("timestamp", foreground="gray", font=('Consolas', 8))

        # Input section
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.input_text = tk.Text(input_frame, height=3, wrap=tk.WORD, font=('Consolas', 10))
        self.input_text.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=1, sticky="ns")

        self.send_button = ttk.Button(button_frame, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_chat)
        self.clear_button.grid(row=1, column=0, sticky="ew")

        self.input_text.bind('<Return>', self.on_enter_key)
        self.input_text.bind('<Shift-Return>', self.on_shift_enter)

        self.create_menu()
        self.add_system_message("Welcome to Tinyllama Chatbot! Loading model, please wait...")

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Chat History", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Chat", command=self.clear_chat)
        edit_menu.add_command(label="Clear History", command=self.clear_history)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def load_model_async(self):
        """Load model in background thread"""
        def load_model():
            success = self.chatbot.load_model()
            self.root.after(0, self.on_model_loaded, success)

        threading.Thread(target=load_model, daemon=True).start()

    def on_model_loaded(self, success: bool):
        """Called when model loading is complete"""
        if success:
            self.status_var.set("Ready")
            self.status_label.config(foreground="green")
            self.send_button.config(state=tk.NORMAL)
            self.add_system_message("Model loaded successfully! You can now start chatting.")
        else:
            self.status_var.set("Model Load Failed")
            self.status_label.config(foreground="red")
            self.add_system_message("Failed to load model. Please check the model file and configuration.")

    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # Shift not pressed
            self.send_message()
            return 'break'

    def on_shift_enter(self, event):
        """Allow Shift+Enter to insert newline"""
        return None

    def send_message(self):
        """Send user message and get response"""
        if self.is_generating:
            return

        user_input = self.input_text.get("1.0", tk.END).strip()
        user_input = clean_text(user_input)
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self.add_user_message(user_input)

        self.is_generating = True
        self.send_button.config(state=tk.DISABLED, text="Generating...")
        self.status_var.set("Generating response...")
        self.status_label.config(foreground="orange")

        def generate_response():
            try:
                prompt = self.prompt_manager.format_prompt(user_input)
                response = self.chatbot.generate_response(prompt)
                self.prompt_manager.add_to_history(user_input, response)
                self.root.after(0, self.on_response_generated, response)
            except Exception as e:
                logging.error(f"Error generating response: {e}")
                self.root.after(0, self.on_response_generated, f"Error: {str(e)}")

        threading.Thread(target=generate_response, daemon=True).start()

    def on_response_generated(self, response: str):
        """Handle response completion"""
        self.add_assistant_message(response)
        self.is_generating = False
        self.send_button.config(state=tk.NORMAL, text="Send")
        self.status_var.set("Ready")
        self.status_label.config(foreground="green")
        self.input_text.focus_set()

    def add_user_message(self, message: str):
        """Display user message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, "You: ", "user")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def add_assistant_message(self, message: str):
        """Display assistant message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, "Assistant: ", "assistant")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def add_system_message(self, message: str):
        """Display system message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, "System: ", "system")
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_system_message("Chat cleared.")

    def clear_history(self):
        """Clear conversation history"""
        self.prompt_manager.clear_history()
        self.add_system_message("Conversation history cleared.")

    def export_history(self):
        """Export chat history to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Chat History"
        )
        if filename:
            success = self.prompt_manager.export_history(filename)
            if success:
                messagebox.showinfo("Export Successful", f"Chat history exported to {filename}")
            else:
                messagebox.showerror("Export Failed", "Failed to export chat history")

    def show_model_info(self):
        """Show model information dialog"""
        info = self.chatbot.get_model_info()
        info_text = f"""Model Information:

Path: {info['model_path']}
Type: {info['model_type']}
Temperature: {info['temperature']}
Max Tokens: {info['max_tokens']}
GPU Layers: {info['gpu_layers']}
Status: {'Loaded' if info['is_loaded'] else 'Not Loaded'}"""
        messagebox.showinfo("Model Information", info_text)

    def show_about(self):
        """Show about dialog"""
        about_text = """TinyllamaChatbot v1.0

An offline AI chatbot powered by Tinyllama 1B model.
Uses ctransformers library for local inference.

Features:
- Completely offline operation
- Configurable model parameters
- Chat history logging
- Clean Tkinter interface

Created with Python and Tkinter."""
        messagebox.showinfo("About TinyllamaChatbot", about_text)
