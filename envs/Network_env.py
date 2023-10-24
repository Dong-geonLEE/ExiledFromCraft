from env.action.orbs import *
from env.action.essence import Essences
from env.action.bench_crafting import Bench_Crafting, Aisling_Veil_Crafting
from env.item.make_item import make_item_info

from collections import deque
import numpy as np

import json
import random as rd

# https://gymnasium.farama.org/_modules/gymnasium/wrappers/record_episode_statistics/#RecordEpisodeStatistics

class ExiledFromCrafting:
    def __init__(self, goal_state=None, itemclass=None, itemlevel=None):
        self.iteminfo = make_item_info(item_level=itemlevel, itembase=itemclass)

        self.steps = 0

        self.episode_count = 0
        self.episode_returns = 0
        self.episode_lengths = 0
        self.return_queue = deque(maxlen=int(100))
        self.length_queue = deque(maxlen=int(100))

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

    def _convert_int_str_action(self, action_int):
        with open('env/src/json/actions_pool_1.json') as f:
            action_dict = json.load(f)

        action = action_dict[str(action_int)]

        if action_int < 12:
            action_type = 'orb'

        elif action_int < 15:
            action_type = 'craft'

        elif action_int < 119:
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

    def transition(self, action: int):
        action, action_type = self._convert_int_str_action(action)
        iteminfo, reward = self._action_to_function(action, action_type)

        self.iteminfo = iteminfo
        self.steps += 1

        if reward < 0:
            terminated = True

        elif self.steps > 1024:
            reward = -10
            terminated = True

        else:
            terminated = False

        self.episode_returns += reward
        self.episode_lengths += 1

        if terminated is True:
            self.return_queue.append(self.episode_returns)
            self.length_queue.append(self.episode_lengths)
            self.episode_count += 1
            self.episode_lengths = 0
            self.episode_returns = 0

        return iteminfo, reward, terminated

    def reset(self):
        # create new item, with rarity is 'normal' without mods.
        iteminfo = self.iteminfo
        self.steps = 0

        self.episode_returns = np.zeros(1)
        self.episode_lengths = np.zeros(1)

        if iteminfo is None:
            return make_item_info()

        elif iteminfo != None:
            itemclass = iteminfo['base']
            itemlevel = iteminfo['item_level']

            return make_item_info(itembase=itemclass, item_level=itemlevel)