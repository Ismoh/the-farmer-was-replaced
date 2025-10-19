from builtins import set

import movement
import costs
import unlocks
import utils

requirements = {}

id = 6
need = 0
item = Items.Gold

drone_index = 0
dirs = [North, East, South, West]
offsets = {North: (0, 1), South: (0, -1), West: (-1, 0), East: (1, 0)}
found = 0


def try_to_plant():
	global requirements
	global item

	if costs.are_costs_covered_to_plant(requirements):
		create_maze()


def get_x_y_of_splitted_square_into_n(S, n):
	# n must be a perfect square of 2
	a = 0
	tmp = n
	while tmp > 1:
		tmp //= 2
		a += 1

	cols = 2 ** ((a + 1) // 2)
	rows = n // cols
	tile_size = S // cols  # oder rows, da quadratisch

	starts = []
	for i in range(rows):
		for j in range(cols):
			x0 = j * tile_size
			y0 = i * tile_size
			starts.append((x0, y0))
	return starts


def create_maze():
	if get_entity_type() != Entities.Hedge:
		plant(Entities.Bush)

		while not can_harvest():
			pass

		if num_items(Items.Weird_Substance) == 0:
			# trade(Items.Weird_Substance)
			if num_items(Items.Weird_Substance) == 0:
				return False  # main()
		key = list(requirements["items"])[0]
		use_item(Items.Weird_Substance, requirements["items"][key])

	hunt_treasure()


def explore(grid):
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


def dfs(grid=None, visited=None):
	if grid == None:
		grid = {}
	if visited == None:
		visited = set()

	global found
	global requirements

	explore(grid)
	x = get_pos_x()
	y = get_pos_y()
	x_y = (x, y)
	visited.add(x_y)

	if x_y == measure() or get_entity_type() == Entities.Treasure:
		boolean, grid, visited, found = double_ckeck(grid, visited, requirements, found)
		return boolean

	for d in dirs:
		x_y = (get_pos_x(), get_pos_y())
		if x_y not in grid:
			explore(grid)
		if grid[x_y][d]:
			dx = offsets[d][0]
			dy = offsets[d][1]
			nx = x_y[0] + dx
			ny = x_y[1] + dy
			if (nx, ny) not in visited:
				if move_dir(d):
					if dfs(grid, visited):
						return True
					back = {North: South, South: North, West: East, East: West}
					move(back[d])
					if x_y == measure() or get_entity_type() == Entities.Treasure:
						boolean, grid, visited, found = double_ckeck(grid, visited, requirements, found)
						return boolean
	return False


def double_ckeck(grid, visited, requirements, found):
	if costs.are_costs_covered_to_plant(requirements):
		key = list(requirements["items"])[0]
		use_item(Items.Weird_Substance, requirements["items"][key])
		quick_print("Treasures found:" + str(found))
	else:
		# no Weird_Substance left for use, stop iteration by setting highest found value
		found = 300
	found += 1
	if found >= 300:
		harvest()
		quick_print("Treasures harvest:" + str(found))
		visited = set()  # reset
		grid = {}
		found = 0
		return True, grid, visited, found
	visited = set()  # reset
	grid = {}
	return False, grid, visited, found


def hunt_treasure():
	while found < 300 and get_entity_type() == Entities.Hedge:
		dfs()


def set_need(req):
	global requirements
	global req_need

	requirements = req
	req_need = requirements["need"]


def drone_run():
	global drone_index

	# example: world 12x12, max_drones 4 -> 3x3 mazes per drone
	smaller_square_start_pos = get_x_y_of_splitted_square_into_n(get_world_size(), max_drones())
	x = smaller_square_start_pos[drone_index][0]
	y = smaller_square_start_pos[drone_index][1]
	x = x + (x / 2)
	y = y + (y / 2)

	# re-set weird_substance amount
	key = list(requirements["items"])[0]
	requirements["items"][key] = smaller_square_start_pos[max_drones() - 1][0]

	movement.move_to(x, y)
	change_hat(Hats.Green_Hat)
	utils.wait(100000 * drone_index)
	run()


def run():
	try_to_plant()


def mazes_main():
	global item
	global requirements
	global drone_index

	clear()
	quick_print("Starting mazes challenge..")
	goal = unlocks.get_next_goal(Items.Gold)
	if goal:
		# goal = (Unlocks.Simulation, {Items.Gold: 5000})
		goal_name = goal[0]
		goal_costs = goal[1]
		req_need = goal[1][list(goal[1])[0]]
		if costs.is_cost_need_reached(item, req_need):
			unlocks.try_unlock(goal[0])
			return
	else:
		goal_costs = 100000000
	total_costs = costs.get_required_costs_by_goal(goal_costs)

	for tc in total_costs:
		for itm in tc:
			req = tc[itm]
			if itm == item:
				req["need"] = goal[1][list(goal[1])[0]]  # only for mazes
				set_need(req)
			else:
				module = utils.get_module(itm)
				module.set_need(req)
				module.run()

	while costs.are_costs_covered_to_plant(requirements) and not costs.is_cost_need_reached(item, requirements["need"]):
		movement.move_to(0, 0)
		drone_index = 0
		for _ in range(max_drones()):
			drone_index += 1
			d = spawn_drone(drone_run)
			utils.wait(100000)

		smaller_square_start_pos = get_x_y_of_splitted_square_into_n(get_world_size(), max_drones())
		# re-set weird_substance amount
		key = list(requirements["items"])[0]
		requirements["items"][key] = smaller_square_start_pos[max_drones() - 1][0]
		run()


if __name__ == "__main__":
	clear()
	mazes_main()
