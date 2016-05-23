import sys



# (optimization needed)
def space_init(dimension, obstacles, initial, goal):
    matrix = []
    """matrix = [ [ "." for i in range(dimension) ] for j in range(dimension) ]
    for obs in obstacles:
        matrix[obs[0], obs[1]] = "1"""

    # set space with obstacles
    for i in range(dimension):
        for j in range(dimension):
            if [i, j] in obstacles:
                matrix[i,j] = "1"
            else:
                matrix[i,j] = "."

    # set inital and goal states
    #matrix[initial[0], initial[1]] = "S"
    #matrix[goal[0], goal[1]] = "G"

    for i in matrix:
        print " ".join(i)
    print"\n"

# (optimization needed)
def read_file(file):
    try:
        file_open = open(file, "r")
        file = file_open.read().splitlines()

        # space dimension
        dimension = int(file[0])

        # obstacles (optimize)
        obstacles_line = file[1].replace(" ", "").split(";")
        obstacles = []
        for obs in obstacles_line:
            x, y = map(int, obs.strip('()').split(','))
            obstacles.append([x, y])

        # initial state
        x, y = map(int, file[2].strip('()').split(','))
        initial = [x, y]

        # goal state
        x, y = map(int, file[3].strip('()').split(','))
        goal = [x, y]

        matrix = space_init(dimension, obstacles, initial, goal)
    except IOError:
        print "Error, file not found"
    finally:
        file_open.close()
        print "File read with success"

def main(argv):
    # test program's args
    if(len(argv) == 2):
        read_file(argv[1])
    else:
        print "The program needs a file as argument."

### START ###

main(sys.argv)