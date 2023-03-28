from operator import itemgetter as nth
from random import random
from mdp import targets


def noop(*args):
    return None


def run(mdp, policy, log=print):
    utility = 0.0
    state = mdp.startState()
    k = 0
    while not mdp.isEnd(state):
        action = policy(state)
        accProb = 0.0
        for target, prob, reward in targets(mdp, state, action):
            accProb += prob
            if random() < accProb:
                log(f"At {state} perform {action} to reach {target}")
                state = target
                utility += reward * mdp.discount() ** k
                break
        k += 1
    log(f"Final state {state} reached, returning utility")
    return utility


def experiment(mdp, policy, report, trials=10**4):
    utilities = {}
    average = 0.0
    for _ in range(trials):
        utility = run(mdp, policy, noop)
        average += utility
        utilities[utility] = utilities.get(utility, 0) + 1
    average /= trials
    distribution = {utility: count / trials for utility, count in utilities.items()}
    return report(distribution, average)


def plain_report(distribution, average):
    print("EXPECTED_UTILITY:", average)
    print("DISTRIBUTION:")
    print("| utility | probability |")
    print("|---------+-------------|")
    for utility, probability in sorted(distribution.items(), key=nth(1), reverse=True):
        bar = "#" * int(probability * 40)
        print(f"| {utility:^7.2f} | {probability:^11.5f} |", bar)
