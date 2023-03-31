from search import SearchAlgorithm

class DepthFirstSearchID(SearchAlgorithm):
    def __init__(self,problem):
        super().__init__(problem)
        self.stack = [(0, [self.startState])]
        self.pastCosts[self.startState] = 0
        self.path = []
        self.cost = 0
        self.finished = False
    def stateCost(self, state):
        return self.pastCosts.get(state, None)

    def step(self):
        problem = self.problem
        if self.finished == True:
            return self.path
        if self.stack == []:
            self.cost += 1
            self.stack = [(0, [self.startState])]
        stack = self.stack
        pathCost, path= stack.pop()
        #print(stack)
        lastState = path[-1]
        print(lastState)
        self.numStatesExplored += 1
        if problem.isEnd(lastState):
            self.finished = True
            self.stack = []
            self.path = path
            return path
        for action, newState, cost in problem.successorsAndCosts(lastState):
            if newState not in path:
                if pathCost + cost <= self.cost:
                    temppath = path.copy()
                    temppath.append(newState)
                    self.stack.append((pathCost+cost, temppath))
                    print(self.stack)
                    self.pastCosts[newState] = self.pastCosts[lastState]+cost
        #print(self.stack)
        return path