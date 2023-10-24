from env.action.orbs import *
from env.action.essence import Essences
from env.action.bench_crafting import Bench_Crafting, Aisling_Veil_Crafting
from env.item.make_item import make_item_info

import json
import random as rd

class ExiledFromCrafting_ValuebasedEnv:
    def __init__(self, goal_state=None, itemclass=None, itemlevel=None):
        self.goal_state = goal_state

        if itemlevel is None:
            itemlevel = 85
        self.iteminfo = make_item_info(item_level=itemlevel, itembase=itemclass)

        self.senarios = 0

    def _generating_random_goal_state(self, item_class):
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
        self.goal_state = goal

    def _crafting(self, action):
        iteminfo = self.iteminfo
        reward = 0

        if action == 'Prefix Bench Crafting':
            iteminfo, reward = Bench_Crafting(iteminfo)

        elif action == 'Suffix Bench Crafting':
            iteminfo, reward = Bench_Crafting(iteminfo)

        elif action == 'Aisling Veil Crafting':
            iteminfo, reward = Aisling_Veil_Crafting(iteminfo)

        return iteminfo, reward

    def _get_observation(self):
        iteminfo = self.iteminfo

        observation = []

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] != None:
                observation.append(iteminfo['explicit']['prefix'][p])

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] != None:
                observation.append(iteminfo['explicit']['suffix'][s])

        observation = set(observation)

        return observation

    def _convert_int_str_action(self, action_int):
        with open('env/src/json/actions_pool_1.json') as f:
            action_dict = json.load(f)

        action = action_dict[str(action_int)]

        if action_int < 11:
            action_type = 'orb'

        elif action_int < 15:
            action_type = 'craft'

        elif action_int < 120:
            action_type = 'essence'

        return action, action_type

    def _action_to_function(self, action, action_type):
        iteminfo = self.iteminfo
        reward = 0

        if action_type == 'essence':
            iteminfo, reward = Essences(iteminfo, action)

        elif action_type == 'craft':
            iteminfo, reward = self._crafting(action)

        else:
            a = action.split()

            action = ''

            for i in a:
                action = action + '_' + i

            action = action.lstrip()

            func = "iteminfo, reward = " + action[1:] + "(iteminfo)"

            exec(func)

        return iteminfo, reward

    def _compare_observation_to_goal(self):
        done = False
        goal_state = self.goal_state
        obs = self._get_observation()

        compare = goal_state & obs

        if len(list(compare)) > 3:
            done = True

        return done

    def transition(self, action: int):
        action, action_type = self._convert_int_str_action(action)
        iteminfo, reward = self._action_to_function(action, action_type)

        self.senarios += 1

        if reward < 0:
            terminated = True
            return iteminfo, reward, terminated

        done = self._compare_observation_to_goal()

        if done:
            reward = 100
            terminated = True

        if self.senarios > 1048:
            reward = -10
            terminated = True

        else:
            terminated = False

        return iteminfo, reward, terminated

    def reset(self):
        # create new item, with rarity is 'normal' without mods.
        iteminfo = self.iteminfo
        self.senarios = 0

        if self.goal_state == None:
            self._generating_random_goal_state(item_class=iteminfo['base'])

        if iteminfo is None:
            return make_item_info()

        elif iteminfo != None:
            itemclass = iteminfo['base']
            itemlevel = iteminfo['item_level']

            return make_item_info(itembase=itemclass, item_level=itemlevel)