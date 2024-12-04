# utils/debug.py

SHOW_COLLISION_BOX = False

def toggle_show_collision_box():
    global SHOW_COLLISION_BOX
    SHOW_COLLISION_BOX = not SHOW_COLLISION_BOX
    print(f"Collision Box Visibility: {'ON' if SHOW_COLLISION_BOX else 'OFF'}")
