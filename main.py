import Unlockss
import Movement
import Pumpkins
import Carrots
import Woods
import Hays
import Weird_Substances
import Golds
import Cactuss

clear_super = clear

def clear(supposed_to_harvest = False):
	if not supposed_to_harvest:
		clear_super()
		return
		
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			Movement.move_to(x, y)
			harvest()
			
clear()

farm = {(0,0):Entities.Grass}

for x in range(get_world_size()):
	for y in range(get_world_size()):
		farm[(x, y)] = None

item_module_map = {
	Items.Hay:Hays,
	Items.Wood:Woods,
	Items.Carrot:Carrots,
	Items.Pumpkin:Pumpkins,
	Items.Cactus:Cactuss,
	Items.Weird_Substance:Weird_Substances,
	Items.Gold:Golds
}

def get_dependency_costs(costs):
	for c in costs:
		if c in item_module_map:
			module = item_module_map[c]
			needs[module.id] = module
			needs[module.id].need = costs[c]
			get_dependency_costs(needs[module.id].get_dependency_costs_for_need())
	
while True:
	goal = Unlockss.get_next_goal()
	#goal = (Unlocks.Simulation,{Items.Gold:5000}) # set goal manually
	quick_print("Unlocks goal: " + str(goal[0]) + " - Needs " + str(goal[1]))

	needs = {}
	for g in goal[1]:
		module = item_module_map[g]
		needs[module.id] = module
		needs[module.id].need = goal[1][g]
		get_dependency_costs(needs[module.id].get_dependency_costs_for_need())		

	for module_id in needs:
		x = 0
		y = 0
		area_size = get_world_size()
		module = needs[module_id]
		quick_print("Farming " + str(module.item) + " with need of " + str(module.need) + ". Contingent of " + str(num_items(module.item)))
		while num_items(module.item) < module.need and module.are_costs_covered():
			time_start = get_time()
			for x in range(get_world_size()):
				if module.is_cost_need_reached():
					break
				for y in range(get_world_size()):
					if module.is_cost_need_reached():
						break
					Movement.move_to(x,y)
					module.plant_area(x, y, area_size, farm)
					farm[(get_pos_x(), get_pos_y())] = get_entity_type()
			if can_harvest():
				harvest()
	Unlockss.try_unlock(goal[0])
