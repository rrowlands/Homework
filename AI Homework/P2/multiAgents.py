# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util, sys


from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()
        """
        
        oldFood = currentGameState.getFood()
        oldCapsules = currentGameState.getCapsules()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        oldPos = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        newFoodGrid = successorGameState.getFood()
        
        moveValue = 0
        
        # Randomness to stop us from getting stuck
        isRandom = random.randint(0, 100)
        
        if isRandom > 92:
            moveValue = moveValue + random.randint(-5000, 5000)
        
        
        # Run away from ghosts
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0 and manhattanDistance(newPos, ghost.getPosition()) <= 1:
                moveValue = -10000000000000
        
        # Don't move into a wall
        if newPos == oldPos:
            moveValue = moveValue + -1000000
        
        # This move eats food. Do it.
        if oldFood[newPos[0]][newPos[1]]:
            moveValue = moveValue + 1000
        for capsule in oldCapsules:
            if capsule == newPos:
                moveValue = moveValue + 1000
        for ghost in newGhostStates:
            if ghost.scaredTimer != 0 and ghost.getPosition() == newPos:
                moveValue = moveValue + 2000
                
        # Eat dat food
        closestFood = 1000.0
        for foodPos in newFoodGrid.asList():
            closestFood = float(min(manhattanDistance(newPos, foodPos), closestFood))
        
        moveValue = moveValue + 1.0 / closestFood
        
        # Dem Capsules
        closestFood = 1000.0
        capsules = successorGameState.getCapsules()
        for capPos in capsules:
            closestFood = float(min(manhattanDistance(newPos, capPos), closestFood) - 1.1)
        
        moveValue = moveValue + 1.0 / closestFood
        
        # Dem Skurrd Ghostz
        closestFood = 1000.0
        isEatableGhost = 0
        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())
            if ghost.scaredTimer > dist:
                closestFood = float(dist) / 2000.0
                isEatableGhost = 1
        
        if isEatableGhost == 1:
            moveValue = moveValue + 1.0 / closestFood

        return moveValue

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          Directions.STOP:
            The stop direction, which is always legal

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        legalActions = gameState.getLegalActions(0)
        
        self.debugOut = ""
        
        maxScore = None
        retAction = None
        for action in legalActions:
            if action != "Stop":
                value = self.recursiveGetValue(gameState.generateSuccessor(0, action), self.depth, 0)
                
#                print "agent = 0; action = " + action + "; value = " + str(value)
#                print self.debugOut
#                self.debugOut = ""
                
                if maxScore == None or value >= maxScore:
                    maxScore = value
                    retAction = action
        
        return retAction
            
    
    def recursiveGetValue(self, gameState, depthNum, agent):
        numAgents = gameState.getNumAgents()
        agent = agent + 1
        if agent == numAgents:
            agent = 0
            depthNum = depthNum - 1
        
        legalActions = gameState.getLegalActions(agent)
        
        minMaxScore = None
        
        for action in legalActions:
            if action != "Stop":
                if depthNum == 1 and agent == numAgents - 1:
                    if agent == 0:
                        if minMaxScore == None:
                            minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                        else:
                            minMaxScore = max(self.evaluationFunction(gameState.generateSuccessor(agent, action)), minMaxScore)
                    else:
                        if minMaxScore == None:
                            minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                        else:
                            minMaxScore = min(self.evaluationFunction(gameState.generateSuccessor(agent, action)), minMaxScore)
                else:
                    if agent == 0:
                        if minMaxScore == None:
                            minMaxScore = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                        else:
                            minMaxScore = max(self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent), minMaxScore)
                    else:
                        if minMaxScore == None:
                            minMaxScore = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                        else:
                            minMaxScore = min(self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent), minMaxScore)
                
#                tabs = "  " * (self.depth - depthNum + 1)
#                self.debugOut = tabs + "agent = " + str(agent) + "; action = " + str(action) + "; value = " + str(minMaxScore) + "\n" + self.debugOut
        
        if minMaxScore == None:
            value = self.evaluationFunction(gameState)
#            tabs = "  " * (self.depth - depthNum + 1)
#            self.debugOut = tabs + "agent = " + str(agent) + "; No legal Moves\n" + self.debugOut
            return value
        
        return minMaxScore


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        
        legalActions = gameState.getLegalActions(0)
        
        self.debugOut = ""
        
        maxScore = None
        retAction = None
        for action in legalActions:
            if action != "Stop":
                value = self.recursiveGetValue(gameState.generateSuccessor(0, action), self.depth, 0)
                
#                print "agent = 0; action = " + action + "; value = " + str(value)
#                print self.debugOut
#                self.debugOut = ""
                
                if maxScore == None or value >= maxScore:
                    maxScore = value
                    retAction = action
        
        return retAction
            
    
    def recursiveGetValue(self, gameState, depthNum, agent):
        numAgents = gameState.getNumAgents()
        agent = agent + 1
        if agent == numAgents:
            agent = 0
            depthNum = depthNum - 1
        
        legalActions = gameState.getLegalActions(agent)
        
        minMaxScore = None
        
        for action in legalActions:
            if action != "Stop":
                if depthNum == 1 and agent == numAgents - 1:
                    if agent == 0:
                        if minMaxScore == None:
                            minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                        else:
                            minMaxScore = max(self.evaluationFunction(gameState.generateSuccessor(agent, action)), minMaxScore)
                    else:
                        if minMaxScore == None:
                            minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                        else:
                            minMaxScore = min(self.evaluationFunction(gameState.generateSuccessor(agent, action)), minMaxScore)
                else:
                    if agent == 0:
                        if minMaxScore == None:
                            minMaxScore = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                        else:
                            minMaxScore = max(self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent), minMaxScore)
                    else:
                        if minMaxScore == None:
                            minMaxScore = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                        else:
                            minMaxScore = min(self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent), minMaxScore)
                
#                tabs = "  " * (self.depth - depthNum + 1)
#                self.debugOut = tabs + "agent = " + str(agent) + "; action = " + str(action) + "; value = " + str(minMaxScore) + "\n" + self.debugOut
        
        if minMaxScore == None:
            value = self.evaluationFunction(gameState)
#            tabs = "  " * (self.depth - depthNum + 1)
#            self.debugOut = tabs + "agent = " + str(agent) + "; No legal Moves\n" + self.debugOut
            return value
        
        return minMaxScore

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        
        legalActions = gameState.getLegalActions(0)
        
        self.debugOut = ""
        
        maxScore = None
        retAction = None
        for action in legalActions:
            if action != "Stop":
                value = self.recursiveGetValue(gameState.generateSuccessor(0, action), self.depth, 0)
                
#                print "agent = 0; action = " + action + "; value = " + str(value)
#                print self.debugOut
#                self.debugOut = ""
                
                if maxScore == None or value >= maxScore:
                    maxScore = value
                    retAction = action
        
        return retAction
            
    
    def recursiveGetValue(self, gameState, depthNum, agent):
        numAgents = gameState.getNumAgents()
        agent = agent + 1
        if agent == numAgents:
            agent = 0
            depthNum = depthNum - 1
        
        legalActions = gameState.getLegalActions(agent)
        
        if "Stop" in legalActions:
            legalActions.remove("Stop")
        
        minMaxScore = None
        
        for action in legalActions:
            if depthNum == 1 and agent == numAgents - 1:
                if agent == 0:
                    if minMaxScore == None:
                        minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                    else:
                        minMaxScore = max(self.evaluationFunction(gameState.generateSuccessor(agent, action)), minMaxScore)
                else:
                    if minMaxScore == None:
                        minMaxScore = self.evaluationFunction(gameState.generateSuccessor(agent, action))
                    else:
                        minMaxScore = minMaxScore + self.evaluationFunction(gameState.generateSuccessor(agent, action))
            else:
                if agent == 0:
                    if minMaxScore == None:
                        minMaxScore = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                    else:
                        minMaxScore = max(self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent), minMaxScore)
                else:
                    value = self.recursiveGetValue(gameState.generateSuccessor(agent, action), depthNum, agent)
                    
                    if minMaxScore == None:
                        minMaxScore = 0
                    
                    minMaxScore = minMaxScore + value
            
#                tabs = "  " * (self.depth - depthNum + 1)
#                self.debugOut = tabs + "agent = " + str(agent) + "; action = " + str(action) + "; value = " + str(minMaxScore) + "\n" + self.debugOut
        
        if minMaxScore == None:
            value = self.evaluationFunction(gameState)
#            tabs = "  " * (self.depth - depthNum + 1)
#            self.debugOut = tabs + "agent = " + str(agent) + "; No legal Moves" + "; value = " + str(value) + "\n" + self.debugOut
            
            return value
        
        if agent != 0 and len(legalActions) != 1:
            minMaxScore = float(minMaxScore) / float(len(legalActions))
        
        return minMaxScore

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Ran from ghosts and ate food.
    """
    food = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    pos = currentGameState.getPacmanPosition()
    ghosts = currentGameState.getGhostStates()
    
    moveValue = currentGameState.getScore()
    
    # There is a ghost at this location.
    for ghost in ghosts:
        if ghost.scaredTimer == 0 and pos == ghost.getPosition():
            moveValue = moveValue + -10000000000000
    
    # Add value based on the distances to food
    for fPos in food:
        moveValue = moveValue + 6.0 / float(manhattanDistance(fPos, pos))
    
    # Add value for capsules
#    for capsule in capsules:
#        moveValue = moveValue + 10.0 / float(manhattanDistance(capsule, pos))
#        
#    # Dem Capsules
#    closestFood = 1000.0
#    for capPos in capsules:
#        closestFood = float(min(manhattanDistance(pos, capPos), closestFood) - 1.1)
#    
#    moveValue = moveValue + 1.0 / closestFood
    
    return moveValue

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

