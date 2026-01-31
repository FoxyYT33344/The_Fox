from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

SAVE_FILE = "savegame.json"

window.icon = 'The_Fox.png'
window.title = 'The Fox 🦊'

app = Ursina()

# ---------------- Hauptmenü ----------------
menu_ui = Entity()
menu_background = Entity(parent=menu_ui, model='quad', scale=(16,9), color=color.azure)
title = Text(text="🦊 The Fox", parent=menu_ui, scale=3, position=(0,0.3,0), origin=(0,0))
play_button = Button(text="▶ Spiel starten", scale=(0.3,0.1), position=(0,0,0), color=color.green, parent=menu_ui)
quit_button = Button(text="❌ Beenden", scale=(0.3,0.1), position=(0,-0.15,0), color=color.red, parent=menu_ui)

# ---------------- Pause-Menü ----------------
pause_ui = Entity(enabled=False)
pause_bg = Entity(parent=pause_ui, model='quad', scale=(0.5,0.5), color=color.rgba(0,0,0,200))
resume_button = Button(text="▶ Zurück zum Spiel", scale=(0.4,0.1), position=(0,0.05,0), color=color.green, parent=pause_ui)
exit_button = Button(text="❌ Beenden", scale=(0.4,0.1), position=(0,-0.15,0), color=color.red, parent=pause_ui)

# ---------------- 3D-Spielwelt ----------------
player = None
hotbar = []
inventory_ui = None
inventory_open = False
selected_slot = 0
items = ["Holz", "Stein", "Schaufel", "Schwert", "Fackel", "Pfeil", "Bogen", "Essen", "Trank"]

# ---------------- Spielstand ----------------
def save_game():
    if not player:
        return
    data = {
        "player_position": [player.x, player.y, player.z],
        "selected_slot": selected_slot
        # weitere Daten wie Inventar kannst du hier hinzufügen
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("Spiel gespeichert!")

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            if player:
                player.position = Vec3(*data["player_position"])
            global selected_slot
            selected_slot = data.get("selected_slot", 0)
            highlight_slot(selected_slot)
        print("Spielstand geladen!")

# ---------------- Spiel starten ----------------
def start_game():
    global player, hotbar, inventory_ui
    menu_ui.visible = False
    player = FirstPersonController()
    player.gravity = 0.5
    player.cursor.visible = True

    # Boden
    ground = Entity(model='plane', scale=64, texture='white_cube', texture_scale=(64,64),
                    collider='box', color=color.dark_gray)

    # Beispiel-Objekt
    box = Entity(model='cube', color=color.orange, scale=2, position=(3,1,3), collider='box')

    # Hotbar
    hotbar.clear()
    for i in range(9):
        slot_bg = Entity(model='quad', scale=(0.08,0.08), color=color.gray, origin=(0,0),
                         parent=camera.ui, x=-0.36 + i*0.08, y=-0.42)
        slot_text = Text(text=items[i], parent=slot_bg, scale=0.5, y=-0.02)
        hotbar.append((slot_bg, slot_text))
    highlight_slot(selected_slot)

    # Inventar unsichtbar
    inventory_ui = Entity(parent=camera.ui, enabled=False)
    inv_bg = Entity(parent=inventory_ui, model='quad', scale=(0.5,0.5), color=color.rgba(50,50,50,200))

    load_game()  # Spielstand laden beim Start

# ---------------- Hotbar ----------------
def highlight_slot(slot_index):
    for i, (bg, _) in enumerate(hotbar):
        bg.color = color.yellow if i == slot_index else color.gray

# ---------------- Eingaben ----------------
def input(key):
    global selected_slot, inventory_open
    if key.isdigit() and int(key) in range(1,10):
        selected_slot = int(key)-1
        highlight_slot(selected_slot)
    elif key == 'i':
        inventory_open = not inventory_open
        if inventory_ui:
            inventory_ui.enabled = inventory_open
    elif key == 'escape':
        if pause_ui.enabled:
            pause_ui.enabled = False
            player.enable()
        else:
            pause_ui.enabled = True
            player.disable()
    elif key == 'f5':
        save_game()  # z.B. F5 = Spiel speichern

# ---------------- Buttons ----------------
resume_button.on_click = lambda: setattr(pause_ui, 'enabled', False) or player.enable()
exit_button.on_click = application.quit
play_button.on_click = start_game
quit_button.on_click = application.quit

app.run()
