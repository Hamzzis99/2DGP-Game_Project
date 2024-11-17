# game_world.py

world = [[] for _ in range(5)]
collision_pairs = {}  # key: [[], []]

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]  # 초기화
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
    world[depth].append(o)

def add_objects(ol, depth=0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o  # 메모리 삭제
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
                    # 마리오의 히트박스와 굼바의 상단 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'top')
                        b.handle_collision(group, a, 'top')
                elif group == 'mario:koomba_bottom':
                    # 마리오의 히트박스와 굼바의 하단 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'bottom')
                        b.handle_collision(group, a, 'bottom')
                elif group == 'mario:brick_top':
                    # 마리오의 히트박스와 Brick의 상단 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'brick_top')
                elif group == 'mario:brick_bottom':
                    # 마리오의 히트박스와 Brick의 하단 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'brick_bottom')
                elif group == 'mario:brick_left':
                    # 마리오의 히트박스와 Brick의 왼쪽 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_left_bb()):
                        a.handle_collision(group, b, 'brick_left')
                elif group == 'mario:brick_right':
                    # 마리오의 히트박스와 Brick의 오른쪽 히트박스를 사용하여 충돌 검사
                    if collide_hitboxes(a.get_bb(), b.get_right_bb()):
                        a.handle_collision(group, b, 'brick_right')
                elif group == 'mario:random_box_top':
                    if collide_hitboxes(a.get_bb(), b.get_top_bb()):
                        a.handle_collision(group, b, 'random_box_top')
                elif group == 'mario:random_box_bottom':
                    if collide_hitboxes(a.get_bb(), b.get_bottom_bb()):
                        a.handle_collision(group, b, 'random_box_bottom')
                        b.handle_collision(group, a, 'random_box_bottom')  # Random_box의 handle_collision 호출

                elif group == 'mario:random_box_left':
                    if collide_hitboxes(a.get_bb(), b.get_left_bb()):
                        a.handle_collision(group, b, 'random_box_left')
                elif group == 'mario:random_box_right':
                    if collide_hitboxes(a.get_bb(), b.get_right_bb()):
                        a.handle_collision(group, b, 'random_box_right')

                elif group == 'mario:grass':
                    # 마리오와 Grass의 충돌 검사
                    if collide(a, b):
                        a.handle_collision(group, b, 'grass')
                else:
                    # 기본적으로 전체 히트박스를 사용
                    if collide(a, b):
                        a.handle_collision(group, b, 'unknown')
                        b.handle_collision(group, a, 'unknown')
    return None
