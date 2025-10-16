id = 1
need = 300
item = Items.Hay
entities = [Entities.Grass]

def get_dependency_costs_for_need(module):
	return {}
	
def are_costs_covered_to_plant(module):
	costs = get_cost(module.entities[0])
	for itm in costs:
		if not num_items(itm) > costs[itm]:
			return False
	return True
	
def is_cost_need_reached(module):
	return num_items(module.item) >= module.need
	
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

def try_to_plant(module):
	if not are_costs_covered_to_plant(module):
		return
	if can_plant():
		plant(module.entities[0])