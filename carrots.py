import costs
import movement
import utils
import unlocks

id = 3
req_need = 0
requirements = {}
item = Items.Carrot


def are_costs_covered_to_plant(module):
	for itm in module.requirements["items"]:
		if num_items(itm) < module.need:
			return False
	return True


def try_to_plant(drone_index):
	global requirements
	global item

	if costs.is_cost_need_reached(item, requirements["need"]):
		return

	if costs.are_costs_covered_to_plant(requirements):
		movement.move_to(drone_index, 0)
		for x in range(0, get_world_size(), max_drones()):
			if x > get_world_size():
				return
			for y in range(get_world_size()):
				movement.move_to(x + drone_index, y)
				for entity in requirements["entities"]:
					if get_entity_type() != entity:
						plant(entity)
						continue
				if not can_harvest():
					for itm in requirements["items"]:
						# use_item(itm, requirements["items"][itm])
						use_item(itm)

				if costs.is_cost_need_reached(item, requirements["need"]):
					return


def try_to_harvest(drone_index):
	movement.move_to(drone_index, 0)
	for x in range(0, get_world_size(), max_drones()):
		if x > get_world_size():
			return
		for y in range(get_world_size()):
			movement.move_to(x + drone_index, y)
			harvest()


def set_need(req):
	global requirements
	global req_need

	requirements = req
	req_need = requirements["need"]


def drone_run(drone_index):
	# inner drone function to be able to use parameters
	def drone():
		change_hat(Hats.Green_Hat)
		movement.move_to(drone_index, 0)
		print("Drone " + str(drone_index))
		utils.wait(100000000 * (max_drones() - drone_index))
		run(drone_index)
		return drone

	return spawn_drone(drone)


def run(drone_index):
	try_to_plant(drone_index)
	try_to_harvest(drone_index)


def main(reset_goal):
	global item
	global requirements

	quick_print("Starting carrots farming..")
	if reset_goal:
		goal = unlocks.get_next_goal(Items.Hay)
		if goal:
			# goal = (Unlocks.Simulation, {Items.Gold: 5000})
			goal_name = goal[0]
			goal_costs = goal[1]
			req_need = goal[1][list(goal[1])[0]]
			if costs.is_cost_need_reached(item, req_need):
				unlocks.try_unlock(goal[0])
				return
		else:
			goal_costs = {Items.Hay: 2000}
		total_costs = costs.get_required_costs_by_goal(goal_costs)

		for tc in total_costs:
			for itm in tc:
				req = tc[itm]
				if itm == item:
					set_need(req)
				else:
					module = utils.get_module(itm)
					module.set_need(req)
					module.run()

	d = None
	while costs.are_costs_covered_to_plant(requirements) and not costs.is_cost_need_reached(item, requirements["need"]):
		movement.move_to(0, 0)
		for i in range(max_drones()):
			if i == 0:
				continue
			d = drone_run(i)
			utils.wait(100000000)
		run(0)
		if d != None:
			wait_for(d)  # wait until all drones are done


if __name__ == "__main__":
	main(True)
