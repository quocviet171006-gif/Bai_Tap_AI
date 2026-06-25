# BFS sớm kiểm tra đích: goal_test được gọi ngay khi sinh node con
# Giúp thoát sớm hơn BFS_1 mà không cần chờ pop ra khỏi frontier mới kiểm tra
from collections import deque
from utils import goal_test, actions, child_node, solution, in_frontier

def breadth_first_search(initial_state):

    # Khởi tạo node gốc từ trạng thái ban đầu
    node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    # Kiểm tra ngay nếu trạng thái đầu đã là đích
    if goal_test(node["state"]):
        return solution(node)

    frontier = deque()
    frontier.append(node)
    reached = {str(initial_state)}

    while frontier:
        node = frontier.popleft()

        for action in actions(node["state"]):
            child = child_node(node, action)
            child_state_str = str(child["state"])

            if child_state_str not in reached:
                # Kiểm tra đích ngay khi sinh ra node con để thoát sớm hơn
                if goal_test(child["state"]):
                    return solution(child)

                reached.add(child_state_str)
                frontier.append(child)

    return "Failure"


if __name__ == "__main__":

    room = [
        [1, 1, 1, 0],
        [0, -1, 2, 1],
        [1, 0, -1, 1]
    ]

    result = breadth_first_search(room)

    def print_room(state):
        for row in state:
            print(row)
        print()

    node = {
        "state": room,
        "parent": None,
        "action": None,
        "cost": 0
    }

    print("Trạng thái ban đầu:")
    print_room(room)

    for action in result:
        node = child_node(node, action)
        print("Action:", action)
        print_room(node["state"])