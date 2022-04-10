# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""
import copy
import json
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np


class DisjointNode(object):  # 并查集项
    def __init__(self, parent: int = -1, belonging: int = -1) -> None:
        self.parent = parent  # 父项
        self.belonging = belonging  # 归属


class Block(object):  # 连通块项
    def __init__(self, belonging: int, ki: set) -> None:
        # self.ancestor = ancestor  # 祖先
        self.belonging = belonging  # 归属
        self.ki = ki  # 气集合


class Board(object):
    def __init__(self, **kwargs) -> None:
        self.width = int(kwargs.get('width', 9))  # 棋盘宽度 9
        self.height = int(kwargs.get('height', 9))  # 棋盘高度 9
        self.states = {}
        # 棋盘状态，以字典存储
        # key：   移动（数字标号）
        # value： 棋手（标号）
        self.players = [1, 2]  # 两个棋手

    def init_board(self, start_player: int = 0) -> None:
        self.current_player = self.players[start_player]  # 先手棋手
        self.availables_1 = list(range(self.width * self.height))  # 将全部可落子位置装入列表
        self.availables_2 = list(range(self.width * self.height))  # 将全部可落子位置装入列表
        # self.availables = []
        # self.set_current_availables()
        self.states = {}
        self.last_move = -1
        self.disjoint = []
        for i in range(self.width * self.height):
            self.disjoint.append(DisjointNode(-1, -1))
        self.blocks = {}  # 连通块字典

    def move_to_location(self, move: int) -> []:
        h = move // self.width  # 行坐标
        w = move % self.width  # 列坐标
        return [h, w]  # 返回坐标

    def location_to_move(self, location: []) -> int:
        if len(location) != 2:  # 列表形式不合规
            return -1
        h = location[0]  # 行坐标
        w = location[1]  # 列坐标
        m = h * self.width + w  # 移动数字标号
        if m not in range(self.width * self.height):  # 超出棋盘范围
            return -1
        return m  # 返回数字标号

    def current_state(self) -> []:  # 以当前棋手的角度返回棋盘状态
        square_state = np.zeros((4, self.width, self.height))  # 状态形状：4*宽*高
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))  # 取出moves和players？
            move_curr = moves[players == self.current_player]  # 当前棋手的moves
            move_oppo = moves[players != self.current_player]  # 对手的moves
            square_state[0][move_curr // self.width, move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width, move_oppo % self.height] = 1.0
            square_state[2][self.last_move // self.width, self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0
        return square_state[:, ::-1, :]

    def do_move(self, move: int) -> None:
        self.states[move] = self.current_player
        if move in self.availables_1:
            self.availables_1.remove(move)  # 从可落子列表删除落子点
        if move in self.availables_2:
            self.availables_2.remove(move)  # 从可落子列表删除落子点
        self.maintain_blocks(move)  # 维护连通块字典
        self.refresh_availables()  # 更新可落子列表
        self.current_player = self.get_current_opponent()  # 换手
        self.last_move = move

    def maintain_blocks(self, move: int) -> None:
        self.disjoint[move].parent = move  # 修改落子点的父项为自己
        self.disjoint[move].belonging = self.current_player  # 修改落子点归属
        up, down, left, right = self.up_down_left_right(move)
        udlr = {up, down, left, right} - {-1}  # 四向，去除-1
        blanks = set()  # 落子点周围空格集合
        for u in udlr:
            if self.disjoint[u].parent == -1:  # 如果是四向中的空格
                blanks.add(u)  # 加入空格集合
        self.blocks[move] = Block(self.current_player, blanks)  # 建立新块
        for u in udlr:
            if self.disjoint[u].belonging == self.get_current_opponent():  # 如果是四向中的对手棋子
                that_ancestor = self.get_ancestor(u)  # 该棋子所属连通块的祖先
                self.blocks[that_ancestor].ki -= {move}  # 该连通块气集合移除落子点
        for u in udlr:
            if self.disjoint[u].belonging == self.current_player:  # 如果是四向中的本方棋子
                that_ancestor = self.get_ancestor(u)  # 该棋子所属连通块的祖先
                if that_ancestor != move:
                    self.blocks[that_ancestor].ki -= {move}  # 该连通块气集合移除落子点
                    self.disjoint[that_ancestor].parent = move  # 该祖先的父项设置为落子点
                    self.blocks[move].ki = self.blocks[move].ki | self.blocks[that_ancestor].ki  # 将该连通块的气集合加入新块
                    self.blocks.pop(that_ancestor)  # 删除该连通块
        self.blocks[move].ki = self.blocks[move].ki - {move}

    def refresh_availables(self) -> None:
        for a in self.availables_1:
            up, down, left, right = self.up_down_left_right(a)
            udlr = {up, down, left, right} - {-1}  # 四向，去除-1
            lib_place = 0
            test_ki = set()
            for u in udlr:
                if self.disjoint[u].belonging == -1:  # 是相邻空格
                    test_ki = test_ki | {u}
                    lib_place += 1
                elif self.disjoint[u].belonging == self.players[1]:  # 是对手的子
                    that_ancestor = self.get_ancestor(u)  # 获取其所在块的祖先
                    if len(self.blocks[that_ancestor].ki) < 2:  # 对方块气数<2，落子会导致吃子
                        if a in self.availables_1:
                            self.availables_1.remove(a)  # 本方不可在此落子，会导致吃子
                        break  # 检查下一个可落子点
                else:  # 是本方的子
                    lib_place += 1
            if lib_place < 1:  # 周围没有空格或本方的子
                if a in self.availables_1:
                    self.availables_1.remove(a)  # 本方不可在此落子，周围都是对手的子
            for u in udlr:
                if self.disjoint[u].belonging == self.players[0]:  # 是本方的子
                    that_ancestor = self.get_ancestor(u)  # 获取其所在块的祖先
                    test_ki = test_ki | self.blocks[that_ancestor].ki - {a}  # 计算潜在新块总气数
            if len(test_ki) < 1:  # 潜在新块总气数<1
                if a in self.availables_1:
                    self.availables_1.remove(a)  # 本方不可在此落子，会导致本方已有块无气
        for b in self.availables_2:
            up, down, left, right = self.up_down_left_right(b)
            udlr = {up, down, left, right} - {-1}  # 四向，去除-1
            lib_place = 0
            test_ki = set()
            for u in udlr:
                if self.disjoint[u].belonging == -1:  # 是相邻空格
                    test_ki = test_ki | {u}
                    lib_place += 1
                elif self.disjoint[u].belonging == self.players[0]:  # 是对手的子
                    that_ancestor = self.get_ancestor(u)  # 获取其所在块的祖先
                    if len(self.blocks[that_ancestor].ki) < 2:  # 对方块气数<2，落子会导致吃子
                        if b in self.availables_2:
                            self.availables_2.remove(b)  # 本方不可在此落子，会导致吃子
                        break  # 检查下一个可落子点
                else:  # 是本方的子
                    lib_place += 1
            if lib_place < 1:  # 周围没有空格或本方的子
                if b in self.availables_2:
                    self.availables_2.remove(b)  # 本方不可在此落子，周围都是对手的子
            for u in udlr:
                if self.disjoint[u].belonging == self.players[1]:  # 是本方的子
                    that_ancestor = self.get_ancestor(u)  # 获取其所在块的祖先
                    test_ki = test_ki | self.blocks[that_ancestor].ki - {b}  # 计算潜在新块总气数
            if len(test_ki) < 1:  # 潜在新块总气数<1
                if b in self.availables_2:
                    self.availables_2.remove(b)  # 本方不可在此落子，会导致本方已有块无气

    def get_current_player(self) -> int:  # 获取本方
        return self.current_player

    def get_current_opponent(self) -> int:  # 获取对手
        if self.current_player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]

    def up_down_left_right(self, point: int):  # 获取四向
        if point % self.width != 0:
            left = point - 1
        else:
            left = -1
        if point % self.width != self.width - 1:
            right = point + 1
        else:
            right = -1
        if point < self.width * (self.width - 1):
            up = point + self.width
        else:
            up = -1
        if point >= self.width:
            down = point - self.width
        else:
            down = -1
        return up, down, left, right

    def get_current_availables(self) -> []:
        if self.current_player == self.players[0]:
            return self.availables_1
        else:
            return self.availables_2

    # def set_current_availables(self) -> None:
    # if self.current_player == self.players[0]:
    # self.availables = self.availables_1
    # else:
    # self.availables = self.availables_2

    def get_ancestor(self, move: int) -> int:  # 找祖先
        while True:
            if self.disjoint[move].parent == move:
                return move
            else:
                move = self.disjoint[move].parent


class Game(object):
    """game server"""

    def __init__(self, board, **kwargs):
        self.board = board  # 初始化棋盘

    def start_play(self, player1, player2, start_player=0, is_shown=1):  # 下棋
        """start a game between two players"""
        line = input().strip()
        full_input = json.loads(line)
        requests = full_input['requests']
        x = requests[0]['x']
        y = requests[0]['y']
        if x < 0:
            start_player = 1
        else:
            start_player = 0
        self.board.init_board(start_player)  # 初始化棋盘
        p1, p2 = self.board.players  # 两个棋手
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if x >= 0:
            current_player = self.board.get_current_player()  # 获取当前棋手
            player_in_turn = players[current_player]
            move = 80 - (x + 1) * 9 + y + 1
            self.board.do_move(move)  # 进行落子
        while True:
            current_player = self.board.get_current_player()  # 获取当前棋手
            player_in_turn = players[current_player]
            # self.board.set_current_availables()     # 设定当前使用的availables
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)  # 进行落子


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class TreeNode(object):
    """A node in the MCTS tree.

    Each node keeps track of its own value Q, prior probability P, and
    its visit-count-adjusted prior score u.
    """

    def __init__(self, parent, prior_p):
        self._parent = parent
        self._children = {}  # a map from action to TreeNode
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self, action_priors):
        """Expand tree by creating new children.
        action_priors: a list of tuples of actions and their prior probability
            according to the policy function.
        """
        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        """Select action among children that gives maximum action value Q
        plus bonus u(P).
        Return: A tuple of (action, next_node)
        """
        return max(self._children.items(),
                   key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):
        """Update node values from leaf evaluation.
        leaf_value: the value of subtree evaluation from the current player's
            perspective.
        """
        # Count visit.
        self._n_visits += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0 * (leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        """Calculate and return the value for this node.
        It is a combination of leaf evaluations Q, and this node's prior
        adjusted for its visit count, u.
        c_puct: a number in (0, inf) controlling the relative impact of
            value Q, and prior probability P, on this node's score.
        """
        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded)."""
        return self._children == {}

    def is_root(self):
        return self._parent is None


class MCTS(object):
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        """
        policy_value_fn: a function that takes in a board state and outputs
            a list of (action, probability) tuples and also a score in [-1, 1]
            (i.e. the expected value of the end game score from the current
            player's perspective) for the current player.
        c_puct: a number in (0, inf) that controls how quickly exploration
            converges to the maximum-value policy. A higher value means
            relying on the prior more.
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout

    def _playout(self, state):
        """Run a single playout from the root to the leaf, getting a value at
        the leaf and propagating it back through its parents.
        State is modified in-place, so a copy must be provided.
        """
        node = self._root
        while (1):
            if node.is_leaf():
                break
            # Greedily select next move.
            action, node = node.select(self._c_puct)
            state.do_move(action)

        # Evaluate the leaf using a network which outputs a list of
        # (action, probability) tuples p and also a score v in [-1, 1]
        # for the current player.
        action_probs, leaf_value = self._policy(state)
        # Check for end of game.
        end, winner = state.game_end()
        if not end:
            node.expand(action_probs)
        else:
            # for end state，return the "true" leaf_value
            if winner == -1:  # tie
                leaf_value = 0.0
            else:
                leaf_value = (
                    1.0 if winner == state.get_current_player() else -1.0
                )

        # Update value and visit count of nodes in this traversal.
        node.update_recursive(-leaf_value)

    def get_move_probs(self, state, temp=1e-3):
        """Run all playouts sequentially and return the available actions and
        their corresponding probabilities.
        state: the current game state
        temp: temperature parameter in (0, 1] controls the level of exploration
        """
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)

        # calc the move probabilities based on visit counts at the root node
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0 / temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):
        """Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def __str__(self):
        return "MCTS"


class MCTSPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board, temp=1e-3, return_prob=0):
        sensible_moves = board.get_current_availables()
        # the pi vector returned by MCTS as in the alphaGo Zero paper
        move_probs = np.zeros(board.width * board.height)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(board, temp)
            move_probs[list(acts)] = probs
            if self._is_selfplay:
                # add Dirichlet Noise for exploration (needed for
                # self-play training)
                move = np.random.choice(
                    acts,
                    p=0.75 * probs + 0.25 * np.random.dirichlet(0.3 * np.ones(len(probs)))
                )
                # update the root node and reuse the search tree
                self.mcts.update_with_move(move)
            else:
                # with the default temp=1e-3, it is almost equivalent
                # to choosing the move with the highest prob
                move = np.random.choice(acts, p=probs)
                # reset the root node
                self.mcts.update_with_move(-1)
            #                location = board.move_to_location(move)
            #                print("AI move: %d,%d\n" % (location[0], location[1]))

            x = 8 - ((80 - move) % 9)
            y = (80 - move) // 9

            print(json.dumps({'response': {'x': x, 'y': y}}))
            print('\n>>>BOTZONE_REQUEST_KEEP_RUNNING<<<\n', flush=True)

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)


def set_learning_rate(optimizer, lr):
    """Sets the learning rate to the given value"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


