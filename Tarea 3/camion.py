from sympy import im
from mdp import MarkovDecisionProcess
from mdp import valueIteration


class MagicBus(MarkovDecisionProcess):
    def __init__(self, blocks, walkCost=1, busCost=1, failProb=0.5, discount=1.0):
        super().__init__(discount)
        self.blocks = blocks
        self.walkReward = -walkCost
        self.busReward = -busCost
        self.failProb = failProb

    def startState(self):
        return 1

    def actions(self, state):
        if state + 1 <= self.blocks:
            yield "walk"
        if 2 * state <= self.blocks:
            yield "bus"

    def transitions(self, source, action):
        if action == "walk":
            yield source + 1
        if action == "bus":
            yield from iter([source, 2 * source])

    def probability(self, source, action, target):
        if action == "bus":
            if source == target:
                return self.failProb
            else:
                return 1 - self.failProb
        return 1.0

    def reward(self, source, action, target):
        if action == "walk":
            return self.walkReward
        if action == "bus":
            return self.busReward

    def isEnd(self, state):
        return state == self.blocks
    
    def states(self):
        return range(1,self.blocks+1)

    def succProbReward(self, state, action):
        if action == "walk":
            return [(state + 1, 1.0, self.walkReward)]
        elif action == "bus":
            return [(state, self.failProb, self.busReward), (2 * state, self.failProb, self.busReward)]
        else:
            return []


mdp = MagicBus(blocks=6, walkCost=1, busCost=2, failProb=0.5, discount=1.0)
valueIteration(mdp)
