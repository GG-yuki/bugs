from environment.theatre import War

import numpy as np
import random
import json
import os
from io import StringIO
import pickle
from io import StringIO

"""
honeycake project

the project for air combat composes of third part, battlespace.py, config.json, _theatre.so.
The simulator uses NED coordinate system.

config.json
    the config.json is the configuration file for the simulator.
    the file format is standard json file. it configures the border of battle space, the pop mode of decision,
    the number of aircraft, and the recursive configuration of aircraft. the reference of json field below:
    border_x:
        the absolute value of battle space x axis, the numerical value range is (0,inf), the unit is meter.
        example: if the value of border_x is 1000, then the battle space x border is [-1000,1000] in the simulator.
    border_y:
        the absolute value of battle space y axis, the numerical value range is (0,inf), the unit is meter.
        example: if the value of border_y is 1000, then the battle space y border is [-1000,1000] in the simulator.
    border_z:
        the value of battle space z axis,the numerical value range is (-inf,0), the unit is meter.
        example: if the value of border_z is -1000, then the battle space z border is [-1000,0](using NED coordinate 
        system).
    interval:
        the value of pop interval time,this value controls the time of pop interval.the numerical value range is [1,inf)
        , the unit is second. example: if the interval field is 10, then every 10 seconds,the simulator will pop to 
        fetch the next decision.(the value should be equal to or larger than 1, if the value of interval less than 1 ,
        the simulator efficiency will go down very hard and the behavior of simulator is undefined.)
    timeout:
        the value of simulator max running time. the numerical value range is (0,inf),this value controls the max 
        running time of simulator, if the simulator time exceed the timeout value, the simulator will stop and pop,
        the "done" interface in battlespace.py will be set true. //TODO
    AMS:
        the aircraft manager system, it composes of the red aircraft list and the blue aircraft list.
    red_config:
        the red aircraft team configuration
    blue_config:
        the blue aircraft team configuration
    data_link:
        the selection of data link model type, this value controls the type of data link model, it is enumeration type which 
        is "no_link" , "normal_link" or "weapon_link" 
    warning_aircraft:
        the selection of warning aircraft mode type, this value controls the mode of warning aircraft, it is enumeration type
        which is "auto", "manual" 
    red_aircraft_list:
        the aircraft configuration list of red side.the length should not be 0.
    blue_aircraft_list:
        the aircraft configuration list of blue side.the length should not be 0.
    maneuver_model:
        the selection of maneuver model type, this value controls the type of aerodynamics maneuver model, it is 
        enumeration type which is "discrete","continuous","hybrid"","F22discrete","F22hybrid","F22stick","F22simpstick".
        different type will impact the action interface in the battlespace.py.
    radar_model:
        the selection of radar model type, this value controls the type of radar model, it is enumeration type which 
        is "normal" or "raptor" 
    fcs_model:
        the selection of fcs model type, this value controls the type of fcs model, it is enumeration type which 
        is "incomplete" or "complete" or "pilot_incomplete"
    SMS:
        the suspension manager system, it composes of missile list.
    type:
        the selection of missile model type,this value controls the type of missile model, it is enumeration 
        type which is "AAM120".

battlespace.py is the wrap file for the native simulator.

authorization_code:
    the code for the usage control, please update it from the provider when the authorization expires.
"""

authorization_code = 'M0Ax2S32kAgAZpm9Jmjqf+DeNoQ9Cevx2HUuVCIfV+gw2lK3PQcxqvwaPqZTTMsYDzPsQcZUm3z9t0bC6iFHrKOq09lViCUv4HZ1UTD1hg6eT25+EbNCkqF6tso8yI7xCyMhUXPeAEizNt5d0y14RcfFZ6DfxLG6KuiErU/LGB03Sb7e1NPcbkUP4vn+rRdIGH+mPaZkUUgQGig6o/cg0K8fKzkQ5wNaghds3JnE+qZfmcNTIsO/R04pnvtPaOR483kvj+XcjqvCbAqNfResJ/tYp5qaR9V2qMgXMioAWLUsjwaVRlz+kz20/DhLZaBWDPKVDWbSQkdtORtRtNdyIw=='


