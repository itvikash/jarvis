"""
stt.py — Speech To Text
------------------------
Listens to your microphone and converts what you say into text.
Uses Google's free web speech API under the hood (requires internet).
"""

import speech_recognition as sr
import config


recognizer = sr.Recognizer()
recognizer.energy_threshold = config.ENERGY_THRESHOLD


def listen() -> str | None:
    """
    Listens on the default microphone and returns the recognized
    text in lowercase. Returns None if nothing was understood.
    """
    with sr.Microphone() as source:
        print("🎤 Listening...")
        # Adjust briefly for background noise (fan, AC, etc.)
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(
                source,
                timeout=config.LISTEN_TIMEOUT,
                phrase_time_limit=config.PHRASE_TIME_LIMIT,
            )
        except sr.WaitTimeoutError:
            print("⌛ No speech detected.")
            return None

    try:
        print("🧠 Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❓ Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Speech service error: {e}")
        return None
