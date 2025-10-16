import unlocks
import Movement
import Pumpkins
import Carrots
import Woods
import hay
import Weird_Substances
import mazes
import cacti
import Bones

clear_super = clear

item_module_map = {
	Items.Hay:hay,
	Items.Wood:Woods,
	Items.Carrot:Carrots,
	Items.Pumpkin:Pumpkins,
	Items.Cactus:cacti,
	Items.Weird_Substance:Weird_Substances,
	Items.Gold:mazes,
	Items.Bone:Bones,
}

def get_dependency_costs(needs, costs):
	for c in costs:
		if c in item_module_map:
			module = item_module_map[c]
			needs[module.id] = module
			needs[module.id].need = costs[c]
			get_dependency_costs(needs, needs[module.id].get_dependency_costs_for_need(needs[module.id]))
	
def clear(supposed_to_harvest = False):
	if not supposed_to_harvest:
		clear_super()
		return
		
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			Movement.move_to(x, y)
			harvest()

def main():
	quick_print("Spawned drones :" + str(num_drones()))
	clear() 
	while True:
		goal = unlocks.get_next_goal()
		#goal = (Unlocks.Simulation,{Items.Gold:5000}) # set goal manually
		quick_print("Unlocks goal: " + str(goal[0]) + " - Needs " + str(goal[1]))

		needs = {}
		for g in goal[1]:
			module = item_module_map[g]
			needs[module.id] = module
			needs[module.id].need = goal[1][g]
			get_dependency_costs(needs, needs[module.id].get_dependency_costs_for_need(needs[module.id]))		

		for module_id in needs:
			x = 0
			y = 0
			area_size = get_world_size()
			module = needs[module_id]
			quick_print("Farming " + str(module.item) + " with need of " + str(module.need) + ". Contingent of " + str(num_items(module.item)))
			while module.is_cost_need_reached(module) and module.are_costs_covered_to_plant(module):
				time_start = get_time()
				for x in range(get_world_size()):
					if module.is_cost_need_reached(module):
						break
					for y in range(get_world_size()):
						if module.is_cost_need_reached(module):
							break
						Movement.move_to(x,y)
						module.try_to_plant(module)
				if can_harvest():
					harvest()
		unlocks.try_unlock(goal[0])

if __name__ == "__main__":
	for dro in range(max_drones()):
		spawn_drone(main)