def find_robot(state):

    rows = len(state)
    cols = len(state[0])
    for row in range(rows):
        for col in range(cols):
            if state[row][col] == 2 or state[row][col] == 3:
                return (row, col)

def goal_test(state):

    for row in state:
        if 1 in row or 3 in row:
            return False
        
    return True

def copy_state(state):
    return [row[:] for row in state]

def actions(state):
    
    rows = len(state)
    cols = len(state[0])
    location_row, location_col = find_robot(state)
    move = []

    if location_row > 0 and state[location_row - 1][location_col] != -1:
        move.append("Up")
    
    if location_row < rows - 1 and state[location_row + 1][location_col] != -1:
        move.append("Down")

    if location_col > 0 and state[location_row][location_col - 1] != -1:
        move.append("Left")
    
    if location_col < cols - 1 and state[location_row][location_col + 1] != -1:
        move.append("Right")
    
    if state[location_row][location_col] == 3:
        move.append("Suck")

    return move

def child_node(parent, action):

    state = parent["state"]
    new_state = copy_state(state)
    lct_row, lct_col = find_robot(state)

    if action == "Suck":
        if new_state[lct_row][lct_col] == 3:
            new_state[lct_row][lct_col] = 2
        
        return {
            "state": new_state,
            "parent": parent,
            "action": action,
            "cost": parent["cost"] + 1
        }

    nx, ny = lct_row, lct_col
    if action == "Up": nx -= 1
    elif action == "Down": nx += 1
    elif action == "Left": ny -= 1
    elif action == "Right": ny += 1

    if new_state[lct_row][lct_col] == 2:
        new_state[lct_row][lct_col] = 0

    if new_state[nx][ny] == 0:
        new_state[nx][ny] = 2
        
    elif new_state[nx][ny] == 1:
        new_state[nx][ny] = 3

    return {
        "state": new_state,
        "parent": parent,
        "action": action,
        "cost": parent["cost"] + 1
    }

def solution(node):

    path = []

    while node["parent"] != None:
        path.append(node["action"])
        node = node["parent"]
    path.reverse()
    
    return path

def in_frontier(frontier, state):
    for node in frontier:
        if node["state"] == state:
            return True
    return False

def heuristic(state):
    h = 0
    for row in state:
        for cell in row:
            if cell == 1 or cell == 3:
                h += 1
    return h