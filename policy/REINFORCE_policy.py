import torch
from torch import nn

# cc. https://gymnasium.farama.org/tutorials/training_agents/reinforce_invpend_gym_v26/

class Policy_Network(nn.Module):
    def __init__(self, obs_space_dims, action_space_dims):
        super().__init__()

        hidden_space1 = 32
        hidden_space2 = 16

        self.shared_net = nn.Sequential(
            nn.Linear(obs_space_dims, hidden_space1),
            nn.Tanh(),
            nn.Linear(hidden_space1, hidden_space2),
            nn.Tanh(),
        )

        self.policy_mean_net = nn.Sequential(
            nn.Linear(hidden_space2, action_space_dims)
        )

        self.policy_stddev_net = nn.Sequential(
            nn.Linear(hidden_space2, action_space_dims)
        )

        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.ones_(m.weight)

    def forward(self, x):
        shared_features = self.shared_net(x.float())

        action_means = self.policy_mean_net(shared_features)
        action_stddevs = torch.log(
            1 + torch.exp(self.policy_stddev_net(shared_features))
        )

        return action_means, action_stddevs