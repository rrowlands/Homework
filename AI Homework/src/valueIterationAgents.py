# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of value iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.previousValues = util.Counter()
        
        states = mdp.getStates()
        
        for i in range(iterations):
            self.previousValues = self.values
            
            for state in states:
                reward = mdp.getReward(state, None, None)
                if reward != 0:
                    #self.values[state] = reward
                    self.previousValues[state] = reward
                    
                posActions = mdp.getPossibleActions(state)
                
                #DEBUG
                if i == 3 and state == (3,0):
                    print "state = " + str(state) + ""
                
                actionValue = 0
                for action in posActions:
                    # if action = north from (0,0), returns:
                    # list: [((0, 1), 0.80000000000000004), ((1, 0), 0.10000000000000001), ((0, 0), 0.10000000000000001)]
                    transStates = mdp.getTransitionStatesAndProbs(state, action)
                    
                    tempActionValue = 0
                    for trans in transStates:
                        tempActionValue = tempActionValue + self.previousValues[trans[0]] * trans[1] * discount
                        
                    if tempActionValue > actionValue:
                        actionValue = tempActionValue
                        
                if reward != 0:
                    actionValue = reward
                    
                #DEBUG
                if i == 3 and state == (2,0):
                    print "state = " + str(state) + ""
                    
                self.values[state] = actionValue
        

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def getQValue(self, state, action):
        """
          The q-value of the (state, action) pair, based
          on the underlying number (k) of value iteration
          updates, plus a final round of q-value updates which include
          the k+1 reward. Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
        

    def getPolicy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        posActions = self.mdp.getPossibleActions(state)
        
        actionValue = 0
        direction = None
        for action in posActions:
            transStates = self.mdp.getTransitionStatesAndProbs(state, action)
            
            tempActionValue = 0
            for trans in transStates:
                tempActionValue = tempActionValue + self.values[trans[0]] * trans[1] * self.discount
            
            if tempActionValue > actionValue:
                actionValue = tempActionValue
                direction = action
        
        return direction

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.getPolicy(state)
