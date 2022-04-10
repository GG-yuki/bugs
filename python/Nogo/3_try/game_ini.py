from __future__ import print_function
import numpy as np


class DisjointNode(object):  # 并查集项
    def __init__(self, parent: int = -1, belonging: int = -1) -> None:
        self.parent = parent  # 父项
        self.belonging = belonging  # 归属


class Block(object):    # 连通块项
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
        self.refresh_availables()    # 更新可落子列表
        self.current_player = self.get_current_opponent()   # 换手
        self.last_move = move

    def maintain_blocks(self, move: int) -> None:
        self.disjoint[move].parent = move   # 修改落子点的父项为自己
        self.disjoint[move].belonging = self.current_player     # 修改落子点归属
        up, down, left, right = self.up_down_left_right(move)
        udlr = {up, down, left, right} - {-1}  # 四向，去除-1
        blanks = set()  # 落子点周围空格集合
        for u in udlr:
            if self.disjoint[u].parent == -1:   # 如果是四向中的空格
                blanks.add(u)   # 加入空格集合
        self.blocks[move] = Block(self.current_player, blanks)  # 建立新块
        for u in udlr:
            if self.disjoint[u].belonging == self.get_current_opponent():   # 如果是四向中的对手棋子
                that_ancestor = self.get_ancestor(u)    # 该棋子所属连通块的祖先
                self.blocks[that_ancestor].ki -= {move}     # 该连通块气集合移除落子点
        for u in udlr:
            if self.disjoint[u].belonging == self.current_player:   # 如果是四向中的本方棋子
                that_ancestor = self.get_ancestor(u)    # 该棋子所属连通块的祖先
                if that_ancestor != move:
                    self.blocks[that_ancestor].ki -= {move}  # 该连通块气集合移除落子点
                    self.disjoint[that_ancestor].parent = move  # 该祖先的父项设置为落子点
                    self.blocks[move].ki = self.blocks[move].ki|self.blocks[that_ancestor].ki   # 将该连通块的气集合加入新块
                    self.blocks.pop(that_ancestor)  # 删除该连通块
        self.blocks[move].ki = self.blocks[move].ki - {move}

    def refresh_availables(self) -> None:
        for a in self.availables_1:
            up, down, left, right = self.up_down_left_right(a)
            udlr = {up, down, left, right} - {-1}  # 四向，去除-1
            lib_place = 0
            test_ki = set()
            for u in udlr:
                if self.disjoint[u].belonging == -1:    # 是相邻空格
                    test_ki = test_ki|{u}
                    lib_place += 1
                elif self.disjoint[u].belonging == self.players[1]:     # 是对手的子
                    that_ancestor = self.get_ancestor(u)    # 获取其所在块的祖先
                    if len(self.blocks[that_ancestor].ki) < 2:  # 对方块气数<2，落子会导致吃子
                        if a in self.availables_1:
                            self.availables_1.remove(a)     # 本方不可在此落子，会导致吃子
                        break   # 检查下一个可落子点
                else:   # 是本方的子
                    lib_place += 1
            if lib_place < 1:   # 周围没有空格或本方的子
                if a in self.availables_1:
                    self.availables_1.remove(a)     # 本方不可在此落子，周围都是对手的子
            for u in udlr:
                if self.disjoint[u].belonging == self.players[0]:   # 是本方的子
                    that_ancestor = self.get_ancestor(u)    # 获取其所在块的祖先
                    test_ki = test_ki|self.blocks[that_ancestor].ki - {a}     # 计算潜在新块总气数
            if len(test_ki) < 1:    # 潜在新块总气数<1
                if a in self.availables_1:
                    self.availables_1.remove(a)     # 本方不可在此落子，会导致本方已有块无气
        for b in self.availables_2:
            up, down, left, right = self.up_down_left_right(b)
            udlr = {up, down, left, right} - {-1}   # 四向，去除-1
            lib_place = 0
            test_ki = set()
            for u in udlr:
                if self.disjoint[u].belonging == -1:    # 是相邻空格
                    test_ki = test_ki|{u}
                    lib_place += 1
                elif self.disjoint[u].belonging == self.players[0]:     # 是对手的子
                    that_ancestor = self.get_ancestor(u)    # 获取其所在块的祖先
                    if len(self.blocks[that_ancestor].ki) < 2:  # 对方块气数<2，落子会导致吃子
                        if b in self.availables_2:
                            self.availables_2.remove(b)     # 本方不可在此落子，会导致吃子
                        break   # 检查下一个可落子点
                else:   # 是本方的子
                    lib_place += 1
            if lib_place < 1:   # 周围没有空格或本方的子
                if b in self.availables_2:
                    self.availables_2.remove(b)     # 本方不可在此落子，周围都是对手的子
            for u in udlr:
                if self.disjoint[u].belonging == self.players[1]:   # 是本方的子
                    that_ancestor = self.get_ancestor(u)    # 获取其所在块的祖先
                    test_ki = test_ki|self.blocks[that_ancestor].ki - {b}     # 计算潜在新块总气数
            if len(test_ki) < 1:    # 潜在新块总气数<1
                if b in self.availables_2:
                    self.availables_2.remove(b)     # 本方不可在此落子，会导致本方已有块无气

    def has_a_winner(self):     # 是否有获胜者
        if self.current_player == self.players[0]:
            if not len(self.availables_1):  # 无处可落子
                return True, self.get_current_opponent()
        else:
            if not len(self.availables_2):  # 无处可落子
                return True, self.get_current_opponent()
        return False, -1

    def game_end(self):     # 是否终局
        win, winner = self.has_a_winner()
        if win:
            return True, winner
        else:
            return False, -1

    def get_current_player(self) -> int:    # 获取本方
        return self.current_player

    def get_current_opponent(self) -> int:  # 获取对手
        if self.current_player == self.players[0]:
            return self.players[1]
        else:
            return self.players[0]

    def up_down_left_right(self, point: int):   # 获取四向
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

    def get_ancestor(self, move: int) -> int:   # 找祖先
        while True:
            if self.disjoint[move].parent == move:
                return move
            else:
                move = self.disjoint[move].parent


