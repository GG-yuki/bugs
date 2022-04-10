import Arena
from MCTS import MCTS
from nogo.NogoGame import NogoGame
from nogo.NogoPlayers import *
from nogo.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

human_vs_cpu = False
g = NogoGame(9)


# all players
rp = RandomPlayer(g).play
hp = HumanNogoPlayer(g).play



# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp', 'best11.pth.tar')
n2 = NNet(g)
n2.load_checkpoint('./temp', 'temp.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
args2 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
mcts2 = MCTS(g, n2, args2)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    player2 = rp

arena = Arena.Arena(rp, n2p, g, display=NogoGame.display)

print(arena.playGames(100, verbose=True))
