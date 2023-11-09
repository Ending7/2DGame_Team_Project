objects = [[] for _ in range(6)] #시각적인 관점에서의 월드

#충돌 관점의 월드
collision_pairs = {} # { 'player:rock' : [ [player], [rock1, rock2 ...] ]}

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


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('이미 존재 하지 않습니다')


def clear():
    for layer in objects:
        layer.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

# { 'player:rock' : [ [player], [rock1, rock2 ...] ]}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'New group {group} added.')
        collision_pairs[group] = [ [], [] ]
    if a: # a가 있을 때, 즉, a기 None이 아니라면
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collision():
    # 등록된 모든 충돌 상황에 대해서 충돌 검사 및 충돌 처리 수행.
    for group, pairs in collision_pairs.items(): #key 'player:rock, value [ [], [] ]
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)