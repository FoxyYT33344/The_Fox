import os
import sys
import subprocess

def start_game():
    # Pfad zum Spiel
    game_file = os.path.join(os.path.dirname(__file__), "The_Fox.py")

    if not os.path.exists(game_file):
        print("❌ The_Fox.py wurde nicht gefunden!")
        return

    # Spiel mit demselben Python starten
    subprocess.Popen([sys.executable, game_file])

if __name__ == "__main__":
    print("🦊 The Fox Launcher startet...")
    start_game()
