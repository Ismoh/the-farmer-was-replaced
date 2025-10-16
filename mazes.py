import Movement

id = 6
need = 0
item = Items.Gold
requirements = {}
requirements['entities'] = {Entities.Bush:1}
requirements['items'] = {Items.Weird_Substance:get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)}

dirs = [North, East, South, West]
offsets = {
	North:(0, 1),
	South:(0, -1),
	West:(-1, 0),
	East:(1, 0)
}
grid = {}
visited = set()
found = 0

def get_dependency_costs_for_need(module):
	costs_need = {}
	for entity in module.requirements['entities']:
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = module.requirements['entities'][entity]
			diff = contingent - req_need
			if diff < 0:
				costs_need[itm] = diff *- 1
		if len(costs) == 0:
			# if no costs for entity, entity amount is still required
			costs_need[entity] = module.requirements['entities'][entity]
			
	for itm in module.requirements['items']:
		#contingent = num_items(itm)
		#req_need = requirements['items'][itm]
		#diff = contingent - req_need
		#if diff < 0:
		#	costs[itm] = diff *- 1
		req_need = module.requirements['items'][itm]
		costs_need[itm] = req_need
	return costs_need
	

def are_costs_covered(module):
	cost = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	if num_items(Items.Weird_Substance) < cost:
		#harvest_leftover(farm)
		return False
	return True

def is_cost_need_reached(module):
	return num_items(module.item) >= module.need


def can_plant():
	return True



def try_to_plant(module):
	if not are_costs_covered(module):
		return
	if can_plant():
		create_maze()

def create_maze():
	Movement.move_to(0,0)
	
	if get_entity_type() != Entities.Hedge:
		plant(Entities.Bush)
		
		while not can_harvest():
			pass
		
		if num_items(Items.Weird_Substance) == 0:
			#trade(Items.Weird_Substance)
			if num_items(Items.Weird_Substance) == 0:
				return False #main()
		substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
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
			use_item(Items.Weird_Substance, requirements['items'][Items.Weird_Substance])
		else:
			# no Weird_Substance left for use, stop iteration by setting highest found value
			found = 300
		found += 1
		if found >= 300:
			harvest()
			return True
		visited = set() # reset
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
					back = { North:South, South:North, West:East, East:West }
					move(back[d])
	return False
					
					
def hunt_treasure():
	while found < 300 and get_entity_type() == Entities.Hedge:
		dfs()