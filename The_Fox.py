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
is_paused = False
pause_ui = None

def start_game():
    global player
    menu_ui.visible = False  # Menü ausblenden
    player = FirstPersonController()
    player.gravity = 0.5

    # Boden
    ground = Entity(model='plane', scale=64, texture='white_cube', texture_scale=(64,64), collider='box', color=color.dark_gray)
    # Beispiel-Objekt
    box = Entity(model='cube', color=color.orange, scale=2, position=(3,1,3), collider='box')

def toggle_pause():
    global is_paused, pause_ui
    if not is_paused:
        is_paused = True
        mouse.locked = False
        # Pause-Menü erstellen
        pause_ui = Entity()
        panel = Entity(parent=pause_ui, model='quad', scale=(0.6,0.6), color=color.rgba(0,0,0,150))
        Text(text="Pause", parent=pause_ui, scale=2, position=(0,0.2,0))
        Button(text="▶ Fortsetzen", parent=pause_ui, scale=(0.3,0.1), position=(0,0,0), color=color.green, on_click=lambda: toggle_pause())
        Button(text="❌ Beenden", parent=pause_ui, scale=(0.3,0.1), position=(0,-0.15,0), color=color.red, on_click=application.quit)
    else:
        is_paused = False
        if pause_ui:
            destroy(pause_ui)
        mouse.locked = True

def input(key):
    if key == 'escape' and player is not None:
        toggle_pause()

play_button.on_click = start_game
quit_button.on_click = application.quit

app.run()
