from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

# ==========================
# EINSTELLUNGEN
# ==========================

SAVE_FILE = "savegame.json"
RESPAWN_HEIGHT = -10
RESPAWN_POINT = Vec3(0, 5, 0)

window.icon = 'The_Fox.png'
window.title = 'The Fox 🦊'

app = Ursina()

# ==========================
# HAUPTMENÜ
# ==========================

menu_ui = Entity(enabled=True)
Entity(parent=menu_ui, model='quad', scale=(16,9), color=color.azure)
Text(text="🦊 The Fox", parent=menu_ui, scale=3, position=(0,0.3,0), origin=(0,0))

play_button = Button(
    text="▶ Spiel starten",
    scale=(0.3,0.1),
    position=(0,0,0),
    color=color.green,
    parent=menu_ui
)

quit_button = Button(
    text="❌ Beenden",
    scale=(0.3,0.1),
    position=(0,-0.15,0),
    color=color.red,
    parent=menu_ui
)

# ==========================
# PAUSE MENÜ
# ==========================

pause_ui = Entity(enabled=False, parent=camera.ui)

Entity(
    parent=pause_ui,
    model='quad',
    scale=(0.8, 0.8),
    color=color.rgba(0, 0, 0, 200),
    z=1
)

Text(
    text="PAUSE",
    parent=pause_ui,
    scale=2,
    position=(0, 0.25, 0),
    origin=(0,0),
    z=2
)

btn_resume = Button(
    text="▶ Zurück zum Spiel",
    parent=pause_ui,
    scale=(0.4, 0.08),
    position=(0, 0.08, 0),
    color=color.green,
    z=2
)

btn_save = Button(
    text="💾 Speichern",
    parent=pause_ui,
    scale=(0.4, 0.08),
    position=(0, -0.02, 0),
    color=color.azure,
    z=2
)

btn_menu = Button(
    text="🏠 Zum Hauptmenü",
    parent=pause_ui,
    scale=(0.4, 0.08),
    position=(0, -0.12, 0),
    color=color.orange,
    z=2
)

btn_exit = Button(
    text="❌ Beenden & Speichern",
    parent=pause_ui,
    scale=(0.4, 0.08),
    position=(0, -0.22, 0),
    color=color.red,
    z=2
)

# ==========================
# SPIEL-DATEN
# ==========================

player = None
hotbar = []
inventory_ui = None
inventory_open = False
selected_slot = 0

items = [
    "Holz", "Stein", "Schaufel", "Schwert",
    "Fackel", "Pfeil", "Bogen", "Essen", "Trank"
]

# ==========================
# SPEICHERN & LADEN
# ==========================

def save_game():
    if not player:
        return

    data = {
        "player_position": [player.x, player.y, player.z],
        "selected_slot": selected_slot
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

    print("✅ Spiel gespeichert!")

def load_game():
    global selected_slot

    if os.path.exists(SAVE_FILE) and player:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            player.position = Vec3(*data["player_position"])
            selected_slot = data.get("selected_slot", 0)
            highlight_slot(selected_slot)
        print("📂 Spielstand geladen!")

# ==========================
# SPIEL STARTEN
# ==========================

def start_game():
    global player, hotbar, inventory_ui

    menu_ui.enabled = False
    pause_ui.enabled = False

    player = FirstPersonController()
    player.gravity = 0.5
    player.position = RESPAWN_POINT

    ground = Entity(
        model='plane',
        scale=64,
        texture='white_cube',
        texture_scale=(64,64),
        collider='box',
        color=color.dark_gray
    )

    Entity(
        model='cube',
        color=color.orange,
        scale=2,
        position=(3,1,3),
        collider='box'
    )

    # -------- HOTBAR --------
    hotbar.clear()
    for i in range(9):
        slot_bg = Entity(
            model='quad',
            scale=(0.08,0.08),
            color=color.gray,
            origin=(0,0),
            parent=camera.ui,
            x=-0.36 + i*0.08,
            y=-0.42
        )

        Text(
            text=items[i],
            parent=slot_bg,
            scale=0.5,
            y=-0.02
        )

        hotbar.append(slot_bg)

    highlight_slot(selected_slot)

    # -------- INVENTAR --------
    inventory_ui = Entity(parent=camera.ui, enabled=False)
    Entity(
        parent=inventory_ui,
        model='quad',
        scale=(0.5,0.5),
        color=color.rgba(50,50,50,200)
    )

    load_game()

# ==========================
# HOTBAR HIGHLIGHT
# ==========================

def highlight_slot(slot_index):
    for i, bg in enumerate(hotbar):
        bg.color = color.yellow if i == slot_index else color.gray

# ==========================
# INPUT
# ==========================

def input(key):
    global selected_slot, inventory_open

    # Hotbar 1-9
    if key.isdigit() and int(key) in range(1,10):
        selected_slot = int(key)-1
        highlight_slot(selected_slot)

    # Inventar öffnen/schließen
    elif key == 'i':
        inventory_open = not inventory_open
        if inventory_ui:
            inventory_ui.enabled = inventory_open

    # Pause-Menü
    elif key == 'escape':
        pause_ui.enabled = not pause_ui.enabled
        mouse.locked = not pause_ui.enabled

# ==========================
# PAUSE BUTTONS
# ==========================

btn_resume.on_click = lambda: (
    setattr(pause_ui, "enabled", False),
    player.enable(),
    setattr(mouse, "locked", True)
)

btn_save.on_click = save_game

btn_menu.on_click = lambda: (
    save_game(),
    setattr(pause_ui, "enabled", False),
    setattr(menu_ui, "enabled", True),
    destroy(player)
)

btn_exit.on_click = lambda: (
    save_game(),
    application.quit()
)

play_button.on_click = start_game
quit_button.on_click = application.quit

# ==========================
# RESPPAWN LOGIK
# ==========================

def update():
    if player:
        if player.y < RESPAWN_HEIGHT:
            print("⚠️ Du bist gefallen! Respawn...")
            player.position = RESPAWN_POINT

# ==========================
# SPIEL STARTEN
# ==========================

app.run()

