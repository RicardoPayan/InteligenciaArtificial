from mdp import MarkovDecisionProcess


class DiceGame(MarkovDecisionProcess):
    def __init__(self, continueReward=4.0, exitReward=10.0, discount=1.0):
        super().__init__(discount)
        self.continueReward = continueReward
        self.exitReward = exitReward
        self.rules = {
            "play": {
                "continue": {
                    "play": {
                        "prob": 2 / 3,
                        "target": "play",
                        "reward": self.continueReward,
                    },
                    "end": {
                        "prob": 1 / 3,
                        "target": "end",
                        "reward": self.continueReward,
                    },
                },
                "exit": {
                    "end": {
                        "prob": 1,
                        "target": "end",
                        "reward": self.exitReward,
                    },
                },
            },
            "end": {},
        }

    def startState(self):
        return "play"

    def actions(self, state):
        if state == "play":
            return iter(["continue", "exit"])
        return iter([])

    def transitions(self, source, action):
        yield from iter(self.rules.get(source, {}).get(action, {}))

    def probability(self, source, action, target):
        return (
            self.rules.get(source, {})
            .get(action, {})
            .get(target, {"prob": 0.0})["prob"]
        )

    def reward(self, source, action, target):
        return (
            self.rules.get(source, {})
            .get(action, {})
            .get(target, {"reward": 0.0})["reward"]
        )

    def isEnd(self, state):
        return state == "end"
