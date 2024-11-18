# game_world.py

world = [[] for _ in range(5)]  # 레이어 0부터 4까지
collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def add_object(o, depth=0):
    if depth < 0 or depth >= len(world):
        raise ValueError(f'Depth {depth} is out of bounds')
    world[depth].append(o)

def add_objects(ol, depth=0):
    if depth < 0 or depth >= len(world):
        raise ValueError(f'Depth {depth} is out of bounds')
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def render_with_camera(camera):
    for layer in world:
        for o in layer:
            if hasattr(o, 'draw_with_camera'):
                o.draw_with_camera(camera)
            else:
                o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non-existing object')

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la >= rb: return False
    if ra <= lb: return False
    if ta <= bb: return False
    if ba >= tb: return False

    return True

def collide_hitboxes(box_a, box_b):
    la, ba, ra, ta = box_a
    lb, bb, rb, tb = box_b

    if la >= rb: return False
    if ra <= lb: return False
    if ta <= bb: return False
    if ba >= tb: return False

    return True

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if group == 'mario:koomba_top':
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'top')
                        b.handle_collision(group, a, 'top')
                elif group == 'mario:koomba_bottom':
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'bottom')
                        b.handle_collision(group, a, 'bottom')
                elif group == 'mario:brick_top':
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'brick_top')
                elif group == 'mario:brick_bottom':
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'brick_bottom')
                elif group == 'mario:brick_left':
                    if collide_hitboxes(a.get_bb(), b.get_left_bb()):
                        a.handle_collision(group, b, 'brick_left')
                elif group == 'mario:brick_right':
                    if collide_hitboxes(a.get_bb(), b.get_right_bb()):
                        a.handle_collision(group, b, 'brick_right')
                elif group == 'mario:random_box_top':
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'random_box_top')
                elif group == 'mario:random_box_bottom':
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'random_box_bottom')
                        b.handle_collision(group, a, 'random_box_bottom')
                elif group == 'mario:random_box_left':
                    if collide_hitboxes(a.get_bb(), b.get_left_bb()):
                        a.handle_collision(group, b, 'random_box_left')
                elif group == 'mario:random_box_right':
                    if collide_hitboxes(a.get_bb(), b.get_right_bb()):
                        a.handle_collision(group, b, 'random_box_right')
                elif group == 'mario:grass':
                    if collide(a, b):
                        a.handle_collision(group, b, 'grass')
                else:
                    if collide(a, b):
                        a.handle_collision(group, b, 'unknown')
                        b.handle_collision(group, a, 'unknown')