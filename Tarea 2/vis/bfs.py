from search import SearchAlgorithm

class BreadthFirstSearch(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)
        self.frontier = []
        self.backrefs = {}
        self.frontier.append((self.startState, 0))
    
    def stateCost(self, state):
        return self.pastCosts.get(state, None)
    
    def path(self, state):
        path = []
        while state != self.problem.startState():
            _, prevState = self.backrefs[state]
            path.append(state)
            state = prevState
        #path.reverse()
        return path

    def step(self):
        problem = self.problem
        startState = self.startState
        frontier = self.frontier
        backrefs = self.backrefs

        if self.actions:
            return self.path(problem.endState())
        
        if frontier:
            state, pastCost = frontier.pop(0)
        else:
            state = None
            pastCost = None
        #print(state)
        if state is None and pastCost is None:
            return []
        
        self.pastCosts[state] = pastCost
        self.numStatesExplored += 1
        path = self.path(state)

        if problem.isEnd(state):
            self.actions = []
            while state != startState:
                action, prevState=backrefs[state]
                self.actions.append(action)
                state = prevState
            self.actions.reverse()
            self.pathCost = pastCost
            return path
        for action, newState, cost in problem.successorsAndCosts(state):
            if newState not in self.pastCosts:
                self.frontier.append((newState, cost))
                self.pastCosts[newState] = self.pastCosts[state]+cost
                backrefs[newState]=(action, state)
        return path