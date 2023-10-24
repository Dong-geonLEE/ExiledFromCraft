import torch
import torch.nn as nn

from torch import optim

class A2C(nn.Module):
    def __init__(self,
                 n_features: int,
                 action_pool: int,
                 device: torch.device,
                 critic_lr: float,
                 actor_lr: float,
                 n_envs: int, ):
        super().__init__()
        self.device = device
        self.n_envs = n_envs

        if action_pool == 1:
            n_actions = 14

        elif action_pool == 2:
            n_actions = 118

        critic_layers = [
            nn.Linear(n_features, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        ]

        actor_layer = [
            nn.Linear(n_features, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, n_actions),
        ]

        for m in self.modules():
            if isinstance(m, nn.Linear):
                torch.nn.init.orthogonal_(m)

        self.critic = nn.Sequential(*critic_layers).to(self.device)
        self.actor = nn.Sequential(*actor_layer).to(self.device)

        self.critic_optim = optim.RMSprop(self.critic.parameters(), lr=critic_lr)
        self.actor_optim = optim.RMSprop(self.actor.parameters(), lr=actor_lr)

    def forward(self, x):
        x = torch.Tensor(x).to(self.device)
        state_values = self.critic(x)
        action_logits_vec = self.actor(x)

        return (state_values, action_logits_vec)

    def select_action(self, x):
        state_values, action_logits = self.forward(x)
        action_pd = torch.distributions.Categorical(
            logits=action_logits
        )
        actions = action_pd.sample()
        action_log_prob = action_pd.log_prob(actions)
        entropy = action_pd.entropy()

        return (actions, action_log_prob, state_values, entropy)

    def get_losses(self, rewards, action_log_probs, value_preds, entropy, masks, gamma, lam, ent_coef, device):
        T = len(rewards)
        advantages = torch.zeros(T, self.n_envs, device=device)

        gae = 0.0
        for t in reversed(range(T - 1)):
            td_error = (
                    rewards[t] + gamma * masks[t] * value_preds[t + 1] - value_preds[t]
            )
            gae = td_error + gamma * lam * masks[t] * gae
            advantages[t] = gae

        critic_loss = advantages.pow(2).mean()

        actor_loss = (
                -(advantages.detach() * action_log_probs).mean() - ent_coef * entropy.mean()
        )

        return (critic_loss, actor_loss)

    def update_parameters(self, critic_loss, actor_loss):
        self.critic_optim.zero_grad()
        critic_loss.backward()
        self.critic_optim.step()

        self.actor_optim.zero_grad()
        actor_loss.backward()
        self.actor_optim.step()