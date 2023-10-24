from FrozenLake import FrozenLakeEnv

import random as rd
import numpy as np

env_list = ['FrozenLakeEnv_Basic',
            'FrozenLakeEnv_SemiReward_Basic',
            'FrozenLakeEnv_Strict',
            'FrozenLakeEnv_SemiReward_Strict']

observation_space_dim = 16
action_space_dim = 4

num_episode = 20000

learning_rate = 0.01
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = epsilon / (num_episode / 2)
min_epsilon = 0.1

for env_name in env_list:
    q_value = np.zeros([observation_space_dim, action_space_dim])
    env = FrozenLakeEnv(env_name=env_name)
    training_error = []

    q_list = []

    for seed in [1, 2, 3, 5, 8, 13, 21, 34]:
        rd.seed(seed)
        print('Env :', env_name, 'Seed :', seed)

        for episode in (range(num_episode)):
            state = env.reset()
            done = False

            while not done:
                if rd.random() < epsilon:
                    action = rd.choice(range(4))

                else: action = np.argmax(q_value[state])

                next_state, reward, terminated = env.step_4x4(action=action)

                if next_state == 15:
                    reward = 1.0
                    terminated = True

                future_q_value = (not terminated) * np.max(q_value[next_state])
                td = reward + discount_factor * future_q_value - q_value[state][action]

                q_value[state][action] = float(round(q_value[state][action] + learning_rate * td, ndigits=4))
                training_error.append(td)

                state = next_state
                done = terminated

            epsilon = max(min_epsilon, epsilon - epsilon_decay)

        q_list.append(q_value)

    q_median = np.median(q_list, axis=0)
    print('Env: ', env)
    print(q_median)
    print("=======================================")