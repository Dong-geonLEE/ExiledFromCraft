import torch.nn as nn
import torch
from torch import optim
from torch.distributions import MultivariateNormal, Normal
import numpy as np

import time

from envs.Network_env import ExiledFromCrafting
from env.action.utils import item_to_observation
from agent.utils import _generating_random_goal_state

# cc. https://github.com/ericyangyu/PPO-for-Beginners/blob/master/ppo.py

class PPO(nn.Module):
    def __init__(self, action_pool: int, **hyperparameters):
        super().__init__()

        if action_pool == 1:
            num_action = 14

        elif action_pool == 2:
            num_action = 118

        self.obs_dim = (11,)
        self.act_dim = (1, num_action)

        self._init_hyperparameters(hyperparameters)

        self.actor_lr = 0.95
        self.critic_lr = 0.95

        self.episode = 0

        self.env = ExiledFromCrafting(goal_state=None)
        self.total_mean_length = []
        self.total_ep_rewards = []

        self.goal = _generating_random_goal_state(self.env.iteminfo['base'])

        critic_layers = [
            nn.Linear(self.obs_dim[0], 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        ]

        actor_layer = [
            nn.Linear(self.obs_dim[0], 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, self.act_dim[0]),
        ]

        # non-constant ini
        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.orthogonal_(m)

        self.critic = nn.Sequential(*critic_layers)
        self.actor = nn.Sequential(*actor_layer)

        self.critic_optim = optim.RMSprop(self.critic.parameters(), lr=self.critic_lr)
        self.actor_optim = optim.RMSprop(self.actor.parameters(), lr=self.actor_lr)

        self.cov_var = torch.full(size=(self.act_dim[0],), fill_value=0.5)
        self.cov_mat = torch.diag(self.cov_var)

        self.logger = {
            'delta_t': time.time_ns(),
            't_so_far': 0,              # timestep
            'i_so_far': 0,              # iteration
            'batch_lens': [],           # episodic lengths in batch
            'batch_rews': [],           # episodic returns in batch
            'actor_losses': [],         # losses of actor net in current iteration
        }

    def learn(self, total_timesteps):
        print(f"learning... Running {self.max_timesteps_per_episode} timesteps per episode, ", end='')
        print(f"{self.timesteps_per_batch} timesteps per batch for a total of {total_timesteps} timesteps")
        t_so_far = 0
        i_so_far = 0

        while t_so_far < total_timesteps:
            if self.episode > self.max_episode:
                break
            batch_obs, batch_acts, batch_log_probs, batch_rtgs, batch_lens = self.rollout()

            t_so_far += np.sum(batch_lens)
            i_so_far += 1

            self.logger['t_so_far'] = t_so_far
            self.logger['i_so_far'] = i_so_far

            V, _ = self.evaluate(batch_obs, batch_acts)
            A_k = batch_rtgs - V.detach()

            A_k = (A_k - A_k.mean()) / (A_k.std() + 1e-10)

            for _ in range(self.n_updates_per_iteration):
                V, curr_log_probs = self.evaluate(batch_obs, batch_acts)

                ratios = torch.exp(curr_log_probs - batch_log_probs)

                surr1 = ratios * A_k
                surr2 = torch.clamp(ratios, 1 - self.clip, 1 + self.clip) * A_k

                actor_loss = (-torch.min(surr1, surr2)).mean()
                critic_loss = nn.MSELoss()(V, batch_rtgs)

                self.actor_optim.zero_grad()
                actor_loss.backward(retain_graph=True)
                self.actor_optim.step()

                self.critic_optim.zero_grad()
                critic_loss.backward()
                self.critic_optim.step()

                self.logger['actor_losses'].append(actor_loss.detach())

            self._log_summary()

            if i_so_far % self.save_freq == 0:
                torch.save(self.actor.state_dict(), './ppo_actor.pth')
                torch.save(self.critic.state_dict(), './ppo_critic_pth')


    def rollout(self):
        batch_obs = []
        batch_acts = []
        batch_log_probs = []
        batch_rews = []
        batch_rtgs = []
        batch_lens = []

        ep_rews = []

        t = 0

        while t < self.timesteps_per_batch:
            ep_rews = []

            iteminfo = self.env.reset()
            obs = item_to_observation(iteminfo)

            done = False

            for ep_t in range(self.max_timesteps_per_episode):
                t += 1

                batch_obs.append(obs)

                action, log_prob = self.get_action(obs)
                action = abs(int(action))
                action = action % self.act_dim[1]
                iteminfo, rew, done = self.env.transition(action)

                cur_mods = set(iteminfo['tag']['implicits_tag'].keys())

                if self.goal & cur_mods == self.goal:
                    done = True
                    rew = 100

                obs = item_to_observation(iteminfo)

                ep_rews.append(rew)
                batch_acts.append(action)
                batch_log_probs.append(log_prob)

                if done:
                    self.episode += 1
                    break

            batch_lens.append(ep_t + 1)
            batch_rews.append(ep_rews)

        batch_obs = torch.tensor(batch_obs, dtype=torch.float)
        batch_acts = torch.tensor(batch_acts, dtype=torch.float)
        batch_log_probs = torch.tensor(batch_log_probs, dtype=torch.float)
        batch_rtgs = self.compute_rtgs(batch_rews)

        self.logger['batch_rews'] = batch_rews
        self.logger['batch_lens'] = batch_lens

        return batch_obs, batch_acts, batch_log_probs, batch_rtgs, batch_lens


    def get_action(self, obs):
        obs = torch.Tensor(obs)

        mean = self.actor(obs)
        dist = Normal(mean, self.cov_mat)

        action = dist.sample()
        log_prob = dist.log_prob(action)

        action = int(np.argmax(np.abs(action)))
        return action, log_prob.detach()


    def compute_rtgs(self, batch_rews):
        batch_rtgs = []

        for ep_rews in reversed(batch_rews):
            discounted_reward = 0

            for rew in reversed(ep_rews):
                discounted_reward = rew + discounted_reward * self.gamma
                batch_rtgs.insert(0, discounted_reward)

        batch_rtgs = torch.Tensor(batch_rtgs)

        return batch_rtgs

    def evaluate(self, batch_obs, batch_acts):
        batch_acts = batch_acts.view(batch_acts.shape[0], 1)
        V = self.critic(batch_obs).squeeze()

        mean = self.actor(batch_obs)
        dist = MultivariateNormal(mean, self.cov_mat)
        log_probs = dist.log_prob(batch_acts)

        return V, log_probs


    def _init_hyperparameters(self, hyperparameters):
        self.timesteps_per_batch = 4800
        self.max_timesteps_per_episode = 1600
        self.n_updates_per_iteration = 5
        self.lr = 0.005
        self.gamma = 0.95
        self.clip = 0.2

        self.max_episode = 100000

        self.seed = None

        for param, val in hyperparameters.items():
            exec('self.' + param + '=' + str(val))

        if self.seed != None:
            assert(type(self.seed) == int)

            torch.manual_seed(self.seed)
            print(f"Successfully set seed to {self.seed}")


    def _log_summary(self):
        delta_t = self.logger['delta_t']
        self.logger['delta_t'] = time.time_ns()
        delta_t = (self.logger['delta_t'] - delta_t) / 1e9
        delta_t = str(round(delta_t, 2))

        t_so_far = self.logger['t_so_far']
        i_so_far = self.logger['i_so_far']
        avg_ep_lens = np.mean(self.logger['batch_lens'])
        avg_ep_rews = np.mean([np.sum(ep_rews) for ep_rews in self.logger['batch_rews']])
        avg_actor_loss = np.mean([losses.float().mean() for losses in self.logger['actor_losses']])

        avg_ep_lens = str(round(avg_ep_lens, 2))
        avg_ep_rews = str(round(avg_ep_rews, 2))
        avg_actor_loss = str(round(avg_actor_loss, 2))

        self.total_mean_length.append(float(avg_ep_lens))
        self.total_ep_rewards.append(float(avg_ep_rews))

        print(flush=True)
        print(f"-------------- Iteration #{i_so_far} --------------------", flush=True)
        print(f"Average Episodic Length: {avg_ep_lens}", flush=True)
        print(f"Average Episodic Return: {avg_ep_rews}", flush=True)
        # print(f"Average Loss: {avg_actor_loss}", flush=True)
        print(f"Episodes So Far: {self.episode}", flush=True)
        # print(f"Timesteps So Far: {t_so_far}", flush=True)
        print(f"Iteration took: {delta_t} secs", flush=True)
        print(f"--------------------------------------------------------", flush=True)
        print(flush=True)

        self.logger['batch_loss'] = []
        self.logger['batch_rews'] = []
        self.logger['actor_losses'] = []