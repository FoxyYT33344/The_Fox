import os
import sys
import subprocess
import urllib.request
import tkinter as tk
from tkinter import messagebox

# ---------------- Pfade ----------------
FOLDER = os.path.dirname(__file__)
GAME_FILE = os.path.join(FOLDER, "The_Fox.py")
LOCAL_VERSION_FILE = os.path.join(FOLDER, "version.py")

# ---------------- GitHub-Links ----------------
GAME_VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/version.py"
LAUNCHER_RAW_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox_launcher.py"

# ---------------- Spiel-Prozess ----------------
game_process = None

# ---------------- Versionen laden ----------------
def get_local_version():
    if not os.path.exists(LOCAL_VERSION_FILE):
        return "0.0.0"
    data = {}
    with open(LOCAL_VERSION_FILE) as f:
        exec(f.read(), data)
    return data.get("VERSION", "0.0.0")

def get_online_version(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
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
    if game_process is None:
        messagebox.showwarning("Info", "Kein Spiel läuft gerade.")
        return
    try:
        game_process.terminate()
        status_label.config(text="Spiel zwangsweise beendet ❌")
        game_process = None
    except Exception as e:
        messagebox.showerror("Fehler", f"Konnte Spiel nicht beenden: {e}")

# ---------------- Update für Spiel ----------------
def update_game():
    online_version = get_online_version(GAME_VERSION_URL)
    local_version = get_local_version()
    if online_version is None:
        messagebox.showerror("Fehler", "Konnte Online-Version nicht abrufen.")
        return
    if online_version == local_version:
        messagebox.showinfo("Info", "Spiel ist auf dem neuesten Stand ✅")
        return

    # Update bestätigen
    if not messagebox.askyesno("Update verfügbar", f"Neue Version {online_version} verfügbar. Update jetzt?"):
        return

    try:
        urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox.py",
            GAME_FILE
        )
        urllib.request.urlretrieve(GAME_VERSION_URL, LOCAL_VERSION_FILE)
        messagebox.showinfo("Update", "Spiel erfolgreich aktualisiert! ✅")
    except Exception as e:
        messagebox.showerror("Fehler", f"Update fehlgeschlagen: {e}")

# ---------------- Update für Launcher ----------------
def update_launcher():
    online_version = get_online_version(GAME_VERSION_URL)
    local_version = get_local_version()
    if online_version is None:
        messagebox.showerror("Fehler", "Konnte Online-Version nicht abrufen.")
        return
    if online_version == local_version:
        messagebox.showinfo("Info", "Launcher ist auf dem neuesten Stand ✅")
        return

    if not messagebox.askyesno("Launcher Update", f"Neue Version verfügbar. Update Launcher jetzt?"):
        return

    try:
        urllib.request.urlretrieve(LAUNCHER_RAW_URL, os.path.join(FOLDER, "The_Fox_launcher.py"))
        messagebox.showinfo("Update", "Launcher erfolgreich aktualisiert! Bitte neu starten ✅")
    except Exception as e:
        messagebox.showerror("Fehler", f"Launcher Update fehlgeschlagen: {e}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🦊 The Fox Launcher")
root.geometry("450x250")
root.resizable(False, False)

title = tk.Label(root, text="🦊 The Fox Launcher", font=("Arial", 16, "bold"))
title.pack(pady=10)

status_label = tk.Label(root, text="Launcher bereit", font=("Arial", 10))
status_label.pack(pady=5)

play_btn = tk.Button(root, text="▶ Spielen", width=35, command=start_game)
play_btn.pack(pady=5)

force_quit_btn = tk.Button(root, text="⛔ Spiel zwangsweise beenden", width=35, command=force_quit_game)
force_quit_btn.pack(pady=5)

update_game_btn = tk.Button(root, text="⬆ Spiel aktualisieren", width=35, command=update_game)
update_game_btn.pack(pady=5)

update_launcher_btn = tk.Button(root, text="⬆ Launcher aktualisieren", width=35, command=update_launcher)
update_launcher_btn.pack(pady=5)

root.mainloop()
