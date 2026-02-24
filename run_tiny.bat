@echo off
echo Starting Tinyllama Chatbot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import ctransformers" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if model file exists at the specified path
if not exist "C:\Users\Blakka\Documents\CHATBOT\model\Tinyllama-1B-miniguanaco.Q2_K.gguf" (
    echo.
    echo WARNING: Model file not found!
    echo Expected location: C:\Users\Blakka\Documents\CHATBOT\model\Tinyllama-1B-miniguanaco.Q2_K.gguf
    echo.
    echo Please ensure the model file is in the correct location.
    echo Download from: https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
    echo.
    pause
)

REM Start the application
echo Starting Tinyllama Chatbot...
python main.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)