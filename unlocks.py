# how hard or expensive to get the item in numbers
cost_order = {
    Items.Hay: 1,
    Items.Wood: 1,
    Items.Carrot: 2,
    Items.Pumpkin: 3,
    Items.Gold: 4,
    Items.Cactus: 5,
    Items.Weird_Substance: 6,
    Items.Water: 7,
    Items.Fertilizer: 7,
    Items.Bone: 8,
}


def filter_cheapest_unlocks(item_type=None):
    unlocks = {}
    cheapest_unlock = None
    cheapest_item = None
    cheapest_cost = 9999999999999999
    cheapest_cost_order = 9999999999999999
    if not item_type:
        quick_print("---> not yet unlocked:")
    for unl in Unlocks:  # type: ignore
        if unl not in unlocks:
            unlocks[unl] = None
        if num_unlocked(unl) == 0 or unlocks[unl] == None:
            costs = get_cost(unl)
            if len(costs) > 0:
                if is_cost_unlocked(costs):
                    unlocks[unl] = costs
                    if not item_type:
                        quick_print(str(unl) + " -> " + str(unlocks[unl]))
                    for item in costs:
                        if item_type != None and item_type != item:
                            continue
                        # quick_print(str(costs))
                        if costs[item] <= cheapest_cost and cost_order[item] <= cheapest_cost_order:
                            cheapest_unlock = unl
                            cheapest_item = costs
                            cheapest_cost = costs[item]
                            cheapest_cost_order = cost_order[item]
    if not cheapest_unlock:
        quick_print("no unlock found")
        return None
    quick_print(
        "cheapest unlock is: "
        + str(cheapest_unlock)
        + " "
        + str(cheapest_item)
        + " "
        + str(cheapest_cost)
        + " "
        + str(cheapest_cost_order)
    )
    return cheapest_unlock, cheapest_item


def filter_by_unlock(unl):
    return unl, get_cost(unl)


def is_cost_unlocked(costs):
    for item in costs:
        unlocked = num_unlocked(item)
        if unlocked == 0:
            return False
    return True


def try_unlock(unlo):
    if unlock(unlo):
        quick_print("---> YAY! " + str(unlo) + " unlocked!")
        return True
    return False


def get_next_goal(item):
    return filter_cheapest_unlocks(item)


def main():
    quick_print(str(filter_cheapest_unlocks()))
    quick_print("---> next goal for item gold:")
    quick_print(str(get_next_goal(Items.Gold)))
    quick_print("---> filter by unlock name:")
    quick_print(str(filter_by_unlock(Unlocks.Expand)))


if __name__ == "__main__":
    main()
