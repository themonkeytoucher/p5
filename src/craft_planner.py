"""
Last time on Dragonball Z:
Working on the check functino
"""
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
        
        # rule['Requires'] is the object that you need (ex: crafting bench) {obj: bool}
        # rule['Consumes'] are the actual items that will be used (ex: 3 wood) {obj: required #}
        # state is your current inventory
        
        #Checks if the item actually consumes anything
        if 'Consumes' in rule.keys():
            consumes_list = list(rule['Consumes'].keys())
        else:
            consumes_list = []

        #Checks if the item requires anything
        if 'Requires'  in rule.keys():
            requires_list = list(rule['Requires'].keys())
        else:
            requires_list = []

        #{item: quantity}
        curr_inv = state[0]
        
        # Checking if we have the resources to do
        for consume in consumes_list:
            if curr_inv[consume] < rule['Consumes'][consume]: # if we do not have enough materials
                return False

        for require in requires_list:
            if curr_inv[require] < 1: #if we have what we require
                return False
        return True

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
        available_actions = [] #openSet

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
        available_actions.append(start_to_current_cost)
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        # {current node: cost}
        start_to_goal_cost = {}

        # For the first node, that value is completely heuristic.
        start_to_goal_cost[state] = heuristic(state)

        while available_actions:
            print("***TESTING [a_star] ************************ THIS IS A NEW ITERATION *********************************")
            print("********* TESTING ********* [a_star] available_actions is " + str(available_actions))

            #Find the min cost
            min_cost = 999999999999 #some number that will always be bigger
            current = None
            for index in range(len(available_actions)):
                for key in available_actions[index].keys():
                    if available_actions[index][key] < min_cost: #if cost you are looking at 
                        min_cost = available_actions[index][key]
                        current = key

            print("********* TESTING ********* [a_star] current is " + str(current))
            
            #if it reaches the goal, end
            if is_goal(current):
                return [(state, actions_taken)]

            #find where that piece of shit current is
            for index in range(len(available_actions)):
                for key in available_actions[index].keys():
                    if current is key:
                        available_actions.remove(available_actions[index])
            
            #dispose of the body and make sure to clean up the crime scene
            actions_taken.append(current)

            # find our next target
            #creates (name, effect, cost)
            list_of_tentative_actions = graph(current)
            for new_action in list_of_tentative_actions:
                if new_action in actions_taken:
                    continue    #Ignore the neighbor which is already evaluated.

                # The distance from start to a neighbor
                print("********* TESTING ********* [a_star] min_action_list is " + str(min_action_list))
                print("********* TESTING ********* [a_star] current is " + str(current))
                tentative_start_to_current_cost = start_to_current_cost[current] + 1 #dist_between(current, neighbor)

                #if we should consider this action
                if new_action not in available_actions:  # Discover a new node!
                    available_actions.append(new_action) # #soulmates #4ever
                elif tentative_start_to_current_cost >= start_to_current_cost[new_action]:
                    continue        # Ew we can do better than that

                # Record it, you sicko...
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

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

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
