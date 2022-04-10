import torch.nn.functional as F
import torch.nn as nn
import torch
import ray
import numpy as np
from utils.utils import select_action

EPS = 1e-10


class PPOlstmDiscrete(nn.Module):
    def __init__(self, states, hidden_layer_size):
        super(PPOlstmDiscrete, self).__init__()

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.update_time = 0  # 更新计数器

        self.linear1 = nn.Linear(states, 256)
        self.linear2 = nn.Linear(256, 256)

        # LSTM Cells
        self.lstm = nn.LSTM(input_size=256, hidden_size=hidden_layer_size, num_layers=1, bidirectional=False)

        # The critic layer
        self.critic_linear = nn.Linear(hidden_layer_size, 1)

        # The vel_cmd layer
        self.vel_cmd_linear = nn.Linear(hidden_layer_size, 14)
        self.horizontal_cmd_linear = nn.Linear(hidden_layer_size, 8)
        self.vertical_cmd_linear = nn.Linear(hidden_layer_size, 7)
        self.ny_cmd_linear = nn.Linear(hidden_layer_size, 10)
        self.flag_after_burning_linear = nn.Linear(hidden_layer_size, 2)
        self.m_target_linear = nn.Linear(hidden_layer_size, 4)
        self.s_action_linear = nn.Linear(hidden_layer_size, 3)

    def _main_part(self, inputs, hidden):
        x = F.leaky_relu(self.linear1(inputs))
        x = F.leaky_relu(self.linear2(x))
        x = x.view(1, x.size(0), -1)  # reshape x

        x, lstm_hidden = self.lstm(x, hidden)

        x = x.view(x.size(1), -1)
        return x, lstm_hidden

    def forward(self, inputs, shoot_target_mask, maneuver_target_mask, flag_after_burning_mask,
                horizontal_cmd_mask, vertical_cmd_mask):
        inputs, hidden = inputs

        x, lstm_hidden = self._main_part(inputs, hidden)

        vel_cmd_dis = F.softmax(self.vel_cmd_linear(x), dim=1)
        horizontal_cmd_dis = F.softmax(self.horizontal_cmd_linear(x), dim=1)
        vertical_cmd_dis = F.softmax(self.vertical_cmd_linear(x), dim=1)
        ny_cmd_dis = F.softmax(self.ny_cmd_linear(x), dim=1)
        flag_after_burning_dis = F.softmax(self.flag_after_burning_linear(x), dim=1)
        m_target_dis = F.softmax(self.m_target_linear(x), dim=1)
        s_action_dis = F.softmax(self.s_action_linear(x), dim=1)
        vel_cmd, vel_cmd_p = select_action(vel_cmd_dis)
        horizontal_cmd, horizontal_cmd_p = select_action(horizontal_cmd_dis, horizontal_cmd_mask)
        vertical_cmd, vertical_cmd_p = select_action(vertical_cmd_dis, vertical_cmd_mask)
        ny_cmd, ny_cmd_p = select_action(ny_cmd_dis)
        flag_after_burning, flag_after_burning_p = select_action(flag_after_burning_dis, flag_after_burning_mask)
        m_target, m_target_p = select_action(m_target_dis, maneuver_target_mask)
        s_action, s_action_p = select_action(s_action_dis, shoot_target_mask)

        return vel_cmd, vel_cmd_p, horizontal_cmd, horizontal_cmd_p, vertical_cmd, vertical_cmd_p, ny_cmd, ny_cmd_p, flag_after_burning, flag_after_burning_p, m_target, m_target_p, s_action, s_action_p, lstm_hidden

    def forward_critic(self, states, hidden):

        x, _ = self._main_part(states, hidden)

        value = self.critic_linear(x)

        return value

    def forward_prob(self, states, hiddens):

        x, _ = self._main_part(states, hiddens)

        vel_cmd_dis = F.softmax(self.vel_cmd_linear(x), dim=1)
        horizontal_cmd_dis = F.softmax(self.horizontal_cmd_linear(x), dim=1)
        vertical_cmd_dis = F.softmax(self.vertical_cmd_linear(x), dim=1)
        ny_cmd_dis = F.softmax(self.ny_cmd_linear(x), dim=1)
        flag_after_burning_dis = F.softmax(self.flag_after_burning_linear(x), dim=1)
        m_target_dis = F.softmax(self.m_target_linear(x), dim=1)
        s_action_dis = F.softmax(self.s_action_linear(x), dim=1)

        value = self.critic_linear(x)

        return vel_cmd_dis, horizontal_cmd_dis, vertical_cmd_dis, ny_cmd_dis, flag_after_burning_dis, m_target_dis, s_action_dis, value

    def initialize_weights(self):
        print(self.modules())

        for m in self.modules():

            if isinstance(m, nn.Linear):
                m.weight.data.fill_(0.0)
                nn.init.xavier_uniform_(m.weight, gain=nn.init.calculate_gain('leaky_relu'))

            if isinstance(m, nn.LSTMCell):
                nn.init.orthogonal(m.weight_ih)
                nn.init.orthogonal(m.weight_hh)
                m.bias_ih.zero_()
                m.bias_hh.zero_()

    def get_proba(self, states, vel_cmds, horizontal_cmds, vertical_cmds, ny_cmds, flag_after_burnings,
                  m_targets, s_actions, minibatch_lstm_hidden0s, minibatch_lstm_hidden1s):
        vel_cmds_output, horizontal_cmds_output, vertical_cmds_output, ny_cmds_output, flag_after_burnings_output, m_targets_output, s_actions_output, values = self.forward_prob(
            states, (minibatch_lstm_hidden0s, minibatch_lstm_hidden1s))

        return torch.gather(vel_cmds_output, dim=1, index=vel_cmds.view(-1, 1)).squeeze(), \
               torch.gather(horizontal_cmds_output, dim=1, index=horizontal_cmds.view(-1, 1)).squeeze(), \
               torch.gather(vertical_cmds_output, dim=1, index=vertical_cmds.view(-1, 1)).squeeze(), \
               torch.gather(ny_cmds_output, dim=1, index=ny_cmds.view(-1, 1)).squeeze(), \
               torch.gather(flag_after_burnings_output, dim=1, index=flag_after_burnings.view(-1, 1)).squeeze(), \
               torch.gather(m_targets_output, dim=1, index=m_targets.view(-1, 1)).squeeze(), \
               torch.gather(s_actions_output, dim=1, index=s_actions.view(-1, 1)).squeeze(), \
               values.squeeze()

    def train_local(self, replay_buffer, config, optimizer, clip_now):

        batch = ray.get(replay_buffer.extract_data.remote())

        states = torch.cat(batch.state, 0)
        vel_cmds = torch.cat(batch.vel_cmd, 0)
        vel_cmd_probs = torch.cat(batch.vel_cmd_p, 0)
        horizontal_cmds = torch.cat(batch.horizontal_cmd, 0)
        horizontal_cmd_probs = torch.cat(batch.horizontal_cmd_p, 0)
        vertical_cmds = torch.cat(batch.vertical_cmd, 0)
        vertical_cmd_probs = torch.cat(batch.vertical_cmd_p, 0)
        ny_cmds = torch.cat(batch.ny_cmd, 0)
        ny_cmd_probs = torch.cat(batch.ny_cmd_p, 0)
        flag_after_burnings = torch.cat(batch.flag_after_burning, 0)
        flag_after_burning_probs = torch.cat(batch.flag_after_burning_p, 0)
        m_targets = torch.cat(batch.m_target, 0)
        m_target_probs = torch.cat(batch.m_target_p, 0)
        s_actions = torch.cat(batch.s_action, 0)
        s_action_probs = torch.cat(batch.s_action_p, 0)
        lstm_hidden0s = torch.cat(batch.lstm_hidden_0, 1)
        lstm_hidden1s = torch.cat(batch.lstm_hidden_1, 1)
        returns = torch.cat(batch.returns, 0)
        advantages = torch.cat(batch.advantage, 0)

        if config.advantage_norm:
            advantages = (advantages - advantages.mean()) / (advantages.std() + EPS)

        for i in range(config.num_epoch * config.batch_size // config.minibatch_size):
            minibatch_ind = np.random.choice(config.batch_size, config.minibatch_size, replace=False)

            minibatch_states = states[minibatch_ind].to(self.device)
            minibatch_vel_cmds = vel_cmds[minibatch_ind].to(self.device)
            minibatch_old_vel_cmd_probs = vel_cmd_probs[minibatch_ind].to(self.device)
            minibatch_horizontal_cmds = horizontal_cmds[minibatch_ind].to(self.device)
            minibatch_old_horizontal_cmd_probs = horizontal_cmd_probs[minibatch_ind].to(self.device)
            minibatch_vertical_cmds = vertical_cmds[minibatch_ind].to(self.device)
            minibatch_old_vertical_cmd_probs = vertical_cmd_probs[minibatch_ind].to(self.device)
            minibatch_ny_cmds = ny_cmds[minibatch_ind].to(self.device)
            minibatch_old_ny_cmd_probs = ny_cmd_probs[minibatch_ind].to(self.device)
            minibatch_flag_after_burnings = flag_after_burnings[minibatch_ind].to(self.device)
            minibatch_old_flag_after_burning_probs = flag_after_burning_probs[minibatch_ind].to(self.device)
            minibatch_m_targets = m_targets[minibatch_ind].to(self.device)
            minibatch_old_m_target_probs = m_target_probs[minibatch_ind].to(self.device)
            minibatch_s_actions = s_actions[minibatch_ind].to(self.device)
            minibatch_old_s_action_probs = s_action_probs[minibatch_ind].to(self.device)
            minibatch_lstm_hidden0s = lstm_hidden0s[:, minibatch_ind, :].to(self.device)
            minibatch_lstm_hidden1s = lstm_hidden1s[:, minibatch_ind, :].to(self.device)

            minibatch_advantages = advantages[minibatch_ind].to(self.device)
            minibatch_returns = returns[minibatch_ind].to(self.device)

            minibatch_vel_cmd_probs, minibatch_horizontal_cmd_probs, minibatch_vertical_cmd_probs, minibatch_ny_cmd_probs, minibatch_flag_after_burning_probs, minibatch_m_target_probs, minibatch_s_action_probs, minibatch_newvalues = self.get_proba(
                minibatch_states,
                minibatch_vel_cmds,
                minibatch_horizontal_cmds,
                minibatch_vertical_cmds,
                minibatch_ny_cmds,
                minibatch_flag_after_burnings,
                minibatch_m_targets, minibatch_s_actions, minibatch_lstm_hidden0s, minibatch_lstm_hidden1s)

            # minibatch_newvalues = self.forward_critic(minibatch_states).squeeze()
            # ratio normalizetion
            ratio = (minibatch_vel_cmd_probs - minibatch_old_vel_cmd_probs +
                     minibatch_horizontal_cmd_probs - minibatch_old_horizontal_cmd_probs +
                     minibatch_vertical_cmd_probs - minibatch_old_vertical_cmd_probs +
                     minibatch_ny_cmd_probs - minibatch_old_ny_cmd_probs +
                     minibatch_flag_after_burning_probs - minibatch_old_flag_after_burning_probs +
                     minibatch_m_target_probs - minibatch_old_m_target_probs +
                     minibatch_s_action_probs - minibatch_old_s_action_probs) / 8
            surr1 = ratio * minibatch_advantages

            surr2 = ratio.clamp(1 - clip_now, 1 + clip_now) * minibatch_advantages
            loss_surr = - torch.mean(torch.min(surr1, surr2))

            if config.lossvalue_norm:
                minibatch_return_6std = 6 * minibatch_returns.std()
                loss_value = torch.mean((minibatch_newvalues - minibatch_returns).pow(2)) / minibatch_return_6std
            else:
                loss_value = torch.mean((minibatch_newvalues - minibatch_returns).pow(2))

            loss_entropy = torch.mean((torch.exp(
                minibatch_vel_cmd_probs + minibatch_horizontal_cmd_probs + minibatch_vertical_cmd_probs + minibatch_ny_cmd_probs + minibatch_flag_after_burning_probs + minibatch_m_target_probs + minibatch_s_action_probs) / 7) * (
                                              (
                                                      minibatch_vel_cmd_probs + minibatch_horizontal_cmd_probs + minibatch_vertical_cmd_probs + minibatch_ny_cmd_probs + minibatch_flag_after_burning_probs + minibatch_m_target_probs + minibatch_s_action_probs) / 7))

            total_loss = loss_surr + config.loss_coeff_value * loss_value + config.loss_coeff_entropy * loss_entropy
            optimizer.zero_grad()
            total_loss.backward()
            # torch.nn.utils.clip_grad_norm(self.parameters(), 0.5)
            optimizer.step()

        current_episode = ray.get(replay_buffer.get_total_episode.remote())
        self.update_time += 1

        return current_episode
