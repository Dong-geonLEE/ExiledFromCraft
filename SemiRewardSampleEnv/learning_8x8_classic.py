from FrozenLake import FrozenLakeEnv

import random as rd
import numpy as np
from tqdm import tqdm

observation_space_dim = 64
action_space_dim = 4

num_episode = 100000

learning_rate = 0.01
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = epsilon / (num_episode / 2)
min_epsilon = 0.1

q_value = np.zeros([observation_space_dim, action_space_dim])
training_error = []
success_rate = []

q_list = []

for seed in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]:
    rd.seed(seed)
    env = FrozenLakeEnv('FrozenLakeEnv_SemiReward_8x8')
    success = 0

    for episode in tqdm(range(num_episode)):
        state = env.reset()
        done = False

        while not done:
            if rd.random() < epsilon:
                action = rd.choice(range(4))

            else: action = np.argmax(q_value[state])

            next_state, reward, terminated = env.step_8x8(action=action)

            if reward < 0:
                reward = 0

            if next_state == env.goal:
                reward = 1.0
                terminated = True
                success += 1

            future_q_value = (not terminated) * np.max(q_value[next_state])
            td = reward + discount_factor * future_q_value - q_value[state][action]

            q_value[state][action] = float(round(q_value[state][action] + learning_rate * td, ndigits=4))
            training_error.append(td)

            state = next_state
            done = terminated

        epsilon = max(min_epsilon, epsilon - epsilon_decay)

    q_list.append(q_value)
    success_rate.append(success / num_episode)


q_mean = np.median(q_list, axis=0)
np.set_printoptions(precision=4, suppress=True)
print(env.map)
print(q_mean)
print(success_rate)