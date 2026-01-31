from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os

# --- Konfiguration ---
SAVE_FILE = "savegame.json"
window.icon = 'The_Fox.png'
window.title = 'The Fox 🦊 - Adventure'

app = Ursina()

# --- Globale Variablen ---
player = None
inventory = []
dialog_ui = None
dialog_text = None
current_interactable = None

# --- Klassen ---

class AdventureItem(Entity):
    def __init__(self, position=(0,0,0), model='sphere', item_name="Gegenstand", info_text="Ein mysteriöses Objekt."):
        super().__init__(
            model=model,
            position=position,
            scale=0.5,
            color=color.gold,
            collider='box'
        )
        self.item_name = item_name
        self.info_text = info_text

class NPC(Entity):
    def __init__(self, position=(0,0,0), name="Eule", dialogue=["Hallo Wanderer!", "Der Wald ist heute sehr nebelig."]):
        super().__init__(
            model='cube', # Hier später ein Fuchs/Eulen Modell
            color=color.brown,
            position=position,
            scale=(1, 2, 1),
            collider='box'
        )
        self.name = name
        self.dialogue = dialogue
        self.dialogue_index = 0
        
        # Name über dem Kopf
        self.label = Text(text=name, parent=self, y=1.2, scale=5, origin=(0,0), color=color.yellow)

# --- Menü-System ---

menu_ui = Entity()
menu_background = Entity(parent=menu_ui, model='quad', scale=(20,11), color=color.dark_gray, z=1)
title = Text(text="🦊 THE FOX: ADVENTURE", parent=menu_ui, scale=4, position=(0, 0.3), origin=(0,0))
play_button = Button(text="▶ Abenteuer starten", scale=(0.3, 0.1), position=(0, 0), color=color.orange, parent=menu_ui)
quit_button = Button(text="❌ Beenden", scale=(0.3, 0.1), position=(0, -0.15), color=color.red, parent=menu_ui)

pause_ui = Entity(enabled=False, z=-1)
pause_bg = Entity(parent=pause_ui, model='quad', scale=(2, 2), color=color.rgba(0,0,0,150))
resume_button = Button(text="▶ Weiter", scale=(0.4, 0.1), position=(0, 0.05), color=color.green, parent=pause_ui)
exit_button = Button(text="❌ Beenden", scale=(0.4, 0.1), position=(0, -0.15), color=color.red, parent=pause_ui)

# --- Spiel-Logik ---

def show_dialog(name, text):
    dialog_ui.enabled = True
    dialog_text.text = f"{name}: {text}"
    player.disable()
    mouse.visible = True

def hide_dialog():
    dialog_ui.enabled = False
    player.enable()
    mouse.visible = False

def start_game():
    global player, dialog_ui, dialog_text
    menu_ui.enabled = False
    
    # Spieler
    player = FirstPersonController()
    player.gravity = 0.5
    player.cursor.visible = False

    # Weltgestaltung
    ground = Entity(model='plane', scale=100, texture='grass', collider='box')
    
    # Bäume zur Deko
    for i in range(20):
        tree = Entity(model='cube', color=color.brown, scale=(0.5, 3, 0.5), 
                      position=(random.uniform(-20, 20), 1.5, random.uniform(-20, 20)),
                      collider='box')
        Entity(model='sphere', color=color.green, scale=2, parent=tree, y=0.5)

    # Ein NPC zum Reden
    npc_wise = NPC(position=(5, 1, 5), name="Der weise Dachs", dialogue=[
        "Willkommen im Wald, kleiner Fuchs.",
        "Ich habe meinen goldenen Ball verloren...",
        "Kannst du ihn für mich suchen?"
    ])

    # Ein Item zum Finden
    AdventureItem(position=(-5, 0.5, 10), item_name="Goldener Ball", info_text="Ein glänzender Ball, der dem Dachs gehört.")

    # Dialog UI
    dialog_ui = Entity(parent=camera.ui, enabled=False)
    db = Entity(parent=dialog_ui, model='quad', scale=(1, 0.25), color=color.black90, y=-0.3)
    dialog_text = Text(text="", parent=dialog_ui, scale=1.2, x=-0.4, y=-0.25)
    close_dialog_btn = Button(text="Weiter", parent=dialog_ui, scale=(0.15, 0.05), position=(0.35, -0.35), color=color.azure)
    close_dialog_btn.on_click = hide_dialog

    Sky()

def update():
    global current_interactable
    if player and player.enabled:
        # Strahl vom Spieler nach vorne, um Dinge zu finden
        hit_info = raycast(player.camera_pivot.world_position, player.camera_pivot.forward, distance=3)
        if hit_info.hit:
            if isinstance(hit_info.entity, (NPC, AdventureItem)):
                current_interactable = hit_info.entity
                # Hier könnte man einen "E drücken" Text anzeigen
            else:
                current_interactable = None
        else:
            current_interactable = None

def input(key):
    if key == 'e' and current_interactable:
        if isinstance(current_interactable, NPC):
            # NPC Dialog starten
            msg = current_interactable.dialogue[current_interactable.dialogue_index]
            show_dialog(current_interactable.name, msg)
            # Nächsten Satz vorbereiten
            current_interactable.dialogue_index = (current_interactable.dialogue_index + 1) % len(current_interactable.dialogue)
            
        elif isinstance(current_interactable, AdventureItem):
            # Item Info anzeigen
            show_dialog("System", f"Du hast {current_interactable.item_name} gefunden! {current_interactable.info_text}")
            inventory.append(current_interactable.item_name)
            destroy(current_interactable)

    if key == 'escape' and not menu_ui.enabled:
        pause_ui.enabled = not pause_ui.enabled
        player.enabled = not pause_ui.enabled
        mouse.visible = pause_ui.enabled

play_button.on_click = start_game
resume_button.on_click = lambda: setattr(pause_ui, 'enabled', False) or player.enable()
quit_button.on_click = application.quit
exit_button.on_click = application.quit

app.run()
