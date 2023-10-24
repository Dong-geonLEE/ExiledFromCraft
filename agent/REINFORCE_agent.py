from policy.REINFORCE_policy import Policy_Network
from env.action.utils import item_to_observation

import torch
from torch.distributions.normal import Normal
import numpy as np
import json


# cc. https://gymnasium.farama.org/tutorials/training_agents/reinforce_invpend_gym_v26/

class REINFORCE:
    def __init__(self, obs_space_dims, action_space_dims):

        # Hyperparameters
        self.learning_rate = 1e-4  # Learning rate for policy optimization
        self.gamma = 0.99  # Discount factor
        self.eps = 1e-6  # small number for mathematical stability

        self.probs = []  # Stores probability values of the sampled action
        self.rewards = []  # Stores the corresponding rewards

        self.net = Policy_Network(obs_space_dims[0], action_space_dims[1])
        self.optimizer = torch.optim.AdamW(self.net.parameters(), lr=self.learning_rate)

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

    def sample_action(self, state) -> float:
        state = item_to_observation(state)
        state = torch.tensor(np.array([state]))
        action_means, action_stddevs = self.net(state)

        # create a normal distribution from the predicted
        #   mean and standard deviation and sample an action
        distrib = Normal(action_means[0] + self.eps, action_stddevs[0] + self.eps)
        action = distrib.sample()
        prob = distrib.log_prob(action)

        action = int(np.argmax(np.abs(action)))
        self.probs.append(prob)

        return action

    def update(self):
        running_g = 0
        gs = []

        # Discounted return (backwards) - [::-1] will return an array in reverse
        for R in self.rewards[::-1]:
            running_g = R + self.gamma * running_g
            gs.insert(0, running_g)

        deltas = torch.tensor(gs)

        loss = 0
        # minimize -1 * prob * reward obtained
        for log_prob, delta in zip(self.probs, deltas):
            loss += log_prob.mean() * delta * (-1)

        # Update the policy network
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Empty / zero out all episode-centric/related variables
        self.probs = []
        self.rewards = []

