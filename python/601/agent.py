import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy
from keras.utils import to_categorical
from torch import Tensor


def write_in_action(env, combat_mode, vel_cmd, horizontal_cmd, vertical_cmd, ny_cmd, flag_after_burning, m_target, s_action, i):
    s_action = s_action - 1

    env.action_interface['AMS'][i]["SemanticManeuver"]["combat_mode"]["value"] = combat_mode
    # print('===')
    # print(env.action_interface['AMS'][i]["SemanticManeuver"]["combat_mode"]["value"])
    # vel_cmd action mapping
    vel_cmd = vel_cmd * 46 + 250

    env.action_interface['AMS'][i]["SemanticManeuver"]["vel_cmd"]["value"] = vel_cmd
    env.action_interface['AMS'][i]["SemanticManeuver"]["horizontal_cmd"]["value"] = horizontal_cmd
    env.action_interface['AMS'][i]["SemanticManeuver"]["vertical_cmd"]["value"] = vertical_cmd
    env.action_interface['AMS'][i]["SemanticManeuver"]["ny_cmd"]["value"] = ny_cmd
    env.action_interface['AMS'][i]["SemanticManeuver"]["flag_after_burning"]["value"] = flag_after_burning
    env.action_interface['AMS'][i]["SemanticManeuver"]["maneuver_target"]["value"] = m_target
    env.action_interface['AMS'][i]["action_shoot_target"]["value"] = s_action

    env.action_interface['AMS'][i]["SemanticManeuver"]['clockwise_cmd']['value'] = 0
    env.action_interface['AMS'][i]["action_shoot_predict_list"][0]["shoot_predict"]["value"] = 0
    env.action_interface['AMS'][i]["action_shoot_predict_list"][1]["shoot_predict"]["value"] = 0
    env.action_interface['AMS'][i]["action_target"]["value"] = 3 - i

def select_action(input_tensor, mask=1, sample=True):
    input_tensor = torch.exp(input_tensor.squeeze()) * mask
    prob = input_tensor / torch.sum(input_tensor)

    if sample:
        try:
            a = prob.multinomial(1).item()
        except RuntimeError as e:
            print(e)
            # print('prob:', prob)
            # print('input:', input_tensor)
            # print('mask:', mask)
            a = prob.argmax(-1).item()

    else:
        a = prob.argmax(-1).item()
    # return a, th.log(prob)[a].item()
    return a, prob[a].item()


def AAM_remain_one_hot(ret, count):
    if count < 1:
        one_hot = np.array([1, 1, 1, 0, 0, 0, 0])
        for i in range(7):
            ret.append(one_hot[i])
    else:
        one_hot = np.hstack((np.array([0, 0]), to_categorical(count, 5)))
        for i in range(7):
            ret.append(one_hot[i])


def to_one_hot(ret, value, dim):
    one_hot = to_categorical(value, 2)
    for i in range(dim):
        ret.append(one_hot[i])