class BattleSpace:
    """
    the main class include many interfaces, such as reset, step, done, action_interface, state_interface, init_interface
    and so on.
    init_interface:
        the initial interface of the simulator, it is json format interface, you can use print function to check the
        interface structure. in the json format interface, each endpoint is a structure including info, max, min, type,
        mask, mask_len, mask_list_head_index, value_index, value, the reference below:
        info:
            the annotation
        max:
            the upper limit of the value
        min:
            the lower limit of the value
        type:
            the type of the value(it is just for hint,do not use this field in your code)
        mask:
            the mask for the data, it is a list of 0,1 mix. 0 represents the value in that place can not be used.
            if the mask is none, there is no restriction
            example:the mask in state_interface informs the value can be used or not,the mask in action_interface
            informs the action can be selected or not.
        mask_len:
            assist field, do not read or assign.
        mask_list_head_index:
            assist field, do not read or assign.
        value_index:
            assist field, do not read or assign.
        value:
            the data value. if it is in state_interface, it should be read. if it is in action_interface or
            init_interface, it should be assigned. (if you read the value, the type is always float, whatever the
            content of "type" field is. if you assign the value, the value you assign will always be cast to
            float inside)
        blue_awacs:
            the blue warning aircraft awacs block,if the value of the field warning_aircraft in config.json is auto,
            the content is the position of awacs. if the value of the field warning_aircraft in config.json is manual
            the content is a list of init estimated position of red bandit aircraft, the length is the red bandit aircraft num
        red_awacs:
            the same as blue_awacs, reverse blue to red
        auto_awacs:
            the auto awacs position block
        init_AWACS_x:
            structure in init_interface,it represents the x position of awacs
        init_AWACS_y:
            structure in init_interface,it represents the y position of awacs
        init_AWACS_z:
            structure in init_interface,it represents the z position of awacs
        init_vg_0_est:
            the init estimated x-axis component of bandit aircraft TAS. unit is m/s.
        init_vg_1_est:
            the init estimated y-axis component of bandit aircraft TAS. unit is m/s.
        init_vg_2_est:
            the init estimated z-axis component of bandit aircraft TAS. unit is m/s.
        init_xg_0_est:
            the init estimated x-coordinate of the bandit aircraft position. unit is m.
        init_xg_1_est:
            the init estimated y-coordinate of the bandit aircraft position. unit is m.
        init_xg_2_est:
            the init estimated z-coordinate of the bandit aircraft position. unit is m.        
        AMS:
            the aircraft manager system, it composes of aircraft init configuration list and red aircraft first.
        init_x:
            structure in init_interface,it represents the initial x position of the aircraft.the min,max field in
            it will correspond to border_x in the config.json
        init_y:
            structure in init_interface, it represents the initial y position of the aircraft. the min, max field in
            it will correspond to border_y in the config.json
        init_z:
            structure in init_interface,it represents the initial z position of the aircraft.the min, max field
            in it will correspond to border_z in the config.json
        init_mu:
            structure in init_interface, it represents the initial roll angle of the aircraft
        init_gamma:
            structure in init_interface, it represents the initial pitch angle of the aircraft
        init_chi:
            structure in init_interface, it represents the initial yaw angle of the aircraft
        init_TAS:
            structure in init_interface,it represents the initial true airspeed of the aircraft.
        init_red_AWACS_x:
            structure in init_interface,it represents the x position of red awacs
        init_red_AWACS_y:
            structure in init_interface,it represents the y position of red awacs
        init_red_AWACS_z:
            structure in init_interface,it represents the z position of red awacs
        init_blue_AWACS_x:
            structure in init_interface,it represents the x position of blue awacs
        init_blue_AWACS_y:
            structure in init_interface,it represents the y position of blue awacs
        init_blue_AWACS_z:
            structure in init_interface,it represents the z position of blue awacs
        init_alive:
            structure in init_interface,it represents the initial alive of the aircraft.
        init_state:
            structure in init_interface,it represents the initial state of the missile.
        init_fuel:
            structure in init_interface,it represents the initial state of the fuel.
    action_interface:
        the action interface of the simulator. it is json format interface, you can use print function to check the
        interface structure. in the json format interface, each endpoint is a structure like init_interface.
        the action_interface will change corresponding to config.json.
        the field "maneuver_model" in config.json is enumeration of "discrete","continuous","hybrid","F22discrete",
        "F22hybrid","F22stick","F22simpstick","chickfighterdiscrete".when you edit the config.json, the action_interface will change as well,
        the reference below:
        if the assignment not in the range,the behavior of simulator is undefined.
        discrete:
            DiscreteManeuver:
                discrete maneuver action
            action_bfm_id:
                discrete maneuver id,the range is 0~11,the detail of each maneuver below:
                0:retain,the steer,overload and speed will keep as current state
                1:cata_intercept,steer to front position of target
                2:crank,steer to slant front
                3:climb_intercept, climb and steer to front position of the target
                4:abort_in, steer to target hard
                5:turn_in, steer to target
                6:beam, steer to the direction perpendicular to the speed direction of the target
                7:dive_retreat, deviate from target and descend
                8:level_retreat,deviate from target
                9:climb_retreat,deviate from target and climb
                10:abort_out, steer away from target hard
                11:turn_out, steer away from target
            maneuver_target:
                target aircraft index, the range corresponds to the number of all aircraft(include friend aircraft), begins with 0.
                example: if there are four  aircraft, the range of target_aircraft is 0~3,the aircraft sequence is as same
                as AMS.

        continuous:
            ContinuousManeuver:
                continuous maneuver action
            action_dchi_c:
                expectation yaw angle of the aircraft, unit of radian, range [-pi,pi]
            action_dgamma_c:
                expectation roll angle, unit of radian,range[-pi/2,pi/2]
            action_nn_c:
                overload, unit of gravity,range[3,9]
            action_v_c:
                expectation speed, unit of m/s, range[0,900]
            maneuver_target:
                the same as discrete
        hybrid:
            HybridManeuver:
                hybrid maneuver action
            action_bfm_id:
                discrete maneuver id, the range is 0~6, the detail of each maneuver below:
                0:cata_intercept, steer to front position of target
                1:crank,steer to slant front
                2:climb_intercept, climb and steer to front position of the target
                3:beam,steer to the direction perpendicular to the speed direction of the target
                4:dive_retreat, deviate from target and descend
                5:level_retreat, deviate from target
                6:climb_retreat, deviate from target and climb
            action_nn_c:
                overload, unit of gravity, range[3,9]
            action_v_c:
                expectation speed, unit of m/s, range[0,900]
            maneuver_target:
                the same as discrete
        F22discrete:
            DiscreteManeuver:
                discrete maneuver action
            action_bfm_id:
                discrete maneuver id,the range is 0~12,the detail of each maneuver below:
                0:cata intercept,steer to front position of target
                1:level intercept,heading to the target,ignoring height difference
                2:crank,steer to slant front
                3:climb_intercept,  steer to front position of the target and climb with the optimized theta
                4:dive_intercept10, steer to front position of the target and dive with 10 deg
                5:defensive_beam,steer to the direction perpendicular to the target
                6:retreat_turn_out,steer away from target,while keeping level
                7:abort_90_dive_30,steer away from target using 'roll and pull',then dive with 30 deg
                8:climb,maintain heading and climb with the optimized theta
                9:retreat_climb,steer away from target , then climb with the optimized theta
                10:abort_90,steer away from target using 'roll and pull'
                11:split S,roll 180 and pull,steer away from targets
                12:roll135 and pull
                13:dogfight mode
            maneuver_target:
                the same as discrete
        F22hybrid:
            HybridManeuver:
                hybrid maneuver action
            action_bfm_id:
                 discrete maneuver id,the range is 0~12,the detail of each maneuver below:
                Same As F22discrete 'action_bfm_id'
            action_v_c:
                expectation speed, unit of m/s, range[0,900]
            action_nn_c:
                normal overload command used in 'roll and pull' maneuver, range[3,9]
            action_afterburning:
                0: engine afterburner not used , 1:engine afterburner used
            maneuver_target:
                the same as discrete
        F22stick:
            F22Stick:
                pilot in the loop model of F22
            action_nyc: normal overload command, range [-1,1];
            action_wxc: roll rate command, range [-1,1];
            action_Tc: throttle command, range [0,1];
        F22simpstick:
            as F22stick
        F22semantic:
            SemanticManeuver:
                semantic maneuver action
            combat_mode:
                 0:Beyond Visual Range
                 1:Visual Range
            horizontal_cmd:
                0:maintain heading
                1:heading towards target
                2:crank 30deg
                3:crank 50deg
                4:turn 90deg to target
                5:turn 180 to target
                6:turn 120deg to target
                7:turn 150deg to target
            vertical_cmd:
                0:maintain height
                1:steer towards target
                2:dive 10deg
                3:dive 25deg
                4:climb 10deg
                5:climb 20deg
                6:splitS and dive 45deg(use splitS when horizontal_cmd is 5 and height enough(more than 4km), else use div 45 deg)
                other vertical cmd may interrupt splitS maneuver, protection of crash is available when height is less than 2500m
            vel_cmd:
                expectation speed, unit of m/s, range[250,900]
            ny_cmd:
                normal overload command used in 'roll and pull' maneuver, range[0,9]
            flag_after_burning:
                0: engine afterburner not used , 1:engine afterburner used
            maneuver_target:
                the same as discrete
            clockwise_cmd:
                -1:anti clockwise
                0:auto
                1:clockwise
        F22bot:
            SemanticManeuver:
                bot maneuver action
            combat_mode:
                 0:Beyond Visual Range
                 1:Visual Range
            horizontal_cmd:
                0:maintain heading
                1:heading towards target
                2:crank 30deg
                3:crank 50deg
                4:turn 90deg to target
                5:turn 180deg to target
                6:turn 120deg to target
                7:turn 150deg to target
            vertical_cmd:
                0:maintain height
                1:steer towards target
                2:dive 10deg
                3:dive 25deg
                4:climb 10deg
                5:climb 20deg
                6:splitS and dive 45deg(use splitS when horizontal_cmd is 5 and height enough(more than 4km), else use div 45 deg)
                other vertical cmd may interrupt splitS maneuver, protection of crash is available when height is less than 2500m
            vel_cmd:
                expectation speed, unit of m/s, range[250,900]
            ny_cmd:
                normal overload command used in 'roll and pull' maneuver, range[0,9]
            flag_after_burning:
                0: engine afterburner not used , 1:engine afterburner used
            maneuver_target:
                the same as discrete
            clockwise_cmd:
                -1:anti clockwise
                0:auto
                1:clockwise
            base_direction:
                given base direction, angle to north, clockwise
                range[-pi,pi] , use given base direction
                [-inf,-pi] or [pi,+inf] ,  use AO to target
        chickfighterdiscrete:
            DiscreteManeuver:
                chick_fighter discrete maneuver action
            action_bfm_id:
                chick_fighter discrete maneuver id,the range is 0~16,the detail of each maneuver below:
                0:cata intercept,steer to front position of target
                1:level intercept,heading to the target,ignoring height difference
                2:crank,steer to slant front
                3:climb_intercept20, climb with 20 deg and steer to front position of the target
                4:climb_intercept10, climb with 10 deg and steer to front position of the target
                5:defensive_beam,steer to the direction perpendicular to the target
                6:retreat_turn_out,steer away from target,while keeping level
                7:abort_90_dive_30,steer away from target using 'roll and pull',then dive with 30 deg, while avoiding
                    crashing to ground
                8:climb_20,maintain heading , climb with 20 deg
                9:retreat_climb_10,steer away from target,while keeping level,and then dive with 10 deg
                10:abort_90,steer away from target using 'roll and pull'
                11:DVM, pull full negative overload ,until theta was equal to -30 deg,rolling until gamma was equal to
                    0deg, then keep diving until about 1000 meters high
                12:intercept_dive_10,steer to front position of target, and dive with 10 deg
                13:dive_30,maintain heading , dive with 30 deg
                14:formal_accelerate,maintain heading ,keep velocity increasing
                15:retreat and level_S,steer away from target,while keeping S shape manuever ,such as AOC keeps changing
                    from -130deg to 130deg
                16:intercept and level_S,heading to the target,while keeping S shape manuever , such as AOC keeps
                    changing from -30deg to 30deg
            maneuver_target:
                the same as discrete
        chickfightersemantic:
            SemanticManeuver:
                semantic maneuver action
            combat_mode:
                 0:Beyond Visual Range
                 1:Visual Range
            horizontal_cmd:
                0:maintain heading
                1:heading towards target
                2:crank 30deg
                3:crank 50deg
                4:turn 90deg to target
                5:turn 180deg to target
                6:turn 120deg to target
                7:turn 150deg to target
            vertical_cmd:
                0:maintain height
                1:steer towards target
                2:dive 10deg
                3:dive 25deg
                4:climb 10deg
                5:climb 20deg
                6:splitS and dive 45deg(use splitS when horizontal_cmd is 5 and height enough(more than 4km), else use div 45 deg)
                other vertical cmd may interrupt splitS maneuver, protection of crash is available when height is less than 2500m
            vel_cmd:
                expectation speed, unit of m/s, range[250,900]
            ny_cmd:
                normal overload command used in 'roll and pull' maneuver, range[0,9]
            flag_after_burning:
                0: engine afterburner not used , 1:engine afterburner used
            maneuver_target:
                the same as discrete
            clockwise_cmd:
                -1:anti clockwise
                0:auto
                1:clockwise
        action_shoot_target:
            shoot action, -1 or 0 ~ n assignment, -1 corresponding to not shooting, 0~n corresponding the bandit
            aircraft index to shooting.
        action_shoot_predict_list:
            the list of shoot prediction action for each opponent aircraft, the size of the list is as same as the
            number of opponent aircraft.
            example:If the current team is red, and the blue team has two aircraft,
            then each aircraft of the red team will have two members in its action_shoot_predict_list corresponding
            to each aircraft in blue team, and the first member of the list corresponding to the first member of the
            blue team.

        shoot_predict:
            the member of the action_shoot_predict_list, it has only two values, 0 or 1, 0 means to not predict shoot
            action of corresponding aircraft of the opponent team, 1 means to predict shoot action of corresponding
            aircraft of the opponent team using some unique technique.
            example:There are two teams, red and blue respectively. Each team has two aircraft. If one of the aircraft
            of the red team has an action_shoot_predict_list value like [0,1], it means it won't predic shoot action of
            the first aircraft of the blue team, and will predict shoot action of the second aircraft of the blue team
            using some unique technique.
        action_target:
            target aircraft index, the range corresponds to the number of all aircraft(include friend aircraft), begins with 0.
            example: if there are four  aircraft, the range of target_aircraft is 0~3,the aircraft sequence is as same
            as AMS,this interface only for vision, no decision meaning.
        AMS:
            the aircraft manager system, it composes of  aircraft action configuration list and red
            aircraft first as init_interface.
        blue_awacs:
            the blue warning aircraft awacs block,if the value of the field warning_aircraft in config.json is manual
            the content is a list of action estimated position of red bandit aircraft, the length is the red bandit aircraft num
        red_awacs:
            the same as blue_awacs, reverse blue to red
        action_vg_0_est:
            the estimated x-axis component of bandit aircraft TAS. unit is m/s.
        action_vg_1_est:
            the estimated y-axis component of bandit aircraft TAS. unit is m/s.
        action_vg_2_est:
            the estimated z-axis component of bandit aircraft TAS. unit is m/s.
        action_xg_0_est:
            the estimated x-coordinate of the bandit aircraft position. unit is m.
        action_xg_1_est:
            the estimated y-coordinate of the bandit aircraft position. unit is m.
        action_xg_2_est:
            the estimated z-coordinate of the bandit aircraft position. unit is m.
        the mask field in action_interface will update after ever step. the assignment should be in the valid
        range and conforms to the mask, otherwise the behavior of simulator is undefined.
    state_interface:
        the state interface of the simulator. it is json format interface, you can use print function to check
        the interface structure. in the json format interface, each endpoint is a structure like init_interface.
        the state_interface will change corresponding to config.json.
        AAM_remain:
            the remain missiles number. when the aircraft launches one missile, this value minus 1.
        FCSModel:
            FCS system. it is a list of FCS_available state, the length of the list equals bandit num.
        FCS_available:
            the FCS state. 1 represents that the FCS has caught the corresponding aircraft,0 reverse.
        RWRModel:
            RWR system. it is a list of RWR_fetched state, the length of the list equals bandit num.
        RWR_fetched:
            the RWR state. 1 represents that the RWR has fetched the corresponding aircraft radar signal ,0 reverse.
        RadarModel:
            radar system. it is a list of FCR_locked state, the length of the list equals bandit num.
        FCR_locked:
            the radar state. 1 represents that the radar has locked the the corresponding aircraft,0 reverse.
        RWR_nailed:
            missile danger alarm state. 1 represents the aircraft has be locked by some bandit missile ,0 reverse.
        RWR_spiked:
            danger alarm state. 1 represents the aircraft has be locked by some bandit aircraft radar,0 reverse.
        SMS:
            suspension manager system. it is a list of missile state.
        FCSGuide:
            FCS guide system. it is a list of fcs_guide_info state, the length of the list equals friend num.
        fcs_guide_info:
            the fcs_guide_info state. 1 represents that the corresponding friend aircraft fcs has guide the missile,
            0 reverse.
        RadarGuide:
            radar guide system. it is a list of radar_guide_info state, the length of the list equals friend num.
        radar_guide_info:
            the radar_guide_info state. 1 represents that the corresponding friend aircraft radar has guide the missile,
            0 reverse.
        Xg_m_0:
            the x-coordinate of the missile position. unit is m.
        Xg_m_1:
            the y-coordinate of the missile position. unit is m.
        Xg_m_2:
            the z-coordinate of the missile position. unit is m.
        Vg_m_0:
            the x-axis component of the missile TAS. unit is m/s.
        Vg_m_1:
            the y-axis component of the missile TAS. unit is m/s.
        Vg_m_2:
            the z-axis component of the missile TAS. unit is m/s.
        attg_m_0:
            missile roll angle, unit is radian
        attg_m_1:
            missile pitch angle, unit is radian
        attg_m_2:
            missile yaw angle, unit is radian
        state:
            missile state 1:mounting 2:flying 3:seeking 4:escape
        target:
            the missile aircraft target index, the range corresponds to the number of bandit aircraft,-1 corresponding
            to no target.
        trigger_bandit_rwr:
            missile radar trigger bandit rwr or not. 1 represents trigger, 0 reverse.
        TGO:
            the remain time of missile hitting the target. its range is [0,200]. if the missile is not launched or the
            missile is expired, the value will be set 200. the unit is seconds.
        TAS_m:
            the true airspeed of the missile
        AO_m:
            planar projection of the angle from the speed direction and the line between current missile
            and target aircraft.
        TA_m:
            planar projection of the angle from the speed direction of current missile and
            the speed direction of target aircraft.
        r_dot_m:
            range rate between current missile and target aircraft, the unit is m/s

        SMS_est_list:
            the list of virtual SMS for each opponent aircraft, the size of the list is as same as the number of
            opponent aircraft. Each member of the list has 4 TGO_est, meaning it assumes the corresponding aircraft
            has 4 missiles.
        TGO_est:
            The estimated TGO of the corresponding aircraft's missile. The calculation of TGO_est depends on the value
            of shoot_predict in action_shoot_predict_list. Only when the value of shoot_predict is 1, the current
            aircraft will start to calculate the TGO_est of the corresponding opponent aircraft, or it will has the default
            value 200.
        attack_zone_list:
            the list of dynamic launch zone for each opponent aircraft, the size of the list is as same as the number of
            opponent aircraft. Each member of the list has sevaral kinds of dynamic launch zones.
        Raero/Ropt/Rmax/Rpi/Rtr/Rmin:
            six kinds of dynamic launch zones which describe different damage effects for target, the distance
            relationship of them is Raero > Ropt > Rmax > Rpi > Rtr > Rmin, unit is m.
        ASE_circle:
            the radius of allowable steer error circle whose max value is 20 degree, unit is degree.
        lost_fcs_guide_timer:
            the interval of losing fcs guide ,unit is second.
        lost_radar_guide_timer:
            the interval of losing radar guide, unit is second.
        flying_time:
            the missile flying time, unit is second.
        fire_event:
            the missile be launched event count from simulator reset.
        get_guide_event:
            the missile gets the guide of own side aircraft event count from simulator reset.
        hit_event:
            the missile hits the target event count from simulator reset
        lose_guide_event:
            the missile loses the guide of own side aircraft event count from simulator reset
        miss_event:
            the missile misses the target and expires event count from simulator reset
        TAS:
            the true airspeed of the aircraft
        Vg_0:
            the x-axis component of the TAS. unit is m/s.
        Vg_1:
            the y-axis component of the TAS. unit is m/s.
        Vg_2:
            the z-axis component of the TAS. unit is m/s.
        Xg_0:
            the x-coordinate of the aircraft position. unit is m.
        Xg_1:
            the y-coordinate of the aircraft position. unit is m.
        Xg_2:
            the z-coordinate of the aircraft position. unit is m.
        Vg_0_est:
            the estimated x-axis component of the TAS from awacs. unit is m/s.
        Vg_1_est:
            the estimated y-axis component of the TAS from awacs. unit is m/s.
        Vg_2_est:
            the estimated z-axis component of the TAS from awacs. unit is m/s.
        Xg_0_est:
            the estimated x-coordinate of the aircraft position from awacs. unit is m.
        Xg_1_est:
            the estimated y-coordinate of the aircraft position from awacs. unit is m.
        Xg_2_est:
            the estimated z-coordinate of the aircraft position from awacs. unit is m.
        attg_0:
            roll angle, unit is radian
        attg_1:
            pitch angle, unit is radian
        attg_2:
            yaw angle, unit is radian
        n_y:
            the y-overload of the aircraft . unit is g.
        alive:
            the aircraft state. 1 represents that the aircraft is alive, 0 reverse.
        fuel:
            the fuel value of aircraft. 0 corresponding to losing propulsion
        out_of_border_time:
            the time of out of border, unit is second
        out_of_border_distance:
            the distance of out of border, when the aircraft in the border, the distance is negative, unit is m
        be_shot_down_event:
            the aircraft is shot down event count from simulator reset. 1 represents the aircraft be shot down,0 reverse.
        crash_event:
            the aircraft crashes event count from simulator reset. if the z-coordinate more than 0(NED coordinate system),
            the aircraft is judged crash
        death_event:
            the alive state goes from 1 to 0 event count from simulator reset
        h_dot:
            rate of climb. unit is m/s.
        in_border_event:
            the aircraft goes from outside to inside of the border event count from simulator reset.
        lock_event:
            the radar of aircraft locks the target event count from simulator reset.
        out_border_event:
            the aircraft goes from inside to outside of the border event count from simulator reset.
        residual_chi:
            the expectation yaw angle minus present yaw angle.
        shoot_down_event:
            the aircraft shoots down the target event count from simulator reset.
        stall_event:
            the aircraft stalls event count from simulator reset.
        lost_event:
            the aircraft lost event(out of border too long and trigger die event) count from simulator reset.
        unlock_event:
            the radar of the aircraft loses the target event count from simulator reset.
        relative_observation:
            the relative state between current aircraft and others. it is a relative state list of which the length
            is equal to the number of all aircraft. the states relative to itself are always 0.
        AO:
            planar projection of the angle from the speed direction and the line between current aircraft and others.
        TA:
            planar projection of the angle from the speed direction of current aircraft and
            the speed direction of other aircraft.
        TA_abs_dot:
            absolute value of the TA rate.
        h_delta:
            altitude difference between current aircraft and others, the unit is meter
        r:
            the range between current aircraft and others, the unit is meter.
        r_dot:
            range rate between current aircraft and others, the unit is m/s
        Truth:
            the relative_observation from the ground truth or estimation, 1 represents the ground truth, 0 reverse.
            if the aircraft is not alive, some state of the aircraft will be set 0 or not changed, and all other aircraft
            relative_observations to the aircraft is set 0.
        tick:
            the min step of the simulator time, equals to 0.03 second simulator time
    done:
        simulator terminate flag value.(time out, no aircraft alive, no valid missile, one side win and so on)
    note: when you fetch the structure copy from the interface ,the method should be deepcopy or the value in it will
        be modified  with reset and step
    """

    def __init__(self, maneuver_list=None, interval=None):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), "r") as f: # file operation must use abspath
            config = f.read()
            if not maneuver_list:
                # use origin method #
                pass
            else:
                config = json.loads(config)
                # print(config)
                for i in range(len(maneuver_list[0])):
                    config["AMS"]["red_config"]["red_aircraft_list"][i]["maneuver_model"] = maneuver_list[0][i]
                for i in range(len(maneuver_list[1])):
                    config["AMS"]["blue_config"]["blue_aircraft_list"][i]["maneuver_model"] = maneuver_list[1][i]

                f_config = StringIO()
                json.dump(config, f_config)
                config = f_config.getvalue()

            # config = json.loads(config)
            if not interval:
                # use origin method #
                pass
            else:
                config = json.loads(config)
                config["interval"] = float(interval)

                f_config = StringIO()
                json.dump(config, f_config)
                config = f_config.getvalue()

            self.war = War(config, authorization_code)
            self.action_interface = self.construct_interface(json.loads(self.war.ToActionInterface()))
            self.init_interface = self.construct_interface(json.loads(self.war.ToInitInterface()))
            self.state_interface = self.construct_interface(json.loads(self.war.ToStateInterface()))
            config = json.loads(config)
            self.border_x = float(config["border_x"])
            self.border_y = float(config["border_y"])
            self.border_z = float(config["border_z"])
            self.red = len(config["AMS"]["red_config"]["red_aircraft_list"])
            self.blue = len(config["AMS"]["blue_config"]["blue_aircraft_list"])
            self.done = False
            self.interval = float(config["interval"])

    def construct_interface(self, raw_interface):
        if type(raw_interface) is list:
            for i in raw_interface:
                self.construct_interface(i)
        elif type(raw_interface) is dict:
            if "value_index" in raw_interface.keys():
                raw_interface["value"] = None
                if raw_interface["mask_len"] > 0:
                    raw_interface["mask"] = [1.0 for _ in range(raw_interface["mask_len"])]
            else:
                for key in raw_interface.keys():
                    self.construct_interface(raw_interface[key])
        return raw_interface

    def step(self):
        """
        simulator step a macro action. this function will read the action_interface and change the state_interface
        and the mask of the action_interface.

        """
        self.communicate_cpp(self.action_interface, "push_value")
        self.war.Step()
        self.communicate_cpp(self.state_interface, "pull_value")
        self.communicate_cpp(self.action_interface, "pull_value")
        self.communicate_cpp(self.action_interface, "pull_mask")
        self.done = self.war.done_

    def reset(self, log=False):
        """
        reset the simulator. if param log is true, a file sim_out.json will be created and the simulator speed
        will go down very hard. this function will read the init_interface and change the state_interface.

        """
        self.communicate_cpp(self.init_interface, "push_value")
        self.war.Reset(log)  # log
        self.communicate_cpp(self.state_interface, "pull_value")
        self.communicate_cpp(self.action_interface, "pull_mask")
        self.done = self.war.done_

    def resort(self, i: int, relative_index: int):
        if i < self.red:
            if relative_index < self.red:
                return (relative_index + i) % self.red
            else:
                return relative_index
        else:
            if relative_index < self.blue:
                return (relative_index + i - self.red) % self.blue + self.red
            else:
                return relative_index - self.blue

    def random_init(self):
        np_random = np.random.RandomState()
        np_random.seed(int(random.SystemRandom().random() * 1000000000000000) % (2 ** 32))
        # print("seed", int(random.SystemRandom().random() * 1000000000000000) % (2 ** 32))
        side = np_random.randint(0, 2)

        if type(self.init_interface["red_awacs"]) is dict:
            if side == 0:
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_x"]["value"] =-self.border_x - 100000
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_y"]["value"] =0
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_z"]["value"] =-12000
            elif side == 1:
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_x"]["value"] =self.border_x + 100000
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_y"]["value"] =0
                self.init_interface["red_awacs"]["auto_awacs"]["init_AWACS_z"]["value"] =-12000
        if type(self.init_interface["red_awacs"]) is list:
            for i in range(self.blue):
                self.init_interface["red_awacs"][i]["init_xg_0_est"]["value"] = 0
                self.init_interface["red_awacs"][i]["init_xg_1_est"]["value"] = 0
                self.init_interface["red_awacs"][i]["init_xg_2_est"]["value"] = -10000
                self.init_interface["red_awacs"][i]["init_vg_0_est"]["value"] = 0
                self.init_interface["red_awacs"][i]["init_vg_1_est"]["value"] = 0
                self.init_interface["red_awacs"][i]["init_vg_2_est"]["value"] = 0

        if type(self.init_interface["blue_awacs"]) is dict:
            if side == 0:
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_x"]["value"] =-self.border_x - 100000
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_y"]["value"] =0
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_z"]["value"] =-12000
            elif side == 1:
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_x"]["value"] =self.border_x + 100000
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_y"]["value"] =0
                self.init_interface["blue_awacs"]["auto_awacs"]["init_AWACS_z"]["value"] =-12000
        if type(self.init_interface["blue_awacs"]) is list:
            for i in range(self.red):
                self.init_interface["blue_awacs"][i]["init_xg_0_est"]["value"] = 0
                self.init_interface["blue_awacs"][i]["init_xg_1_est"]["value"] = 0
                self.init_interface["blue_awacs"][i]["init_xg_2_est"]["value"] = -1000
                self.init_interface["blue_awacs"][i]["init_vg_0_est"]["value"] = 0
                self.init_interface["blue_awacs"][i]["init_vg_1_est"]["value"] = 0
                self.init_interface["blue_awacs"][i]["init_vg_2_est"]["value"] = 100
                
        for i, aircraft in enumerate(
                self.init_interface["AMS"]):  # red first note: use enumerate is necessary, usage of index is not crrect
            if (side == 0 and i < self.red) or (side == 1 and i >= self.red):  # red

                aircraft["init_x"]["value"] = np_random.uniform(-self.border_x + 10000.0, -self.border_x + 15000.0)
                aircraft["init_y"]["value"] = np_random.uniform(-10000.0, 10000.0)
                aircraft["init_z"]["value"] = np_random.uniform(-7000, -5000)
                aircraft["init_mu"]["value"] = 0
                aircraft["init_gamma"]["value"] = 0
                aircraft["init_chi"]["value"] = 0
                aircraft["init_TAS"]["value"] = 400.0
                aircraft["init_alive"]["value"] = 1.0
                aircraft["init_fuel"]["value"] = 600000.0
                aircraft["SMS"][0]["init_state"]["value"] = 1.0
                aircraft["SMS"][1]["init_state"]["value"] = 1.0
                aircraft["SMS"][2]["init_state"]["value"] = 1.0
                aircraft["SMS"][3]["init_state"]["value"] = 1.0
            else:  # blue

                aircraft["init_x"]["value"] = np_random.uniform(self.border_x - 15000.0, self.border_x - 10000.0)
                aircraft["init_y"]["value"] = np_random.uniform(-10000.0, 10000.0)
                aircraft["init_z"]["value"] = np_random.uniform(-7000, -5000)
                aircraft["init_mu"]["value"] = 0
                aircraft["init_gamma"]["value"] = 0
                aircraft["init_chi"]["value"] = 180 / 57.3
                aircraft["init_TAS"]["value"] = 400.0
                aircraft["init_alive"]["value"] = 1.0
                aircraft["init_fuel"]["value"] = 600000.0
                aircraft["SMS"][0]["init_state"]["value"] = 1.0
                aircraft["SMS"][1]["init_state"]["value"] = 1.0
                aircraft["SMS"][2]["init_state"]["value"] = 1.0
                aircraft["SMS"][3]["init_state"]["value"] = 1.0

    def rsi_init(self, rsi_obs:[]):
        for i, aircraft in enumerate(
                self.init_interface["AMS"]):  # red first note: use enumerate is necessary, usage of index is not crrect
                aircraft["init_x"]["value"] = rsi_obs[i]["x"]
                aircraft["init_y"]["value"] = rsi_obs[i]["y"]
                aircraft["init_z"]["value"] = rsi_obs[i]["z"]
                aircraft["init_mu"]["value"] = rsi_obs[i]["mu"]
                aircraft["init_gamma"]["value"] = rsi_obs[i]["gamma"]
                aircraft["init_chi"]["value"] = rsi_obs[i]["chi"]
                aircraft["init_TAS"]["value"] = rsi_obs[i]["TAS"]
                aircraft["init_alive"]["value"] = rsi_obs[i]["alive"]
                aircraft["init_fuel"]["value"] = 600000.0
                aircraft["SMS"][0]["init_state"]["value"] = rsi_obs[i]["msl_stats"][0]
                aircraft["SMS"][1]["init_state"]["value"] = rsi_obs[i]["msl_stats"][1]
                aircraft["SMS"][2]["init_state"]["value"] = rsi_obs[i]["msl_stats"][2]
                aircraft["SMS"][3]["init_state"]["value"] = rsi_obs[i]["msl_stats"][3]

        self.init_interface["init_red_AWACS_x"]["value"] = -self.border_x - 100000
        self.init_interface["init_red_AWACS_y"]["value"] = 0
        self.init_interface["init_red_AWACS_z"]["value"] = -12000
        self.init_interface["init_blue_AWACS_x"]["value"] = self.border_x + 100000
        self.init_interface["init_blue_AWACS_y"]["value"] = 0
        self.init_interface["init_blue_AWACS_z"]["value"] = -12000

    def communicate_cpp(self, data, pull_or_push):
        if type(data) is list:
            for i in data:
                self.communicate_cpp(i, pull_or_push)
        elif type(data) is dict:
            if "value_index" in data.keys():
                if pull_or_push is "pull_value":
                    data["value"] = float(self.war.data_bridge[int(data["value_index"] + 0.1)])
                elif pull_or_push is "pull_mask":
                    for i in range(data["mask_len"]):
                        data["mask"][i] = float(1.0) if self.war.data_bridge[int(
                            data["mask_list_head_index"] + i + 0.1)] > 0.1 else float(0.0)
                elif pull_or_push is "push_value":
                    self.war.data_bridge[int(data["value_index"] + 0.1)] = float(
                        data["value"])  # TODO int64 cant implicit cast, must cast to float?
            else:
                for key in data.keys():
                    self.communicate_cpp(data[key], pull_or_push)

    @staticmethod
    def normalize(data):
        if "value_index" in data.keys():
            if data["value"] < data["min"]:
                return 0.0
            elif data["value"] > data["max"]:
                return 1.0
            else:
                return (float(data["value"]) - float(data["min"])) / (
                        float(data["max"]) - float(data["min"]))  # TODO must cast to float

    @staticmethod
    def normalize_with_bias(data):
        # method for normalize valid data to [0.2, 1], often this data 0 represent data invalid or date of agent die
        if "value_index" in data.keys():
            if data["value"] < data["min"]:
                return 0.2
            elif data["value"] > data["max"]:
                return 1.0
            else:
                return (float(data["value"]) - float(data["min"])) / (
                        float(data["max"]) - float(data["min"])) * 0.8 + 0.2  # TODO must cast to float

    # @staticmethod
    # def denormalize(data, normalized_value):
    #     if "value_index" in data.keys():
    #         if normalized_value < 0.0:
    #             return float(data["min"])
    #         elif normalized_value > 1.0:
    #             return float(data["max"])
    #         else:
    #             return float(normalized_value)*(float(data["max"])-float(data["min"])) + float(data["min"])

    @staticmethod
    def denormalize(data, key, key_low=-1.0, key_high=1.0):
        if "value_index" in data.keys():
            key = max(key_low, min(key, key_high))
            return ((key - key_low) / (key_high - key_low)) * (float(data["max"]) - float(data["min"])) + float(
                data["min"])

    def to_list(self, des_list, src_data):
        if type(src_data) is list:
            for i in src_data:
                self.to_list(des_list, i)
        elif type(src_data) is dict:
            if "value_index" in src_data.keys():
                des_list.append(src_data)
            else:
                for key in src_data.keys():
                    self.to_list(des_list, src_data[key])

    def judge_red_win(self):
        # class GAMERESULT(Enum):
        #     LOSE = -1
        #     DRAW = 0
        #     WIN = 1
        red_alive = 0
        blue_alive = 0
        red_win = 0
        # Counting red/blue alive agents
        for i in range(self.red):
            if self.state_interface["AMS"][i]["alive"]["value"] + 0.1 > 1.0:
                red_alive += 1
        for i in range(self.red, self.red + self.blue):
            if self.state_interface["AMS"][i]["alive"]["value"] + 0.1 > 1.0:
                blue_alive += 1

                # Episodic rewarding based on remaining alive agents
        if red_alive > blue_alive:
            red_win = 1
        elif red_alive < blue_alive:
            red_win = -1

        return red_win


