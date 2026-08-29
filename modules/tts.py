"""
tts.py — Text To Speech
------------------------
Makes Jarvis speak out loud. Uses pyttsx3, which works fully offline
on Windows via the built-in SAPI5 voices.
"""

import pyttsx3
import config

engine = pyttsx3.init()
engine.setProperty("rate", config.TTS_RATE)
engine.setProperty("volume", config.TTS_VOLUME)

voices = engine.getProperty("voices")
if voices and config.TTS_VOICE_INDEX < len(voices):
    engine.setProperty("voice", voices[config.TTS_VOICE_INDEX].id)


def speak(text: str) -> None:
    """Speaks the given text out loud and prints it to console."""
    print(f"{config.ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()
