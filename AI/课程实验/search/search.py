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
#

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import grading
#import imp
import optparse
import os
import re
import sys
import projectParams
import random
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

    #返回（可达节点，动作，代价）
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

def depthFirstSearch(problem: SearchProblem):
    #DFS用栈实现
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    action = []
    #state栈保存状态
    statestack = util.Stack()
    #action栈保存state栈对应节点的动作
    actionstack = util.Stack()
    statestack.push(state)
    actionstack.push(action)
    visitedState = []
    #若达到目标节点或栈清空则退出循环
    while not (problem.isGoalState(state) or statestack.isEmpty()):
        visitedState.append(state)
        nearbyState = problem.getSuccessors(state)
        for n_state in nearbyState:
            if n_state[0] not in visitedState:
                statestack.push(n_state[0])
                actionstack.push(action+[n_state[1]])
        state = statestack.pop()
        action = actionstack.pop()
    return action
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    state = problem.getStartState()
    action = []
    #与DFS不同之处只有队列
    statequeue = util.Queue()
    actionqueue = util.Queue()
    statequeue.push(state)
    actionqueue.push(action)
    visitedState = []
    # while not (problem.isGoalState(state) or statequeue.isEmpty()):
    # 检查重复遍历节点方式和DFS有差距，因为是队列，所以节点和子节点都要检查重复
    # 因为DFS是栈，每次新节点插入到栈顶，只用检查一次重复
    while not statequeue.isEmpty():
        state = statequeue.pop()
        action = actionqueue.pop()
        if problem.isGoalState(state):
            return action
        #检查节点是否重复
        if state not in visitedState:
            visitedState.append(state)
            successors = problem.getSuccessors(state)
            for n_state in successors:
                #检查子节点是否重复
                if n_state[0] not in visitedState:
                    statequeue.push(n_state[0])
                    actionqueue.push(action + [n_state[1]])
    return action
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #与bfs基本相同
    state = problem.getStartState()
    action = []
    statepQueue = util.PriorityQueue()
    actionpQueue = util.PriorityQueue()
    statepQueue.push(state,0)
    actionpQueue.push(action,0)
    visitedState = []
    while not statepQueue.isEmpty():
        state = statepQueue.pop()
        action = actionpQueue.pop()
        if problem.isGoalState(state):
            return action
        if state not in visitedState:
            visitedState.append(state)
            successors = problem.getSuccessors(state)
            for n_state in successors:
                if n_state[0] not in visitedState:
                    statepQueue.push(n_state[0], problem.getCostOfActions(action+[n_state[1]]))
                    actionpQueue.push(action + [n_state[1]], problem.getCostOfActions(action+[n_state[1]]))
    return action
    util.raiseNotDefined()

#启发函数，具体在searchAgents.py里实现，计算曼哈顿启发函数
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #priorityQueue类似于最小顶heap
    #与ucs类似，不同在于cost用 cost(action) + heuristic(state)代替
    state = problem.getStartState()
    action = []
    statepQueue = util.PriorityQueue()
    actionpQueue = util.PriorityQueue()
    statepQueue.push(state, heuristic(state,problem))
    actionpQueue.push(action, heuristic(state,problem))
    visitedState = []
    while not statepQueue.isEmpty():
        #选择代价最小的节点进行扩展
        state = statepQueue.pop()
        action = actionpQueue.pop()
        if problem.isGoalState(state):
            return action
        if state not in visitedState:
            visitedState.append(state)
            successors = problem.getSuccessors(state)
            for n_state in successors:
                if n_state[0] not in visitedState:
                    #计算astar的代价
                    cost = problem.getCostOfActions(action + [n_state[1]]) + heuristic(n_state[0],problem)
                    statepQueue.push(n_state[0], cost)
                    actionpQueue.push(action + [n_state[1]], cost)
    return action
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
