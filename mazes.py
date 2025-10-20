from builtins import set

import movement
import costs
import unlocks
import utils

requirements = {}

id = 6
need = 0
item = Items.Gold

dirs = [North, East, South, West]
offsets = {North: (0, 1), South: (0, -1), West: (-1, 0), East: (1, 0)}
drone_start_pos_reached = {}


def try_to_plant(drone_index):
	global requirements
	global item

	if costs.are_costs_covered_to_plant(requirements):
		create_maze(drone_index)


def get_x_y_of_splitted_square_into_n(S, n):
	# n = power of 2
	pow2 = {2, 4, 8, 16, 32, 64}
	if n not in pow2:
		while True:
			print("n = " + str(n) + " isn't power of 2..")
	a = 0
	tmp = n
	while tmp > 1:
		tmp //= 2
		a += 1

	# cols = 2 ** ((a + 1) // 2)  # cols = S // a
	# rows = n // cols  # rows = cols
	# tile_size = S // cols
	cols = S // 2 ** ((a + 1) // 2)
	rows = cols
	tile_size = S // cols

	starts = []
	for i in range(rows):
		for j in range(cols):
			x0 = j * tile_size
			y0 = i * tile_size
			starts.append((x0, y0))
	return starts


def create_maze(drone_index):
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

	hunt_treasure(drone_index)


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


def dfs(drone_index, found, grid=None, visited=None):
	global requirements

	if grid == None:
		grid = {}
	if visited == None:
		visited = set()

	explore(grid)
	x = get_pos_x()
	y = get_pos_y()
	x_y = (x, y)
	visited.add(x_y)

	if x_y == measure() and get_entity_type() == Entities.Treasure:
		boolean, grid, visited, found = double_ckeck(drone_index, grid, visited, requirements, found)
		return boolean, found

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
					boolean, found = dfs(drone_index, found, grid, visited)
					if boolean:
						return True, found
					back = {North: South, South: North, West: East, East: West}
					move(back[d])
					if x_y == measure() and get_entity_type() == Entities.Treasure:
						boolean, grid, visited, found = double_ckeck(drone_index, grid, visited, requirements, found)
						return boolean, found
	return False, found


def double_ckeck(drone_index, grid, visited, requirements, found):
	if costs.are_costs_covered_to_plant(requirements):
		key = list(requirements["items"])[0]
		use_item(Items.Weird_Substance, requirements["items"][key])
		quick_print("Drone " + str(drone_index) + " used weird_substance " + str(found) + " times.")
		found += 1
		visited = set()  # reset
		grid = {}
		return True, grid, visited, found
	else:
		# no Weird_Substance left for use, stop iteration by setting highest found value
		found = 300
	if found > 300:
		harvest()
		quick_print("Drone " + str(drone_index) + " harvested treasure after " + str(found) + " times.")
		visited = set()  # reset
		grid = {}
		found = 0
		return True, grid, visited, found
	visited = set()  # reset
	grid = {}
	return False, grid, visited, found


def hunt_treasure(drone_index):
	found = 0
	while found < 300 and get_entity_type() == Entities.Hedge:
		_, found = dfs(drone_index, found)


def set_need(req):
	global requirements
	global req_need

	requirements = req
	# requirements["items"][Items.Weird_Substance] = requirements["items"][Items.Weird_Substance] * max_drones() * 300
	req_need = requirements["need"]


def get_required_weird_substance_amount():
	smaller_square_start_pos = get_x_y_of_splitted_square_into_n(
		get_world_size(), max_drones()
	)  # not correct! https://chatgpt.com/c/68f55c0e-e108-8327-915d-4f509e337041
	amount = smaller_square_start_pos[1][0]
	return amount


def drone_run(drone_index):
	# inner drone function to be able to use parameters
	def drone():

		# example: world 12x12, max_drones 4 -> 3x3 mazes per drone
		smaller_square_start_pos = get_x_y_of_splitted_square_into_n(get_world_size(), max_drones())
		smallest_factor = smaller_square_start_pos[1][0]
		x = smaller_square_start_pos[drone_index][0]
		y = smaller_square_start_pos[drone_index][1]
		x = x + (smallest_factor // 2)
		y = y + (smallest_factor // 2)

		# re-set weird_substance amount
		key = list(requirements["items"])[0]
		requirements["items"][key] = smaller_square_start_pos[1][0]

		movement.move_to(x, y)
		change_hat(Hats.Green_Hat)
		utils.wait(100000000 * (max_drones() - drone_index))
		print("Drone " + str(drone_index))
		run(drone_index)
		return drone

	return spawn_drone(drone)


def run(drone_index):
	try_to_plant(drone_index)


def mazes_main():
	global item
	global requirements

	quick_print("Starting mazes challenge..")
	goal = unlocks.get_next_goal(Items.Gold)
	if goal:
		# goal = (Unlocks.Simulation, {Items.Gold: 5000})
		goal_name = goal[0]
		goal_costs = goal[1]
		req_need = goal[1][list(goal[1])[0]]
		if costs.is_cost_need_reached(item, req_need):
			if unlocks.try_unlock(goal[0]):
				goal = None
			return goal
	else:
		goal_costs = {Items.Gold: 100000}
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
				module.main(False)  # module.run()

	drones = []
	while costs.are_costs_covered_to_plant(requirements) and not costs.is_cost_need_reached(item, requirements["need"]):
		movement.move_to(0, 0)
		for i in range(max_drones()):
			if i == 0:
				continue
			drones.append(drone_run(i))
			utils.wait(100000000)

		smaller_square_start_pos = get_x_y_of_splitted_square_into_n(get_world_size(), max_drones())
		# re-set weird_substance amount
		key = list(requirements["items"])[0]
		requirements["items"][key] = smaller_square_start_pos[1][0]
		run(0)
		for d in range(drones):
			if d != None:
				wait_for(d)

	if costs.is_cost_need_reached(item, req_need):
		if unlocks.try_unlock(goal[0]):
			goal = None

	return goal


if __name__ == "__main__":
	clear()
	goal = mazes_main()
	while goal != None:
		mazes_main()
