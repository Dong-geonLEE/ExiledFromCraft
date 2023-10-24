import json
import random as rd

def _generating_random_goal_state(item_class):
    with open('env/src/json/global_mods.json') as f:
        mods_dict = json.load(f)

    goal = []
    goal_groups = []

    mods = mods_dict[item_class]
    mods_list = list(mods.keys())

    num_goal = rd.choices(population=range(4, 7), weights=[3, 2, 1])[0]

    while len(goal) < num_goal:
        r = rd.choices(population=mods_list, weights=mods['mod_weight'])[0]
        r_group = mods[r]['groups']

        if r_group not in goal_groups:
            goal.append(r)
            goal_groups.append(mods[r]['groups'])

    goal = set(goal)
    return goal