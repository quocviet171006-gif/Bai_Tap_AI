# DFS sớm kiểm tra đích: goal_test được gọi ngay khi sinh node con
# Khác DFS_1 ở chỗ không cần pop ra mới kiểm tra, thoát sớm hơn khi gặp đích
from collections import deque
from utils import goal_test, actions, child_node, solution

def depth_first_search(initial_state):

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

    frontier = []
    frontier.append(node)
    reached = set()

    while frontier:
        node = frontier.pop()
        state_str = str(node["state"])

        # Bỏ qua nếu trạng thái này đã được duyệt trước đó
        if state_str in reached:
            continue
        reached.add(state_str)

        for action in actions(node["state"]):
            child = child_node(node, action)

            if str(child["state"]) not in reached:
                # Kiểm tra đích ngay khi sinh ra node con
                if goal_test(child["state"]):
                    return solution(child)
                frontier.append(child)

    return "Failure"

if __name__ == "__main__":

    room = [
        [1, 1, 1, 0],
        [0, -1, 2, 1],
        [1, 0, -1, 1]
    ]

    result = depth_first_search(room)

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