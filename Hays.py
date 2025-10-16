id = 1
need = 300
item = Items.Hay
entities = [Entities.Grass]

def get_dependency_costs_for_need():
	return {}
	
def are_costs_covered():
	costs = get_cost(entities[0])
	for item in costs:
		if not num_items(item) > costs[item]:
			return False
	return True
	
def is_cost_need_reached():
	return num_items(item) >= need
	
def can_plant():
	if get_entity_type() == None:
		return True
	if get_entity_type() == Entities.Pumpkin:
		return False
	if get_entity_type() == Entities.Dead_Pumpkin:
		till()
		return True
	if can_harvest():
		harvest()
	return True

def plant_area(x, y, size, farm):
	if not are_costs_covered():
		return
	if can_plant():
		plant(entities[0])