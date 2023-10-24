from agent.ppo_agent import PPO

import sys
import torch
import os
import numpy as np

import matplotlib.pyplot as plt

# cc.https://github.com/ericyangyu/PPO-for-Beginners/blob/master/main.py

os.environ['KMP_DUPLICATE_LIB_OK']='True'
action_pool = 1

def train(hyperparameters, actor_model, critic_model, total_timesteps):
    print(f"Training", flush=True)

    model = PPO(action_pool=action_pool, **hyperparameters)

    if actor_model != '' and critic_model != '':
        print(f"Loading in {actor_model} and {critic_model}...", flush=True)
        model.actor.load_state_dict(torch.load(actor_model))
        model.critic.load_state_dict(torch.load(critic_model))
        print(f"Successfully loaded.", flush=True)

    elif actor_model != '' or critic_model != '':
        print(f"Error: Either specify both actor/critic models or none at all.")
        sys.exit(0)

    else:
        print(f"Training from scratch.", flush=True)

    model.learn(total_timesteps=total_timesteps)


hyperparameter = {'timesteps_per_batch': 2048, 'max_timesteps_per_episode': 512, 'gamma': 0.99, 'n_updates_per_iteration': 10, 'lr': 1e-4, 'clip': 0.2, 'save_freq': 1e15, 'seed': 42}
total_timesteps = 51200000

model = PPO(action_pool=action_pool, **hyperparameter)
model.learn(total_timesteps)

print(np.mean(model.total_mean_length))
print(np.mean(model.total_ep_rewards))

rolling_length = 50
fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
fig.suptitle(
    f"Training plots for {model.__class__.__name__} in the value based model \n"
    f"Number of Action Pool : 1"
)

# episode length
axs[0].set_title("Episode Lengths")
episode_length = (
    np.convolve(np.array(model.total_mean_length), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[0].plot(episode_length)
axs[0].set_xlabel("Number of episodes")

# avg episode reward
axs[1].set_title("Avg Reward")
rewards_average = (
    np.convolve(np.array(model.total_ep_rewards), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[1].plot(rewards_average)
axs[1].set_xlabel("Number of episodes")

plt.tight_layout()
plt.show()