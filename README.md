# Jarvis — Free, Local AI Voice Assistant (Windows)

A Jarvis-inspired voice assistant that listens to you, thinks using a
**free local AI model** (via Ollama — no API key, no cost, no internet
required after setup), and can control your Windows laptop — opening
apps, checking your battery, taking screenshots, and more.

## Features
- Voice input (speech-to-text)
- Voice output (text-to-speech)
- Natural conversation powered by a local LLM (100% free)
- System control: open/close apps, battery status, CPU/RAM usage,
  screenshots, web search, shutdown timer
- Remembers recent conversation context
- Runs entirely on your PC — no data sent to any company

> **Note from the author:** This is my first time building and
> sharing an open-source project. If you spot something wrong,
> inefficient, or that could just be done better, please open an
> issue or a PR — I'd genuinely appreciate the feedback and would
> love to learn from it!

## Requirements
- Windows 10/11
- Python 3.10+
- A working microphone
- ~8GB+ RAM recommended (16GB+ ideal) for smooth local model performance
- [Ollama](https://ollama.com/download) installed (free)

## Setup

1. **Install Ollama**
   - Download and install from [ollama.com/download](https://ollama.com/download)
   - Pull a model that supports tool calling (this one's a good default):
     ```bash
     ollama pull llama3.1
     ```
   - Ollama runs as a background service automatically after install.
     You can verify it's running by visiting `http://localhost:11434`
     in a browser.

2. **Clone the repo**
   ```bash
   git clone https://github.com/itvikash/jarvis.git
   cd jarvis
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > Note: `pyaudio` can be tricky on Windows. If it fails, run:
   > `pip install pipwin` then `pipwin install pyaudio`

5. **Copy the env file** (no key needed, just default settings)
   - Copy `.env.example` to `.env`

6. **Run it**
   ```bash
   python main.py
   ```

> If your PC struggles with `llama3.1` (8B params), try a smaller
> model like `ollama pull qwen2.5:3b` and set `OLLAMA_MODEL=qwen2.5:3b`
> in your `.env`. Smaller = faster but less capable.

Say something like *"Jarvis, open notepad"* or *"what's my battery
percentage"* and watch it work. Say **"exit"** to quit.

## Project Structure

```
jarvis/
├── main.py                 # entry point / main loop
├── config.py                # all settings (voice, model, thresholds)
├── requirements.txt
├── .env.example
└── modules/
    ├── stt.py                # speech-to-text
    ├── tts.py                # text-to-speech
    ├── brain.py              # Ollama API + tool-use logic
    └── system_tools.py       # functions Jarvis can execute + tool registry
```

## Adding New Commands
1. Write a function in `modules/system_tools.py`
2. Add its schema to `TOOL_DEFINITIONS`
3. Register it in `TOOL_FUNCTIONS`

That's it — the AI will automatically start using it when relevant.

## Roadmap Ideas
- [ ] Wake word detection ("Hey Jarvis") using Porcupine
- [ ] Offline speech recognition with Whisper (removes the last internet
      dependency — Google's speech API currently still needs internet)
- [ ] Simple GUI overlay
- [ ] Smart home integration

## Notes on "Fully Free"
- The AI brain (Ollama) is 100% free and runs offline.
- Speech-to-text currently uses Google's free web API, which needs
  internet. For a fully offline experience, swap in Whisper (see
  roadmap above) — not required, just an option.

## Contributing
This is my first open-source project, so I'm sure there's plenty of
room to improve — better error handling, cleaner code, smarter tool
routing, whatever you notice. Issues and pull requests are very
welcome, and I'm open to any suggestions.

## License
MIT — free to use, modify, and share.
```
