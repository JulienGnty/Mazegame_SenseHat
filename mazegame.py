import mazegen
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED, DIRECTION_DOWN, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_RIGHT
from time import sleep

COLORS = [(200,0,0),(0,200,0),(0,0,200),(200,200,0),(200,0,200),(0,200,200)]
CW = (50,50,50)
CC = (0,0,0)


class GameWonException(Exception):
    pass


def set_view_limits(position, w_total, h_total, w_reduce, h_reduce):
    """
        Return the limits of the maze part which will be displayed
    """
    x = position[1]
    y = position[0]

    if x < w_reduce//2:
        limit_l = 0
        limit_r = w_reduce
    elif x > w_total-1-w_reduce//2:
        limit_l = w_total-w_reduce
        limit_r = w_total
    else:
        limit_l = x-(w_reduce//2 - 1)
        limit_r = x+(w_reduce//2 + 1)

    if y < (h_reduce//2)+1:
        limit_u = 0
        limit_d = h_reduce
    elif y > h_total-1-h_reduce//2:
        limit_u = h_total-h_reduce
        limit_d = h_total
    else:
        limit_u = y-(h_reduce//2)
        limit_d = y+(h_reduce//2)
        
    return limit_l,limit_r,limit_u,limit_d



def set_maze_display(maze_d, player, cw=(192,192,192), cc=(50,50,50), display_w=8, display_h=8, see_players=False):
    """
        Return a 1-dimension list filled with colors in tuple (R,G,B)

        display_w: width of the maze part which wiil be displayed (default = 8 tiles)
        display_h: height of the maze part which wiil be displayed (default = 8 tiles)
        see_players: if True, player can see all other players who are in his view; else he can see only players next to him
    """
    grid = []

    left,right,up,down = set_view_limits(maze_d["players"][player]["pos"], len(maze_d["maze"][0]), len(maze_d["maze"]), display_w, display_h)
    try:
        for i in range(up, down):
            for j in range(left, right):
                if player == "vuedaigle":
                    if maze_d["players"][player]["solve"][i][j]:
                        grid.append((255,128,64))
                        continue
                if maze_d["players"][player]["view"][i][j]:
                    if maze_d["maze"][i][j] == mazegen.CELL:
                        grid.append(cc)
                    else:
                        grid.append(cw)
                else:
                    grid.append((0,0,0))
            
                    
        y = maze_d["players"][player]["pos"][0]
        x = maze_d["players"][player]["pos"][1]
        
        for p in maze_d["players"]:
            if p != player and maze_d["players"][p]["status"] != "end":
                y_p = maze_d["players"][p]["pos"][0]
                x_p = maze_d["players"][p]["pos"][1]
                if see_players:
                    if maze_d["players"][player]["view"][y_p][x_p] and (up <= y_p < down) and (left <= x_p < right):
                        grid[(maze_d["players"][p]["pos"][0]-up)*display_w + (maze_d["players"][p]["pos"][1]-left)] = maze_d["players"][p]["color"]
                else:
                    if (y-1 <= y_p <= y+1) and (x-1 <= x_p <= x+1):
                        grid[(y_p-up)*display_w + (x_p-left)] = maze_d["players"][p]["color"]

        coord = (y-up)*display_w + (x-left)
        grid[coord] = maze_d["players"][player]["color"]
    except:
        grid = [cc]*64
        print("grid cannot be displayed correctly")
    return grid


def move_player_up(maze_d, player):
    """
        Move a player to a cell above
        Return the maze dictionnary
    """
    x = maze_d["players"][player]["pos"][1]
    y = maze_d["players"][player]["pos"][0]
    if y > 0:        
        if maze_d["maze"][y-1][x] == mazegen.CELL:
            maze_d["players"][player]["pos"][0] -= 1
    return maze_d


def move_player_down(maze_d, player):
    """
        Move a player to a cell below
        Return the maze dictionnary
    """
    x = maze_d["players"][player]["pos"][1]
    y = maze_d["players"][player]["pos"][0]
    if y < len(maze_d["maze"])-1:
        if maze_d["maze"][y+1][x] == mazegen.CELL:
            maze_d["players"][player]["pos"][0] += 1
    return maze_d


def move_player_left(maze_d, player):
    """
        Move a player to a cell on the left
        Return the maze dictionnary
    """
    x = maze_d["players"][player]["pos"][1]
    y = maze_d["players"][player]["pos"][0]
    if x > 0:        
        if maze_d["maze"][y][x-1] == mazegen.CELL:
            maze_d["players"][player]["pos"][1] -= 1
    return maze_d


def move_player_right(maze_d, player):
    """
        Move a player to a cell on the right
        Return the maze dictionnary
    """
    x = maze_d["players"][player]["pos"][1]
    y = maze_d["players"][player]["pos"][0]
    if x < len(maze_d["maze"][0])-1:        
        if maze_d["maze"][y][x+1] == mazegen.CELL:
            maze_d["players"][player]["pos"][1] += 1
    return maze_d


def check_players_status(maze_d):
    """
        Set players status to "end" if they reached the end cell
        Return the maze dictionnary
    """
    for p in maze_d["players"]:
        x = maze_d["players"][p]["pos"][1]
        y = maze_d["players"][p]["pos"][0]
        if (y,x) == maze_d["end"]:
            maze_d["players"][p]["status"] = "end"
            maze_d["players"][p]["rank"] = count_winners(maze_d)
    return maze_d


def count_winners(maze_d):
    """
        Return the number of players who have finished
    """
    count = 0
    for p in maze_d["players"]:
        if maze_d["players"][p]["status"] == "end":
            count += 1
    return count


def update_player_view(maze_d, player):
    """
        Set the tile view next to the player position to True
        Return the maze dictionnary
    """
    x = maze_d["players"][player]["pos"][1]
    y = maze_d["players"][player]["pos"][0]
    up = y > 0
    down = y < len(maze_d["maze"])-1
    left = x > 0
    right = x < len(maze_d["maze"][0])-1

    if up and left:
        maze_d["players"][player]["view"][y-1][x-1] = True
    if up and right:
        maze_d["players"][player]["view"][y-1][x+1] = True
    if up:
        maze_d["players"][player]["view"][y-1][x] = True
    if left:
        maze_d["players"][player]["view"][y][x-1] = True
    if right:
        maze_d["players"][player]["view"][y][x+1] = True
    if down and left:
        maze_d["players"][player]["view"][y+1][x-1] = True
    if down and right:
        maze_d["players"][player]["view"][y+1][x+1] = True
    if down:
        maze_d["players"][player]["view"][y+1][x] = True

    maze_d["players"][player]["view"][y][x] = True
    return maze_d


def add_player(maze_d, name, visible=False):
    """
        Add a player in the maze dictionnary
        Return the maze dictionnary

        visible: set the player view;
            -> if True, by default this player can see all the maze tiles
            -> if False, this player will see only maze tile next to him

        "vuedaigle" as name is a cheat code; this player can see the shortest path to the exit
    """
    maze_d["players"][name] = {
        "color": COLORS[len(maze_d["players"])],
        "pos": [maze_d["start"][0],maze_d["start"][1]],
        "status": "ingame",
        "rank": 0,
        "view": [[visible for i in range(len(maze_d["maze"][0]))] for j in range(len(maze_d["maze"]))]
    }
    if name == "vuedaigle":
        maze_d["players"][name]["solve"] = mazegen.solve(maze_d)
    return update_player_view(maze_d, name)


def init_maze(width=16, height=16):
    """
        Initialize the maze

        Return a maze dictionnary which contains:
            -> "maze": a 2-dimensional list
            -> "start": coordinates of the entrance
            -> "end": coordinates of the exit
            -> "players": an empty dictionnary which will contain every players
    """
    maze_dict = mazegen.create_maze(width,height)
    maze_dict["players"] = {}
    return maze_dict


def main():
    S = SenseHat()
    try:
        width = 0
        height = 0
        while not(8 <= width <= 40):
            width = int(input("Width of maze (between 8 and 40 inclusive): "))
        while not(8 <= height <= 40):
            height = int(input("Height of maze (between 8 and 40 inclusive): "))
        maze_dict = init_maze(width,height)
        mazegen.print_maze(maze_dict["maze"])
        p1 = "p1"
        maze_dict = add_player(maze_dict,p1)
        maze_dict = add_player(maze_dict,"p2")        
        
        S.set_pixels(set_maze_display(maze_dict,p1))
        
        while True:
            already_treated = False
            for event in S.stick.get_events():
                if event.action in (ACTION_PRESSED, ACTION_HELD) and not already_treated:
                    if event.direction == DIRECTION_DOWN:
                        move_player_down(maze_dict, p1)
                        already_treated = True
                    if event.direction == DIRECTION_UP:
                        move_player_up(maze_dict, p1)
                        already_treated = True
                    if event.direction == DIRECTION_RIGHT:
                        move_player_right(maze_dict, p1)
                        already_treated = True
                    if event.direction == DIRECTION_LEFT:
                        move_player_left(maze_dict, p1)
                        already_treated = True
                    update_player_view(maze_dict, p1)
                    S.set_pixels(set_maze_display(maze_dict,p1))
                    check_players_status(maze_dict)
                    if maze_dict["players"][p1]["status"] == "end":
                        raise GameWonException("WIN")
    except KeyboardInterrupt as e:
        S.clear()
    except GameWonException:
        S.show_message("WIN")
        S.clear()
    except BaseException as e:
        print(e)

if __name__== "__main__":
    main()
