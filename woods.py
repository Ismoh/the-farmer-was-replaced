import costs
import movement
import unlocks
import utils

id = 2
req_need = 0
requirements = {}
item = Items.Wood


x_loop_step = (get_world_size() // max_drones()) * max_drones()
if x_loop_step == 0:
    x_loop_step = max_drones()


def get_max_drones_to_spawn():
    w_s = get_world_size()
    m_d = max_drones()
    if m_d > w_s:
        return w_s
    return m_d


def are_costs_covered_to_plant(module):
    for itm in module.requirements["items"]:
        if num_items(itm) < module.need:
            return False
    return True


def try_to_plant_and_harvest(drone_index):
    global requirements
    global item
    global x_loop_step

    if costs.is_cost_need_reached(item, requirements["need"]):
        return

    if costs.are_costs_covered_to_plant(requirements):
        for x in range(0, get_world_size(), x_loop_step):
            x = x + drone_index
            if x > get_world_size():
                return
            for y in range(get_world_size()):
                movement.move_to(x, y)

                if can_harvest():
                    harvest()

                for entity in requirements["entities"]:
                    if get_entity_type() != entity:
                        if get_ground_type() != Grounds.Soil:
                            till()
                        plant(entity)
                        continue
                if not can_harvest():
                    for itm in requirements["items"]:
                        use_item(itm)

                if costs.is_cost_need_reached(item, requirements["need"]):
                    return


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
        # print(drone_index)
        run(drone_index)
        return drone

    return spawn_drone(drone)


def run(drone_index):
    try_to_plant_and_harvest(drone_index)


def main(reset_goal, goal_costs):
    global item
    global requirements

    quick_print("Starting woods farming..")
    if reset_goal:
        goal = unlocks.get_next_goal(Items.Wood)
        if goal:
            goal_name = goal[0]
            goal_costs = goal[1]
            req_need = goal[1][list(goal[1])[0]]
            if costs.is_cost_need_reached(item, req_need):
                unlocks.try_unlock(goal[0])
                return
        else:
            if not goal_costs:
                goal_costs = {Items.Wood: 100000}
        total_costs = costs.get_required_costs_by_goal(goal_costs)

        if len(total_costs) == 0:
            # print("No depending costs.")
            req = {}
            req["entities"] = {Entities.Bush: goal_costs[Items.Wood]}  # TODO: Add Trees!
            req["items"] = {}
            req["need"] = goal_costs[Items.Wood]
            set_need(req)

        for tc in total_costs:
            for itm in tc:
                req = tc[itm]
                if itm == item:
                    set_need(req)
                else:
                    module = utils.get_module(itm)
                    module.set_need(req)
                    module.main(False)

    d = None
    while costs.are_costs_covered_to_plant(requirements) and not costs.is_cost_need_reached(item, requirements["need"]):
        movement.move_to(0, 0)
        for i in range(get_max_drones_to_spawn()):
            if i == 0:
                continue
            d = drone_run(i)
        run(0)


if __name__ == "__main__":
    main(True, None)
