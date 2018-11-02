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
    #Implement a function that returns a function to determine whether a state meets a
    #rule's requirements. This code runs once, when the rules are constructed before
    #the search is attempted.
    #print("[make_checker] rule is " + str(rule))
    def check(state):
        #This code is called by graph(state) and runs millions of times.
        #Tip: Do something with rule['Consumes'] and rule['Requires'].
        
        #rule['Requires'] is the object that you need (ex: crafting bench) {obj: bool}
        #rule['Consumes'] are the actual items that will be used (ex: 3 wood) {obj: required #}
        #state is your current inventory
        
        consumes_list = []
        requires_list = []
        #Checks if the item actually consumes anything
        if 'Consumes' in rule.keys():
            consumes_list = list(rule['Consumes'].keys())

        #Checks if the item requires anything
        if 'Requires'  in rule.keys():
            requires_list = list(rule['Requires'].keys())

        #{item: quantity}
        curr_inv = state
        
        #Checking if we have the resources to do
        for consume in consumes_list:
            if curr_inv[consume] < rule['Consumes'][consume]: #if we do not have enough materials
                return False

        for require in requires_list:
            if curr_inv[require] < 1: #if we have what we require
                return False
        return True

    return check


def make_effector(rule):
    #Implement a function that returns a function which transitions from state to
    #new_state given the rule. This code runs once, when the rules are constructed
    #before the search is attempted.

    def effect(state):
        #This code is called by graph(state) and runs millions of times
        #Tip: Do something with rule['Produces'] and rule['Consumes'].

        #list of keys for the rule[produces] and rule[consumes]
        consumes_list = []
        produce_list = []

        #check if they actually need to consume anything or produces anything
        if 'Consumes' in rule.keys():
            consumes_list = list(rule['Consumes'].keys())

        if 'Produces' in rule.keys():
            produce_list = list(rule['Produces'].keys())

        #sets the next state as the current state so we can work with it
        next_state = state 

        #for each of the resources, add to inv if we are producing it and take away if we are consuming it
        #doesn't run if we don't consume or produce anything since they would stay as empty lists thus the loop doesn't run
        for resources in produce_list:
            next_state[resources] += rule['Produces'][resources] #adds the stuff produced into inventory

        for consume in consumes_list:
            next_state[consume] -= rule['Consumes'][consume]
        return next_state

    return effect


def make_goal_checker(goal):
    #Implement a function that returns a function which checks if the state has
    #met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        #This code is used in the search process and may be called millions of times.
        if goal in state:
            return True
        return False

    return is_goal


def graph(state):
    #Iterates through all recipes/rules, checking which are valid in the given state.
    #If a rule is valid, it returns the rule's name, the resulting state after application
    #to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

"""
Input: current inventory
Output: A score for the best path
Prunes available actions by:
 1. Setting making tools you already have to very high numbers
 2. 
"""
def heuristic(state):
    #Implement your heuristic here!
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
    Output: returns [(state, action), (state, action), ...]
    """
    def a_star():
        curr_inv = state
        #The set of nodes already evaluated
        actions_taken = [] #closedSet

        #The set of currently discovered nodes that are not evaluated yet.
        #Initially, only the start node is known.
        starting_actions = graph(curr_inv)
        available_actions =  []
        
        #list that we will be returning. [(state, action), (state, action), ...]
        return_list = []

        #For each node, the cost of getting from the start node to that node.
        #{current node: cost}
        start_to_current_cost = {}
        
        #For each node, the total cost of getting from the start node to the goal
        #by passing by that node. That value is partly known, partly heuristic.
        #{current node: cost}
        heuristic_cost = {}

        #keeping track of costs and length
        item_cost = 0
        len_cost = 0
        
        #loop through the action and add
        for actions in starting_actions:
            
            #putting possible actions into the list
            available_actions.append(actions)
            
            #heuristics plus actual distance
            heuristic_cost[actions[0]] = heuristic(actions)

            #going to itself
            start_to_current_cost[actions[0]] = actions[2]

        while available_actions:
            #print("***************** TESTING ***************** [a_star] ************************ THIS IS A NEW ITERATION *********************************")
            
            #Figuring out which action we should be taking
            #Find the min cost
            print("***************** TESTING ***************** heuristic_cost is " + str(heuristic_cost.keys()))
            print("************** TESTING ************** available_actions[0] is " + str(available_actions[0]))
            min_cost = heuristic_cost[available_actions[0][0]] #initial minimum cost
            current = available_actions[0] #initial current
            curr_index = 0

            #find the action that costs the least
            for index in range(len(available_actions)):
                action = available_actions[index]
                challenger = heuristic_cost[action[0]]
                if challenger < min_cost: #if cost you are looking at 
                    min_cost = challenger
                    current = action
                    curr_index = index

            #if it reaches the goal, end
            if is_goal(current):
                return return_list

            #do the action and update inventory
            available_actions.remove(available_actions[curr_index])
            actions_taken.append(current)
            item_cost += current[2]
            len_cost += 1
            return_list.append((curr_inv, current)) #update the steps taken
            curr_inv = current[1] #changes the state

            #loop through all neighbors and update their info
            #creates (name, effect, cost)
            list_of_tentative_actions = graph(curr_inv)
            #print("************** TESTING ************** current in key " + str(current in start_to_current_cost.keys()))
            for new_action in list_of_tentative_actions:
                #print("************** TESTING ************** current in key " + str(current in start_to_current_cost.keys()))
                #print("************** TESTING ************** current is " + str(current))

                if new_action in actions_taken:
                    continue    #Ignore the neighbor which is already evaluated.

                #The distance from start to a neighbor
                tentative_start_to_current_cost = start_to_current_cost[current[0]] + 1 #dist_between(current, neighbor)

                #if we should consider this action
                if new_action not in available_actions: #Discover a new node!
                    available_actions.append(new_action)
                elif tentative_start_to_current_cost >= start_to_current_cost[new_action]:
                    continue        #Ew we can do better than that

                #Update
                start_to_current_cost[new_action[0]] = tentative_start_to_current_cost
                heuristic_cost[new_action] = start_to_current_cost[new_action[0]] + heuristic(current)
                print("************** TESTING ************** heuristic_cost[new_action] is " + str(heuristic_cost[new_action]))


    #Implement your search here! Use your heuristic here!
    #When you find a path to the goal return a list of tuples [(state, action)]
    #representing the path. Each element (tuple) of the list represents a state
    #in the path and the action that took you to this state
    #make A* here
    while time() - start_time < limit:
        return a_star()

    #Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    #List of items that can be in your inventory:
    #print('All items:', Crafting['Items'])
    
    #List of items in your initial inventory with amounts:
    #print('Initial inventory:', Crafting['Initial'])
    
    #List of items needed to be in your inventory at the end of the plan:
    #print('Goal:',Crafting['Goal'])
    
    #Dict of crafting recipes (each is a dict):
    #print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    #Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    #Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    #Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    #Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        #Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
