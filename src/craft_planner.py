import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.
    #print("[make_checker] rule is " + str(rule))
    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        print ("[check] state is " + str(state))
        if state['Consumes'] == rule['Consumes'] and state['Requires'] == rule['Requires']:
            return True
        return False

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = None
        print("[effect] state is " + str(state))
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        if state is goal:
            return True
        return False

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # Implement your heuristic here!
    return 0

"""
Input:  graph = graph()
        state = {item: amount}
        is_goal = make_goal()
        limit = int
        heuristic()
"""
def search(graph, state, is_goal, limit, heuristic):

    start_time = time()
    """
    Input: Finds a path to the goal
    Output: returns [(state, action)]
    """
    def a_star():
        # The set of nodes already evaluated
        seenNodes = []

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        adjNodes = [graph(state)]

        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, cameFrom will eventually contain the
        # most efficient previous step.
        cameFrom = None

        # For each node, the cost of getting from the start node to that node.
        # {current node: cost}
        start_to_current_cost = {}

        # The cost of going from start to start is zero.
        start_to_current_cost[state] = 0

        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        # {current node: cost}
        start_to_goal_cost := {}

        # For the first node, that value is completely heuristic.
        start_to_goal_cost[state] := heuristic(state)

        while adjNodes is not None
            state = the node in openSet having the lowest fScore[] value
            if current = goal
                return reconstruct_path(cameFrom, current)

            openSet.Remove(current)
            closedSet.Add(current)

            for each neighbor of current
                if neighbor in closedSet
                    continue        # Ignore the neighbor which is already evaluated.

                # The distance from start to a neighbor
                tentative_gScore := gScore[current] + dist_between(current, neighbor)

                if neighbor not in openSet  # Discover a new node
                    openSet.Add(neighbor)
                else if tentative_gScore >= gScore[neighbor]
                    continue        # This is not a better path.

                # This path is the best until now. Record it!
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := gScore[neighbor] + heuristic_cost_estimate(neighbor, goal)


    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    # make A* here
    print("[search] is_goal is " + str(graph))
    while time() - start_time < limit:
        return a_star()

    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print('All items:', Crafting['Items'])
    
    # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])
    
    # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])
    
    # Dict of crafting recipes (each is a dict):
    print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    print("[main] Crafting[Initial] is " + str(Crafting['Initial']))
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
