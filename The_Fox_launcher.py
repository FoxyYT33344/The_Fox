import tkinter as tk
from tkinter import messagebox
import urllib.request
import subprocess
import sys
import os

# =====================
# VERSION & URLS
# =====================
LAUNCHER_VERSION = "1.2.1"

# Achte darauf, dass dieser Pfad exakt stimmt (Raw-Link nutzen!)
VERSION_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/version.launcher.py"
GAME_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox.py"
UPDATER_URL = "https://raw.githubusercontent.com/FoxyYT33344/The_Fox/main/The_Fox_Launcher_update.py"

GAME_FILE = "The_Fox.py"
UPDATE_FILE = "The_Fox_Launcher_update.py"

# =====================
# FUNKTIONEN
# =====================

def get_online_launcher_version():
    """Liest die Online-Version vom GitHub Repository"""
    try:
        with urllib.request.urlopen(VERSION_URL, timeout=5) as response:
            content = response.read().decode("utf-8")
            # Wir suchen nach einer Zeile wie: VERSION = "1.2.2"
            for line in content.splitlines():
                if "VERSION" in line:
                    return line.split("=")[1].strip().replace('"', "").replace("'", "")
    except Exception as e:
        print(f"Versions-Check Fehler: {e}")
    return None

def is_update_available(local, online):
    """Vergleicht Versionsnummern (z.B. 1.2.1 < 1.2.2)"""
    try:
        local_parts = [int(p) for p in local.split('.')]
        online_parts = [int(p) for p in online.split('.')]
        return online_parts > local_parts
    except:
        # Fallback auf einfachen String-Vergleich
        return online > local

def download_updater_if_missing():
    """Lädt den Updater herunter, falls er nicht existiert"""
    if not os.path.exists(UPDATE_FILE):
        try:
            urllib.request.urlretrieve(UPDATER_URL, UPDATE_FILE)
            return True
        except:
            return False
    return True

def check_launcher_update():
    """Prüft auf Updates und startet den Updater-Prozess"""
    online_version = get_online_launcher_version()
    
    if online_version and is_update_available(LAUNCHER_VERSION, online_version):
        update = messagebox.askyesno(
            "Update verfügbar",
            f"Neue Launcher-Version verfügbar!\n\n"
            f"Deine Version: {LAUNCHER_VERSION}\n"
            f"Neue Version: {online_version}\n\n"
            f"Möchtest du den Launcher jetzt aktualisieren?"
        )
        if update:
            if download_updater_if_missing():
                try:
                    # Updater starten und Launcher schließen
                    subprocess.Popen([sys.executable, UPDATE_FILE])
                    root.destroy()
                    sys.exit()
                except Exception as e:
                    messagebox.showerror("Fehler", f"Updater konnte nicht gestartet werden:\n{e}")
            else:
                messagebox.showerror("Fehler", "Die Update-Hilfsdatei konnte nicht heruntergeladen werden.")
    elif online_version:
        messagebox.showinfo("Launcher", "Du nutzt bereits die neueste Version.")
    else:
        messagebox.showwarning("Fehler", "Die Online-Version konnte nicht ermittelt werden.\nPrüfe deine Internetverbindung.")

def install_game():
    """Installiert das Spiel von GitHub"""
    try:
        urllib.request.urlretrieve(GAME_URL, GAME_FILE)
        messagebox.showinfo("Installation", "Spiel wurde erfolgreich installiert!")
        refresh_button()
    except Exception as e:
        messagebox.showerror("Fehler", f"Installation fehlgeschlagen:\n{e}")

def uninstall_game():
    """Deinstalliert das Spiel"""
    if not os.path.exists(GAME_FILE):
        return

    if messagebox.askyesno("Löschen", "Möchtest du das Spiel wirklich löschen?"):
        try:
            os.remove(GAME_FILE)
            messagebox.showinfo("Erfolg", "Spiel wurde gelöscht!")
            refresh_button()
        except Exception as e:
            messagebox.showerror("Fehler", f"Löschen fehlgeschlagen:\n{e}")

def start_game():
    """Startet das Spiel oder installiert es"""
    if not os.path.exists(GAME_FILE):
        if messagebox.askyesno("Nicht installiert", "Spiel installieren?"):
            install_game()
        return

    try:
        subprocess.Popen([sys.executable, GAME_FILE])
    except Exception as e:
        messagebox.showerror("Fehler", f"Start fehlgeschlagen:\n{e}")

def refresh_button():
    """Aktualisiert den Button-Zustand"""
    global action_button
    if action_button:
        action_button.destroy()

    if os.path.exists(GAME_FILE):
        action_button = tk.Button(root, text="🗑 Spiel deinstallieren", width=36, height=2, command=uninstall_game, bg="#ffcccc")
    else:
        action_button = tk.Button(root, text="⬇ Spiel installieren", width=36, height=2, command=install_game, bg="#ccffcc")
    action_button.pack(pady=10)

# =====================
# GUI SETUP
# =====================
root = tk.Tk()
root.title("🦊 Fox Launcher")
root.geometry("440x420")
root.resizable(False, False)

tk.Label(root, text="🦊 Fox Launcher", font=("Arial", 22, "bold")).pack(pady=15)
tk.Label(root, text=f"Version: {LAUNCHER_VERSION}", font=("Arial", 10)).pack(pady=2)

action_button = None
refresh_button()

tk.Button(root, text="▶ Spiel starten", width=36, height=2, command=start_game).pack(pady=5)
tk.Button(root, text="🔄 Nach Launcher-Updates suchen", width=36, height=2, command=check_launcher_update).pack(pady=5)
tk.Button(root, text="❌ Beenden", width=36, height=2, command=root.destroy).pack(pady=10)

root.mainloop()
