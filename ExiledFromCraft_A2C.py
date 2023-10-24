from tqdm import tqdm
import torch
import numpy as np
import matplotlib.pyplot as plt
import os

from envs.Network_env import ExiledFromCrafting
from agent.A2C_agent import A2C
from env.action.utils import item_to_observation
from agent.utils import _generating_random_goal_state

#cc. https://wikidocs.net/173021

os.environ['KMP_DUPLICATE_LIB_OK']='True'

action_pool = 1

n_envs = 1
n_updates = int(3e4)
n_steps_per_update = 100

gamma = 0.99
lam = 0.95
ent_coef = 0.01
actor_lr = 0.001
critic_lr = 0.005

obs_shape = (11, )

device = torch.device('cpu')

agent = A2C(obs_shape[0], action_pool, device=device, critic_lr=critic_lr, actor_lr=actor_lr, n_envs=n_envs)
env = ExiledFromCrafting(goal_state=None)
goal = _generating_random_goal_state(env.iteminfo['base'])

critic_losses = []
actor_losses = []
entropies = []
steps = []
num_epi = 0

for sample_phase in tqdm(range(n_updates)):
    if num_epi >= 100000:
        break
    ep_value_preds = torch.zeros(n_steps_per_update, n_envs, device=device)
    ep_rewards = torch.zeros(n_steps_per_update, n_envs, device=device)
    ep_action_log_probs = torch.zeros(n_steps_per_update, n_envs, device=device)
    masks = torch.zeros(n_steps_per_update, n_envs, device=device)

    if sample_phase == 0:
        iteminfo = env.reset()

    obs = item_to_observation(iteminfo)
    ep_step = 0

    for step in range(n_steps_per_update):
        actions, action_log_probs, state_value_preds, entorpy = agent.select_action(x=obs)
        action = abs(actions.item())

        next_iteminfo, reward, terminated = env.transition(action)
        ep_step += 1

        cur_mods = set(next_iteminfo['tag']['implicits_tag'].keys())

        if goal & cur_mods == goal:
            reward = 100
            terminated = True

        ep_value_preds[step] = torch.squeeze(state_value_preds)
        ep_rewards[step] = torch.tensor(reward, device=device)
        ep_action_log_probs[step] = action_log_probs

        masks[step] = torch.tensor(terminated)

        iteminfo = next_iteminfo
        obs = item_to_observation(iteminfo)

        if terminated:
            steps.append(ep_step)
            ep_step = 0
            num_epi += 1

    critic_loss, actor_loss = agent.get_losses(
        ep_rewards,
        ep_action_log_probs,
        ep_value_preds,
        entorpy,
        masks,
        gamma,
        lam,
        ent_coef,
        device
    )

    agent.update_parameters(critic_loss, actor_loss)

    critic_losses.append(critic_loss.detach().cpu().numpy())
    actor_losses.append(actor_loss.detach().cpu().numpy())
    entropies.append(entorpy.detach().cpu().numpy())

print(ep_rewards.mean(axis=0)[0])
print(np.mean(steps))

rolling_length = 2000
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 5))
fig.suptitle(
    f"Training plots for {agent.__class__.__name__} in the ExiledFromCraft \n \
             (n_steps_per_update={n_steps_per_update}, action_pool = 2)"
)

# episode return
axs[0][0].set_title("Episode Returns")
episode_returns_moving_average = (
    np.convolve(
        np.array(ep_rewards).flatten(),
        np.ones(rolling_length),
        mode="valid",
    )
    / rolling_length
)
axs[0][0].plot(episode_returns_moving_average)
axs[0][0].set_xlabel("Number of episodes")

# entropy
axs[1][0].set_title("Entropy")
entropy_moving_average = (
    np.convolve(np.array(entropies), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[1][0].plot(entropy_moving_average)
axs[1][0].set_xlabel("Number of updates")


# critic loss
axs[0][1].set_title("Critic Loss")
critic_losses_moving_average = (
    np.convolve(
        np.array(critic_losses).flatten(), np.ones(rolling_length), mode="valid"
    )
    / rolling_length
)
axs[0][1].plot(critic_losses_moving_average)
axs[0][1].set_xlabel("Number of updates")


# actor loss
axs[1][1].set_title("Actor Loss")
actor_losses_moving_average = (
    np.convolve(np.array(actor_losses).flatten(), np.ones(rolling_length), mode="valid")
    / rolling_length
)
axs[1][1].plot(actor_losses_moving_average)
axs[1][1].set_xlabel("Number of updates")

plt.tight_layout()
plt.show()