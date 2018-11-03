# p5
minecraft crafting

Anthony Tom and Artemis Huang
The search approach looks at only its neighboring nodes and chooses the lowest cost neighbor based on the heuristic.
The heuristic checks:
	1. If you have more than 10 of that items. If you do then the cost of doing an action to get that item will steadily increase
	2. If the item you are about to produce is part of the goal. If it is part of the goal then it will choose that action
	3. If you only require 1 of the item that is about to be produced such as a pickaxe, axe, etc. if it is and you already have one,
	then it will not produce it.