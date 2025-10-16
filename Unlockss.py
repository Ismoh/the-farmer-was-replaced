unlocks = {
	Unlocks.Auto_Unlock:None,
	Unlocks.Cactus:None,
	Unlocks.Carrots:None,
	Unlocks.Costs:None,
	Unlocks.Debug:None,
	Unlocks.Debug_2:None,
	Unlocks.Dictionaries:None,
	Unlocks.Dinosaurs:None,
	Unlocks.Expand:None,
	Unlocks.Fertilizer:None,
	Unlocks.Functions:None,
	Unlocks.Grass:None,
	Unlocks.Hats:None,
	Unlocks.Import:None,
	Unlocks.Leaderboard:None,
	Unlocks.Lists:None,
	Unlocks.Loops:None,
	Unlocks.Mazes:None,
	Unlocks.Megafarm:None,
	Unlocks.Operators:None,
	Unlocks.Plant:None,
	Unlocks.Polyculture:None,
	Unlocks.Pumpkins:None,
	Unlocks.Senses:None,
	Unlocks.Simulation:None,
	Unlocks.Speed:None,
	Unlocks.Sunflowers:None,
	Unlocks.The_Farmers_Remains:None,
	Unlocks.Timing:None,
	Unlocks.Top_Hat:None,
	Unlocks.Trees:None,
	Unlocks.Utilities:None,
	Unlocks.Variables:None,
	Unlocks.Watering:None
}

# how hard or expensive to get the item in numbers
cost_order = {
	Items.Hay:1,
	Items.Wood:1,
	Items.Carrot:2,
	Items.Pumpkin:3,
	Items.Gold:4,
	Items.Cactus:5,
	Items.Weird_Substance:6,
	Items.Water:7,
	Items.Fertilizer:7,
	Items.Bone:8
}

def get_next_goal():
	return filter_cheapest_unlocks()

def filter_cheapest_unlocks():
	cheapest_unlock = None
	cheapest_item = None
	cheapest_cost = 9999999999999999
	cheapest_cost_order = 9999999999999999
	for unl in unlocks:
		if unlocks[unl] == None or num_unlocked(unl) == 0:
			costs = get_cost(unl)
			if len(costs) > 0:
				if is_cost_unlocked(costs):
					unlocks[unl] = costs
					quick_print(str(unl) + " -> " + str(unlocks[unl]))
					for item in costs:
						quick_print(str(costs))
						if costs[item] <= cheapest_cost and cost_order[item] <= cheapest_cost_order:
							cheapest_unlock = unl
							cheapest_item = costs
							cheapest_cost = costs[item]
							cheapest_cost_order = cost_order[item]
							quick_print(str(cheapest_unlock) + " " + str(cheapest_item) + " " + str(cheapest_cost) + " " + str(cheapest_cost_order))
	return cheapest_unlock, cheapest_item

def is_cost_unlocked(costs):
	for item in costs:
		unlocked = num_unlocked(item)
		if unlocked == 0:
			return False
	return True

def try_unlock(unlo):
	if unlock(unlo):
		quick_print("---> YAY! " + str(unlo) + " unlocked!")