import os
import sys
import subprocess
import urllib.request
import tkinter as tk
from tkinter import messagebox
import threading
import time

# ------------------ Ordner & Dateien ------------------
FOLDER = os.path.dirname(__file__)
GAME_FILE = os.path.join(FOLDER, "The_Fox.py")
LOCAL_VERSION_FILE = os.path.join(FOLDER, "local_version.py")

VERSION_URL = "https://raw.githubusercontent.com/DEINNAME/The_Fox_Updates/main/version.py"
GAME_URL = "https://raw.githubusercontent.com/DEINNAME/The_Fox_Updates/main/The_Fox.py"

# ------------------ Globale Variablen ------------------
game_process = None
checker_thread = None

# ------------------ Versions-Funktionen ------------------
def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    data = {}
    with open(LOCAL_VERSION_FILE, "r") as f:
        exec(f.read(), data)
    return data.get("VERSION", "0.0.0")

def get_online_version():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=3) as r:
            data = {}
            exec(r.read().decode(), data)
            return data.get("VERSION")
    except:
        return None

def save_local_version(v):
    with open(LOCAL_VERSION_FILE, "w") as f:
        f.write(f'VERSION = "{v}"')

def download_game():
    urllib.request.urlretrieve(GAME_URL, GAME_FILE)

# ------------------ Spiel starten ------------------
def start_game():
    global game_process, checker_thread
    if not os.path.exists(GAME_FILE):
        messagebox.showerror("Fehler", "Spiel ist nicht installiert.")
        return

    if sys.platform == "win32":
        game_process = subprocess.Popen([sys.executable, GAME_FILE],
                                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        game_process = subprocess.Popen([sys.executable, GAME_FILE], start_new_session=True)

    status_label.config(text="Spiel gestartet! Launcher überwacht das Spiel ✅")

    if checker_thread is None:
        checker_thread = threading.Thread(target=monitor_game, daemon=True)
        checker_thread.start()

# ------------------ Crash-Monitor ------------------
def monitor_game():
    global game_process
    while True:
        if game_process:
            ret = game_process.poll()
            if ret is not None:
                root.after(0, lambda: crashed_prompt())
                game_process = None
        time.sleep(1)

def crashed_prompt():
    response = messagebox.askyesno(
        "Spiel beendet",
        "Ist das Spiel abgestürzt?\n\nJa → Neustart\nNein → Launcher schließen"
    )
    if response:
        start_game()
    else:
        root.destroy()
        sys.exit()

# ------------------ Zwangsbeenden ------------------
def force_quit_game():
    global game_process
    if game_process is None:
        messagebox.showwarning("Info", "Kein Spiel läuft gerade.")
        return

    try:
        if sys.platform == "win32":
            subprocess.call(f"taskkill /F /PID {game_process.pid}", shell=True)
        else:
            game_process.terminate()
        status_label.config(text="Spiel wurde zwangsweise beendet ❌")
        game_process = None
    except Exception as e:
        messagebox.showerror("Fehler", f"Konnte Spiel nicht beenden: {e}")

# ------------------ Update-Funktion ------------------
def update_game():
    online = get_online_version()
    if online is None:
        messagebox.showwarning(
            "Offline",
            "Kein Internet.\nOffline spielen möglich,\naber evtl. nicht neueste Version :("
        )
        return

    local = get_local_version()
    if local == online:
        messagebox.showinfo("Info", "Spiel ist bereits aktuell ✅")
        return

    if messagebox.askyesno(
        "Update verfügbar",
        f"Neue Version verfügbar:\n{local} → {online}\n\nUpdate installieren?"
    ):
        download_game()
        save_local_version(online)
        messagebox.showinfo("Fertig", "Update erfolgreich installiert ✅")
        update_status()

# ------------------ Statusanzeige ------------------
def update_status():
    online = get_online_version()
    local = get_local_version()
    if online is None:
        status_label.config(
            text=f"Status: Offline spielen\nVersion: {local} (evtl. nicht neueste)"
        )
    else:
        status_label.config(
            text=f"Status: Online\nVersion: {local} (Server: {online})"
        )

# ------------------ Launcher schließen ------------------
def on_close():
    if messagebox.askyesno("FuchsWelt verlassen", "Wollen Sie wirklich die FuchsWelt verlassen :((("):
        # Optional: Spielprozess schließen, wenn gewünscht
        if game_process:
            try:
                if sys.platform == "win32":
                    subprocess.call(f"taskkill /F /PID {game_process.pid}", shell=True)
                else:
                    game_process.terminate()
            except:
                pass
        root.destroy()
        sys.exit()

# ------------------ GUI ------------------
root = tk.Tk()
root.title("The Fox Launcher 🦊")
root.geometry("400x350")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_close)

title = tk.Label(root, text="🦊 The Fox Launcher", font=("Arial", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

play_btn = tk.Button(root, text="▶ Spielen", width=30, command=start_game)
play_btn.pack(pady=5)

update_btn = tk.Button(root, text="🔄 Update prüfen", width=30, command=update_game)
update_btn.pack(pady=5)

offline_btn = tk.Button(root, text="📴 Offline spielen", width=30, command=start_game)
offline_btn.pack(pady=5)

force_quit_btn = tk.Button(root, text="⛔ Spiel zwangsweise beenden", width=30, command=force_quit_game)
force_quit_btn.pack(pady=5)

update_status()
root.mainloop()
