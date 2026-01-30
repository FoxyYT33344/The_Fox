from ursina import *

app = Ursina()

# ------------------ Boden ------------------
ground = Entity(
    model='plane',
    scale=(50,1,50),
    texture='grass',
    texture_scale=(10,10),
    collider='box'
)

# ------------------ Spieler ------------------
player = Entity(
    model='cube',         # Collider
    color=color.clear,    # unsichtbar
    scale=(1,2,1),
    position=(0,1.5,0),
    collider='box'
)

# ------------------ Kamera ------------------
camera.rotation = (0,0,0)

# ------------------ Parameter ------------------
speed = 5
jump_speed = 5
gravity = 9.81
velocity_y = 0
mouse_sensitivity = 40

mouse.locked = True

def update():
    global velocity_y

    # ------------------ Bewegung ------------------
    move = Vec3((held_keys['d'] - held_keys['a']), 0, (held_keys['w'] - held_keys['s'])) * speed * time.dt
    player.position += player.forward * move.z + player.right * move.x

    # ------------------ Gravitation ------------------
    if player.y > 1.5:
        velocity_y -= gravity * time.dt
    else:
        velocity_y = 0
        player.y = 1.5

    if held_keys['space'] and player.y <= 1.51:
        velocity_y = jump_speed * time.dt

    player.y += velocity_y

    # ------------------ Mausrotation ------------------
    player.rotation_y += mouse.velocity[0] * mouse_sensitivity  # Links/Rechts
    camera.rotation_x -= mouse.velocity[1] * mouse_sensitivity  # Oben/Unten
    camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    # ------------------ Kamera folgt Spieler ------------------
    camera.position = player.position + Vec3(0,1,0)

# Licht
DirectionalLight(y=10, z=10)
AmbientLight(color=color.rgba(100,100,100,0.5))

app.run()
