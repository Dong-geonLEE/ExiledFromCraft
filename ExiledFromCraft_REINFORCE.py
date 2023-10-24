from envs.Network_env import ExiledFromCrafting
from agent.REINFORCE_agent import REINFORCE
from agent.utils import _generating_random_goal_state

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'
action_pool = 1

obs_space_dims = (11, )                  # obs: (int, int, int, int, int, int, int, int, int, int, int)
if action_pool == 1:
    action_space_dims = (1, 14)              # action: int

elif action_pool == 2:
    action_space_dims = (1, 118)


env = ExiledFromCrafting(goal_state=None)

total_num_episodes = 100000

agent = REINFORCE(obs_space_dims=obs_space_dims, action_space_dims=action_space_dims)
goal = _generating_random_goal_state(env.iteminfo['base'])
reward_over_episodes = []
steps_over_episodes = []

for episode in tqdm(range(total_num_episodes)):
    iteminfo = env.reset()

    done = False
    while not done:
        action = agent.sample_action(iteminfo)

        next_iteminfo, reward, terminated = env.transition(action)

        cur_mods = set(next_iteminfo['tag']['implicits_tag'].keys())
        if goal & cur_mods == goal:
            reward = 100
            terminated = True

        agent.rewards.append(reward)
        done = terminated

        iteminfo = next_iteminfo

    reward_over_episodes.append(env.return_queue[-1])
    steps_over_episodes.append(env.length_queue[-1])
    agent.update()

    if episode % 2000 == 0:
        avg_reward = int(np.mean(env.return_queue))
        print("Episode:", episode, "Average Reward :", avg_reward)


print(np.mean(steps_over_episodes))
print(np.mean(reward_over_episodes))


rolling_length = 2500
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
fig.suptitle(
    f"Training plots for {agent.__class__.__name__} in the value based model \n"
    f"Number of Action Pool : 1"
)

# episode return
axs[0].set_title("Episode Lengths")
episode_length = (
    np.convolve(np.array(steps_over_episodes), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[0].plot(episode_length)
axs[0].set_xlabel("Number of episodes")

# entropy
axs[1].set_title("Avg Reward")
rewards_average = (
    np.convolve(np.array(reward_over_episodes), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[1].plot(rewards_average)
axs[1].set_xlabel("Number of episodes")

plt.tight_layout()
plt.show()