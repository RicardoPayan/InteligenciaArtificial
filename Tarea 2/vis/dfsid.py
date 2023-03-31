from search import SearchAlgorithm

class DepthFirstSearchID(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.path = []
        self.cost = 0
        self.finished = False

    def stateCost(self, state):
        return self.pastCosts.get(state, float("inf"))

    def step(self):
        problem = self.problem
        if self.finished:
            return self.path
        stack = [(self.startState, 0, [self.startState])]
        self.pastCosts = {self.startState: 0}
        while stack:
            lastState, pathCost, path = stack.pop()
            self.numStatesExplored += 1
            if problem.isEnd(lastState):
                self.finished = True
                self.path = path
                return path
            if pathCost <= self.cost:
                for action, newState, cost in problem.successorsAndCosts(lastState):
                    newCost = self.pastCosts[lastState] + cost
                    if newCost < self.stateCost(newState):
                        self.pastCosts[newState] = newCost
                        newPath = path + [newState]
                        newStackItem = (newState, newCost, newPath)
                        stack.append(newStackItem)
        self.cost += 1
        return self.path
