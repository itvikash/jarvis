"""
main.py — Entry point
-----------------------
Run this file to start Jarvis: python main.py

Loop: listen to mic -> send text to Claude -> speak the reply.
Say "exit" or "stop listening" any time to quit.
"""

import config
from modules import stt, tts, brain


def run():
    tts.speak(f"{config.ASSISTANT_NAME} online. How can I help?")

    while True:
        user_text = stt.listen()

        if not user_text:
            continue  # nothing understood, just listen again

        if any(exit_word in user_text for exit_word in config.EXIT_WORDS):
            tts.speak("Goodbye.")
            break

        try:
            reply = brain.think(user_text)
        except RuntimeError as e:
            reply = str(e)

        tts.speak(reply)


if __name__ == "__main__":
    run()
