id = 2
need = 0
item = Items.Wood


def is_cost_need_reached(module):
	conti = num_items(module.item)
	target = module.need
	return conti >= target


def run(module):
	for x in range(get_world_size()):
		if module.is_cost_need_reached(module):
			break
		for y in range(get_world_size()):
			if module.is_cost_need_reached(module):
				break
			movement.move_to(x, y)
			module.try_to_plant(module)
	if can_harvest():
		harvest()


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
	if can_plant(module):
		plant(list(module.requirements["entities"])[0])


def woods_main():
	print("woods.main - not yet implemented")


if __name__ == "__main__":
	woods_main()
