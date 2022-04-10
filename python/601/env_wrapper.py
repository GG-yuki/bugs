from environment.battlespace import BattleSpace
from tensorflow.keras.utils import to_categorical
import numpy as np


class EnvWrapper(BattleSpace):

    def __init__(self):
        super().__init__()
        self.shoot_down = [0, 0, 0, 0]
        self.death = [0, 0, 0, 0]
        self.fire = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.crash = [0, 0, 0, 0]
        self.out_border = [0, 0, 0, 0]

    def get_ith_aircraft_all_state(self, i: int, all_relative_obs=False):
        ret = []
        aircraft_i = self.state_interface["AMS"][i]  # aircraft manager system

        ret.append(self.normalize(aircraft_i["AAM_remain"]))  # 剩余导弹数量  1维度  int

        for j in range(len(aircraft_i["FCSModel"])):  # 火控系统list--有几个敌人就有几个火控系统状态
            ret.append(self.normalize(aircraft_i["FCSModel"][j]["FCS_available"]))  # 火控系统是否捕捉到敌机  1维度  boolean

        for j in range(len(aircraft_i["RWRModel"])):  # 被动雷达(雷达告警器)----有几个敌人就有几个被动雷达状态
            ret.append(self.normalize(aircraft_i["RWRModel"][j]["RWR_fetched"]))  # RWR 是否捕获了雷达信号 1维度  boolean
        ret.append(self.normalize(aircraft_i["RWR_nailed"]))  # 导弹危险警报状态,被敌方导弹锁定状态   1维度  boolean
        ret.append(self.normalize(aircraft_i["RWR_spiked"]))  # 危险警报状态,被敌方雷达锁定状态   1维度  boolean
        for j in range(len(aircraft_i["RadarModel"])):  # 火控雷达list--有几个敌人就有几个火控雷达状态
            ret.append(self.normalize(aircraft_i["RadarModel"][j]["FCR_locked"]))  # 对其中一个敌人的火控雷达状态   1维度  boolean

        for j in range(len(aircraft_i["SMS"])):  # 导弹控制系统，4枚导弹的状态
            ret.append(self.normalize(aircraft_i["SMS"][j]["AO_m"]))  # 从速度方向到当前导弹与目标飞机之间的直线的角度的平面投影
            for k in range(len(aircraft_i["SMS"][j]["FCSGuide"])):
                ret.append(self.normalize(aircraft_i["SMS"][j]["FCSGuide"][k]["fcs_guide_info"]))  # 友军飞机的fcs是否对导弹制导了
            for l in range(len(aircraft_i["SMS"][j]["RadarGuide"])):
                ret.append(
                    self.normalize(aircraft_i["SMS"][j]["RadarGuide"][l]["radar_guide_info"]))  # 友军飞机的rarda是否对导弹制导了
            ret.append(self.normalize(aircraft_i["SMS"][j]["TAS_m"]))  # 导弹的真空速
            ret.append(self.normalize(aircraft_i["SMS"][j]["TA_m"]))  # 从当前导弹的速度方向和目标飞机的速度方向的角度的平面投影
            ret.append(
                self.normalize(aircraft_i["SMS"][j]["TGO"]))  # 导弹击中目标的剩余时间。 其范围是[0,200]。 如果导弹未发射或导弹到期，则将值设置为200。单位为秒。
            ret.append(self.normalize(aircraft_i["SMS"][j]["Vg_m_0"]))  # 导弹TAS的x轴分量
            ret.append(self.normalize(aircraft_i["SMS"][j]["Vg_m_1"]))  # 导弹TAS的y轴分量
            ret.append(self.normalize(aircraft_i["SMS"][j]["Vg_m_2"]))  # 导弹TAS的z轴分量
            ret.append(self.normalize(aircraft_i["SMS"][j]["Xg_m_0"]))  # 导弹位置的x坐标
            ret.append(self.normalize(aircraft_i["SMS"][j]["Xg_m_1"]))  # 导弹位置的y坐标
            ret.append(self.normalize(aircraft_i["SMS"][j]["Xg_m_2"]))  # 导弹位置的Z坐标
            ret.append(self.normalize(aircraft_i["SMS"][j]["attg_m_0"]))  # 导弹侧倾角，单位为弧度
            ret.append(self.normalize(aircraft_i["SMS"][j]["attg_m_1"]))  # 导弹俯仰角，单位为弧度
            ret.append(self.normalize(aircraft_i["SMS"][j]["attg_m_2"]))  # 导弹偏航角，单位为弧度
            ret.append(self.normalize(aircraft_i["SMS"][j]["fire_event"]))  # 从模拟器重置开始导弹发射事件计数。
            ret.append(self.normalize(aircraft_i["SMS"][j]["hit_event"]))  # 导弹从模拟器重置中命中目标事件计数。
            ret.append(self.normalize(aircraft_i["SMS"][j]["miss_event"]))  # 导弹未击中目标并因模拟器重置而终止事件计数。
            ret.append(self.normalize(aircraft_i["SMS"][j]["r_dot_m"]))  # 当前导弹与目标飞机之间的range速率，单位为m / s。
            ret.append(self.normalize(aircraft_i["SMS"][j]["state"]))  # 导弹状态1：安装2：飞行3：寻找4：逃生
            ret.append(self.normalize(aircraft_i["SMS"][j]["target"]))  # 导弹飞机的目标指标，范围对应于强盗飞机的数量，-1对应于无目标。
            ret.append(self.normalize(aircraft_i["SMS"][j]["target_index"]))  # 导弹飞机的目标指标，范围对应于强盗飞机的数量，-1对应于无目标。
            ret.append(self.normalize(aircraft_i["SMS"][j]["trigger_bandit_rwr"]))  # 导弹雷达是否触发强盗rwr。 1表示触发，0表示反向。。

        for j in range(len(
                aircraft_i["SMS_est_list"])):  # 每个对手飞机的虚拟SMS列表，列表的大小与对手飞机的数量相同。 列表中的每个成员都有4个TGO_est，这意味着它假定相应的飞机上有4枚导弹。
            for k in range(len(aircraft_i["SMS_est_list"][j])):
                ret.append(self.normalize(aircraft_i["SMS_est_list"][j][k][
                                              "TGO_est"]))  # 相应飞机导弹的估计TGO。 TGO_est的计算取决于action_shoot_predict_list中shoot_predict的值。 仅当shoot_predict的值为1时，当前飞机才会开始计算相应对手飞机的TGO_est，否则它将具有默认值200。

        ret.append(self.normalize(aircraft_i["TAS"]))  # 飞机的真实空速  1维度 int  TAS: the true airspeed of the aircraft
        ret.append(self.normalize(aircraft_i["Vg_0"]))  # TAS的x轴分量 1维度 int
        ret.append(self.normalize(aircraft_i["Vg_0_est"]))  # 估计TAS的x轴分量from预警机。 1单位是米/秒。 1维度 int
        ret.append(self.normalize(aircraft_i["Vg_1"]))  # TAS的y轴分量 1维度 int
        ret.append(self.normalize(aircraft_i["Vg_1_est"]))  # 估计TAS的y轴分量from预警机 1维度 int
        ret.append(self.normalize(aircraft_i["Vg_2"]))  # TAS的Z轴分量 1维度 int
        ret.append(self.normalize(aircraft_i["Vg_2_est"]))  # 估计TAS的z轴分量from预警机 1维度 int
        ret.append(self.normalize(aircraft_i["Xg_0"]))  # 飞机位置的x坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_0_est"]))  # 估计飞机位置的x坐标from预警机  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_1"]))  # 飞机位置的y坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_1_est"]))  # 估计飞机位置的y坐标from预警机  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_2"]))  # 飞机位置的z坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_2_est"]))  # 估计飞机位置的z坐标from预警机  1维度 连续值
        ret.append(self.normalize(aircraft_i["alive"]))  # 战机是否活着 1维度  boolean

        for j in range(len(aircraft_i["attack_zone_list"])):  # 对每个敌机的动态发射区列表，列表的大小与敌机的数量相同。 列表中的每个成员都有几种动态发射区。
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["ASE_circle"]))  # 最大值为20度的允许转向误差圆的半径，单位为度。
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j][
                                          "Raero"]))  # 六种动态发射区描述了不同的目标伤害效果，它们之间的距离关系为Raero> Ropt> Rmax> Rpi> Rtr> Rmin，单位为m。
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["Ropt"]))
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["Rmax"]))
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["Rpi"]))
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["Rtr"]))
            ret.append(self.normalize(aircraft_i["attack_zone_list"][j]["Rmin"]))

        ret.append(self.normalize(aircraft_i["attg_0"]))  # 滚动角，单位为弧度
        ret.append(self.normalize(aircraft_i["attg_1"]))  # 俯仰角，单位为弧度
        ret.append(self.normalize(aircraft_i["attg_2"]))  # 偏航角，单位为弧度
        ret.append(self.normalize(aircraft_i["be_shot_down_event"]))  # 模拟器重置后飞机被击落事件计数。 1表示飞机被击落，0表示倒退。
        ret.append(self.normalize(aircraft_i["crash_event"]))  # 模拟器重置导致飞机坠毁事件计数。 如果z坐标大于0（NED坐标系），则判断飞机坠毁
        ret.append(self.normalize(aircraft_i["death_event"]))  # 模拟器重置后，活动状态从1变为0事件计数
        ret.append(self.normalize(aircraft_i["h_dot"]))  # 爬升率 1维度 int  高度变化的速率对应时间
        ret.append(self.normalize(aircraft_i["in_border_event"]))  # 模拟器重置后，飞机从边界事件计数的外部到内部。
        ret.append(self.normalize(aircraft_i["lock_event"]))  # 飞机雷达锁定目标事件计数。
        ret.append(self.normalize(aircraft_i["lost_event"]))  # 飞机失误事件（越境时间过长并触发死亡事件）计数
        ret.append(self.normalize(aircraft_i["n_y"]))  # 飞机的y超载,单位是克。
        ret.append(self.normalize(aircraft_i["out_border_event"]))  # 飞机从内到外计数
        ret.append(self.normalize(aircraft_i["out_of_border_distance"]))  # 到边界的距离，在边界内距离为负数   1维度  continue
        ret.append(self.normalize(aircraft_i["out_of_border_time"]))  # 出界时间，单位为秒
        ret.append(self.normalize(aircraft_i["residual_chi"]))  # 期望航向角减去当前航向角  1维度 连续值
        ret.append(self.normalize(aircraft_i["shoot_down_event"]))  # 飞机击落目标事件计数
        ret.append(self.normalize(aircraft_i["stall_event"]))  # 飞机失速事件计数
        ret.append(self.normalize(aircraft_i["unlock_event"]))  # 飞机的雷达失去目标事件计数

        # for j in range(len(self.state_interface["AMS"])):   # 遍历全局四架飞机的导弹击中目标剩余时间 16维度 int
        #     for k in self.state_interface["AMS"][self.resort(i, j)]["SMS"]:
        #         ret.append(1.0 - self.normalize(k["TGO"]))  # 导弹击中目标剩余时间 1维度 int
        # for j in range(len(self.state_interface["AMS"])):   # 战机是否活着
        #     ret.append(self.normalize(self.state_interface["AMS"][self.resort(i, j)]["alive"]))     # 战机是否活着 1维度  boolean

        temp = []
        if not all_relative_obs:
            for j in range(self.red + self.blue):
                self.to_list(temp, aircraft_i["relative_observation"][self.resort(i, j)])
        else:
            for j in range(self.blue + self.red):
                for t in range(j + 1, self.red + self.blue):
                    self.to_list(temp, self.state_interface["AMS"][self.resort(i, j)]["relative_observation"][
                        self.resort(i, t)])
                    # AO     从速度方向到当前飞机与其他飞机之间的直线的角度的平面投影。
                    # TA     从当前飞机的速度方向和其他飞机的速度方向的角度的平面投影。
                    # TA_abs_dot  TA率的绝对值。
                    # Truth  根据基本事实或估计的relative_observation，1表示基本事实，0表示相反。
                    # h_delta  当前飞机与其他飞机之间的高度差，单位为米
                    # r     当前飞机与其他飞机之间的距离，单位为米。
                    # r_dot  当前飞机与其他飞机之间的rate速率，单位为m / s

        for k in temp:
            ret.append(self.normalize(k))
        return ret  # 205 dim

    def get_ith_aircraft_reward(self, i):

        aircraft_i = self.state_interface["AMS"][i]
        shoot_down = 0
        death = 0
        missile_score = 0
        crash = 0
        out_border = 0

        for j, missile in enumerate(aircraft_i["SMS"]):
            # for missile in aircraft_i["SMS"]:
            if missile["fire_event"]["value"] > self.fire[i][j]:
                missile_score = - 0.25
                self.fire[i][j] += 1
        if aircraft_i["death_event"]["value"] > self.death[i]:
            death = - 5
            self.death[i] += 1

        if aircraft_i["shoot_down_event"]["value"] > self.shoot_down[i]:
            shoot_down = 5
            self.shoot_down[i] += 1

        if aircraft_i["crash_event"]["value"] > self.crash[i]:
            crash = - 6
            self.crash[i] += 1

        if aircraft_i["out_border_event"]["value"] > self.out_border[i]:
            out_border = -6
            self.out_border[i] += 1

        return shoot_down + death + missile_score + crash + out_border

    def check_victor(self, fighter=2):
        """red win -> 1; blue win -> 2; tie -> 0"""
        alive_red = 0
        alive_blue = 0
        for i in range(2 * fighter):
            if i < fighter and self.state_interface['AMS'][i]['alive']['value'] > 0.5:
                alive_red += 1
            if i >= fighter and self.state_interface['AMS'][i]['alive']['value'] > 0.5:
                alive_blue += 1
        if alive_red == alive_blue:
            return 0
        if alive_red > alive_blue:
            return 1
        if alive_red < alive_blue:
            return 2

    def reset(self, log=False):
        """
        reset the simulator. if param log is true, a file sim_out.json will be created and the simulator speed
        will go down very hard. this function will read the init_interface and change the state_interface.

        """
        self.random_init()
        super().reset(log)
        # 该方法为重写的，下方为新增语句
        self.shoot_down = [0, 0, 0, 0]
        self.death = [0, 0, 0, 0]
        self.fire = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.crash = [0, 0, 0, 0]
        self.out_border = [0, 0, 0, 0]

        for i in range(4):
            self.action_interface['AMS'][i]["action_shoot_predict_list"][0]["shoot_predict"]["value"] = 0
            self.action_interface['AMS'][i]["action_shoot_predict_list"][1]["shoot_predict"]["value"] = 0
            self.action_interface['AMS'][i]["action_target"]["value"] = 3 - i


    # ======================================================================================================================

    def get_ith_aircraft_state(self, i: int, all_relative_obs=False):
        ret = []
        aircraft_i = self.state_interface["AMS"][i]  # aircraft manager system

        self.AAM_remain_one_hot(ret, aircraft_i["AAM_remain"]["value"])  # 剩余导弹数量  7维  one-hot

        for j in range(len(aircraft_i["RadarModel"])):  # 火控雷达list--有几个敌人就有几个火控雷达状态
            self.to_one_hot(ret, aircraft_i["RadarModel"][j]["FCR_locked"]["value"], 2)  # 对其中一个敌人的火控雷达状态   2维度  one-hot
        for j in range(len(aircraft_i["FCSModel"])):  # 火控系统list--有几个敌人就有几个火控系统状态
            self.to_one_hot(ret, aircraft_i["FCSModel"][j]["FCS_available"]["value"], 2)  # 火控系统是否捕捉到敌机  2维  one-hot

        # for j in range(len(aircraft_i["SMS"])):  # 导弹控制系统，4枚导弹的状态
        #     for k in range(len(aircraft_i["SMS"][j]["FCSGuide"])):
        #         ret.append(self.normalize(aircraft_i["SMS"][j]["FCSGuide"][k]["fcs_guide_info"]))  # 友军飞机的fcs是否对导弹制导了
        #     for l in range(len(aircraft_i["SMS"][j]["RadarGuide"])):
        #         ret.append(
        #             self.normalize(aircraft_i["SMS"][j]["RadarGuide"][l]["radar_guide_info"]))  # 友军飞机的radar是否对导弹制导了

        for j in range(len(aircraft_i["RWRModel"])):  # 被动雷达(雷达告警器)----有几个敌人就有几个被动雷达状态
            self.to_one_hot(ret, aircraft_i["RWRModel"][j]["RWR_fetched"]["value"], 2)  # RWR 是否捕获了雷达信号 2维  one-hot
        self.to_one_hot(ret, aircraft_i["RWR_nailed"]["value"], 2)  # 导弹危险警报状态,被敌方导弹锁定状态   2维  one-hot
        self.to_one_hot(ret, aircraft_i["RWR_spiked"]["value"], 2)  # 危险警报状态,被敌方雷达锁定状态   2维  one-hot

        for j in range(len(self.state_interface["AMS"])):  # 战机是否活着
            self.to_one_hot(ret, self.state_interface["AMS"][self.resort(i, j)]["alive"]["value"],
                            2)  # 战机是否活着  2维  one-hot

        ret.append(self.normalize(aircraft_i["TAS"]))  # 飞机的真实空速  1维度 int
        ret.append(self.normalize(aircraft_i["Vg_0"]))  # TAS的x轴分量  1维度 int
        ret.append(self.normalize(aircraft_i["Vg_1"]))  # TAS的x轴分量  1维度 int
        ret.append(self.normalize(aircraft_i["Vg_2"]))  # TAS的Z轴分量  1维度 int
        ret.append(self.normalize(aircraft_i["Xg_0"]))  # 飞机位置的x坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_1"]))  # 飞机位置的y坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["Xg_2"]))  # 飞机位置的z坐标  1维度 连续值
        ret.append(self.normalize(aircraft_i["h_dot"]))  # 爬升率 1维度 int
        ret.append(self.normalize(aircraft_i["residual_chi"]))  # 期望航向角减去当前航向角  1维度 连续值

        for j in range(len(self.state_interface["AMS"])):  # 遍历全局四架飞机的导弹击中目标剩余时间 16维度 int
            for k in self.state_interface["AMS"][self.resort(i, j)]["SMS"]:
                ret.append(1.0 - self.normalize(k["TGO"]))  # 导弹击中目标剩余时间 1维度 int

        temp = []
        if not all_relative_obs:
            for j in range(self.red + self.blue):
                self.to_list(temp, aircraft_i["relative_observation"][self.resort(i, j)])
        else:
            for j in range(self.blue + self.red):
                for t in range(j + 1, self.red + self.blue):
                    self.to_list(temp, self.state_interface["AMS"][self.resort(i, j)]["relative_observation"][
                        self.resort(i, t)])
        for k in temp:
            ret.append(self.normalize(k))
        return ret

    def AAM_remain_one_hot(self, ret, count):
        if count < 1:
            one_hot = np.array([1, 1, 1, 0, 0, 0, 0])
            for i in range(7):
                ret.append(one_hot[i])
        else:
            one_hot = np.hstack((np.array([0, 0]), to_categorical(count, 5)))
            for i in range(7):
                ret.append(one_hot[i])

    def to_one_hot(self, ret, value, dim):
        one_hot = to_categorical(value, 2)
        for i in range(dim):
            ret.append(one_hot[i])

    def write_in_action(self, combat_mode, vel_cmd, horizontal_cmd, vertical_cmd, ny_cmd, flag_after_burning, m_target, s_action, i):
        s_action = s_action - 1

        self.action_interface['AMS'][i]["SemanticManeuver"]["combat_mode"]["value"] = combat_mode

        #vel_cmd action mapping
        vel_cmd = vel_cmd*46 + 250

        self.action_interface['AMS'][i]["SemanticManeuver"]["vel_cmd"]["value"] = vel_cmd
        self.action_interface['AMS'][i]["SemanticManeuver"]["horizontal_cmd"]["value"] = horizontal_cmd
        self.action_interface['AMS'][i]["SemanticManeuver"]["vertical_cmd"]["value"] = vertical_cmd
        self.action_interface['AMS'][i]["SemanticManeuver"]["ny_cmd"]["value"] = ny_cmd
        self.action_interface['AMS'][i]["SemanticManeuver"]["flag_after_burning"]["value"] = flag_after_burning
        self.action_interface['AMS'][i]["SemanticManeuver"]["maneuver_target"]["value"] = m_target
        self.action_interface['AMS'][i]["action_shoot_target"]["value"] = s_action

        self.action_interface['AMS'][i]["SemanticManeuver"]['clockwise_cmd']['value'] = 0


