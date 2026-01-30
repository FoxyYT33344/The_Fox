from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# ---------------- Hauptmenü ----------------
menu_ui = Entity()
menu_background = Entity(parent=menu_ui, model='quad', scale=(16,9), color=color.azure)
title = Text(text="🦊 The Fox", parent=menu_ui, scale=3, position=(0,0.3,0), origin=(0,0))
play_button = Button(text="▶ Spiel starten", scale=(0.3,0.1), position=(0,0,0), color=color.green, parent=menu_ui)
quit_button = Button(text="❌ Beenden", scale=(0.3,0.1), position=(0,-0.15,0), color=color.red, parent=menu_ui)

# ---------------- 3D-Spielwelt ----------------
player = None
hotbar = []
inventory_ui = None
inventory_open = False
selected_slot = 0

# Beispiel-Items
items = ["Holz", "Stein", "Schaufel", "Schwert", "Fackel", "Pfeil", "Bogen", "Essen", "Trank"]

def start_game():
    global player, hotbar, inventory_ui
    menu_ui.visible = False  # Menü ausblenden
    player = FirstPersonController()
    player.gravity = 0.5

    # Boden
    ground = Entity(model='plane', scale=64, texture='white_cube', texture_scale=(64,64),
                    collider='box', color=color.dark_gray)

    # Beispiel-Objekt
    box = Entity(model='cube', color=color.orange, scale=2, position=(3,1,3), collider='box')

    # Hotbar
    hotbar = []
    for i in range(9):
        slot_bg = Entity(model='quad', scale=(0.08,0.08), color=color.gray, origin=(0,0),
                         parent=camera.ui, x=-0.36 + i*0.08, y=-0.42)
        slot_text = Text(text=items[i], parent=slot_bg, scale=0.5, y=-0.02)
        hotbar.append((slot_bg, slot_text))
    highlight_slot(selected_slot)

    # Inventar (unsichtbar am Start)
    inventory_ui = Entity(parent=camera.ui, enabled=False)
    inv_bg = Entity(parent=inventory_ui, model='quad', scale=(0.5,0.5), color=color.rgba(50,50,50,200))

def highlight_slot(slot_index):
    """Hebt den ausgewählten Hotbar-Slot hervor"""
    for i, (bg, _) in enumerate(hotbar):
        if i == slot_index:
            bg.color = color.yellow
        else:
            bg.color = color.gray

def input(key):
    global selected_slot, inventory_open
    if key.isdigit() and int(key) in range(1,10):
        selected_slot = int(key)-1
        highlight_slot(selected_slot)
    elif key == 'i':
        inventory_open = not inventory_open
        inventory_ui.enabled = inventory_open

play_button.on_click = start_game
quit_button.on_click = application.quit

app.run()