if __name__ == "__main__":
    import time
    start_time = time.time()
    env = BattleSpace()
    print(json.dumps(env.action_interface))
    print(json.dumps(env.state_interface))
    print(json.dumps(env.init_interface))

    sum_step = 0
    for loop in range(1):
        if sum_step == 1000000000:
            break
        env.random_init()
        env.reset(True)

        # environment.normalize_state()
        # print(json.dumps(environment.state_interface))
        while True:
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
            
            for i, action in enumerate(env.action_interface["AMS"]):
                if i < env.red:  # red

                    action["SemanticManeuver"]["combat_mode"]["value"] = 0
                    action["SemanticManeuver"]["maneuver_target"]["value"] = 2
                    action["SemanticManeuver"]["vel_cmd"]["value"] = 400
                    action["SemanticManeuver"]["horizontal_cmd"]["value"] = 1
                    action["SemanticManeuver"]["vertical_cmd"]["value"] = 1
                    action["SemanticManeuver"]["ny_cmd"]["value"] = 8
                    action["SemanticManeuver"]["flag_after_burning"]["value"] = 1
                    action["SemanticManeuver"]["clockwise_cmd"]["value"] = 1
                    # action["SemanticManeuver"]["base_direction"]["value"] = 100
                    # action["DiscreteManeuver"]["action_bfm_id"]["value"] = 13
                    # action["DiscreteManeuver"]["maneuver_target"]["value"] = 2
                    action["action_shoot_predict_list"][0]["shoot_predict"]["value"] = 0
                    action["action_shoot_predict_list"][1]["shoot_predict"]["value"] = 0

                    # action["action_shoot_predict_list"][2]["shoot_predict"]["value"] = 0
                    # action["action_shoot_predict_list"][3]["shoot_predict"]["value"] = 0

                    action["action_shoot_target"]["value"] =0# random.randint(-1,1)
                    action["action_target"]["value"] = 2

                else:  # blue
                    action["SemanticManeuver"]["combat_mode"]["value"] = 0
                    action["SemanticManeuver"]["maneuver_target"]["value"] = 0
                    action["SemanticManeuver"]["vel_cmd"]["value"] = 400
                    action["SemanticManeuver"]["horizontal_cmd"]["value"] = 1
                    action["SemanticManeuver"]["vertical_cmd"]["value"] = 1
                    action["SemanticManeuver"]["ny_cmd"]["value"] = 8
                    action["SemanticManeuver"]["flag_after_burning"]["value"] = 1
                    action["SemanticManeuver"]["clockwise_cmd"]["value"] = 1
                    # action["SemanticManeuver"]["base_direction"]["value"] = 100
                    # action["DiscreteManeuver"]["action_bfm_id"]["value"] = 15
                    # action["DiscreteManeuver"]["maneuver_target"]["value"] = 0
                    action["action_shoot_predict_list"][0]["shoot_predict"]["value"] = 0
                    action["action_shoot_predict_list"][1]["shoot_predict"]["value"] = 0
                    # action["action_shoot_predict_list"][2]["shoot_predict"]["value"] = 0
                    # action["action_shoot_predict_list"][3]["shoot_predict"]["value"] = 0

                    action["action_shoot_target"]["value"] =0#random.randint(-1, 1)
                    action["action_target"]["value"] = 0

                    #
                    # action["F22Stick"]["action_Tc"]["value"] = 1
                    # action["F22Stick"]["action_nyc"]["value"] = 0.6
                    # action["F22Stick"]["action_wxc"]["value"] = 0
                    # action["action_shoot_predict_list"][0]["shoot_predict"]["value"] = 0
                    # action["action_shoot"]["value"] = 0 if random.randint(0, 10) is 1 else 0
                    # target_aircraft = 0
                    # action["target_aircraft"]["value"] = 0
            for i, state in enumerate(env.state_interface["AMS"]):
                print(i, state["Xg_0_est"]["value"],state["Xg_1_est"]["value"],state["Xg_2_est"]["value"])
                print("\t")
                #print(state["fuel"]["value"])
                pass

            #print(json.dumps(env.state_interface))

            env.step()

            sum_step = sum_step + 1
            # print(json.dumps(environment.state_interface))
            # print(json.dumps(environment.state_interface))
            # print(environment.state_to_list())
            # for i in range(environment.red+environment.red):
            #     print(environment.get_ith_aircraft_state(i))
            # print(environment.get_ith_aircraft_state(0))
            # print(environment.state_interface)
            # print([environment.get_ith_aircraft_reward(i) for i in range(environment.blue + environment.red)])
            # print([environment.get_ith_aircraft_state(i) for i in range(environment.blue + environment.red)])
            if env.done:
                # print("--- %s seconds ---" % (time.time() - start_time))
                break
    print("sum step ", sum_step)
    print("--- %s seconds ---" % (time.time() - start_time))