class Net(nn.Module):
    """policy-value network module"""

    def __init__(self, board_width, board_height):
        super(Net, self).__init__()

        self.board_width = board_width
        self.board_height = board_height
        # common layers
        self.conv1 = nn.Conv2d(4, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        # action policy layers
        self.act_conv1 = nn.Conv2d(128, 4, kernel_size=1)
        self.act_fc1 = nn.Linear(4 * board_width * board_height,
                                 board_width * board_height)
        # state value layers
        self.val_conv1 = nn.Conv2d(128, 2, kernel_size=1)
        self.val_fc1 = nn.Linear(2 * board_width * board_height, 64)
        self.val_fc2 = nn.Linear(64, 1)

    def forward(self, state_input):
        # common layers
        x = F.relu(self.conv1(state_input))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        # action policy layers
        x_act = F.relu(self.act_conv1(x))
        x_act = x_act.view(-1, 4 * self.board_width * self.board_height)
        x_act = F.log_softmax(self.act_fc1(x_act), dim=1)
        # state value layers
        x_val = F.relu(self.val_conv1(x))
        x_val = x_val.view(-1, 2 * self.board_width * self.board_height)
        x_val = F.relu(self.val_fc1(x_val))
        x_val = torch.tanh(self.val_fc2(x_val))
        return x_act, x_val


class PolicyValueNet():
    """policy-value network """

    def __init__(self, board_width, board_height,
                 model_file=True, use_gpu=False):
        self.use_gpu = use_gpu
        self.board_width = board_width
        self.board_height = board_height
        self.l2_const = 1e-4  # coef of l2 penalty
        # the policy value net module
        if self.use_gpu:
            self.policy_value_net = Net(board_width, board_height).cuda()
        else:
            self.policy_value_net = Net(board_width, board_height)
        self.optimizer = optim.Adam(self.policy_value_net.parameters(),
                                    weight_decay=self.l2_const)

        if model_file:
            # net_params = torch.load(model_file)
            self.policy_value_net.load_state_dict(torch.load(r'./data/best_policy.pkl'))

    def policy_value(self, state_batch):
        """
        input: a batch of states
        output: a batch of action probabilities and state values
        """
        if self.use_gpu:
            state_batch = Variable(torch.FloatTensor(state_batch).cuda())
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.cpu().numpy())
            return act_probs, value.data.cpu().numpy()
        else:
            state_batch = Variable(torch.FloatTensor(state_batch))
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.numpy())
            return act_probs, value.data.numpy()

    def policy_value_fn(self, board):
        """
        input: board
        output: a list of (action, probability) tuples for each available
        action and the score of the board state
        """
        legal_positions = board.get_current_availables()
        current_state = np.ascontiguousarray(board.current_state().reshape(
            -1, 4, self.board_width, self.board_height))
        if self.use_gpu:
            log_act_probs, value = self.policy_value_net(
                Variable(torch.from_numpy(current_state)).cuda().float())
            act_probs = np.exp(log_act_probs.data.cpu().numpy().flatten())
        else:
            log_act_probs, value = self.policy_value_net(
                Variable(torch.from_numpy(current_state)).float())
            act_probs = np.exp(log_act_probs.data.numpy().flatten())
        act_probs = zip(legal_positions, act_probs[legal_positions])
        value = value.data[0][0]
        return act_probs, value

    def train_step(self, state_batch, mcts_probs, winner_batch, lr):
        """perform a training step"""
        # wrap in Variable
        if self.use_gpu:
            state_batch = Variable(torch.FloatTensor(state_batch).cuda())
            mcts_probs = Variable(torch.FloatTensor(mcts_probs).cuda())
            winner_batch = Variable(torch.FloatTensor(winner_batch).cuda())
        else:
            state_batch = Variable(torch.FloatTensor(state_batch))
            mcts_probs = Variable(torch.FloatTensor(mcts_probs))
            winner_batch = Variable(torch.FloatTensor(winner_batch))

        # zero the parameter gradients
        self.optimizer.zero_grad()
        # set learning rate
        set_learning_rate(self.optimizer, lr)

        # forward
        log_act_probs, value = self.policy_value_net(state_batch)
        # define the loss = (z - v)^2 - pi^T * log(p) + c||theta||^2
        # Note: the L2 penalty is incorporated in optimizer
        value_loss = F.mse_loss(value.view(-1), winner_batch)
        policy_loss = -torch.mean(torch.sum(mcts_probs * log_act_probs, 1))
        loss = value_loss + policy_loss
        # backward and optimize
        loss.backward()
        self.optimizer.step()
        # calc policy entropy, for monitoring only
        entropy = -torch.mean(
            torch.sum(torch.exp(log_act_probs) * log_act_probs, 1)
        )
        return loss.item(), entropy.item()
        # for pytorch version >= 0.5 please use the following line instead.
        # return loss.item(), entropy.item()

    def get_policy_param(self):
        net_params = self.policy_value_net.state_dict()
        return net_params

    def save_model(self, model_file):
        """ save model params to file """
        net_params = self.get_policy_param()  # get model params
        # torch.save(net, save_epoch + '.pkl')  # 保存整个网络
        torch.save(net_params, model_file)


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        line = input().strip()
        full_input = json.loads(line)
        x = full_input['x']
        y = full_input['y']
        move = 80 - (x + 1) * 9 + y + 1
        return move


def run():
    # n = 5
    width, height = 9, 9  # width, height = 8, 8
    # model_file = './best_policy.pkl'
    # board = Board(width=width, height=height, n_in_row=n)
    board = Board(width=width, height=height)
    game = Game(board)

    # ############### human VS AI ###################
    # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

    # best_policy = PolicyValueNet(width, height, model_file = model_file)
    # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

    # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
    # try:
    #     policy_param = pickle.load(open(model_file, 'rb'))
    # policy_param = pickle.load(open(model_file, 'rb'),
    #                                encoding='bytes')  # To support python3
    best_policy = PolicyValueNet(width, height)
    mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                             c_puct=5,
                             n_playout=400)  # set larger n_playout for better performance

    # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
    # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

    # human player, input your move in the format: 2,3
    human = Human()

    # set start_player=0 for human first
    game.start_play(human, mcts_player, start_player=0, is_shown=0)


if __name__ == '__main__':
    run()
