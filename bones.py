import movement

id = 8
need = 0
item = Items.Bone


dirs = [North, East, South, West]
offsets = {North: (0, 1), South: (0, -1), West: (-1, 0), East: (1, 0)}
grid = {}
visited = set()
found = 0


def get_dependency_costs_for_need(module):
	costs_need = {}
	for entity in module.requirements["entities"]:
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = module.requirements["entities"][entity]
			diff = contingent - req_need
			if diff < 0:
				costs_need[itm] = diff * -1
		if len(costs) == 0:
			# if no costs for entity, entity amount is still required
			costs_need[entity] = module.requirements["entities"][entity]

	for itm in module.requirements["items"]:
		# contingent = num_items(itm)
		# req_need = requirements['items'][itm]
		# diff = contingent - req_need
		# if diff < 0:
		# 	costs[itm] = diff *- 1
		req_need = module.requirements["items"][itm]
		costs_need[itm] = req_need
	return costs_need


def are_costs_covered(module):
	# if num_items(item) < need:
	# 	return False
	# return True
	for itm in module.requirements["items"]:
		if num_items(itm) < module.need:
			return False
	return True


def is_cost_need_reached(module):
	conti = num_items(module.item)
	target = module.need
	return conti >= target


def can_plant(module):
	return True


def try_to_plant(module):
	if not are_costs_covered(module):
		return
	if can_plant(module):
		create_maze()


def create_maze():
	movement.move_to(0, 0)

	if get_entity_type() != Entities.Hedge:
		plant(Entities.Bush)

		while not can_harvest():
			pass

		if num_items(Items.Weird_Substance) == 0:
			# trade(Items.Weird_Substance)
			if num_items(Items.Weird_Substance) == 0:
				return False  # main()
		substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)

	if num_drones() < max_drones():
		spawn_drone(hunt_treasure)
	hunt_treasure()


def explore():
	x_y = (get_pos_x(), get_pos_y())
	if x_y not in grid:
		grid[(x_y)] = {}
		for d in dirs:
			grid[x_y][d] = can_move(d)


def move_dir(d):
	if can_move(d):
		move(d)
		return True
	return False


def dfs():
	global grid
	global visited
	global found

	explore()
	x = get_pos_x()
	y = get_pos_y()
	x_y = (x, y)
	visited.add(x_y)

	if x_y == measure() or get_entity_type() == Entities.Treasure:
		if are_costs_covered():
			use_item(
				Items.Weird_Substance, requirements["items"][Items.Weird_Substance]
			)
		else:
			# no Weird_Substance left for use, stop iteration by setting highest found value
			found = 300
		found += 1
		if found >= 300:
			harvest()
			return True
		visited = set()  # reset
		return False

	for d in dirs:
		x_y = (get_pos_x(), get_pos_y())
		if grid[x_y][d]:
			dx = offsets[d][0]
			dy = offsets[d][1]
			nx = x_y[0] + dx
			ny = x_y[1] + dy
			if (nx, ny) not in visited:
				if move_dir(d):
					if dfs():
						return True
					back = {North: South, South: North, West: East, East: West}
					move(back[d])
	return False


def hunt_treasure():
	while found < 300 and get_entity_type() == Entities.Hedge:
		dfs()


def create_maze_old(iteration):
	visits = {(0, 0)}
	movement.move_to(0, 0)

	if get_entity_type() != Entities.Hedge:
		plant(Entities.Bush)
		itr = 0

		while not can_harvest():
			pass

		if num_items(Items.Weird_Substance) == 0:
			# trade(Items.Weird_Substance)
			if num_items(Items.Weird_Substance) == 0:
				return False  # main()
		substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)

	if num_drones() < max_drones():
		spawn_drone(spawn_drone_treasure_hunt)

	while iteration <= 300:
		iteration = treasure_hunt(
			directions[random() * len(directions) // 1], iteration, visits
		)
	# create_maze(iteration)


def spawn_drone_treasure_hunt():
	iteration = 0
	visits = {(0, 0)}
	while iteration <= 300:
		iteration = treasure_hunt(
			directions[random() * len(directions) // 1], iteration, visits
		)


def treasure_hunt(dir, iteration, visits):
	# 	x, y = measure()
	x = get_pos_x()
	y = get_pos_y()
	while True:
		if get_entity_type() != Entities.Hedge:
			return 300
		if x % 2:
			dir = directions[random() * len(directions) // 1]
		move(dir)
		visits.add((x, y))

		x2 = get_pos_x()
		y2 = get_pos_y()

		if x == x2 and y == y2:
			if dir == West:
				dir = North
			elif dir == North:
				dir = East
			elif dir == East:
				dir = South
			elif dir == South:
				dir = West
		else:
			x = get_pos_x()
			y = get_pos_y()

			if dir == West:
				dir = South
			elif dir == North:
				dir = West
			elif dir == East:
				dir = North
			elif dir == South:
				dir = East

		# doesnt work with iterations
		if iteration == 16:
			return iteration

		if get_entity_type() == Entities.Treasure:
			if iteration < 300:
				if num_items(Items.Weird_Substance) < get_world_size() * 2 ** (
					num_unlocked(Unlocks.Mazes) - 1
				):
					iteration = 300
					return iteration
				substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
				use_item(Items.Weird_Substance, substance)
				iteration += 1
			else:
				harvest()
			return iteration


def bones_main():
	print("bones.main - not yet implemented")


if __name__ == "__main__":
	bones_main()
