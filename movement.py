def move_to(x, y):
    if get_pos_x() != x:
        move_least_distance(x, get_pos_x, East, West)
    if get_pos_y() != y:
        move_least_distance(y, get_pos_y, North, South)
    
def move_least_distance(goal, get_pos_func, plus_dir, minus_dir):    
    delta = goal - get_pos_func()
    if delta < 0:
        count = delta * -1 #abs(delta)
    else:
        count = delta #abs(delta)
    if count <= get_world_size() // 2:
        if delta > 0:
            move_dir(plus_dir, count)
        else:
            move_dir(minus_dir, count)
    else:
        count = get_world_size() - count
        if delta > 0:
            move_dir(minus_dir, count)
        else:
            move_dir(plus_dir, count)
    
    
def move_dir(direction, count):
    for i in range(count):
        move(direction)