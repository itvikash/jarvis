"""
brain.py — The "thinking" part of Jarvis
------------------------------------------
Sends what you said to a LOCAL AI model running via Ollama (free,
no API key, runs entirely on your PC). The model decides whether to
just reply in words, or call one of the system tools (open an app,
check battery, etc.). This file handles that back-and-forth.
"""

import json
import requests
import config
from modules.system_tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

SYSTEM_PROMPT = f"""You are {config.ASSISTANT_NAME}, a helpful voice assistant
running on the user's Windows laptop, inspired by Iron Man's J.A.R.V.I.S.
Keep spoken replies SHORT (1-3 sentences) since they'll be read aloud by
text-to-speech. Use the available tools when the user asks you to do
something on their computer. Be a little witty, but stay useful."""

# Ollama's tool schema is the same "input_schema" -> "parameters" shape
# used by OpenAI-style function calling. We convert our tool defs once.
OLLAMA_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": t["name"],
            "description": t["description"],
            "parameters": t["input_schema"],
        },
    }
    for t in TOOL_DEFINITIONS
]

# Keeps recent turns so Jarvis has short-term memory of the conversation.
conversation_history: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]


def _trim_history():
    max_len = config.MAX_CONVERSATION_HISTORY * 2 + 1  # +1 for system msg
    if len(conversation_history) > max_len:
        # keep the system prompt (index 0) and drop oldest turns after it
        del conversation_history[1: len(conversation_history) - max_len + 1]


def _call_ollama() -> dict:
    """Sends the current conversation to the local Ollama server."""
    payload = {
        "model": config.OLLAMA_MODEL,
        "messages": conversation_history,
        "tools": OLLAMA_TOOLS,
        "stream": False,
    }
    try:
        resp = requests.post(config.OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Can't reach Ollama. Make sure it's installed and running "
            "(open a terminal and run: ollama serve)."
        )


def think(user_text: str) -> str:
    """
    Sends user_text to the local model, executes any tool calls it
    requests, and returns the final spoken reply as a string.
    """
    conversation_history.append({"role": "user", "content": user_text})
    _trim_history()

    data = _call_ollama()
    message = data["message"]

    # Keep resolving tool calls until the model gives a final text answer.
    while message.get("tool_calls"):
        conversation_history.append(message)

        for call in message["tool_calls"]:
            name = call["function"]["name"]
            args = call["function"]["arguments"]
            if isinstance(args, str):
                args = json.loads(args)

            func = TOOL_FUNCTIONS.get(name)
            if func:
                try:
                    result = func(**args)
                except Exception as e:
                    result = f"Error running {name}: {e}"
            else:
                result = f"Unknown tool: {name}"

            conversation_history.append({
                "role": "tool",
                "content": str(result),
            })

        data = _call_ollama()
        message = data["message"]

    conversation_history.append(message)
    _trim_history()

    return (message.get("content") or "").strip() or "Done."
