from search import SearchAlgorithm

class Backtracking(SearchAlgorithm):
    def __init__(self, problem):
        super().__init__(problem)     
        self.path = []   
        self.backrefs = {}
        # Se crea un diccionario para almacenar los nodos visitados y sus respectivos predecesores.

    def stateCost(self, state):
        return self.pastCosts.get(state, None)
        # Devuelve el costo acumulado de un estado si este ha sido visitado previamente, de lo contrario devuelve None.

        
    def path(self, state):
        path = []
        while state != self.problem.startState():
            _, prevState = self.backrefs[state]
            path.append(state)
            state = prevState
        return path

    def step(self):
        problem = self.problem
        startState = self.startState        
        path = self.path
        pastCosts = self.pastCosts
        backrefs = self.backrefs

        if self.actions:
            return self.path(problem.endState())
            # Si ya se encontró la solución, se devuelve el camino desde el estado inicial hasta el estado final.
       
        if not path:
            path.append(startState)

        state = path[-1]
        if problem.isEnd(state):
            self.actions = []
            while state == startState:
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

        if len(path) != 0:
            path.pop()
        return path