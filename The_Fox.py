from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

SAVE_FILE = "savegame.json"

window.icon = 'The_Fox.png'
window.title = 'The Fox 🦊'

app = Ursina()

# ---------------- Variablen ----------------
inventory = ["Leer"] * 9
selected_slot = 0
inventory_open = False

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
exit_button = Button(text="🏠 Hauptmenü", scale=(0.4,0.1), position=(0,-0.1,0), color=color.orange, parent=pause_ui)

# ---------------- Inventar UI ----------------
hotbar = []
hotbar_ui = Entity(parent=camera.ui, position=(0, -0.4))

def setup_hotbar():
    for i in range(9):
        slot = Entity(
            parent=hotbar_ui,
            model='quad',
            scale=(0.1, 0.1),
            x=(i - 4) * 0.11,
            color=color.gray,
            texture='white_cube'
        )
        item_text = Text(text=inventory[i], parent=slot, scale=0.5, origin=(0,0), y=-0.1)
        hotbar.append((slot, item_text))
    highlight_slot(0)

def highlight_slot(index):
    for i, (slot, _) in enumerate(hotbar):
        slot.color = color.yellow if i == index else color.gray

def update_hotbar_text():
    for i, (_, text_entity) in enumerate(hotbar):
        text_entity.text = inventory[i]

# ---------------- Welt & Spieler ----------------
ground = Entity(model='plane', scale=100, texture='grass', collider='mesh', enabled=False)
player = FirstPersonController(enabled=False, y=2)
sky = Sky()

# Objekte
dachs = Entity(model='cube', color=color.brown, scale=(1, 0.5, 1.5), position=(5, 0.25, 5), collider='box', enabled=False)
dachs_label = Text(text="Dachs", parent=dachs, y=2, scale=5, billboard=True, enabled=False)

kugel = Entity(model='sphere', color=color.blue, scale=0.5, position=(-3, 0.5, 3), collider='sphere', enabled=False)

# ---------------- Logik ----------------
def start_game():
    menu_ui.enabled = False
    ground.enabled = True
    player.enabled = True
    dachs.enabled = True
    kugel.enabled = True
    setup_hotbar()
    load_game()

def save_game():
    data = {
        "pos": [player.x, player.y, player.z],
        "inventory": inventory
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    global inventory
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            player.position = data.get("pos", (0,2,0))
            inventory = data.get("inventory", ["Leer"] * 9)
            update_hotbar_text()

play_button.on_click = start_game
quit_button.on_click = application.quit
resume_button.on_click = lambda: setattr(pause_ui, 'enabled', False) or player.enable()

def input(key):
    global selected_slot
    if not player.enabled and not pause_ui.enabled: return

    # Hotbar Auswahl
    if key in '123456789':
        selected_slot = int(key) - 1
        highlight_slot(selected_slot)

    # Interaktion
    if key == 'e':
        # Kugel aufheben
        if distance(player, kugel) < 3 and kugel.enabled:
            for i in range(9):
                if inventory[i] == "Leer":
                    inventory[i] = "Kugel"
                    kugel.enabled = False
                    update_hotbar_text()
                    break
        
        # Kugel dem Dachs geben
        elif distance(player, dachs) < 3:
            if inventory[selected_slot] == "Kugel":
                inventory[selected_slot] = "Leer"
                update_hotbar_text()
                message = Text(text="Danke für die Kugel! 🦊❤️", position=(0,0.4), origin=(0,0), scale=2, color=color.yellow)
                destroy(message, delay=2)
            else:
                message = Text(text="Du hast keine Kugel in der Hand!", position=(0,0.4), origin=(0,0), scale=2, color=color.red)
                destroy(message, delay=2)

    if key == 'escape':
        pause_ui.enabled = not pause_ui.enabled
        player.enabled = not pause_ui.enabled
        mouse.locked = not pause_ui.enabled

def update():
    if ground.enabled:
        # Dachs Label anzeigen wenn nah dran
        dachs_label.enabled = distance(player, dachs) < 5

app.run()
