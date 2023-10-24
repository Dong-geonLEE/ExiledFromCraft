from FrozenLakeGrid import FrozenLakeEnv_Basic, FrozenLakeEnv_SemiReward_Basic, FrozenLakeEnv_Strict, FrozenLakeEnv_SemiReward_Strict
from FrozenLakeGrid8x8 import creaft_8x8_frozen_lake_grid

import random as rd

class FrozenLakeEnv():
    def __init__(self, env_name: str):
        self.num_step = 0
        self.start_state = int(0)
        self.state = self.start_state

        if env_name == 'FrozenLakeEnv_Basic':
            self.env = FrozenLakeEnv_Basic

        elif env_name == 'FrozenLakeEnv_SemiReward_Basic':
            self.env = FrozenLakeEnv_SemiReward_Basic

        elif env_name == 'FrozenLakeEnv_Strict':
            self.env = FrozenLakeEnv_Strict

        elif env_name == 'FrozenLakeEnv_SemiReward_Strict':
            self.env = FrozenLakeEnv_SemiReward_Strict

        elif env_name == 'FrozenLakeEnv_SemiReward_8x8':
            self.env, self.goal, self.map = creaft_8x8_frozen_lake_grid()


    def reset(self):
        self.num_step = 0
        self.state = self.start_state
        return self.start_state

    def step_4x4(self, action):
        action_list = self.env[self.state][action]

        _, next_state, reward, terminated = rd.choices(population=action_list)[0]

        self.num_step += 1
        self.state = next_state

        if self.num_step > 100:
            reward = 0.0
            terminated = True

        return next_state, reward, terminated

    def step_8x8(self, action):
        action_list = self.env[self.state][1][action]

        _, next_state, reward, terminated = rd.choices(population=action_list)[0]

        self.num_step += 1
        self.state = next_state

        if self.num_step > 100:
            reward = 0.0
            terminated = True

        return next_state, reward, terminated