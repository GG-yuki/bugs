import argparse
from torch.optim import Adam
import torch as th
import ray
import time

from utils import utils
from policy.lstm import PPOlstmDiscrete
from policy.lstm_rollout import worker_rollout
from replay_buffer.lstm_replay_buffer import ReplayBuffer

total_update = 0


@ray.remote
class ParameterServer(object):
    def __init__(self, weights):
        # 将master中初始化得到的网络参数存下，用于全局初始化一致
        self.weights = weights

    def push(self, weights):
        self.weights = weights

    def pull(self):
        return self.weights

    def get_weights(self):
        return self.weights


def worker_train_local(ps, replay_buffer, config, agents, optimizers, clip_now=0.2):
    global total_update
    start_time = time.time()

    # weights是新policy网络和V值网络的参数,是要从主函数创建的net里取新policy网络和V值网络的参数，以保持全局初始化网络的权重值一致
    # state_dicts = ray.get(ps.pull.remote())
    # [agents[i].load_state_dict(state_dicts[i]) for i in range(args.fighter_num)]

    [agents[i].to(agents[i].device) for i in range(2)]  # 在这里将要进行学习的agent送到显卡上

    current_episode = agents[0].train_local(replay_buffer[0], config, optimizers[0], clip_now)
    agents[0].train_local(replay_buffer[1], config, optimizers[0], clip_now)
    agents[1].train_local(replay_buffer[2], config, optimizers[1], clip_now)
    agents[1].train_local(replay_buffer[3], config, optimizers[1], clip_now)

    # 将参数推入ps
    state_dicts = [agents[i].cpu().state_dict() for i in range(2)]
    # print("weight0", agents[0].linear1.weight[0][0])
    # print("weight1", agents[1].linear1.weight[0][0])
    ps.push.remote(state_dicts)

    # 清空replay_buffer
    [replay_buffer[i].buffer_reset.remote() for i in range(config.fighter_num)]

    if (total_update + 1) % config.save_interval == 0:
        for j in range(2):
            th.save(agents[j].state_dict(),
                    config.save_model_location + str(j) + '---' + str(current_episode) + '---' + str(total_update))
        print("save model at episode:{}".format(str(current_episode)))

    total_update += 1
    print('total_update time:{}'.format(total_update))
    print('current local_train process duration: {}'.format(str(time.time() - start_time)))
    return agents[0].update_time


def load_model(net, num, iter_num):
    num = str(num)
    iter_num = str(iter_num)
    print("======载入模型继续训练======")
    # net[2].load_state_dict(
    #     th.load('./load_model/final_1---' + num
    #             # , map_location='cpu'
    #             ))
    # net[3].load_state_dict(
    #     th.load('./load_model/final_1---' + num
    #             # , map_location='cpu'
    #             ))
    net[0].load_state_dict(
        th.load('./load_model/final_0---' + num + '---' + iter_num
                # , map_location='cpu'
                ))
    net[1].load_state_dict(
        th.load('./load_model/final_0---' + num + '---' + iter_num
                # , map_location='cpu'
                ))
    print("======模型加载成功======")


def wait(buffer, batch_size):
    # print('wait sample data...')
    begin = time.time()
    while ray.get(buffer[0].get_size.remote()) < batch_size or ray.get(
            buffer[1].get_size.remote()) < batch_size or ray.get(buffer[2].get_size.remote()) < batch_size or ray.get(
        buffer[3].get_size.remote()) < batch_size:
        print('replay_buffer_0_size:{}'.format(ray.get(buffer[0].get_size.remote())))
        print('replay_buffer_1_size:{}'.format(ray.get(buffer[1].get_size.remote())))
        print('replay_buffer_2_size:{}'.format(ray.get(buffer[2].get_size.remote())))
        print('replay_buffer_3_size:{}'.format(ray.get(buffer[3].get_size.remote())))
        time.sleep(6)
    print('sample batch_data process time:{}'.format(str(time.time() - begin)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_rollout_threads", default=12, type=int)
    parser.add_argument("--save_interval", default=200, type=int, help="Number of update times per save interval")
    parser.add_argument("--batch_size", default=32000, type=int, help="Batch size for training")
    parser.add_argument("--minibatch_size", default=3200, type=int, help="Minibatch size for training")
    parser.add_argument("--continue_train", default=False, type=bool, help="Load model to continue train or not")
    parser.add_argument("--load_model_location", default='./load_model/final_', type=str,
                        help="Load model location")
    parser.add_argument("--save_model_location", default='./output_model/final_', type=str,
                        help="Load model location")
    parser.add_argument("--max_episodes", default=100000, type=int)
    parser.add_argument("--episode_length", default=20, type=int)
    parser.add_argument("--num_epoch", default=10, type=int,
                        help="(epoch)Number of updates per update cycle")
    parser.add_argument("--gamma", default=0.9, type=float)
    parser.add_argument("--clip", default=0.2, type=float)
    parser.add_argument("--loss_coeff_value", default=0.5, type=float)
    parser.add_argument("--loss_coeff_entropy", default=0.01, type=float)
    parser.add_argument("--lr", default=float(3e-4), type=float)
    parser.add_argument("--state_dim", default=98, type=int)
    parser.add_argument("--hidden_layer_size", default=256, type=int, help="Lstm hidden units")
    parser.add_argument("--fighter_num", default=4, type=int)
    parser.add_argument("--timeout", default=600, type=int)

    # tricks
    parser.add_argument("--ratio_norm", default=True, type=bool)
    parser.add_argument("--advantage_norm", default=True, type=bool)
    parser.add_argument("--lossvalue_norm", default=True, type=bool)

    config = parser.parse_args()
    utils.setup_seed()  # 设置随机初始化种子，神经网络需要初始化，使用同样的随机初始化种子可保证每次初始化都相同

    ray.init(local_mode=False)
    # ray.init(address='auto', redis_password='5241590000000000',local_mode=False)

    ps_agents = [PPOlstmDiscrete(config.state_dim, config.hidden_layer_size) for i in
                 range(2)]  # 2 represent red and blue
    if config.continue_train:
        load_model(ps_agents, num=490734, iter_num=1199)
    else:
        [a.initialize_weights() for a in ps_agents]
    optimizers = [Adam(a.parameters(), lr=config.lr) for a in ps_agents]

    state_dicts = [a.cpu().state_dict() for a in
                   ps_agents]  # model.state_dict()其实返回的是一个OrderDict，存储了网络结构的名字和对应的参数, 并且.cpu(
    # )是为了给worker进程用cpu进行采样，所以权重是cpu的

    ps = ParameterServer.remote(state_dicts)

    replay_buffer = [ReplayBuffer.remote() for i in range(config.fighter_num)]

    for i in range(config.n_rollout_threads):
        worker_rollout.remote(ps, replay_buffer, config)

    while True:
        wait(replay_buffer, config.batch_size)
        update_time = worker_train_local(ps, replay_buffer, config, ps_agents, optimizers)

        # ***trick***
        # if args.schedule_clip == 'linear':
        #     ep_ratio = 1 - (current_episode / args.delay_episode)
        #     clip_now = args.clip * ep_ratio

        # ***trick***
        # if args.schedule_adam == 'linear':
        #     if (update_time + 1) % 200 == 0:
        #         # ep_ratio = 1 - (current_episode / args.delay_episode)
        #         ep_ratio = 0.95
        #         lr_now = lr_now * ep_ratio
        #         # set learning rate
        #         # ref: https://stackoverflow.com/questions/48324152/
        #         for j in range(args.fighter_num):
        #             for g in optimizers[j].param_groups:
        #                 g['lr'] = lr_now
