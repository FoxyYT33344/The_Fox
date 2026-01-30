import tkinter as tk
from tkinter import messagebox
import urllib.request
import subprocess
import sys
import os

# =====================
# VERSION
# =====================
LAUNCHER_VERSION = "1.08"

VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/version.py"
GAME_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox.py"
GAME_FILE = "The_Fox.py"
UPDATE_FILE = "The_Fox_Launcher_update.py"

# =====================
# FUNKTIONEN
# =====================

def get_online_version():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            content = response.read().decode("utf-8")
            for line in content.splitlines():
                if line.startswith("VERSION"):
                    return line.split("=")[1].strip().replace('"', "")
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Abrufen der Version:\n{e}")
    return None


def check_update():
    online_version = get_online_version()
    if not online_version:
        return

    if online_version > LAUNCHER_VERSION:
        if messagebox.askyesno(
            "Update verfügbar",
            f"Neue Launcher-Version gefunden!\n\n"
            f"Deine Version: {LAUNCHER_VERSION}\n"
            f"Neue Version: {online_version}\n\n"
            f"Jetzt aktualisieren?"
        ):
            subprocess.Popen([sys.executable, UPDATE_FILE])
            root.destroy()
    else:
        messagebox.showinfo("Launcher", "Launcher ist auf dem neuesten Stand.")


def install_game():
    try:
        urllib.request.urlretrieve(GAME_URL, GAME_FILE)
        messagebox.showinfo("Installation", "Spiel wurde erfolgreich installiert!")
    except Exception as e:
        messagebox.showerror("Fehler", f"Installation fehlgeschlagen:\n{e}")


def start_game():
    if not os.path.exists(GAME_FILE):
        install = messagebox.askyesno(
            "Spiel nicht installiert",
            "Das Spiel ist nicht installiert.\n\nWillst du das Spiel installieren?"
        )

        if install:
            install_game()
        else:
            messagebox.showinfo("Schade...", "Schade… 😿")
        return

    subprocess.Popen([sys.executable, GAME_FILE])


def exit_launcher():
    root.destroy()

# =====================
# GUI
# =====================

root = tk.Tk()
root.title("Fox Launcher")
root.geometry("420x320")
root.resizable(False, False)

tk.Label(
    root,
    text="🦊 Fox Launcher",
    font=("Arial", 20, "bold")
).pack(pady=10)

tk.Label(
    root,
    text=f"Launcher Version: {LAUNCHER_VERSION}"
).pack(pady=5)

tk.Button(
    root,
    text="▶ Spiel starten",
    width=32,
    command=start_game
).pack(pady=6)

tk.Button(
    root,
    text="🔄 Nach Updates suchen",
    width=32,
    command=check_update
).pack(pady=6)

tk.Button(
    root,
    text="❌ Launcher beenden",
    width=32,
    command=exit_launcher
).pack(pady=12)

root.mainloop()
