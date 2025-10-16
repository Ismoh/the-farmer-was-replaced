id = 2
need = 0
item = Items.Wood
requirements = {}
requirements['entities'] = {Entities.Bush:1} #, Entities.Tree:1}
requirements['items'] = {}

def get_dependency_costs_for_need(module):
	costs_need = {}
	for entity in module.requirements['entities']:
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = module.requirements['entities'][entity] * module.need
			diff = contingent - req_need
			if diff < 0:
				costs_need[itm] = diff *- 1
		if len(costs) == 0:
			# if no costs for entity, entity amount is still required
			costs_need[entity] = module.requirements['entities'][entity] * module.need
			
	for itm in module.requirements['items']:
		#contingent = num_items(itm)
		#req_need = requirements['items'][itm]
		#diff = contingent - req_need
		#if diff < 0:
		#	costs[itm] = diff *- 1
		req_need = module.requirements['items'][itm]
		costs_need[itm] = req_need * module.need
	return costs_need

def are_costs_covered_to_plant(module):
	costs = get_cost(module.requirements['entities'][0])
	for itm in costs:
		if not num_items(itm) > costs[itm]:
			return False
	return True
	
def is_cost_need_reached(module):
	return num_items(module.item) >= module.need
	
def can_plant(module):
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