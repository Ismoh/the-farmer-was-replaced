import Movement

id = 4
need = 0
item = Items.Pumpkin
entities = [Entities.Pumpkin, Entities.Dead_Pumpkin]


def get_dependency_costs_for_need():
	costs = get_cost(entities[0])
	for itm in costs:
		contingent = num_items(item)
		diff = contingent - need
		if diff < 0:
			costs[itm] = diff *- 1
		else:
			return {}
	return costs
	

def are_costs_covered():
	costs = get_cost(entities[0])
	for item in costs:
		if not num_items(item) > costs[item] * size * size * 1.2:
			harvest_leftover(farm)
			return False
	return True
	
	
def is_cost_need_reached():
	return num_items(item) >= need


def can_plant():
	if get_entity_type() == Entities.Pumpkin:
		return False
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
		return True
	if get_entity_type() == None:
		return True
	if get_entity_type() == Entities.Dead_Pumpkin:
		till()
		till()
		return True


def plant_area(x, y, size, farm):
	if not are_costs_covered():
		return
	if can_plant():
		plant(entities[0])
		while not can_harvest():
			if get_water() < 1:
				use_item(Items.Water)
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant_area(x, y, size, farm)
			
				
def harvest_leftover(farm):
	clear(True)