def get_ith_aircraft_state(env, i: int, all_relative_obs=False):
    ret = []
    aircraft_i = env.state_interface["AMS"][i]  # aircraft manager system

    AAM_remain_one_hot(ret, aircraft_i["AAM_remain"]["value"])  # 剩余导弹数量  7维  one-hot

    for j in range(len(aircraft_i["RadarModel"])):  # 火控雷达list--有几个敌人就有几个火控雷达状态
        to_one_hot(ret, aircraft_i["RadarModel"][j]["FCR_locked"]["value"], 2)  # 对其中一个敌人的火控雷达状态   2维度  one-hot
    for j in range(len(aircraft_i["FCSModel"])):  # 火控系统list--有几个敌人就有几个火控系统状态
        to_one_hot(ret, aircraft_i["FCSModel"][j]["FCS_available"]["value"], 2)  # 火控系统是否捕捉到敌机  2维  one-hot

    # for j in range(len(aircraft_i["SMS"])):  # 导弹控制系统，4枚导弹的状态
    #     for k in range(len(aircraft_i["SMS"][j]["FCSGuide"])):
    #         ret.append(self.normalize(aircraft_i["SMS"][j]["FCSGuide"][k]["fcs_guide_info"]))  # 友军飞机的fcs是否对导弹制导了
    #     for l in range(len(aircraft_i["SMS"][j]["RadarGuide"])):
    #         ret.append(
    #             self.normalize(aircraft_i["SMS"][j]["RadarGuide"][l]["radar_guide_info"]))  # 友军飞机的radar是否对导弹制导了

    for j in range(len(aircraft_i["RWRModel"])):  # 被动雷达(雷达告警器)----有几个敌人就有几个被动雷达状态
        to_one_hot(ret, aircraft_i["RWRModel"][j]["RWR_fetched"]["value"], 2)  # RWR 是否捕获了雷达信号 2维  one-hot
    to_one_hot(ret, aircraft_i["RWR_nailed"]["value"], 2)  # 导弹危险警报状态,被敌方导弹锁定状态   2维  one-hot
    to_one_hot(ret, aircraft_i["RWR_spiked"]["value"], 2)  # 危险警报状态,被敌方雷达锁定状态   2维  one-hot

    for j in range(len(env.state_interface["AMS"])):  # 战机是否活着
        to_one_hot(ret, env.state_interface["AMS"][env.resort(i, j)]["alive"]["value"], 2)  # 战机是否活着  2维  one-hot

    ret.append(env.normalize(aircraft_i["TAS"]))  # 飞机的真实空速  1维度 int
    ret.append(env.normalize(aircraft_i["Vg_0"]))  # TAS的x轴分量  1维度 int
    ret.append(env.normalize(aircraft_i["Vg_1"]))  # TAS的x轴分量  1维度 int
    ret.append(env.normalize(aircraft_i["Vg_2"]))  # TAS的Z轴分量  1维度 int
    ret.append(env.normalize(aircraft_i["Xg_0"]))  # 飞机位置的x坐标  1维度 连续值
    ret.append(env.normalize(aircraft_i["Xg_1"]))  # 飞机位置的y坐标  1维度 连续值
    ret.append(env.normalize(aircraft_i["Xg_2"]))  # 飞机位置的z坐标  1维度 连续值
    ret.append(env.normalize(aircraft_i["h_dot"]))  # 爬升率 1维度 int
    ret.append(env.normalize(aircraft_i["residual_chi"]))  # 期望航向角减去当前航向角  1维度 连续值

    for j in range(len(env.state_interface["AMS"])):  # 遍历全局四架飞机的导弹击中目标剩余时间 16维度 int
        for k in env.state_interface["AMS"][env.resort(i, j)]["SMS"]:
            ret.append(1.0 - env.normalize(k["TGO"]))  # 导弹击中目标剩余时间 1维度 int

    temp = []
    if not all_relative_obs:
        for j in range(env.red + env.blue):
            env.to_list(temp, aircraft_i["relative_observation"][env.resort(i, j)])
    else:
        for j in range(env.blue + env.red):
            for t in range(j + 1, env.red + env.blue):
                env.to_list(temp, env.state_interface["AMS"][env.resort(i, j)]["relative_observation"][
                    env.resort(i, t)])
    for k in temp:
        ret.append(env.normalize(k))
    return ret


