# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np


class Board(object):
    """board for the game"""

    def __init__(self, **kwargs):
        self.width = int(kwargs.get('width', 9))
        self.height = int(kwargs.get('height', 9))
        # board states stored as a dict,
        # key: move as location on the board,
        # value: player as pieces type
        self.states = {}
        # need how many pieces in a row to win
        self.players = [1, 2]  # player1 and player2

    def init_board(self, start_player=0):
        self.current_player = self.players[start_player]  # start player
        # keep available moves in a list
        self.availables = {}
        for player in self.players:
            self.availables[player] = list(range(self.width * self.height))
        self.states = {}
        self.last_move = -1

    def move_to_location(self, move):
        """
        3*3 board's moves like:
        6 7 8
        3 4 5
        0 1 2
        and move 5's location is (1,2)
        """
        h = move // self.width
        w = move % self.width
        return [h, w]

    def location_to_move(self, location):
        if len(location) != 2:
            return -1
        h = location[0]
        w = location[1]
        move = h * self.width + w
        if move not in range(self.width * self.height):
            return -1
        return move

    def current_state(self):
        """return the board state from the perspective of the current player.
        state shape: 4*width*height
        """

        square_state = np.zeros((4, self.width, self.height))
        if self.states:
            moves, players = np.array(list(zip(*self.states.items())))
            move_curr = moves[players == self.current_player]
            move_oppo = moves[players != self.current_player]
            square_state[0][move_curr // self.width,
                            move_curr % self.height] = 1.0
            square_state[1][move_oppo // self.width,
                            move_oppo % self.height] = 1.0
            # indicate the last move location
            square_state[2][self.last_move // self.width,
                            self.last_move % self.height] = 1.0
        if len(self.states) % 2 == 0:
            square_state[3][:, :] = 1.0  # indicate the colour to play
        return square_state[:, ::-1, :]

    def adjacent_moves(self, move):
        h, w = self.move_to_location(move)
        adjs = []
        if h > 0: adjs.append(self.location_to_move((h-1, w)))
        if h < self.height - 1: adjs.append(self.location_to_move((h+1, w)))
        if w > 0: adjs.append(self.location_to_move((h, w-1)))
        if w < self.width - 1: adjs.append(self.location_to_move((h, w+1)))
        return adjs

    def has_vacancy(self, move, visited):
        if visited[move] == 1: return False
        visited[move] = True

        for adj_move in self.adjacent_moves(move):
            if visited[adj_move] == 1: continue
            if adj_move not in self.states:
                return True
            if self.states[adj_move] == self.states[move]:
                if self.has_vacancy(adj_move, visited):
                    return True
        return False

    def is_movable(self, move, player):
        if move in self.states: return False
        if move >= self.width * self.height: return False
        if move < 0: return False

        # do not lock other player
        other_player = self.get_other_player(player)
        for adj_move in self.adjacent_moves(move):
            if adj_move in self.states and self.states[adj_move] == other_player:
                visited = [0] * (self.width * self.height)
                visited[move] = 1
                if not self.has_vacancy(adj_move, visited):
                    return False

        # do not block current player
        for adj_move in self.adjacent_moves(move):
            if adj_move not in self.states:
                return True

        visited = [0] * (self.width * self.height)
        visited[move] = 1

        for adj_move in self.adjacent_moves(move):
            if adj_move in self.states and self.states[adj_move] == player:
                if self.has_vacancy(adj_move, visited):
                    return True

        return False

    def do_move(self, move):
        self.states[move] = self.current_player
        self.current_player = self.get_other_player(self.current_player)
        self.last_move = move

        for player in self.players:
            if move in self.availables[player]:
                self.availables[player].remove(move)

        for player in self.players:
            trash = []
            for can_move in self.availables[player]:
                if not self.is_movable(can_move, player):
                    trash.append(can_move)

            for can_move in trash:
                self.availables[player].remove(can_move)

    def game_end(self):
        """Check whether the game is ended or not"""
        if len(self.availables[self.current_player]) == 0:
            winner = self.get_other_player(self.current_player)
            return True, winner
        else:
            return False, -1

    def get_current_player(self):
        return self.current_player

    def get_other_player(self, player):
        if player == self.players[1]:
            return self.players[0]
        else:
            return self.players[1]

class Game(object):
    """game server"""

    def __init__(self, board, **kwargs):
        self.board = board

    def graphic(self, board, player1, player2):
        """Draw the board and show game info"""
        width = board.width
        height = board.height

        print("{} with X: availables: {}".format(player1, len(self.board.availables[player1.player])))
        print("{} with O: availables: {}".format(player2, len(self.board.availables[player2.player])))
        print()
        for x in range(width):
            print("{0:8}".format(x), end='')
        print('\r\n')
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                loc = i * width + j
                p = board.states.get(loc, -1)
                if p == player1.player:
                    print('X'.center(8), end='')
                elif p == player2.player:
                    print('O'.center(8), end='')
                else:
                    print('_'.center(8), end='')
            print('\r\n\r\n')

    def start_play(self, player1, player2, start_player=0, is_shown=1):
        """start a game between two players"""
        if start_player not in (0, 1):
            raise Exception('start_player should be either 0 (player1 first) '
                            'or 1 (player2 first)')
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        player1.set_player_ind(p1)
        player2.set_player_ind(p2)
        players = {p1: player1, p2: player2}
        if is_shown:
            self.graphic(self.board, player1, player2)
        while True:
            current_player = self.board.get_current_player()
            player_in_turn = players[current_player]
            move = player_in_turn.get_action(self.board)
            self.board.do_move(move)
            if is_shown:
                self.graphic(self.board, player1, player2)
            end, winner = self.board.game_end()
            if end:
                if is_shown:
                    print("Game end. Winner is", players[winner])
                return winner

    def start_self_play(self, player, temp=1e-3):
        """ start a self-play game using a MCTS player, reuse the search tree,
        and store the self-play data: (state, mcts_probs, z) for training
        """
        self.board.init_board()
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move
            self.board.do_move(move)
            end, winner = self.board.game_end()
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                return winner, zip(states, mcts_probs, winners_z)
