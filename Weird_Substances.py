id = 5
need = 0
item = Items.Weird_Substance
requirements = {}
requirements['entities'] = {Entities.Bush:1}
requirements['items'] = {Items.Fertilizer:1}

def get_dependency_costs_for_need(module):
	for entity in module.requirements['entities']:
		costs_need = {}
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = module.requirements['entities'][entity]
			diff = contingent - module.need
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
		req_need = module.requirements['items'][itm] * module.need
		costs_need[itm] = req_need
	return costs_need
	
def are_costs_covered_to_plant(module):
	#if num_items(item) < need:
	#	return False
	#return True
	for itm in module.requirements['items']:
		if num_items(itm) < module.need:
			return False
	return True

def is_cost_need_reached(module):
	return num_items(module.item) >= module.need
	
def can_plant():
	return True

def try_to_plant(module):
	for entity in module.requirements['entities']:
		plant(entity)
	for itm in module.requirements['items']:
		use_item(itm, module.requirements['items'][itm])
	while not can_harvest():
		pass
	harvest()
