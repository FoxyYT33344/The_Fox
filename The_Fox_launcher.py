import os
import sys
import subprocess
import urllib.request
import tkinter as tk
from tkinter import messagebox

# ---------------- Pfade ----------------
FOLDER = os.path.dirname(__file__)
GAME_FILE = os.path.join(FOLDER, "The_Fox.py")
LOCAL_LAUNCHER_VERSION = os.path.join(FOLDER, "version.launcher.py")
LOCAL_GAME_VERSION = os.path.join(FOLDER, "game.version.py")

# ---------------- GitHub-Links (Raw) ----------------
GAME_VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/game.version.py"
LAUNCHER_VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/version.launcher.py"

# ---------------- Spiel-Prozess ----------------
game_process = None

# ---------------- Versions-Helper ----------------
def get_local_version(file_path):
    if not os.path.exists(file_path):
        return "0.0.0"
    data = {}
    with open(file_path) as f:
        exec(f.read(), data)
    return data.get("VERSION", "0.0.0")

def get_online_version(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = {}
            exec(r.read().decode(), data)
            return data.get("VERSION", None)
    except:
        return None

# ---------------- Spiel starten ----------------
def start_game():
    global game_process
    if not os.path.exists(GAME_FILE):
        messagebox.showerror("Fehler", "Spiel ist nicht installiert.")
        return
    game_process = subprocess.Popen([sys.executable, GAME_FILE])
    status_label.config(text="Spiel gestartet! Launcher läuft weiter ✅")

# ---------------- Spiel zwangsweise beenden ----------------
def force_quit_game():
    global game_process
    if game_process:
        game_process.terminate()
        game_process = None
        status_label.config(text="Spiel zwangsweise beendet ❌")
    else:
        messagebox.showinfo("Info", "Kein Spiel läuft gerade.")

# ---------------- Launcher beenden ----------------
def quit_launcher():
    if messagebox.askyesno("Launcher beenden", "Wollen Sie den Launcher wirklich beenden?"):
        root.destroy()

# ---------------- Versionscheck ----------------
def check_updates():
    online_game = get_online_version(GAME_VERSION_URL)
    online_launcher = get_online_version(LAUNCHER_VERSION_URL)
    local_game = get_local_version(LOCAL_GAME_VERSION)
    local_launcher = get_local_version(LOCAL_LAUNCHER_VERSION)

    msg = ""
    restart_needed = False

    # Prüfen ob online Version höher ist
    if online_game and online_game > local_game:
        msg += f"Neue Spiel-Version verfügbar: {online_game}\n"
        restart_needed = True

    if online_launcher and online_launcher > local_launcher:
        msg += f"Neue Launcher-Version verfügbar: {online_launcher}\n"
        restart_needed = True

    if restart_needed:
        messagebox.showinfo("Update verfügbar", msg + "\nBitte Launcher neu starten!")
    else:
        messagebox.showinfo("Up-to-date", "Alles ist auf dem neuesten Stand ✅")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🦊 The Fox Launcher")
root.geometry("450x300")
root.resizable(False, False)

title = tk.Label(root, text="🦊 The Fox Launcher", font=("Arial", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="Launcher bereit", font=("Arial", 10))
status_label.pack(pady=5)

play_btn = tk.Button(root, text="▶ Spielen", width=35, command=start_game)
play_btn.pack(pady=5)

force_quit_btn = tk.Button(root, text="⛔ Spiel zwangsweise beenden", width=35, command=force_quit_game)
force_quit_btn.pack(pady=5)

check_update_btn = tk.Button(root, text="⬆ Updates prüfen", width=35, command=check_updates)
check_update_btn.pack(pady=5)

quit_launcher_btn = tk.Button(root, text="❌ Launcher beenden", width=35, command=quit_launcher)
quit_launcher_btn.pack(pady=5)

root.mainloop()
