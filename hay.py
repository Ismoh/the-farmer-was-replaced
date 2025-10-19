import costs

id = 1
need = 0
item = Items.Hay


def can_plant():
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


def try_to_plant(entities):
	if not costs.are_costs_covered_to_plant(entities):
		return
	if can_plant():
		plant(list(entities)[0])


def hay_main():
	print("hay.main - not yet implemented")


if __name__ == "__main__":
	hay_main()
