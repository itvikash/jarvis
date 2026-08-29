"""
system_tools.py — System Control
----------------------------------
Every function here is a "tool" the AI brain can choose to call.
Add new functions here, then register them in TOOL_DEFINITIONS below
so Claude knows they exist and when to use them.
"""

import os
import subprocess
import webbrowser
import datetime
import psutil
import pyautogui

# Common Windows apps -> the command used to launch them.
# Add your own favorites here.
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vscode": "code.exe",
    "file explorer": "explorer.exe",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
}


def open_app(app_name: str) -> str:
    """Opens a known Windows application by name."""
    app_name = app_name.lower().strip()
    command = APP_PATHS.get(app_name)
    if not command:
        return f"I don't know how to open '{app_name}'. Add it to APP_PATHS in system_tools.py."
    try:
        subprocess.Popen(command, shell=True)
        return f"Opening {app_name}."
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"


def close_app(app_name: str) -> str:
    """Closes a running application by process name (e.g. 'notepad')."""
    app_name = app_name.lower().strip()
    exe_name = APP_PATHS.get(app_name, app_name)
    if not exe_name.endswith(".exe"):
        exe_name += ".exe"

    closed = False
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] and proc.info["name"].lower() == exe_name.lower():
            proc.kill()
            closed = True
    return f"Closed {app_name}." if closed else f"{app_name} doesn't seem to be running."


def get_battery_status() -> str:
    """Reports current battery percentage and charging status."""
    battery = psutil.sensors_battery()
    if battery is None:
        return "This device doesn't report battery info (might be a desktop)."
    plugged = "charging" if battery.power_plugged else "not charging"
    return f"Battery is at {battery.percent}% and {plugged}."


def get_current_time() -> str:
    """Returns the current date and time."""
    now = datetime.datetime.now()
    return now.strftime("It's %I:%M %p on %A, %B %d, %Y.")


def search_web(query: str) -> str:
    """Opens the default browser with a Google search for the query."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching the web for {query}."

def take_screenshot(filename: str = "screenshot.png") -> str:
    """Takes a screenshot and saves it to the current folder."""
    path = os.path.join(os.getcwd(), filename)
    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}."


def get_system_info() -> str:
    """Reports basic CPU and RAM usage."""
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return f"CPU usage is {cpu}% and RAM usage is {ram}%."


def shutdown_pc(minutes: int = 0) -> str:
    """Schedules (or immediately triggers) a Windows shutdown."""
    seconds = max(minutes, 0) * 60
    os.system(f"shutdown /s /t {seconds}")
    if minutes > 0:
        return f"Shutting down in {minutes} minutes. Say 'cancel shutdown' to stop it."
    return "Shutting down now."


def cancel_shutdown() -> str:
    """Cancels a previously scheduled shutdown."""
    os.system("shutdown /a")
    return "Shutdown cancelled."


# ---------------------------------------------------------------------
# Tool registry: tells Claude what functions exist, in the format the
# Anthropic API's tool-use feature expects. Keep this in sync with the
# functions above whenever you add a new capability.
# ---------------------------------------------------------------------
TOOL_DEFINITIONS = [
    {
        "name": "open_app",
        "description": "Open a desktop application by name, e.g. notepad, chrome, calculator.",
        "input_schema": {
            "type": "object",
            "properties": {"app_name": {"type": "string"}},
            "required": ["app_name"],
        },
    },
    {
        "name": "close_app",
        "description": "Close a running application by name.",
        "input_schema": {
            "type": "object",
            "properties": {"app_name": {"type": "string"}},
            "required": ["app_name"],
        },
    },
    {
        "name": "get_battery_status",
        "description": "Get the laptop's current battery percentage and charging status.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "search_web",
        "description": "Search Google for a query in the default browser.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "take_screenshot",
        "description": "Take a screenshot of the current screen and save it.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_system_info",
        "description": "Get current CPU and RAM usage percentages.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "shutdown_pc",
        "description": "Shut down the Windows PC, optionally after a delay in minutes.",
        "input_schema": {
            "type": "object",
            "properties": {"minutes": {"type": "integer"}},
        },
    },
    {
        "name": "cancel_shutdown",
        "description": "Cancel a previously scheduled shutdown.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

# Maps tool name (string) -> actual Python function to call.
TOOL_FUNCTIONS = {
    "open_app": open_app,
    "close_app": close_app,
    "get_battery_status": get_battery_status,
    "get_current_time": get_current_time,
    "search_web": search_web,
    "take_screenshot": take_screenshot,
    "get_system_info": get_system_info,
    "shutdown_pc": shutdown_pc,
    "cancel_shutdown": cancel_shutdown,
}
