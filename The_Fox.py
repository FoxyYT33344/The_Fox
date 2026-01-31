from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

SAVE_FILE = "savegame.json"

app = Ursina()
window.title = "🦊 The Fox"
window.borderless = False
window.fullscreen = False

# ======== APP ICON ========
if os.path.exists("The_Fox.png"):
    app.icon = "The_Fox.png"

# ======================================
# HAUPTMENÜ
# ======================================
menu_ui = Entity()
Entity(parent=menu_ui, model='quad', scale=(16,9), color=color.azure)
Text(text="🦊 The Fox", parent=menu_ui, scale=3, position=(0,0.3), origin=(0,0))

def start_game():
    menu_ui.disable()
    start_world()

def quit_game():
    application.quit()

Button(text="▶ Spiel starten", scale=(0.3,0.1), position=(0,0), color=color.green, parent=menu_ui, on_click=start_game)
Button(text="❌ Beenden", scale=(0.3,0.1), position=(0,-0.15), color=color.red, parent=menu_ui, on_click=quit_game)

# ======================================
# SPIELWELT
# ======================================
player = None
ground = None

def start_world():
    global player, ground

    player = FirstPersonController()
    player.gravity = 0.5

    ground = Entity(
        model='plane',
        scale=64,
        texture='white_cube',
        texture_scale=(64,64),
        collider='box',
        color=color.dark_gray
    )

    # Beispiel-Objekte
    Entity(model='cube', color=color.orange, scale=2, position=(3,1,3), collider='box')
    Entity(model='cube', color=color.lime, scale=2, position=(-3,1,-3), collider='box')

    load_game()

    create_hotbar()
    create_inventory()
    create_pause_menu()

# ======================================
# HOTBAR (9 SLOTS)
# ======================================
hotbar = []
selected_slot = 0

def create_hotbar():
    for i in range(9):
        slot = Button(
            text=str(i+1),
            scale=(0.08, 0.08),
            position=(-0.4 + i*0.1, -0.45),
            color=color.gray
        )
        hotbar.append(slot)

def update_hotbar():
    for i, slot in enumerate(hotbar):
        slot.color = color.gold if i == selected_slot else color.gray

def input(key):
    global selected_slot

    if key in "123456789":
        selected_slot = int(key) - 1
        update_hotbar()

    if key == "e":
        toggle_inventory()

    if key == "escape":
        toggle_pause()

# ======================================
# INVENTAR (E)
# ======================================
inventory_ui = Entity(enabled=False)
inventory_bg = Entity(parent=inventory_ui, model='quad', scale=(1.2,0.8), color=color.rgba(0,0,0,180))

def create_inventory():
    Text("Inventar", parent=inventory_ui, position=(0,0.35), scale=2)

    y = 0.2
    for i in range(12):
        Button(
            text=f"Slot {i+1}",
            parent=inventory_ui,
            scale=(0.18,0.08),
            position=(-0.45 + (i%4)*0.3, y - (i//4)*0.15),
            color=color.dark_gray
        )

def toggle_inventory():
    inventory_ui.enabled = not inventory_ui.enabled
    mouse.locked = not inventory_ui.enabled
    mouse.visible = inventory_ui.enabled

# ======================================
# PAUSE MENÜ (ESC)
# ======================================
pause_ui = Entity(enabled=False)

Entity(parent=pause_ui, model='quad', scale=(16,9), color=color.rgba(0,0,0,120))
Text("PAUSE", parent=pause_ui, scale=3, position=(0,0.25))

def toggle_pause():
    pause_ui.enabled = not pause_ui.enabled
    mouse.locked = not pause_ui.enabled
    mouse.visible = pause_ui.enabled

def resume_game():
    pause_ui.disable()
    mouse.locked = True
    mouse.visible = False

def save_game():
    if player:
        data = {
            "x": player.x,
            "y": player.y,
            "z": player.z
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Spiel gespeichert!")

def back_to_menu():
    application.restart()

Button(text="▶ Weiter", parent=pause_ui, scale=(0.25,0.1), position=(0,0.05), color=color.green, on_click=resume_game)
Button(text="💾 Speichern", parent=pause_ui, scale=(0.25,0.1), position=(0,-0.05), color=color.azure, on_click=save_game)
Button(text="🏠 Hauptmenü", parent=pause_ui, scale=(0.25,0.1), position=(0,-0.15), color=color.orange, on_click=back_to_menu)
Button(text="❌ Beenden", parent=pause_ui, scale=(0.25,0.1), position=(0,-0.25), color=color.red, on_click=application.quit)

# ======================================
# SPEICHERN & LADEN
# ======================================
def load_game():
    if os.path.exists(SAVE_FILE) and player:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            player.position = Vec3(data["x"], data["y"], data["z"])
            print("Spielstand geladen!")

# ======================================
# START
# ======================================
app.run()
