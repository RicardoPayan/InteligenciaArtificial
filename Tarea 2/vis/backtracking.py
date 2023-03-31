from search import SearchAlgorithm

class Backtracking(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.stack = [(0,[self.startState])]
        self.bestPath = (float("inf"), [])
        self.pastCosts[self.startState] = 0

    def stateCost(self, state):
        return self.pastCosts.get(state, None)

    def step(self):
        problem = self.problem
        stack = self.stack
        if stack == []:
            return self.bestPath[1]
        pathCost, path= stack.pop()
        lastState = path[-1]
        self.numStatesExplored += 1
        if problem.isEnd(lastState):
            bestCost, _ = self.bestPath
            if pathCost<bestCost:
                self.bestPath = (pathCost, path)
            return path
        for action, newState, cost in problem.successorsAndCosts(lastState):
            if newState not in path:
                temppath = path.copy()
                temppath.append(newState)
                self.stack.append((pathCost+cost, temppath))
                self.pastCosts[newState] = self.pastCosts[lastState]+cost
        #print(self.stack)
        return path