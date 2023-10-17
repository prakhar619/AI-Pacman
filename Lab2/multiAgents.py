#Vibesh Kumar  
#Prakhar Gupta


# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFood = successorGameState.getFood()
        min_foodDisList = [(abs(newPos[0] - Food[0])+ abs(newPos[1] - Food[1])) for Food in newFood.asList()]
        if(len(min_foodDisList) == 0):
            return 10
        min_foodDis = min(min_foodDisList)
        foodPar = [1 for particle in newFood.asList()]
        no_of_foodPar = sum(foodPar)
        ghost_pos = currentGameState.getGhostPositions()
        min_ghost_DisList = [(abs(newPos[0] - ghost[0])+ abs(newPos[1] - ghost[1])) for ghost in ghost_pos]
        min_ghostDis = min(min_ghost_DisList)

        if(min_ghostDis <= 2):
            return -10000
        eval_function  = -no_of_foodPar**2 + 1.0/ min_foodDis 
        return eval_function

def scoreEvaluationFunction(currentGameState: GameState):
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


    def recursive_search_max(self, gameState, depth):
        pacMan_actionList =gameState.getLegalActions(0)
        maxx = float("-inf")
        for eachAction in pacMan_actionList:
            newState = gameState.generateSuccessor(0,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth-1,1)
            maxx = max(maxx,eachAction_eval)
            if maxx == eachAction_eval:
                action  = eachAction
        return (action,maxx)


    def recursive_search_min(self,gameState,depth,agentNum):
        if((depth == 0 and agentNum >= gameState.getNumAgents()) or gameState.isWin() or gameState.isLose() ):
            return self.evaluationFunction(gameState)
        if(agentNum >= gameState.getNumAgents() and depth != 0):
            return self.recursive_search_max(gameState,depth)[1]
        ghost_actionList = gameState.getLegalActions(agentNum)
        minn = float("inf")
        for eachAction in ghost_actionList:
            newState = gameState.generateSuccessor(agentNum,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth,agentNum+1)
            minn = min(minn,eachAction_eval)
        
        return minn

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        action = self.recursive_search_max(gameState, self.depth)[0]
        return action
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def recursive_search_max(self, gameState, depth, alpha, beta):
        pacMan_actionList =gameState.getLegalActions(0)
        maxx = float("-inf")
        for eachAction in pacMan_actionList:
            newState = gameState.generateSuccessor(0,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth-1,1,alpha,beta)
            maxx = max(maxx,eachAction_eval)
            if maxx == eachAction_eval:
                action  = eachAction
            if( maxx > beta): return (eachAction,maxx)
            alpha = max(alpha,maxx)
        return (action,maxx)


    def recursive_search_min(self,gameState,depth,agentNum, alpha, beta):
        if((depth == 0 and agentNum >= gameState.getNumAgents()) or gameState.isWin() or gameState.isLose() ):
            return self.evaluationFunction(gameState)
        if(agentNum >= gameState.getNumAgents() and depth != 0):
            return self.recursive_search_max(gameState,depth,alpha,beta)[1]
        ghost_actionList = gameState.getLegalActions(agentNum)
        minn = float("inf")
        for eachAction in ghost_actionList:
            newState = gameState.generateSuccessor(agentNum,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth,agentNum+1,alpha,beta)
            minn = min(minn,eachAction_eval)
            if (minn < alpha): return minn
            beta = min(minn,beta)
        return minn

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")
        action = self.recursive_search_max(gameState, self.depth,alpha,beta)[0]
        return action

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def recursive_search_max(self, gameState, depth):
        pacMan_actionList =gameState.getLegalActions(0)
        maxx = float("-inf")
        for eachAction in pacMan_actionList:
            newState = gameState.generateSuccessor(0,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth-1,1)
            maxx = max(maxx,eachAction_eval)
            if maxx == eachAction_eval:
                action  = eachAction
        return (action,maxx)


    def recursive_search_min(self,gameState,depth,agentNum):
        if((depth == 0 and agentNum >= gameState.getNumAgents()) or gameState.isWin() or gameState.isLose() ):
            return self.evaluationFunction(gameState)
        if(agentNum >= gameState.getNumAgents() and depth != 0):
            return self.recursive_search_max(gameState,depth)[1]
        ghost_actionList = gameState.getLegalActions(agentNum)
        expectation_val = 0
        for eachAction in ghost_actionList:
            newState = gameState.generateSuccessor(agentNum,eachAction)
            eachAction_eval = self.recursive_search_min(newState,depth,agentNum+1)
            expectation_val += eachAction_eval/len(ghost_actionList)
        return expectation_val
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        action = self.recursive_search_max(gameState, self.depth)[0]
        return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    newFood = successorGameState.getFood()
    min_foodDisList = [(abs(newPos[0] - Food[0])+ abs(newPos[1] - Food[1])) for Food in newFood.asList()]
    if(len(min_foodDisList) == 0):
        return 10
    min_foodDis = min(min_foodDisList)
    foodPar = [1 for particle in newFood.asList()]
    no_of_foodPar = sum(foodPar)
    ghost_pos = currentGameState.getGhostPositions()
    min_ghost_DisList = [(abs(newPos[0] - ghost[0])+ abs(newPos[1] - ghost[1])) for ghost in ghost_pos]
    min_ghostDis = min(min_ghost_DisList)
    if(min_ghostDis <= 2 and newScaredTimes[0] == 0):
        return -10000
    eval_function  = -no_of_foodPar**2 + 1.0/ min_foodDis 
    return eval_function

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