class Game(object):
    """game server"""

    def __init__(self, board, **kwargs):
        self.board = board  # 初始化棋盘

    def graphic(self, board, player1, player2, new_step=-1):  # 画棋盘 from board.state
        """Draw the board and show game info"""
        zis = ['0 ', '1 ', '2 ', '3 ', '4 ', '5 ', '6 ', '7 ', '8 ']
        print("Player", player1, "with ●".rjust(3))
        print("Player", player2, "with ○".rjust(3))
        print()
        print("{0:2}".format(' ') + ' ', end='')
        for x in range(board.width):
            print("{0:2}".format(zis[x]), end='')
        print('')
        for i in range(board.height - 1, -1, -1):
            print("{0:2d}".format(i) + ' ', end='')
            for j in range(board.width):
                loc = i * board.width + j
                p = board.states.get(loc, -1)
                if p == player1:
                    if loc == new_step:
                        print('◆'.center(2), end='')
                    else:
                        print('●'.center(2), end='')
                elif p == player2:
                    if loc == new_step:
                        print('◇'.center(2), end='')
                    else:
                        print('○'.center(2), end='')
                else:
                    print('.'.center(2), end='')
            print('')

    def start_play(self, player1, player2, start_player=0, is_shown=1):     # 下棋
        """start a game between two players"""
        if start_player not in (0, 1):  # 棋手标号不合规
            raise Exception('start_player should be either 0 (player1 first) '
                            'or 1 (player2 first)')
        self.board.init_board(start_player)  # 初始化棋盘
        p1, p2 = self.board.players  # 两个棋手
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:  # 是否显示
            self.graphic(self.board, player1.player, player2.player)    # 画棋盘
        while True:
            current_player = self.board.get_current_player()  # 获取当前棋手
            player_in_turn = players[current_player]
            # self.board.set_current_availables()     # 设定当前使用的availables
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)  # 进行落子
            print('>>>>Player ' + str(player_in_turn) + ' at ' + str(move))
            if is_shown:
                self.graphic(self.board, player1.player, player2.player, move)
            end, winner = self.board.game_end()  # 终局信息
            if end:     # 是否终局
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is", players[winner])
                    else:
                        print("Game end. Tie")
                return winner

    def start_self_play(self, player, is_shown=1, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training
        """
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        steps = 0
        step_place = []
        while True:
            # self.board.set_current_availables()  # 设定当前使用的availables
            move = -1
            both_able = set(self.board.availables_1) & set(self.board.availables_2)
            if len(both_able) > 0:
                while move not in both_able:
                    move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            else:
                while move not in self.board.get_current_availables():
                    move, move_probs = player.get_action(self.board, temp=temp, return_prob=1)
            # store the data
            states.append(self.board.current_state())   # append 局面
            mcts_probs.append(move_probs)   # append MCTS
            current_players.append(self.board.current_player)   # append 当前棋手
            # perform a move
            self.board.do_move(move)    # 下子
            steps += 1
            step_place = self.board.move_to_location(move)
            print()
            print('\tPlayer 1 is able to drop at')
            print(self.board.availables_1)
            print()
            print('\tPlayer 2 is able to drop at')
            print(self.board.availables_2)
            print('>>>Step ' + str(steps))
            print('>>>Player ' + str(self.board.get_current_opponent()) + ' at ' + str(move) + ' (' + str(step_place[0]) + ',' + str(step_place[1]) + ')')
            if is_shown:    # 是否显示
                self.graphic(self.board, p1, p2, move)    # 画棋盘
            end, winner = self.board.game_end()     # 终局信息
            if end:     # 是否终局
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()   # 重设
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)