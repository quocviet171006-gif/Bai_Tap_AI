# DFS theo dạng Graph Search: tìm kiếm theo chiều sâu có kiểm tra trùng lặp
# Dùng stack (list) để mô phỏng hành vi LIFO, ưu tiên đào sâu trước
from collections import deque
from utils import goal_test, actions, child_node, solution, in_frontier

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

    # Dùng list như stack: pop() lấy từ cuối (LIFO)
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

        # Kiểm tra đích sau khi xác nhận chưa duyệt
        if goal_test(node["state"]):
            return solution(node)

        for action in actions(node["state"]):
            child = child_node(node, action)
            if str(child["state"]) not in reached:
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