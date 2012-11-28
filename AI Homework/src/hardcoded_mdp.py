# hardcoded_mdp.py
# ----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
Provide a way to hardcode an MDP for use via gridworld.py via a class named T.
The EXAMPLE_MDP constant below illustrates how to use T.

"""

import random
import sys
import mdp
import environment
import util
import optparse

class T(object):
    """
    T represents an MDP transition from state s1 via action a to state s2,
    with the given probability, resulting in the given reward.
    """

    def __init__(self, s1, a, s2, probability, reward=0):
        self.s1 = s1
        self.a = a
        self.s2 = s2
        self.probability = probability
        self.reward = reward

class HardcodedMDP(mdp.MarkovDecisionProcess):
    """
      Hardcoded MDP, e.g. for testing.
    """
    def __init__(self, startstate, transitions):
        # transitions is a hard-coded list of T objects
        self.startstate = startstate
        self.transitions = transitions

    def getPossibleActions(self, state):
        """
        Returns list of valid actions for 'state'.
        """
        actions = [t.a for t in self.transitions if t.s1 == state]
        return list(set(actions))

    def getStates(self):
        """
        Return list of all states.
        """
        states = [t.s1 for t in self.transitions]
        return list(set(states))

    def getReward(self, state, action, nextState):
        """
        Get reward for state, action, nextState transition.

        Note that the reward depends only on the state being
        departed (as in the R+N book examples, which more or
        less use this convention).
        """
        matches = [t for t in self.transitions if t.s1 == state and t.a == action and t.s2 == nextState]
        if len(matches) == 1:
            return matches[0].reward
        else:
            raise "no such transition!"

    def getStartState(self):
        return self.startstate

    def isTerminal(self, state):
        """
        Hmm - is this important for Hardcoded MDPs?

        Only the TERMINAL_STATE state is *actually* a terminal state.
        The other "exit" states are technically non-terminals with
        a single action "exit" which leads to the true terminal state.
        This convention is to make the grids line up with the examples
        in the R+N textbook.
        """
        return [] == [t.s1 for t in self.transitions if t.s1 == state]


    def getTransitionStatesAndProbs(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.
        """

        matches = [(t.s2, t.probability) for t in self.transitions if t.s1 == state and t.a == action]

        return matches

class HardcodedEnvironment(environment.Environment):

    def __init__(self, mdp):
        self.mdp = mdp
        self.reset()

    def getCurrentState(self):
        return self.state

    def getPossibleActions(self, state):
        return self.mdp.getPossibleActions(state)

    def doAction(self, action):
        successors = self.mdp.getTransitionStatesAndProbs(self.state, action)
        sum = 0.0
        rand = random.random()
        state = self.getCurrentState()
        for nextState, prob in successors:
            sum += prob
            if sum > 1.0:
                raise 'Total transition probability more than one; sample failure.'
            if rand < sum:
                reward = self.mdp.getReward(state, action, nextState)
                self.state = nextState
                return (nextState, reward)
        raise 'Total transition probability less than one; sample failure.'

    def reset(self):
        self.state = self.mdp.getStartState()

EXAMPLE_MDP = [
  T("R", "dump", "lose", 0.5),
  T("R", "dump", "win", 0.5, reward = 1.0),
  T("R", "setup", "lose", 0.25),
  T("R", "setup", "setup", 0.75),
  T("setup", "spike", "lose", 0.5),
  T("setup", "spike", "win", 0.5, reward = 1.0),
  T("setup", "dump", "win", 1.0/3, reward = 1.0),
  T("setup", "dump", "R", 2.0/3, reward=0.0)
]
