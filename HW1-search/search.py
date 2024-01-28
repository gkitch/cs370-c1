# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    #need to make it not expand on nodes that have already been visited

    frontier = util.Stack() #this is our frontier
    parents = {} #format is state:state except for the children of the start state which is state:coord
    actions = [] #this will be what we return
    visited = [problem.getStartState()] #keep track of states that have already been explored

    #we have started at our goal
    if problem.isGoalState(problem.getStartState()):
        return actions
    
    #get successors of start state and put them into frontier
    toAdd = problem.getSuccessors(problem.getStartState())
    for successor in toAdd:
        frontier.push(successor)
        parents.update({successor:problem.getStartState()})
    
    #take first successor from frontier. This is the direction we will start heading in
    currentState = frontier.pop()
    
    
    while problem.isGoalState(currentState[0]) is not True: #while we are not at the goal state, keep looping
        visited.append(currentState[0]) #add coordinates of current position to visited
        toAdd = problem.getSuccessors(currentState[0]) #get successors of our current position
        for successor in toAdd: 
            if successor[0] not in visited:
                if problem.isGoalState(successor[0]): #if successor of current state hasn't been visited, check if it's the goal state
                    parents.update({successor:currentState}) #update parents
                    currentState = successor #set currentState to the goal so we can start backtracking
                    #backtrack through parents to get a list of actions to return
                    while parents.get(currentState) != problem.getStartState():
                        print(currentState)
                        actions.append(currentState[1])
                        currentState = parents.get(currentState)
                    
                    actions.append(currentState[1])
                    actions.reverse()
                    return actions

                #if successor hasn't been visited and it's not the goal state, push it to the frontier and update parents
                else:
                    frontier.push(successor)
                    parents.update({successor:currentState})
        
        #if frontier is empty, we haven't found a solution, so return none
        if frontier.isEmpty():
            return None

        #update current state to be the next item in stack if it hasn't been visited already
        currentState = frontier.pop()
        while currentState in visited:
            if not frontier.isEmpty():
                currentState = frontier.pop()
            else: #this happens if the frontier contains no states that haven't been visited
                return None
            

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    parents = {}
    actions = []
    visited = [problem.getStartState()]

    if problem.isGoalState(problem.getStartState()):
        return actions

    toAdd = problem.getSuccessors(problem.getStartState())
    for successor in toAdd:
        frontier.push(successor)
        parents.update({successor:problem.getStartState()})
    
    currentState = frontier.pop()

    while problem.isGoalState(currentState[0]) is not True:
        visited.append(currentState[0])
        toAdd = problem.getSuccessors(currentState[0])
        for successor in toAdd:
            if successor[0] not in visited:
                frontier.push(successor)
                parents.update({successor:currentState})
        
        if frontier.isEmpty():
            return None
        else:
            while currentState[0] in visited:
                if not frontier.isEmpty():
                    currentState = frontier.pop()
                else:
                    return None
    
    while currentState != problem.getStartState():
        actions.append(currentState[1])
        currentState = parents.get(currentState)
    
    actions.reverse()
    return actions


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #push coordinates to this
    costs = {} #key is coordinates, val is int
    parents = {} #key is coordinates, val is coordinates
    actionsFromParent = {} #key is coordinates, val is action
    actions = [] #this is list to return

    currentState = problem.getStartState()
    costs.update({problem.getStartState():0})

    while problem.isGoalState(currentState) is not True:
        toAdd = problem.getSuccessors(currentState)
        for successor in toAdd:
            pathCost = successor[2] + costs.get(currentState)
            if successor[0] not in costs.keys(): #this means we haven't reached this node before
                costs.update({successor[0]:pathCost})
                parents.update({successor[0]:currentState}) 
                actionsFromParent.update({successor[0]:successor[1]})
                frontier.update(successor[0], pathCost)
            else:
                if pathCost < costs.get(successor[0]):
                    costs.update({successor[0]:pathCost})
                    parents.update({successor[0]:currentState})
                    actionsFromParent.update({successor[0]:successor[1]})
                    frontier.update(successor[0], pathCost)
        
        if frontier.isEmpty():
            return None
        
        currentState = frontier.pop()
    
    while currentState != problem.getStartState():
        actions.append(actionsFromParent.get(currentState))
        currentState = parents.get(currentState)
    
    actions.reverse()
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue() #push coordinates to this
    costs = {} #key is coordinates, val is int
    parents = {} #key is coordinates, val is coordinates
    actionsFromParent = {} #key is coordinates, val is action
    actions = [] #this is list to return

    currentState = problem.getStartState()
    costs.update({problem.getStartState():0})

    while problem.isGoalState(currentState) is not True:
        toAdd = problem.getSuccessors(currentState)
        for successor in toAdd:
            pathCostWithHeur = successor[2] + costs.get(currentState) + heuristic(successor[0], problem)
            pathCostNoHeur = successor[2] + costs.get(currentState)
            if successor[0] not in costs.keys(): #this means we haven't reached this node before
                costs.update({successor[0]:pathCostNoHeur})
                parents.update({successor[0]:currentState}) 
                actionsFromParent.update({successor[0]:successor[1]})
                frontier.update(successor[0], pathCostWithHeur)
            else:
                if pathCostNoHeur < costs.get(successor[0]):
                    costs.update({successor[0]:pathCostNoHeur})
                    parents.update({successor[0]:currentState})
                    actionsFromParent.update({successor[0]:successor[1]})
                    frontier.update(successor[0], pathCostWithHeur)
        
        if frontier.isEmpty():
            return None
        
        currentState = frontier.pop()
    
    while currentState != problem.getStartState():
        actions.append(actionsFromParent.get(currentState))
        currentState = parents.get(currentState)
    
    actions.reverse()
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch