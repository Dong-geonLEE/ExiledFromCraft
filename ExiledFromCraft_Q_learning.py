from envs.q_learning_env import ExiledFromCrafting_ValuebasedEnv
from agent.q_learning_agent import ValueBasedAgent
from env.action.utils import item_to_observation

from tqdm import tqdm

import matplotlib.pyplot as plt
import numpy as np
import json

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

num_episodes = 3000
steps = []
rewards = []

agent = ValueBasedAgent(num_episodes=num_episodes, action_pool=1)
env = ExiledFromCrafting_ValuebasedEnv(goal_state=None)

for episode in tqdm(range(int(num_episodes))):
    iteminfo = env.reset()
    done = False

    step = 0
    rew = 0

    while not done:
        action = agent._get_actions(iteminfo)
        observation = item_to_observation(iteminfo)
        new_iteminfo, reward, terminated = env.transition(action)
        next_observation = item_to_observation(new_iteminfo)

        agent.value_update(observation, action, reward, terminated, next_observation)

        done = terminated
        step += 1
        rew += reward
        iteminfo = new_iteminfo

    agent.decay_epsilon()

    # if episode % 1000 == 0:
    #     steps.append(env.steps)

    steps.append(step)
    rewards.append(rew / step)


# 학습된 q_value를 적용하였을 때의 action sequence
done = False
iteminfo = env.reset()
action_list = []

with open('env/src/json/actions_pool_1.json') as f:
    action_dict = json.load(f)

while not done:
    action = agent._get_actions(iteminfo)
    observation = item_to_observation(iteminfo)
    new_iteminfo, reward, terminated = env.transition(action)
    next_observation = item_to_observation(new_iteminfo)

    action_list.append(action_dict[str(action)])
    done = terminated
    iteminfo = new_iteminfo



print(action_list)
print(env.goal_state)
print(np.mean(steps))
print(np.mean(rewards))


rolling_length = 2000
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
fig.suptitle(
    f"Training plots for {agent.__class__.__name__} in the value based model \n"
    f"Number of Action Pool : 1"
)

# episode return
axs[0].set_title("Episode Lengths")
episode_length = (
    np.convolve(np.array(steps), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[0].plot(episode_length)
axs[0].set_xlabel("Number of episodes")

# entropy
axs[1].set_title("Avg Reward")
rewards_average = (
    np.convolve(np.array(rewards), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[1].plot(rewards_average)
axs[1].set_xlabel("Number of episodes")

plt.tight_layout()
plt.show()