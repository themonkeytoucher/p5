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
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
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
        actions_taken = [] #closedSet

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        available_actions = [state] #openSet

        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, came_from will eventually contain the
        # most efficient previous step.
        came_from = {}
        came_from[state] = None

        # For each node, the cost of getting from the start node to that node.
        # {current node: cost}
        start_to_current_cost = {}

        # The cost of going from start to start is zero.
        start_to_current_cost[state] = 0

        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        # {current node: cost}
        start_to_goal_cost = {}

        # For the first node, that value is completely heuristic.
        start_to_goal_cost[state] = heuristic(state)
        while available_actions:
            print("***TESTING [a_star] ************************ THIS IS A NEW ITERATION *********************************")
            min_action_list = start_to_goal_cost.items() #turns it into [(key, value), (key2, value2)]
            #print("***TESTING [a_star] what is start_to_goal_cost? " + str(start_to_goal_cost))
            #print("***TESTING [a_star] what is min_action_list? " + str(min_action_list))
            current = min(min_action_list, key = lambda p: p[1]) #the node in available_actions having the lowest start_to_goal_cost value
            
            # print("***TESTING [a_star] what is start_to_goal_cost? " + str(start_to_goal_cost))
            print("***TESTING [a_star] what is available_actions? " + str(available_actions))
            print("***TESTING [a_star] what is current? " + str(current))
            print("***TESTING [a_star] what is state? " + str(state)) 
            print("***TESTING [a_star] state == current? " + str(state == current[0])) #current has a cost associated to it from the item() in min_action_list
            print("***TESTING [a_star] is current in available_actions? " + str(current[0] in available_actions)) 

            #if it reaches the goal, end
            if is_goal(current):
                return [(state, actions_taken)]

            available_actions.remove(current[0]) #current is [(state, cost)]
            actions_taken.append(current[0])

            #evalation of the next possible actions
            list_of_possible_actions = graph(current)
            for new_action in list_of_possible_actions:
                print("***TESTING [a_star] what is new_action? " + str(new_action))
                if new_action in actions_taken:
                    continue    #Ignore the neighbor which is already evaluated.

                # The distance from start to a neighbor
                tentative_start_to_current_cost = start_to_current_cost[current] + 1 #dist_between(current, neighbor)

                #if we should consider this action
                if new_action not in available_actions:  # Discover a new node
                    print("***TESTING [a_star] THIS SHOULD NOT BE WORKING")
                    available_actions.append(new_action)
                elif tentative_start_to_current_cost >= start_to_current_cost[new_action]:
                    continue        # This is not a better path.

                # This path is the best until now. Record it!
                came_from[new_action] = current
                start_to_current_cost[new_action] = tentative_start_to_current_cost
                start_to_goal_cost[new_action] = start_to_current_cost[new_action] + heuristic(state)


    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    # make A* here
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
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
