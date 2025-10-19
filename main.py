quick_print(get_cost(Entities.Carrot))

from bones import bones_main
from cacti import cacti_main
from carrots import carrots_main
from hay import hay_main
from mazes import mazes_main
from pumpkins import pumpkins_main
from weird_substances import weird_substances_main
from woods import woods_main

import movement
import unlocks

clear_super = clear

item_module_map = {
	Items.Bone: bones,
	Items.Cactus: cacti,
	Items.Carrot: carrots,
	Items.Gold: mazes,
	Items.Hay: hay,
	Items.Pumpkin: pumpkins,
	Items.Weird_Substance: weird_substances,
	Items.Wood: woods,
}


def get_dependency_costs(needs, costs):
	for c in costs:
		if c in item_module_map:
			module = item_module_map[c]
			needs[module.id] = module
			needs[module.id].need = costs[c]
			get_dependency_costs(
				needs, needs[module.id].get_dependency_costs_for_need(needs[module.id])
			)


def clear(supposed_to_harvest=False):
	if not supposed_to_harvest:
		clear_super()
		return

	for x in range(get_world_size()):
		for y in range(get_world_size()):
			movement.move_to(x, y)
			harvest()


def main():
	bones_main()
	cacti()
	carrots()
	hay()
	mazes()
	pumpkins()
	weird_substances()
	woods()

	quick_print("Spawned drones :" + str(num_drones()))
	clear()
	while True:
		goal = unlocks.get_next_goal()
		goal = (Unlocks.Simulation, {Items.Gold: 5000})  # set goal manually
		quick_print("Unlocks goal: " + str(goal[0]) + " - Needs " + str(goal[1]))

		needs = {}
		for g in goal[1]:
			module = item_module_map[g]
			needs[module.id] = module
			needs[module.id].need = goal[1][g]
			get_dependency_costs(
				needs, needs[module.id].get_dependency_costs_for_need(needs[module.id])
			)

		for module_id in needs:
			x = 0
			y = 0
			area_size = get_world_size()
			module = needs[module_id]
			quick_print(
				"Farming "
				+ str(module.item)
				+ " with need of "
				+ str(module.need)
				+ ". Contingent of "
				+ str(num_items(module.item))
			)
			while not module.is_cost_need_reached(
				module
			) and module.are_costs_covered_to_plant(module):
				time_start = get_time()
				module.run()
		unlocks.try_unlock(goal[0])


if __name__ == "__main__":
	for dro in range(max_drones()):
		test = spawn_drone(main)
		quick_print(test)


# indent fixen
# jede datei zB mazes.py muss für sich selbst laufen können
# costs berechnung nicht in main machen sondern in jeder datei selbst
# alle gleichen functions auslagern und dann importen
# OOP pattern funktioniert einfach nicht
