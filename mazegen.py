"""
From https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
"""

import random

CELL = " "
WALL = "w"
UNVISITED = "u"
WIDTH = HEIGHT = 8
DIRECTIONS = [[-1,0],[0,-1],[1,0],[0,1]]    # up, left, down, right

def solve(maze_d):
    """
        Compute the shortest path in the maze between entrance and exit
        Return a 2-dimensional bool list with same lengths than maze
        Elements are True if they are part of the shortest path
    """
    position = maze_d["start"]
    direction = -1
    cell_list = [position]
    
    if position[0] == len(maze_d["maze"])-1:
        direction = 0
    elif position[0] == 0:
        direction = 2
    elif position[1] == len(maze_d["maze"][0])-1:
        direction = 1
    elif position[1] == 0:
        direction = 3
    else:
        return [[False]*len(maze_d["maze"][0])]*len(maze_d["maze"])
    try:
        while position != maze_d["end"]:
            if maze_d["maze"][position[0] + DIRECTIONS[((direction+3)%4)][0]][position[1] + DIRECTIONS[((direction+3)%4)][1]] == CELL:
                direction += 3
            elif maze_d["maze"][position[0] + DIRECTIONS[((direction+0)%4)][0]][position[1] + DIRECTIONS[((direction+0)%4)][1]] == CELL:
                direction += 0
            elif maze_d["maze"][position[0] + DIRECTIONS[((direction+1)%4)][0]][position[1] + DIRECTIONS[((direction+1)%4)][1]] == CELL:
                direction += 1
            elif maze_d["maze"][position[0] + DIRECTIONS[((direction+2)%4)][0]][position[1] + DIRECTIONS[((direction+2)%4)][1]] == CELL:
                direction += 2
            else:
                return [[False]*len(maze_d["maze"][0])]*len(maze_d["maze"])
            position = (position[0] + DIRECTIONS[((direction)%4)][0],position[1] + DIRECTIONS[((direction)%4)][1])
            cell_list.append(position)
            
        for c in cell_list:
            if c in cell_list[cell_list.index(c)+1:len(cell_list)]:
                next_index = cell_list[cell_list.index(c)+1:len(cell_list)].index(c)
                del cell_list[cell_list.index(c):cell_list.index(c)+1+next_index]
        solver_list = [[((y,x) in cell_list) for x in range(len(maze_d["maze"][y]))] for y in range(len(maze_d["maze"]))]
    except:
        return [[False]*len(maze_d["maze"][0])]*len(maze_d["maze"])
    return solver_list

def init_maze(width, height):
    return [[UNVISITED for i in range(width)] for j in range(height)]

def print_maze(maze):
    res = ""
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            res += str(maze[i][j])
            res += " "
        res += "\n"
    print(res)

def surroundingCells(rand_wall,maze):
    s_cells = 0
    if (maze[rand_wall[0]-1][rand_wall[1]] == CELL):
        s_cells += 1
    if (maze[rand_wall[0]+1][rand_wall[1]] == CELL):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]-1] == CELL):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]+1] == CELL):
        s_cells += 1
    return s_cells

def create_maze(width = WIDTH, height = HEIGHT):
    maze_dict = {}
    
    maze = init_maze(width,height)
    
    starting_height = int(random.random()*height)
    starting_width = int(random.random()*width)

    if starting_height == 0:
        starting_height += 1
    if starting_height == height-1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width-1:
        starting_width -= 1
    

    maze[starting_height][starting_width] = CELL
    walls = []
    walls.append([starting_height-1, starting_width])
    walls.append([starting_height, starting_width-1])
    walls.append([starting_height, starting_width+1])
    walls.append([starting_height+1, starting_width])
    maze[starting_height-1][starting_width] = WALL
    maze[starting_height][starting_width-1] = WALL
    maze[starting_height][starting_width+1] = WALL
    maze[starting_height+1][starting_width] = WALL

    while (walls):
        rand_wall = walls[int(random.random()*len(walls))-1]
        walls.remove(rand_wall)

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == UNVISITED and maze[rand_wall[0]][rand_wall[1]+1] == CELL):
                # Find the number of surrounding cells
                s_cells = surroundingCells(rand_wall,maze)
                
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                    
                    # Bottom cell
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])
                            
                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])
                continue
        
        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == UNVISITED and maze[rand_wall[0]+1][rand_wall[1]] == CELL):
                s_cells = surroundingCells(rand_wall,maze)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                continue

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == UNVISITED and maze[rand_wall[0]-1][rand_wall[1]] == CELL):
                s_cells = surroundingCells(rand_wall,maze)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]-1] = WALL
                        if ([rand_wall[0], rand_wall[1]-1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]-1])

                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])
                
                continue

        # Check the right wall
        if (rand_wall[1] != width-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == UNVISITED and maze[rand_wall[0]][rand_wall[1]-1] == CELL):
                s_cells = surroundingCells(rand_wall,maze)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = CELL

                    # Mark the new walls
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != CELL):
                            maze[rand_wall[0]][rand_wall[1]+1] = WALL
                        if ([rand_wall[0], rand_wall[1]+1] not in walls):
                            walls.append([rand_wall[0], rand_wall[1]+1])

                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]+1][rand_wall[1]] = WALL
                        if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]+1, rand_wall[1]])

                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != CELL):
                            maze[rand_wall[0]-1][rand_wall[1]] = WALL
                        if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                            walls.append([rand_wall[0]-1, rand_wall[1]])
                continue

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == UNVISITED):
                maze[i][j] = WALL

    # Set entrance and exit
    ent = []
    for i in range(1, width):
        if (maze[height-2][i] == CELL):
            ent.append(i)

    choice = random.choice(ent)
    maze[height-1][choice] = CELL
    maze_dict["start"] = (height-1,choice)
    
    exi = []
    for i in range(width-1, 0, -1):
        if (maze[1][i] == CELL):
            exi.append(i)

    choice = random.choice(exi)
    maze[0][choice] = CELL
    maze_dict["end"] = (0,choice)
        
    maze_dict["maze"] = maze[:][:]

    return maze_dict
    

def main():
    maze_dict = create_maze(16,16)
    print_maze(maze_dict["maze"])
    solver_list = solve(maze_dict)
    res = ""
    for i in range(len(solver_list)):
        for j in range(len(solver_list[i])):
            if solver_list[i][j]:
                res += " "
            else:
                res += "w"
            res += " "
        res += "\n"
    print(res)

if __name__ == "__main__":
    main()
