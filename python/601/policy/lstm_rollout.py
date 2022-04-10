from collections import namedtuple
from env_wrapper import EnvWrapper
from policy.lstm import PPOlstmDiscrete

import torch
import time
import ray
import copy
from torch import Tensor

Transition = namedtuple('Transition', (
    'state', 'vel_cmd', 'vel_cmd_p', 'horizontal_cmd', 'horizontal_cmd_p',
    'vertical_cmd', 'vertical_cmd_p', 'ny_cmd', 'ny_cmd_p', 'flag_after_burning', 'flag_after_burning_p', 'm_target',
    'm_target_p', 's_action', 's_action_p', 'lstm_hidden_0', 'lstm_hidden_1', 'reward'))


class Memory(object):
    def __init__(self):
        self.memory = []

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self):
        return Transition(*zip(*self.memory))

    def __len__(self):
        return len(self.memory)


@ray.remote
def worker_rollout(ps, replay_buffer, config):
    env = EnvWrapper()

    update = False
    agents = []
    # 造4个网络，并从ps中拉取和master造的网络相同的初始化参数
    weights = ray.get(ps.pull.remote())
    for k in range(config.fighter_num):
        agent = PPOlstmDiscrete(config.state_dim, config.hidden_layer_size)
        if k < 2:
            agent.load_state_dict(weights[0])
        else:
            agent.load_state_dict(weights[1])
        # agent.to('cpu')  # 如果在本地调试，将网络放在cpu上
        agents.append(agent)

    for i_episode in range(config.max_episodes):
        replay_buffer[0].count_episode.remote()

        env.reset()

        # 监听replay buffer并拉取参数
        count = 0
        while ray.get(replay_buffer[0].get_size.remote()) >= config.batch_size and ray.get(
                replay_buffer[1].get_size.remote()) >= config.batch_size and ray.get(
            replay_buffer[2].get_size.remote()) >= config.batch_size and ray.get(
            replay_buffer[3].get_size.remote()) >= config.batch_size:
            time.sleep(1)
            count += 1
            update = True
            if count >= config.timeout:
                print('ps dead, this process exit!')
                return None
        if update:
            update = False
            # 从ps上拉取参数
            weights = ray.get(ps.pull.remote())
            agents[0].load_state_dict(weights[0])
            agents[1].load_state_dict(weights[0])
            agents[2].load_state_dict(weights[1])
            agents[3].load_state_dict(weights[1])
            print('pull weights from ps at {} episode'.format(i_episode))

        memories = [Memory() for i in range(config.fighter_num)]

        h_out0 = h_out1 = h_out2 = h_out3 = (torch.zeros([1, 1, config.hidden_layer_size], dtype=torch.float32),
                                             torch.zeros([1, 1, config.hidden_layer_size], dtype=torch.float32))

        while not env.done:
            states = [(env.get_ith_aircraft_state(i, True)) for i in range(config.fighter_num)]

            shoot_target_masks = [copy.deepcopy(env.action_interface["AMS"][agent_id]["action_shoot_target"]["mask"])
                                  for agent_id in range(config.fighter_num)]

            maneuver_target_masks = [
                env.action_interface["AMS"][agent_id]["SemanticManeuver"]["maneuver_target"]["mask"] for agent_id in
                range(config.fighter_num)]

            flag_after_burning_masks = [
                env.action_interface["AMS"][agent_id]["SemanticManeuver"]["flag_after_burning"]["mask"] for agent_id in
                range(config.fighter_num)]

            horizontal_cmd_masks = [env.action_interface["AMS"][agent_id]["SemanticManeuver"]["horizontal_cmd"]["mask"]
                                    for agent_id in range(config.fighter_num)]

            vertical_cmd_masks = [
                env.action_interface["AMS"][agent_id]["SemanticManeuver"]["vertical_cmd"]["mask"] for agent_id in
                range(config.fighter_num)]

            [shoot_target_masks[i].insert(0, 1.0) for i in range(config.fighter_num)]

            h_in0 = h_out0
            h_in1 = h_out1
            h_in2 = h_out2
            h_in3 = h_out3

            # vel_cmd_mean, vel_cmd_logstd, horizontal_cmd, horizontal_cmd_p, vertical_cmd, vertical_cmd_p, ny_cmd, ny_cmd_p, flag_after_burning, flag_after_burning_p, m_target, m_target_p, s_action, s_action_p, value, lstm_hidden
            vel_cmd0, vel_cmd_p0, horizontal_cmd0, horizontal_cmd_p0, vertical_cmd0, vertical_cmd_p0, ny_cmd0, ny_cmd_p0, flag_after_burning0, flag_after_burning_p0, m_target0, m_target_p0, s_action0, s_action_p0, h_out0 = \
                agents[0]((Tensor(states[0]).unsqueeze(0), h_in0), shoot_target_mask=Tensor(shoot_target_masks[0]),
                          maneuver_target_mask=Tensor(maneuver_target_masks[0]),
                          flag_after_burning_mask=Tensor(flag_after_burning_masks[0]),
                          horizontal_cmd_mask=Tensor(horizontal_cmd_masks[0]),
                          vertical_cmd_mask=Tensor(vertical_cmd_masks[0]))
            # print("action mean:",vel_cmd0, horizontal_cmd0, vertical_cmd0, ny_cmd0, flag_after_burning0, m_target0, s_action0)
            vel_cmd1, vel_cmd_p1, horizontal_cmd1, horizontal_cmd_p1, vertical_cmd1, vertical_cmd_p1, ny_cmd1, ny_cmd_p1, flag_after_burning1, flag_after_burning_p1, m_target1, m_target_p1, s_action1, s_action_p1, h_out1 = \
                agents[1]((Tensor(states[1]).unsqueeze(0), h_in1), shoot_target_mask=Tensor(shoot_target_masks[1]),
                          maneuver_target_mask=Tensor(maneuver_target_masks[1]),
                          flag_after_burning_mask=Tensor(flag_after_burning_masks[1]),
                          horizontal_cmd_mask=Tensor(horizontal_cmd_masks[1]),
                          vertical_cmd_mask=Tensor(vertical_cmd_masks[1]))
            vel_cmd2, vel_cmd_p2, horizontal_cmd2, horizontal_cmd_p2, vertical_cmd2, vertical_cmd_p2, ny_cmd2, ny_cmd_p2, flag_after_burning2, flag_after_burning_p2, m_target2, m_target_p2, s_action2, s_action_p2, h_out2 = \
                agents[2]((Tensor(states[2]).unsqueeze(0), h_in2), shoot_target_mask=Tensor(shoot_target_masks[2]),
                          maneuver_target_mask=Tensor(maneuver_target_masks[2]),
                          flag_after_burning_mask=Tensor(flag_after_burning_masks[2]),
                          horizontal_cmd_mask=Tensor(horizontal_cmd_masks[2]),
                          vertical_cmd_mask=Tensor(vertical_cmd_masks[2]))
            vel_cmd3, vel_cmd_p3, horizontal_cmd3, horizontal_cmd_p3, vertical_cmd3, vertical_cmd_p3, ny_cmd3, ny_cmd_p3, flag_after_burning3, flag_after_burning_p3, m_target3, m_target_p3, s_action3, s_action_p3, h_out3 = \
                agents[3]((Tensor(states[3]).unsqueeze(0), h_in3), shoot_target_mask=Tensor(shoot_target_masks[3]),
                          maneuver_target_mask=Tensor(maneuver_target_masks[3]),
                          flag_after_burning_mask=Tensor(flag_after_burning_masks[3]),
                          horizontal_cmd_mask=Tensor(horizontal_cmd_masks[3]),
                          vertical_cmd_mask=Tensor(vertical_cmd_masks[3]))

            if "blue_awacs" in env.action_interface.keys():
                for i in range(env.red):
                    env.action_interface["blue_awacs"][i]["action_xg_0_est"]["value"] = -200000
                    env.action_interface["blue_awacs"][i]["action_xg_1_est"]["value"] = 50000
                    env.action_interface["blue_awacs"][i]["action_xg_2_est"]["value"] = -3000
                    env.action_interface["blue_awacs"][i]["action_vg_0_est"]["value"] = 100
                    env.action_interface["blue_awacs"][i]["action_vg_1_est"]["value"] = 100
                    env.action_interface["blue_awacs"][i]["action_vg_2_est"]["value"] = 0

            if "red_awacs" in env.action_interface.keys():
                for i in range(env.blue):
                    env.action_interface["red_awacs"][i]["action_xg_0_est"]["value"] = 100000
                    env.action_interface["red_awacs"][i]["action_xg_1_est"]["value"] = -100000
                    env.action_interface["red_awacs"][i]["action_xg_2_est"]["value"] = -3000
                    env.action_interface["red_awacs"][i]["action_vg_0_est"]["value"] = 100
                    env.action_interface["red_awacs"][i]["action_vg_1_est"]["value"] = 100
                    env.action_interface["red_awacs"][i]["action_vg_2_est"]["value"] = 0

            env.write_in_action(0, vel_cmd0, horizontal_cmd0, vertical_cmd0, ny_cmd0, flag_after_burning0,
                                m_target0, s_action0, 0)
            env.write_in_action(0, vel_cmd1, horizontal_cmd1, vertical_cmd1, ny_cmd1, flag_after_burning1,
                                m_target1, s_action1, 1)
            env.write_in_action(0, vel_cmd2, horizontal_cmd2, vertical_cmd2, ny_cmd2, flag_after_burning2,
                                m_target2, s_action2, 2)
            env.write_in_action(0, vel_cmd3, horizontal_cmd3, vertical_cmd3, ny_cmd3, flag_after_burning3,
                                m_target3, s_action3, 3)
            # Step the env
            env.step()

            # get reward
            rewards = [env.get_ith_aircraft_reward(i) for i in range(config.fighter_num)]

            if env.state_interface["AMS"][0]["alive"]["value"]:
                memories[0].push(states[0], vel_cmd0,
                                 vel_cmd_p0, horizontal_cmd0, horizontal_cmd_p0, vertical_cmd0, vertical_cmd_p0,
                                 ny_cmd0, ny_cmd_p0, flag_after_burning0, flag_after_burning_p0,
                                 m_target0, m_target_p0, s_action0, s_action_p0, h_in0[0], h_in0[1], rewards[0])
            if env.state_interface["AMS"][1]["alive"]["value"]:
                memories[1].push(states[1], vel_cmd1,
                                 vel_cmd_p1, horizontal_cmd1, horizontal_cmd_p1, vertical_cmd1, vertical_cmd_p1,
                                 ny_cmd1, ny_cmd_p1, flag_after_burning1, flag_after_burning_p1,
                                 m_target1, m_target_p1, s_action1, s_action_p1, h_in1[0], h_in1[1], rewards[1])
            if env.state_interface["AMS"][2]["alive"]["value"]:
                memories[2].push(states[2], vel_cmd2,
                                 vel_cmd_p2, horizontal_cmd2, horizontal_cmd_p2, vertical_cmd2, vertical_cmd_p2,
                                 ny_cmd2, ny_cmd_p2, flag_after_burning2, flag_after_burning_p2,
                                 m_target2, m_target_p2, s_action2, s_action_p2, h_in2[0], h_in2[1], rewards[2])
            if env.state_interface["AMS"][3]["alive"]["value"]:
                memories[3].push(states[3], vel_cmd3,
                                 vel_cmd_p3, horizontal_cmd3, horizontal_cmd_p3, vertical_cmd3, vertical_cmd_p3,
                                 ny_cmd3, ny_cmd_p3, flag_after_burning3, flag_after_burning_p3,
                                 m_target3, m_target_p3, s_action3, s_action_p3, h_in3[0], h_in3[1], rewards[3])
            if env.done:
                prev_return_list = []
                final_states = [env.get_ith_aircraft_state(i, True) for i in range(config.fighter_num)]
                prev_return_list.append(
                    (agents[0].forward_critic(Tensor(final_states[0]).unsqueeze(0), h_out0)).detach())
                prev_return_list.append(
                    (agents[1].forward_critic(Tensor(final_states[1]).unsqueeze(0), h_out1)).detach())
                prev_return_list.append(
                    (agents[2].forward_critic(Tensor(final_states[2]).unsqueeze(0), h_out2)).detach())
                prev_return_list.append(
                    (agents[3].forward_critic(Tensor(final_states[3]).unsqueeze(0), h_out3)).detach())

                for j in range(config.fighter_num):

                    batch = memories[j].sample()
                    batch_size = len(memories[j])

                    # step2: extract variables from trajectories
                    states = Tensor(batch.state)
                    vel_cmds = torch.LongTensor(batch.vel_cmd)
                    vel_cmd_probs = Tensor(batch.vel_cmd_p)
                    horizontal_cmds = torch.LongTensor(batch.horizontal_cmd)
                    horizontal_cmd_probs = Tensor(batch.horizontal_cmd_p)
                    vertical_cmds = torch.LongTensor(batch.vertical_cmd)
                    vertical_cmd_probs = Tensor(batch.vertical_cmd_p)
                    ny_cmds = torch.LongTensor(batch.ny_cmd)
                    ny_cmd_probs = Tensor(batch.ny_cmd_p)
                    flag_after_burnings = torch.LongTensor(batch.flag_after_burning)
                    flag_after_burning_probs = Tensor(batch.flag_after_burning_p)
                    m_targets = torch.LongTensor(batch.m_target)
                    m_target_probs = Tensor(batch.m_target_p)
                    s_actions = torch.LongTensor(batch.s_action)
                    s_action_probs = Tensor(batch.s_action_p)
                    lstm_hidden0s = torch.cat(batch.lstm_hidden_0, 1).detach()
                    lstm_hidden1s = torch.cat(batch.lstm_hidden_1, 1).detach()
                    rewards = Tensor(batch.reward)

                    returns = Tensor(batch_size)
                    advantages = Tensor(batch_size)

                    prev_return = prev_return_list[j]
                    # prev_advantage = 0
                    for i in reversed(range(batch_size)):
                        returns[i] = rewards[i] + config.gamma * prev_return
                        advantages[i] = (
                                returns[i] - agents[j].forward_critic(Tensor(states[i]).unsqueeze(0),
                                                                      (lstm_hidden0s[:, i, :].unsqueeze(0),
                                                                       lstm_hidden1s[:, i, :].unsqueeze(0)))).detach()

                        prev_return = returns[i]
                        # prev_advantage = advantages[i]

                    # Store experience to replay buffer
                    replay_buffer[j].push.remote(states, vel_cmds,
                                                 vel_cmd_probs, horizontal_cmds,
                                                 horizontal_cmd_probs, vertical_cmds, vertical_cmd_probs, ny_cmds,
                                                 ny_cmd_probs, flag_after_burnings, flag_after_burning_probs,
                                                 m_targets, m_target_probs, s_actions, s_action_probs, lstm_hidden0s,
                                                 lstm_hidden1s, rewards, returns, advantages)
                    replay_buffer[j].count_size.remote(batch_size)

                break
