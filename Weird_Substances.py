id = 5
need = 0
item = Items.Weird_Substance
requirements = {}
requirements['entities'] = {Entities.Bush:1}
requirements['items'] = {Items.Fertilizer:1}

def get_dependency_costs_for_need():
	for entity in requirements['entities']:
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = requirements['entities'][entity]
			diff = contingent - need
			if diff < 0:
				costs[itm] = diff *- 1
		if len(costs) == 0:
			# if no costs for entity, entity amount is still required
			costs[entity] = requirements['entities'][entity]
			
	for itm in requirements['items']:
		#contingent = num_items(itm)
		#req_need = requirements['items'][itm]
		#diff = contingent - req_need
		#if diff < 0:
		#	costs[itm] = diff *- 1
		req_need = requirements['items'][itm]
		costs[itm] = req_need
	return costs
	
def are_costs_covered(): # rename to 'are_costs_covered_to_plant'
	#if num_items(item) < need:
	#	return False
	#return True
	for item in requirements['items']:
		if num_items(item) < need:
			return False
	return True

def is_cost_need_reached():
	return num_items(item) >= need
	
def can_plant():
	return True

def plant_area(x, y, size, farm):
	for entity in requirements['entities']:
		plant(entity)
	for item in requirements['items']:
		use_item(item, requirements['items'][item])
	while not can_harvest():
		pass
	harvest()
