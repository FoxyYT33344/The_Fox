import os
import sys
import subprocess
import urllib.request
import tkinter as tk
from tkinter import messagebox

# ---------------- Pfade ----------------
FOLDER = os.path.dirname(__file__)
GAME_FILE = os.path.join(FOLDER, "The_Fox.py")
VERSION_FILE = os.path.join(FOLDER, "version.py")

# ---------------- GitHub-Links ----------------
GAME_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox.py"
VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/version.py"

game_process = None

# ---------------- Version ----------------
def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return "0.0.0"
    data = {}
    with open(VERSION_FILE, "r") as f:
        exec(f.read(), data)
    return data.get("VERSION", "0.0.0")

def get_online_version():
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as r:
            data = {}
            exec(r.read().decode(), data)
            return data.get("VERSION", "0.0.0")
    except:
        return None

def parse_version(v):
    return [int(x) for x in v.split(".")]

# ---------------- Spiel starten ----------------
def start_game():
    global game_process
    if not os.path.exists(GAME_FILE):
        messagebox.showerror("Fehler", "Spiel ist nicht installiert.")
        return
    game_process = subprocess.Popen([sys.executable, GAME_FILE])
    status_label.config(text="Spiel läuft ✅")

# ---------------- Spiel beenden ----------------
def force_quit_game():
    global game_process
    if game_process:
        game_process.terminate()
        game_process = None
        status_label.config(text="Spiel beendet ❌")

# ---------------- Installieren ----------------
def install_game():
    try:
        urllib.request.urlretrieve(GAME_URL, GAME_FILE)
        messagebox.showinfo("Erfolg", "Spiel wurde installiert ✅")
        status_label.config(text="Spiel installiert")
        update_install_button()
    except Exception as e:
        messagebox.showerror("Fehler", f"Installation fehlgeschlagen:\n{e}")

# ---------------- Deinstallieren ----------------
def uninstall_game():
    if not messagebox.askyesno(
        "Bestätigung",
        "Willst du das Spiel wirklich löschen?"
    ):
        return

    if not messagebox.askyesno(
        "Letzte Warnung",
        "Bist du dir GANZ sicher?\nDas Spiel wird gelöscht!"
    ):
        return

    try:
        if os.path.exists(GAME_FILE):
            os.remove(GAME_FILE)
        messagebox.showinfo("Fertig", "Spiel wurde gelöscht 🗑️")
        status_label.config(text="Spiel nicht installiert")
        update_install_button()
    except Exception as e:
        messagebox.showerror("Fehler", f"Konnte Spiel nicht löschen:\n{e}")

# ---------------- Update prüfen ----------------
def check_updates():
    online = get_online_version()
    local = get_local_version()

    if not online:
        messagebox.showwarning("Offline", "Keine Verbindung möglich")
        return

    if parse_version(online) > parse_version(local):
        messagebox.showinfo(
            "Update verfügbar",
            f"Neue Version: {online}\nBitte Launcher neu starten"
        )
    else:
        messagebox.showinfo("OK", "Spiel ist aktuell ✅")

# ---------------- Install / Deinstall Button ----------------
def update_install_button():
    if os.path.exists(GAME_FILE):
        install_btn.config(
            text="🗑️ Spiel deinstallieren",
            command=uninstall_game
        )
    else:
        install_btn.config(
            text="⬇ Spiel installieren",
            command=install_game
        )

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🦊 The Fox Launcher")
root.geometry("460x420")
root.resizable(False, False)

tk.Label(
    root,
    text="🦊 The Fox Launcher",
    font=("Arial", 16, "bold")
).pack(pady=10)

status_label = tk.Label(root, text="Launcher bereit", font=("Arial", 10))
status_label.pack(pady=5)

tk.Button(
    root,
    text="▶ Spielen",
    width=40,
    command=start_game
).pack(pady=5)

tk.Button(
    root,
    text="⛔ Spiel zwangsweise beenden",
    width=40,
    command=force_quit_game
).pack(pady=5)

tk.Button(
    root,
    text="⬆ Updates prüfen",
    width=40,
    command=check_updates
).pack(pady=5)

install_btn = tk.Button(root, width=40)
install_btn.pack(pady=10)

update_install_button()

tk.Button(
    root,
    text="❌ Launcher beenden",
    width=40,
    command=root.destroy
).pack(pady=5)

root.mainloop()
