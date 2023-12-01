objects = [[] for _ in range(6)] #시각적인 관점에서의 월드
records = []
#충돌 관점의 월드
collision_pairs = {} # { 'player:rock' : [ [player], [rock1, rock2 ...] ]}
record_sum = [[9999.0,9999.0,9999.0,9999.0] for _ in range(4)]
item = [1,1,1]

def add_object(o, depth=0):
    objects[depth].append(o)

def add_success_time(time):
    records.append(time)

def delete_record_time():
    records.clear()

def confirm_record_time():
    record_sum.append([])
    for i in records:
        record_sum[-1].append(i)
    record_sum.sort(key=lambda x: (x[3], x[0]))

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
    pass

def remove_all_object(group):
    collision_pairs.pop(group, None)

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) #시각적 월드에서 지운다.
            remove_collision_object(o) #충돌 그룹에서 삭제 완료
            del o #객체 자체도 완전히 삭제해 줘야한다. free. 메모리에서 완전히 삭제
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