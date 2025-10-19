import movement
import costs

id = 5
req_need = 0
requirements = {}
item = Items.Weird_Substance


def are_costs_covered_to_plant(module):
	# if num_items(item) < need:
	# 	return False
	# return True
	for itm in module.requirements["items"]:
		if num_items(itm) < module.need:
			return False
	return True


def try_to_plant():
	global requirements
	global item

	if costs.is_cost_need_reached(item, requirements["need"]):
		return

	if costs.are_costs_covered_to_plant(requirements):
		movement.move_to(0, 0)
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				movement.move_to(x, y)
				for entity in requirements["entities"]:
					plant(entity)
				for itm in requirements["items"]:
					use_item(itm, requirements["items"][itm])

				if costs.is_cost_need_reached(item, requirements["need"]):
					return


def try_to_harvest():
	movement.move_to(0, 0)
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			movement.move_to(x, y)
			harvest()


def set_need(req):
	global requirements
	global req_need

	requirements = req
	req_need = requirements["need"]


def run():
	if costs.is_cost_need_reached(item, requirements["need"]):
		return
	try_to_plant()
	try_to_harvest()


def weird_substances_main():
	print("weird_substances.main - not yet implemented")


if __name__ == "__main__":
	weird_substances_main()
