import sys
import operator

# Implementation of Node class
class Node:
    def __init__(self, position, f_cost = 0, g_cost = 0):
        self.position = position
        self.f_cost = f_cost
        self.parent = None
        self.g_cost = g_cost

    def update_f_cost(self, goal):
        self.f_cost += self.g_cost + calc_heuristic(self, goal)


# Formula for heuristic calculation for a grid
def calc_heuristic(current, goal):
    return abs(goal.position[0] - current.position[0]) + abs(goal.position[1] - current.position[1])


# Calculate F cost
def calc_f_cost(q, goal):
    [x.update_f_cost(goal) for x in q]


# Goal check
def is_goal(current, goal):
    return True if current.position == goal.position else False


# Check expansion Nodes and filter unreachable ones
def calc_expansion(current, obstacles, dimension, closed_paths):
    expansion = [Node([current.position[0] + 1, current.position[1]]),
            Node([current.position[0] - 1, current.position[1]]),
            Node([current.position[0], current.position[1] + 1]),
            Node([current.position[0], current.position[1] - 1])]

    expansion = [x for x in expansion if x.position not in obstacles
            and (0 <= x.position[0] < dimension)
            and (0 <= x.position[1] < dimension)]

    for x in closed_paths:
        for y in expansion:
            if x.position == y.position:
                expansion.remove(y)

    return expansion


# Returns path with less F cost from Q list
def return_best_path(path_list):
    best = path_list[0]
    for x in path_list:
        if best.f_cost > x.f_cost:
            best = x

    return path_list.index(best)


# Loop to print best three paths
def print_best_three_paths(q, initial):
    print "\n### Best three paths:"
    #for x in check_length(q):
    for x in xrange(3) if len(q) > 3 else xrange(len(q)):
        print "Best path ", x + 1
        print_path(q[x], initial)


# Print all nodes sequencialy as a path
def print_path(node, initial):
    path = []
    iterator_node = node
    while iterator_node.parent is not initial:
        iterator_node = iterator_node.parent
        path.append(iterator_node.position)
    path.reverse()
    print(' '.join([str(i) for i in path]))
    print "Cost: ", node.f_cost
    print "--------------------"

# Main function for A Star search
def a_star(initial, goal, obstacles, matrix, dimension):
    closed_paths = []
    q = [initial]
    i = 1

    print "##### Starting A* algorithm pathfind #####\n "

    while len(q):
        print "\n####################"
        print "### Iteration ", i
        print "### Initial Q"

        h = q.pop(return_best_path(q))
        closed_paths.append(h)

        print "### Head of the list (best path)\n", h.position
        r = q
        if is_goal(h, goal):
            print " \nBest path found in %d iterations" % i
            print_path(h, initial)
            print_path_on_matrix(h, matrix, initial)
            break
        else:
            q = calc_expansion(h, obstacles, dimension, closed_paths)
            for node in q: node.parent = h;
            for node in q: node.g_cost += 1 + node.parent.g_cost
            calc_f_cost(q, goal)
            q.extend(r)
            q.sort(key=operator.attrgetter("f_cost"))
            print_best_three_paths(q, initial)
            i += 1


# Print final path on screen
# Iterating over parent nodes
def print_path_on_matrix(h, matrix, initial):
    node = h
    while node.parent is not initial:
        node = node.parent
        insert_objects_in_matrix(matrix, node.position, "x")
    print_matrix(matrix)


# Print matrix                
def print_matrix(matrix):
    file = open("path.txt", "w")
    for i in matrix:
        print " ".join(i)
        file.write(" ".join(i) + "\n")
    print"\n"


def insert_objects_in_matrix(matrix, position, object):
    matrix[position[0]][position[1]] = object


# Initializing space with data from file
def initialize_space(dimension, obstacles, initial, goal):
    matrix = [ [ "." for i in range(dimension) ] for j in range(dimension) ]
    for obstacle in obstacles:
        insert_objects_in_matrix(matrix, obstacle, "1")
    insert_objects_in_matrix(matrix, initial.position, "S")
    insert_objects_in_matrix(matrix, goal.position, "G")
    print_matrix(matrix)

    return matrix


# Read file function
# Reading line by line, striping and spliting to get coordinates
def read_file(file_input):
    try:
        file = open(file_input, "r")
        file_input = file.read().splitlines()

        # Space dimension
        dimension = int(file_input[0])

        # obstacles
        obstacles_line = file_input[1].replace(" ", "").split(";")
        obstacles = []
        for obstacle in obstacles_line:
            x, y = map(int, obstacle.strip('()').split(','))
            obstacles.append([x, y])

        # initial state
        x, y = map(int, file_input[2].strip('()').split(','))
        initial = Node([x, y])

        # goal state
        x, y = map(int, file_input[3].strip('()').split(','))
        goal = Node([x, y])

        return initial, goal, obstacles, dimension
    except IOError:
        print "Error, file not found"
    finally:
        file.close()
        print "File read with success"


def main(argv):
    # main program arg test
    if len(argv) == 2:
        initial, goal, obstacles, dimension = read_file(argv[1])
        # initialize space with dimension, obstacles, initial and goal state
        matrix = initialize_space(dimension, obstacles, initial, goal)
        # run A* algorithm
        a_star(initial, goal, obstacles, matrix, dimension)
    else:
        print "The program needs the file as argument."

### START ###
main(sys.argv)