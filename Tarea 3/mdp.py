class MarkovDecisionProcess:
    def __init__(self, discount):
        self.discountFactor = discount

    def startState(self):
        """
        Returns a valid initial state.
        """
        raise NotImplementedError("Method should be overriden")

    def actions(self, state):
        """
        Yields actions that can be performed on the given state.
        """
        raise NotImplementedError("Method should be overriden")

    def transitions(self, source, action):
        """
        Yields all target states reachable from the source state by
        performing the given action.
        """
        raise NotImplementedError("Method should be overriden")

    def probability(self, source, action, target):
        """
        Returns the probability of reaching the target state from the
        source state by performing the given action.
        """
        raise NotImplementedError("Method should be overriden")

    def reward(self, source, action, target):
        """
        Returns the reward for reaching the target state from the
        source state by performing the given action.
        """
        raise NotImplementedError("Method should be overriden")

    def isEnd(self, state):
        """
        Predicate for end states.
        """
        raise NotImplementedError("Method should be overriden")

    def discount(self):
        """
        Returns the discount factor between 0 and 1 inclusive.
        """
        return self.discountFactor


def targets(mdp, source, action):
    """
    Yields all triplets (target, prob, reward) where:
    - target is the next state
    - prob is the probability of reaching target
    - reward is the reward for reaching target
    """
    for target in mdp.transitions(source, action):
        prob = mdp.probability(source, action, target)
        reward = mdp.reward(source, action, target)
        yield (target, prob, reward)

def valueIteration(mdp):
    V = {}
    for state in mdp.states():
        V[state] = 0
    def Q(state, action):
        return sum(prob * (reward + mdp.discount() * V[target])
                   for target, prob, reward in mdp.succProbReward(state, action))
    while True:
        Vnew = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                Vnew[state] = 0
            else:
                Vnew[state] = max(Q(state, action) for action in mdp.actions(state))
        if max(abs(Vnew[state] - V[state]) for state in mdp.states()) < 0.0001:
            break
        V = Vnew  

        pi = {}
        for state in mdp.states():
            if mdp.isEnd(state):
                pi[state] = None
            else:
                pi[state] = max(mdp.actions(state), key=lambda action: Q(state, action))

        for state in mdp.states():
            print(state, V[state], pi[state])
        input("Press Enter to continue...") 
