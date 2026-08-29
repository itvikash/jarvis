"""
config.py
---------
Central place for all settings. Beginners: this is the file you'll
tweak most often (voice speed, model name, etc.) without touching
the "real" logic in the other files.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# ---- Local AI model (Ollama) ----
# No API key needed — this runs fully on your own PC, for free.
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")  # must support tool calling

# ---- Assistant identity ----
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Jarvis")

# ---- Text-to-speech settings ----
TTS_RATE = 175        # words per minute (default ~200, lower = calmer)
TTS_VOLUME = 1.0      # 0.0 to 1.0
TTS_VOICE_INDEX = 0   # 0 = usually male voice, 1 = usually female (Windows SAPI5)

# ---- Speech recognition settings ----
LISTEN_TIMEOUT = 5           # seconds to wait for speech to start
PHRASE_TIME_LIMIT = 12       # max seconds for one spoken command
ENERGY_THRESHOLD = 300       # mic sensitivity (raise if it triggers on background noise)

# ---- Behavior ----
EXIT_WORDS = ["exit", "quit", "stop listening", "goodbye jarvis", "shut down jarvis"]
MAX_CONVERSATION_HISTORY = 10  # how many past turns to keep in context