class Agent():
    def __init__(self):
        self.begin = 0
        self.interval = 12
        self.maneuver = ['F22semantic', 'F22semantic', 'F22semantic', 'F22semantic']
        self.red_maneuver = ['F22semantic', 'F22semantic']
        self.blue_maneuver = ['F22semantic', 'F22semantic']
        self.name = 'wangche'
        self.interval = 4

        self.red_1_actor = PPOlstmDiscrete(98, 256)
        self.red_1_actor.load_state_dict(torch.load('./model/wangche/model0'))
        self.red_2_actor = PPOlstmDiscrete(98, 256)
        self.red_2_actor.load_state_dict(torch.load('./model/wangche/model0'))
        self.blue_1_actor = PPOlstmDiscrete(98, 256)
        self.blue_1_actor.load_state_dict(torch.load('./model/wangche/model1'))
        self.blue_2_actor = PPOlstmDiscrete(98, 256)
        self.blue_2_actor.load_state_dict(torch.load('./model/wangche/model1'))
        print("model load success")

    def team(self, team):
        self.ourteam = team
        if team == 'blue':
            self.begin = 2
        else:
            self.begin = 0

    def get_maneuver(self):
        if self.ourteam == 'blue':
            return self.blue_maneuver
        else:
            return self.red_maneuver

    def gen_action(self, env):
        states = [(get_ith_aircraft_state(env, i, True)) for i in range(self.begin, self.begin + 2)]
        for i in range(len(states)):
           states[i][64] = 0.
           states[i][71] = 0.
           states[i][78] = 0.
           states[i][85] = 0.


        # print("state mean:", states[0])
        shoot_target_masks = [copy.deepcopy(env.action_interface["AMS"][agent_id]["action_shoot_target"]["mask"])
                              for agent_id in range(4)]

        maneuver_target_masks = [
            env.action_interface["AMS"][agent_id]["SemanticManeuver"]["maneuver_target"]["mask"] for agent_id in
            range(4)]

        flag_after_burning_masks = [
            env.action_interface["AMS"][agent_id]["SemanticManeuver"]["flag_after_burning"]["mask"] for agent_id in
            range(4)]

        horizontal_cmd_masks = [env.action_interface["AMS"][agent_id]["SemanticManeuver"]["horizontal_cmd"]["mask"]
                                for agent_id in range(4)]

        vertical_cmd_masks = [
            env.action_interface["AMS"][agent_id]["SemanticManeuver"]["vertical_cmd"]["mask"] for agent_id in
            range(4)]


        [shoot_target_masks[i].insert(0, 1.0) for i in range(4)]

        h_out0 = h_out1 = h_out2 = h_out3 = (torch.zeros([1, 1, 256], dtype=torch.float32),
                                             torch.zeros([1, 1, 256], dtype=torch.float32))
        h_in0 = h_out0
        h_in1 = h_out1
        h_in2 = h_out2
        h_in3 = h_out3

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

        # vel_cmd_mean, vel_cmd_logstd, horizontal_cmd, horizontal_cmd_p, vertical_cmd, vertical_cmd_p, ny_cmd, ny_cmd_p, flag_after_burning, flag_after_burning_p, m_target, m_target_p, s_action, s_action_p, value, lstm_hidden
        if self.begin >= 2:
            vel_cmd2, vel_cmd_p2, horizontal_cmd2, horizontal_cmd_p2, vertical_cmd2, vertical_cmd_p2, ny_cmd2, ny_cmd_p2, flag_after_burning2, flag_after_burning_p2, m_target2, m_target_p2, s_action2, s_action_p2, h_out2 = \
                self.blue_1_actor((Tensor(states[0]).unsqueeze(0), h_in2),
                                  shoot_target_mask=Tensor(shoot_target_masks[2]),
                                  maneuver_target_mask=Tensor(maneuver_target_masks[2]),
                                  flag_after_burning_mask=Tensor(flag_after_burning_masks[2]),
                                  horizontal_cmd_mask=Tensor(horizontal_cmd_masks[2]),
                                  vertical_cmd_mask=Tensor(vertical_cmd_masks[2]))
            vel_cmd3, vel_cmd_p3, horizontal_cmd3, horizontal_cmd_p3, vertical_cmd3, vertical_cmd_p3, ny_cmd3, ny_cmd_p3, flag_after_burning3, flag_after_burning_p3, m_target3, m_target_p3, s_action3, s_action_p3, h_out3 = \
                self.blue_2_actor((Tensor(states[1]).unsqueeze(0), h_in3),
                                  shoot_target_mask=Tensor(shoot_target_masks[3]),
                                  maneuver_target_mask=Tensor(maneuver_target_masks[3]),
                                  flag_after_burning_mask=Tensor(flag_after_burning_masks[3]),
                                  horizontal_cmd_mask=Tensor(horizontal_cmd_masks[3]),
                                  vertical_cmd_mask=Tensor(vertical_cmd_masks[3]))
            # print("action2:", vel_cmd2, horizontal_cmd2,  vertical_cmd2, ny_cmd2, flag_after_burning2, m_target2, s_action2)
            write_in_action(env, 0, vel_cmd2, horizontal_cmd2, vertical_cmd2, ny_cmd2, flag_after_burning2,
                                m_target2, s_action2, 2)
            # print("action3:", vel_cmd3, horizontal_cmd3, vertical_cmd3, ny_cmd3, flag_after_burning3, m_target3, s_action3)
            write_in_action(env, 0, vel_cmd3, horizontal_cmd3, vertical_cmd3, ny_cmd3, flag_after_burning3,
                                m_target3, s_action3, 3)
        else:
            vel_cmd0, vel_cmd_p0, horizontal_cmd0, horizontal_cmd_p0, vertical_cmd0, vertical_cmd_p0, ny_cmd0, ny_cmd_p0, flag_after_burning0, flag_after_burning_p0, m_target0, m_target_p0, s_action0, s_action_p0, h_out0 = \
                self.red_1_actor((Tensor(states[0]).unsqueeze(0), h_in0),
                                 shoot_target_mask=Tensor(shoot_target_masks[0]),
                                 maneuver_target_mask=Tensor(maneuver_target_masks[0]),
                                 flag_after_burning_mask=Tensor(flag_after_burning_masks[0]),
                                 horizontal_cmd_mask=Tensor(horizontal_cmd_masks[0]),
                                 vertical_cmd_mask=Tensor(vertical_cmd_masks[0]))
            vel_cmd1, vel_cmd_p1, horizontal_cmd1, horizontal_cmd_p1, vertical_cmd1, vertical_cmd_p1, ny_cmd1, ny_cmd_p1, flag_after_burning1, flag_after_burning_p1, m_target1, m_target_p1, s_action1, s_action_p1, h_out1 = \
                self.red_2_actor((Tensor(states[1]).unsqueeze(0), h_in1),
                                 shoot_target_mask=Tensor(shoot_target_masks[1]),
                                 maneuver_target_mask=Tensor(maneuver_target_masks[1]),
                                 flag_after_burning_mask=Tensor(flag_after_burning_masks[1]),
                                 horizontal_cmd_mask=Tensor(horizontal_cmd_masks[1]),
                                 vertical_cmd_mask=Tensor(vertical_cmd_masks[1]))
            # print("action0:", vel_cmd0, horizontal_cmd0, vertical_cmd0, ny_cmd0, flag_after_burning0, m_target0, s_action0)
            write_in_action(env, 0, vel_cmd0, horizontal_cmd0, vertical_cmd0, ny_cmd0, flag_after_burning0,
                                m_target0, s_action0, 0)
            # print("action1:", vel_cmd1, horizontal_cmd1, vertical_cmd1, ny_cmd1, flag_after_burning1, m_target1, s_action1)
            write_in_action(env, 0, vel_cmd1, horizontal_cmd1, vertical_cmd1, ny_cmd1, flag_after_burning1,
                                m_target1, s_action1, 1)


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
        # self.vel_cmd_mean_linear = nn.Linear(hidden_layer_size, 1)
        # self.vel_cmd_logstd_linear = nn.Parameter(torch.zeros(hidden_layer_size, 1))

        # The horizontal_cmd layer
        self.horizontal_cmd_linear = nn.Linear(hidden_layer_size, 8)

        # The vertical_cmd layer
        self.vertical_cmd_linear = nn.Linear(hidden_layer_size, 7)

        # The ny_cmd layer
        self.ny_cmd_linear = nn.Linear(hidden_layer_size, 10)

        # The flag_after_burning layer
        self.flag_after_burning_linear = nn.Linear(hidden_layer_size, 2)

        # The maneuver_target layer
        self.m_target_linear = nn.Linear(hidden_layer_size, 4)

        # The shoot_action layer
        self.s_action_linear = nn.Linear(hidden_layer_size, 3)

    def _main_part(self, inputs, hidden):
        x = F.leaky_relu(self.linear1(inputs))
        x = F.leaky_relu(self.linear2(x))
        # 把原先tensor中的数据按照行优先的顺序排成一个一维的数据（这里应该是因为要求地址是连续存储的）,然后按照参数组合成其他维度的tensor.
        # -1在这里的意思是让电脑帮我们计算,这个维度应该是多少
        x = x.view(1, x.size(0), -1)  # reshape x

        # x的3维 seq_len表示每个batch输入多少数据, batch表示把数据分成了batch批, input_size表示每个数据的属性向量的长度
        x, lstm_hidden = self.lstm(x, hidden)

        x = x.view(x.size(1), -1)
        return x, lstm_hidden

    def forward(self, inputs, shoot_target_mask, maneuver_target_mask, flag_after_burning_mask,
                horizontal_cmd_mask, vertical_cmd_mask):
        inputs, hidden = inputs

        x, lstm_hidden = self._main_part(inputs, hidden)

        # if math.isnan(x[0][0]):
        #     print(inputs)
        #     print(memories.memory[memories.memory.__len__()-1].m_target)
            # print(hidden)
            # print(x)
            # print(lstm_hidden)

        vel_cmd_dis = F.softmax(self.vel_cmd_linear(x), dim=1)
        # vel_cmd_mean = self.vel_cmd_mean_linear(vel_cmd_dis)
        # vel_cmd_logstd = self.vel_cmd_logstd_linear.expand_as(vel_cmd_mean)
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
            # print(m)
            if isinstance(m, nn.Linear):
                # print(m.weight.data.type())
                # input()
                m.weight.data.fill_(1.0)
                nn.init.xavier_uniform_(m.weight, gain=nn.init.calculate_gain('leaky_relu'))
                # print(m.weight)

            if isinstance(m, nn.LSTMCell):
                # use orthogonal init for LSTM weights
                nn.init.orthogonal(m.weight_ih)
                nn.init.orthogonal(m.weight_hh)
                # use zero init for GRU layer0 bias
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


