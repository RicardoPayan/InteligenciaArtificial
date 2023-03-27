from search import SearchAlgorithm

class Backtracking(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.path = []
        self.backrefs = {}

    def stateCost(self, state):
        return self.pastCosts.get(state, None)
    
    def step(self):
        problem = self.problem
        startState = self.startState
        path = self.path
        pastCosts = self.pastCosts
        backrefs = self.backrefs
        pastCosts = self.pastCosts
        

        if self.actions:
            return self.path(problem.endState())

        if not path:
            path.append(startState)

        state = path[-1]
        if problem.isEnd(state):
            self.actions = []
            while state != startState:
                action, prevState = backrefs[state]
                self.actions.append(action)
                state = prevState
            self.actions.reverse()
            self.pathCost = pastCosts[state]
            return path

        for action, newState, cost in problem.successorsAndCosts(state):
            if newState not in pastCosts:
                path.append(newState)
                pastCosts[newState] = pastCosts.get(state,0) + cost
                return path

        path.pop()
        return path