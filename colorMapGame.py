import sys
import collections
import operator

class graphNode(object):
	"""docstring for graphNode"""
	def __init__(self, name, neighbors, color, player, possible_colors):
		
		self.name = name
		self.neighbors = neighbors
		self.color = color
		self.player = player
		self.possible_colors = possible_colors
		

lines = []
with open(sys.argv[2]) as f:
		lines.extend(f.read().splitlines())
colors = sorted(lines[0].split(', '))
initials = lines[1].split(', ')
maxdepth = int(lines[2])
player1 = lines[3].split(', ')
player2 = lines[4].split(', ')
length = len(lines)
graph = lines[5:length]
nodeInfo = {}
dictionary = {}
assigned = set()



# ******parse graph. each nodes neighbors in dictionary******
for line in graph:
	sets = line.split(': ')
	node = sets[0]
	neighbors = sets[1]
	nodeset = {}
	neighbor = neighbors.strip().split(', ')
	index = 0
	dictionary[node] = neighbor
	nodeInfo[node] = graphNode(node, neighbor, '', 0, colors)
	
# ******initial values of each variable******

colorvalue1 = {}
colorvalue2 = {}
# ******parse player1's scores for each color******
for i in player1:
	score = i.split(':')
	color = score[0].strip()
	val = score[1].strip()
	colorvalue1[color] = int(val)

# *******parse player2's scores for each color*******
for i in player2:
	score = i.split(':')
	color = score[0].strip()
	val = score[1].strip()
	colorvalue2[color] = int(val)


evaluation = 0
# *******parse initial state. assigned nodes and colors in init1 and init2*******
init1_color = []
init2_color = []
init1_node = []
init2_node = []

for i in initials:
	node = i.split(':')[0].strip()
	val = i.split(':')[1].strip()
	player = val.strip().split('-')[1]
	color = val.strip().split('-')[0]
	assigned.add(node)
	nodeInfo[node].color = color
	nodeInfo[node].possible_colors = []

	if player == '1':
		init1_color.append(color)
		init1_node.append(node)
		evaluation += colorvalue1[color]
		nodeInfo[node].player = 1
	else:
		init2_color.append(color)
		init2_node.append(node)
		evaluation -= colorvalue2[color]
		nodeInfo[node].player = 2
initial_evalutation = evaluation
initial_state = list(init2_node)[len(init2_node) - 1]

# ****** initial states ******
choices = set()
orderedNodes = collections.OrderedDict(sorted(nodeInfo.items()))
colormap = {}

for i in assigned:
	curcolor = nodeInfo[i].color
	colormap[i] = curcolor

	for j in nodeInfo[i].neighbors:
		if j not in assigned:
			choices.add(j)

nodecolor = set()
for i in choices:
	colorok = set()
	for j in assigned:
		if j in nodeInfo[i].neighbors:
			colorok.add(nodeInfo[j].color)
	possiblec = list(set(colors)-colorok)
	for c in possiblec:
		nodecolor.add((i, c))


def findNext(current, choices):

	nextNodes = sorted(list(choices))
	return nextNodes


def terminal_test(state, depth, choices, assigned, colors):
	if depth >= maxdepth:
		return 1
	if len(choices) == 0:
		return 1
	while len(choices) != 0:
		nextNode = sorted(list(choices))[0]
		colorset = set()
		for i in assigned:
			if i in nodeInfo[nextNode].neighbors:
				colorset.add(nodeInfo[i].color)
		possible_colors = set(colors) - colorset
		if len(possible_colors) == 0:
			choices.remove(nextNode) 
			continue
		else:
			return 0
	return 1


assigned_dict = {}


alpha = -float('inf')
beta = float('inf')

fo = open("output.txt", "wb")
result_value = -float('inf') 

#find out the choice for one player to get highest scores: #
def max_value(state, curcolor, depth, alpha, beta, score, choices, assigned, colors):
	global result_node
	global result_color
	global result_value

	v = -float('inf')
	if depth > 0: 
		nodeInfo[state].color = curcolor
		score -= colorvalue2[curcolor]

	if state in choices: 
		choices.remove(state)
	
	assigned.add(state)
	nodeInfo[state].player1 = 2
	for i in nodeInfo[state].neighbors:
		if i not in assigned:
			choices.add(i)
	
	if terminal_test(state, depth, choices, assigned, colors) == 1:
		v = score
		fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
		assigned.remove(state)
		return score

	fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
	
	
	for a in findNext(state, choices):
		colorset = set()
		for i in assigned:
			
			if i in nodeInfo[a].neighbors:
				colorset.add(nodeInfo[i].color)
		
		possible_colors = sorted(list(set(colors)-colorset))
		
		for c in possible_colors:
			newchoices = set(choices)
			for i in assigned:
				for j in nodeInfo[i].neighbors:
					if j not in assigned:
						newchoices.add(j)
			for i in nodeInfo[a].neighbors:
				if i not in assigned:
					newchoices.add(i)
			v = max(v, min_value(a, c, depth + 1, alpha, beta, score, newchoices, assigned, colors))
			if v >= beta: 
				assigned.remove(state)
				fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
				return v
			alpha = max(alpha, v)
			fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
			if v > result_value and depth == 0:
				result_value = v
				result_color = c
				result_node = a
				#print a, c, v
	
	assigned.remove(state)
	return v
	
#find out the choice for one player to get lowest scores: #
def min_value(state, curcolor, depth, alpha, beta, score, choices, assigned, colors):
	v = float('inf')
	
	nodeInfo[state].color = curcolor
	score += colorvalue1[curcolor]
	

	if state in choices: 
		choices.remove(state)
	assigned.add(state)
	nodeInfo[state].player1 = 1

	
	if terminal_test(state, depth, choices, assigned, colors) == 1:
		v = score
		fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
		assigned.remove(state)
		return score

	fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')

	for a in findNext(state, choices):
		colorset = set()
		for i in assigned:
			if i in nodeInfo[a].neighbors:
				colorset.add(nodeInfo[i].color)
		
		possible_colors = sorted(list(set(colors)-colorset))

		for c in possible_colors:
			newchoices = set(choices)
			for i in assigned:
				for j in nodeInfo[i].neighbors:
					if j not in assigned:
						newchoices.add(j)
			for i in nodeInfo[a].neighbors:
				if i not in assigned:
					newchoices.add(i)
			v = min(v, max_value(a, c, depth + 1, alpha, beta, score, newchoices, assigned, colors))
			if v <= alpha:
				assigned.remove(state)
				fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
				return v
			beta = min(beta, v)
			fo.write(state + ', ' + nodeInfo[state].color + ', ' + str(depth) + ', ' + str(v) + ', ' + str(alpha) + ', ' + str(beta) + '\n')
	assigned.remove(state)
	return v
	

depth = 0
curcolor = nodeInfo[initial_state].color

max_value(initial_state, curcolor, 0, alpha, beta, initial_evalutation, choices, assigned, colors)

#output:#
fo.write(result_node + ', ' + result_color + ', ' + str(result_value))
