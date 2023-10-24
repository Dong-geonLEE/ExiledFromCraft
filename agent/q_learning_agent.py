import json
import random as rd
import numpy as np

from collections import defaultdict

# https://gymnasium.farama.org/tutorials/training_agents/blackjack_tutorial/

"""
q-value based agent following the rules from Sutton & Barto.

"""

class ValueBasedAgent:
    def __init__(self, num_episodes, action_pool: int):
        super().__init__()

        """
        observation_space_dim = [number of actions] * [total number of mods] * [max number of mod for an item]
        """

        if action_pool == 1:
            num_actions = 15

        elif action_pool == 2:
            num_actions = 118

        self.action_space_dim = (1, num_actions)              # number of actions
        self.observation_space_dim = (11,)                    # number of observations

        self.q_value = defaultdict(lambda: np.zeros(self.action_space_dim[1]), )
        # self.q_value = defaultdict(lambda: np.full(self.action_space_dim[1], fill_value=10))
        # self.q_value = defaultdict(lambda: np.random.rand(self.action_space_dim[1]), )

        self.exploration_rate = 0.99
        self.decay_rate = self.exploration_rate / (num_episodes / 2)
        self.discount_rate = 0.95
        self.learning_rate = 0.005
        self.final_epsilon = 0.1

        self.training_error = []

    def _get_observation(self, iteminfo):
        observation = []

        for p in iteminfo['explicit']['prefix']:
            if iteminfo['explicit']['prefix'][p] != None:
                observation.append(iteminfo['explicit']['prefix'][p])

        for s in iteminfo['explicit']['suffix']:
            if iteminfo['explicit']['suffix'][s] != None:
                observation.append(iteminfo['explicit']['suffix'][s])

        observation.sort()
        observation = set(observation)

        return observation

    def _get_observation_as_number(self, iteminfo):
        observation = []
        obs = []

        for p in iteminfo['explicit']['prefix']:
            observation.append(iteminfo['explicit']['prefix'][p])

        for s in iteminfo['explicit']['suffix']:
            observation.append(iteminfo['explicit']['suffix'][s])

        with open('src/env/mods_num.json') as f:
            mods_num_dict = json.load(f)

        for o in observation:
            if o is None:
                obs.append(-1)

            else:
                num = mods_num_dict[o]
                obs.append(num)

        return obs

    def _get_actions(self, iteminfo):
        exploration_rate = self.exploration_rate
        q_value = self.q_value

        with open('env/src/json/actions_pool_1.json') as f:
            action_space = json.load(f)
        action_key = list(action_space.keys())

        observation = self._get_observation(iteminfo)
        observation = tuple(observation)

        ex = rd.random()

        # random selection
        if ex < exploration_rate:
            action = int(rd.choice(action_key))

        # greedy selection
        elif ex >= exploration_rate:
            action = int(np.argmax(q_value[observation]))

        return action

    def value_update(self, observation, action, reward, terminated, next_observation):
        observation = tuple(observation)
        next_observation = tuple(next_observation)

        future_q_value = (not terminated) * np.max(self.q_value[next_observation])
        td = (reward + self.discount_rate * future_q_value - self.q_value[observation][action])

        self.q_value[observation][action] = (
            self.q_value[observation][action] + self.learning_rate * td
        )
        self.training_error.append(td)

    def decay_epsilon(self):
        self.exploration_rate = max(self.final_epsilon, self.exploration_rate - self.decay_rate)