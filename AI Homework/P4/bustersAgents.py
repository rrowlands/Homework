# bustersAgents.py
# ----------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference

class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None ):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules: inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        for index, inf in enumerate(self.inferenceModules):
            if not self.firstMove: inf.elapseTime(gameState)
            self.firstMove = False
            inf.observeState(gameState)
            self.ghostBeliefs[index] = inf.getBeliefDistribution()
        self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "ExactInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that
        has not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (in maze distance!).

        To find the maze distance between any two positions, use:
        self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
        successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief distributions
        for each of the ghosts that are still alive.  It is defined based
        on (these are implementation details about which you need not be
        concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.

        You may remove Directions.STOP from the list of available actions.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions() if a != Directions.STOP]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = [beliefs for i,beliefs
                                            in enumerate(self.ghostBeliefs)
                                            if livingGhosts[i+1]]
        "*** YOUR CODE HERE ***"
        
        """
        for x in range(0, 100):
            try :
                tempDist = self.distancer.getDistance(pacmanPosition, (x, 1))
            except Exception:
                print "Exception occurred at x = " + str(x)
        
        for y in range(0, 100):
            try :
                tempDist = self.distancer.getDistance(pacmanPosition, (3, y))
            except Exception:
                print "Exception occurred at y = " + str(y)
        """
        
        ghostLocs = util.Counter()
        for agent in range(0, len(livingGhostPositionDistributions)):
            #xcomList = [(0, 10000), (10, 5), (-20, 5)]
            xcomList = [(pos[0], prob) for pos, prob in livingGhostPositionDistributions[agent].iteritems()]
            ycomList = [(pos[1], prob) for pos, prob in livingGhostPositionDistributions[agent].iteritems()]
            
            ghostLocs[agent] = self.clampOntoBoard( ( self.centerOfMass(xcomList), self.centerOfMass(ycomList) ), pacmanPosition )
        
        ghostDist = 999999999999
        closestAgent = 0
        for agent in range(0, len(livingGhostPositionDistributions)):
            
            tempDist = 99999999999
            try :
                tempDist = self.distancer.getDistance(pacmanPosition, ghostLocs[agent])
            except Exception:
                print "Exception, not on board: " + str(pacmanPosition) + ", " + str(ghostLocs[agent])
            
            if (ghostDist >= tempDist):
                ghostDist = tempDist
                closestAgent = agent
        
        bestDist = 999999999999
        bestAct = legal[0]
        for action in legal:
            tempDist = 999999999
            if ghostLocs[closestAgent] == (0, 0):
                pass
            else:
                tempDist = self.distancer.getDistance(ghostLocs[closestAgent], self.castTuple(Actions.getSuccessor(pacmanPosition, action)))
            
            if tempDist < bestDist:
                bestDist = tempDist
                bestAct = action
        
        return bestAct
        
    
    # The input should be a tuple of (position, mass)
    def centerOfMass(self, list):
        
        sumOfProbs = 0
        sumOfProbsXPos = 0
        
        debugStr = ""
        for pos, prob in list:
            debugStr = debugStr + "(" + str(pos) + ", " + str(prob) + ")"
            sumOfProbs = sumOfProbs + prob
            sumOfProbsXPos = sumOfProbsXPos + (pos * prob)
        
        if sumOfProbs == 0:
            return 0
        
        ret = int(round(sumOfProbsXPos / sumOfProbs))
        
        return ret
    
    def castTuple(self, tuple):
        x = tuple[0]
        y = tuple[1]
        
        return (int(x), int(y))
    
    # If the center of mass equation returns a point that is off the board, this equation will move it onto the board
    def clampOntoBoard(self, point, pacmanPos):
        
        # clamp the X
        for delta in range(0, 10):
            try :
                self.distancer.getDistance(pacmanPos, (point[0] - delta, point[1]))
                return (point[0] - delta, point[1])
            except Exception:
                pass
            
            try :
                self.distancer.getDistance(pacmanPos, (point[0] + delta, point[1]))
                return (point[0] + delta, point[1])
            except Exception:
                pass
            
            try :
                self.distancer.getDistance(pacmanPos, (point[0], point[1] + delta))
                return (point[0], point[1] + delta)
            except Exception:
                pass
            
            try :
                self.distancer.getDistance(pacmanPos, (point[0], point[1] - delta))
                return (point[0], point[1] - delta)
            except Exception:
                pass
            
            delta = delta + 1
        
        print "Unable to find a clamp for pos " + str(point)
        
        return (0, 0)
            