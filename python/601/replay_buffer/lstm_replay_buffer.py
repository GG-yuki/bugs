import ray
from collections import namedtuple

Transition = namedtuple('Transition', (
    'state', 'vel_cmd', 'vel_cmd_p', 'horizontal_cmd', 'horizontal_cmd_p',
    'vertical_cmd', 'vertical_cmd_p', 'ny_cmd', 'ny_cmd_p', 'flag_after_burning', 'flag_after_burning_p', 'm_target',
    'm_target_p', 's_action', 's_action_p', 'lstm_hidden_0', 'lstm_hidden_1', 'reward', 'returns', 'advantage'))


@ray.remote
class ReplayBuffer:

    def __init__(self):
        self.size = 0
        self.episode = 0
        self.memory = []

    def push(self, *args):
        self.memory.append(Transition(*args))

    def get_size(self):
        return self.size

    def count_size(self, count):
        self.size = self.size + count

    def buffer_reset(self):
        self.size = 0
        self.memory.clear()

    def extract_data(self):
        return Transition(*zip(*self.memory))

    def count_episode(self):
        self.episode += 1

    def get_total_episode(self):
        return self.episode
