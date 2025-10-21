id = 4
need = 0
item = Items.Pumpkin
requirements = get_cost(Entities.Pumpkin)


def get_dependency_costs_for_need(module):
	costs_need = {}
	costs = get_cost(Entities.Pumpkin)
	for itm in costs:
		contingent = num_items(item)
		diff = contingent - module.need
		if diff < 0:
			costs_need[itm] = diff * -1
	return costs_need


def are_costs_covered_to_plant(module):
	costs = get_cost(Entities.Pumpkin)
	for itm in costs:
		if not num_items(itm) > module.need * costs[itm] * 1.2:
			harvest_leftover()
			return False
	return True


def is_cost_need_reached(module):
	conti = num_items(module.item)
	target = module.need
	return conti >= target


def can_plant(module):
	if get_entity_type() == Entities.Pumpkin:
		return False
	if can_harvest():
		harvest()
	if get_ground_type() != Grounds.Soil:
		till()
		return True
	if get_entity_type() == None:
		return True
	if get_entity_type() == Entities.Dead_Pumpkin:
		till()
		till()
		return True


def try_to_plant(module):
	if not are_costs_covered_to_plant(module):
		return
	if can_plant(module):
		plant(Entities.Pumpkin)
		while not can_harvest():
			if get_water() < 1:
				use_item(Items.Water)
			if get_entity_type() == Entities.Dead_Pumpkin:
				try_to_plant()


def harvest_leftover():
	clear(True)


def pumpkins_main():
	print("pumpkins.main - not yet implemented")


if __name__ == "__main__":
	pumpkins_main()
