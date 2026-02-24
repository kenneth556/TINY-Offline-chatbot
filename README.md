TinyllamaChatbot – Offline AI Chatbot

A fully offline AI chatbot powered by TinyLlama 1B Instruct v0.2 using the ctransformers library.
Features a clean Tkinter GUI, chat history logging, configurable settings, and complete local operation.

🚀 Features

Completely Offline – No internet required

TinyLlama 1B GGUF Model – Efficient Q2_K quantized inference

Clean Tkinter GUI – Scrollable chat interface

Configurable Settings – Temperature, max tokens, GPU layers, and more

Chat History Logging – Automatic timestamped logs

Cross-Platform – Windows, macOS, Linux

🖥 Requirements

Python 3.8+

Minimum 4GB RAM (8GB recommended)

TinyLlama 1B GGUF model file

📦 Installation
1️⃣ Clone the Repository
git clone <your-repo-url>
cd TinyllamaChatbot
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Download the Model

Download:

Tinyllama-1B-miniguanaco.Q2_K.gguf

Place it inside:

model/Tinyllama-1B-miniguanaco.Q2_K.gguf
▶ Usage
Windows

Double-click:

run_Tinyllama.bat

Or run:

python main.py
macOS / Linux
python3 main.py
⚙ Configuration

Edit:

config/settings.json
Options

model_path – Path to GGUF model

temperature – Creativity (0.1 – 1.0)

max_tokens – Maximum response length

gpu_layers – Layers to offload to GPU

logging_enabled – Enable/disable chat logging

🖼 GUI Features

Status Indicator (model loading state)

Scrollable chat display with timestamps

Multi-line input box

Send / Clear buttons

Menu bar (export history, clear logs, help)

⌨ Keyboard Shortcuts

Enter – Send message

Shift + Enter – New line

Ctrl + L – Clear chat (if implemented)

🛠 Troubleshooting
Model Not Loading

Ensure model path is correct

Confirm at least 4GB free RAM

Verify model file integrity

Slow Performance

Reduce max_tokens

Set gpu_layers to 0 if no GPU

Close memory-heavy applications

GUI Issues

Ensure Tkinter is installed. Test with:

python -m tkinter
🧠 Model Information

Model: TinyLlama 1B Instruct v0.2

Format: GGUF (Q2_K quantization)

Size: ~2.8GB

Context Length: 2048 tokens

Primary Language: English

License: Apache 2.0

📝 Logging

Chat logs → logs/chat_history.txt

App logs → logs/Tinyllama_chatbot.log

Controlled via settings.json

🤝 Contributing

Issues, improvements, and suggestions are welcome.

📜 License

Open-source project.
Please respect the TinyLlama model license.

⚠ Disclaimer

This is an offline AI chatbot for educational and personal use.
Responses are AI-generated and may not always be accurate or appropriate.
