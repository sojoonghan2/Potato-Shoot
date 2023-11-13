objects = [[] for _ in range(4)]  # 시각 관점의 월드

collision_pairs = {}  # 충돌 관점의 월드


def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)  # 시각적 월드에서 지움
            remove_collision_object(o)  # 충돌 그룹에서 삭제 완료
            del o  # 객체 자체를 완전히 메모리에서 제거
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


def r_to_r_collide(a, b):
    # 사각형과 사각형 충돌(충돌범위와 병의 충돌)
    la, ba, ra, ta = a.get_bb_r()
    lb, bb, rb, tb = b.get_bb_r()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True

def r_to_c_collide(a, b):
    # 사각형과 원 충돌(감자 자체와 병의 충돌)
    la, ba, ra, ta = a.get_bb_r()
    lb_1, bb_1, rb_1, tb_1 = b.get_bb_c_1()
    lb_2, bb_2, rb_2, tb_2 = b.get_bb_c_2()
    lb_3, bb_3, rb_3, tb_3 = b.get_bb_c_3()
    lb_4, bb_4, rb_4, tb_4 = b.get_bb_c_4()
    lb_5, bb_5, rb_5, tb_5 = b.get_bb_c_5()
    lb_6, bb_6, rb_6, tb_6 = b.get_bb_c_6()

    if la > rb_1: return False
    if ra < lb_1: return False
    if ta < bb_1: return False
    if ba > tb_1: return False

    if la > rb_2: return False
    if ra < lb_2: return False
    if ta < bb_2: return False
    if ba > tb_2: return False

    if la > rb_3: return False
    if ra < lb_3: return False
    if ta < bb_3: return False
    if ba > tb_3: return False

    if la > rb_4: return False
    if ra < lb_4: return False
    if ta < bb_4: return False
    if ba > tb_4: return False

    if la > rb_5: return False
    if ra < lb_5: return False
    if ta < bb_5: return False
    if ba > tb_5: return False

    if la > rb_6: return False
    if ra < lb_6: return False
    if ta < bb_6: return False
    if ba > tb_6: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'New group {group} added.')
        collision_pairs[group] = [[], []]
    if a:  # a가 있을 때, 즉, a가 None 이 아니면
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collisions():
    # 등록된 모든 충돌 상황에 대해서 충돌 검사 및 충돌 처리 수행
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if r_to_r_collide(a, b):
                    a.handle_collision_r(group, b)
                    b.handle_collision_r(group, a)
                if r_to_c_collide(a, b):
                    a.handle_collision_c(group, b)
                    b.handle_collision_c(group, a)