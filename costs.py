# Some cropped items like Gold need when planting additional items like weird_substance
item_costs_map = {
	Items.Bone: {
		"entities": {Entities.Apple: 1},
		"items": {},
	},
	Items.Cactus: {
		"entities": {Entities.Cactus: 1},
		"items": {},
	},
	Items.Carrot: {
		"entities": {Entities.Carrot: 1},
		"items": {},
	},
	Items.Fertilizer: {
		"entities": {},
		"items": {},
	},
	Items.Gold: {
		"entities": {Entities.Bush: 1},
		"items": {Items.Weird_Substance: (get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)) / max_drones()},
	},
	Items.Hay: {
		"entities": {Entities.Grass: 1},
		"items": {},
	},
	Items.Pumpkin: {
		"entities": {Entities.Pumpkin: 1},
		"items": {},
	},
	Items.Weird_Substance: {
		"entities": {Entities.Bush: 1},
		"items": {Items.Fertilizer: 1},
	},
	Items.Wood: {
		"entities": {Entities.Bush: 1, Entities.Tree: 1},
		"items": {},
	},
}

entity_item_map = {
	Entities.Bush: Items.Wood,
}

# total_costs = {}
total_costs = []


def get_required_costs(item, multiplier):
	#                 Items.Gold, 5000, {Entity.Bush:1}, {Items.Weird_Substance:12}
	#                 Items.Carrot, 5000, {Entity.Grass:8, Entity.Bush:8}, {}
	# {Items.Gold: 5000}
	global item_costs_map
	global total_costs

	req_costs = {
		"entities": {},
		"items": {},
		"need": 0,
	}
	for entity in item_costs_map[item]["entities"]:
		costs = get_cost(entity)
		for itm in costs:
			contingent = num_items(itm)
			req_need = item_costs_map[item]["entities"][entity] * multiplier
			diff = contingent - req_need
			if diff < 0:
				req_costs["items"][itm] = diff * -1
		if len(costs) == 0:
			# if no costs for entity, entity amount is still required
			req_costs["entities"][entity] = item_costs_map[item]["entities"][entity] * multiplier

	for itm in item_costs_map[item]["items"]:
		# contingent = num_items(itm)
		req_need = item_costs_map[item]["items"][itm]
		# diff = contingent - req_need
		# if diff < 0:
		req_costs["items"][itm] = req_need * multiplier

	if len(req_costs["entities"]) != 0 and len(req_costs["items"]) != 0:
		req_costs["need"] = multiplier
		total_costs.insert(0, {item: req_costs})

	for entities_or_items in req_costs:
		if entities_or_items == "need":
			continue
		for cn in req_costs[entities_or_items]:
			if cn in entity_item_map:
				continue  # entity costs are only interesting when planting
			multiplier = req_costs[entities_or_items][cn]
			get_required_costs(cn, multiplier)

	return total_costs


def get_required_costs_by_goal(goal_costs):
	# global total_costs
	for item in goal_costs:
		multiplier = goal_costs[item]
		if item == Items.Gold:
			multiplier = 1  # maze only a multiplier by 1
		return get_required_costs(item, multiplier)
	return {}


def are_costs_covered_to_plant(requirements):
	#    """
	#    Checks if the costs for each entity in entities are covered.
	#    If one cost isn't covered, returns False, because the drone isn't able to plant.
	#
	#    Parameters:
	#            entities(dict[]): entities to check
	#
	#    Returns:
	#            bool: If one cost isn't covered, returns False, because the drone isn't able to plant.
	#    """
	for entity in requirements["entities"]:
		costs = get_cost(entity)
		for itm in costs:
			if not num_items(itm) > costs[itm]:
				return False
	for itm in requirements["items"]:
		if not num_items(itm) > requirements["items"][itm]:
			return False
	return True


def is_cost_need_reached(item, requirements_need):
	conti = num_items(item)
	req_amount = requirements_need
	return conti >= req_amount
