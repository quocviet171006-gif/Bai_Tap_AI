# Greedy Best-First Search: luôn chọn node có heuristic h(n) thấp nhất
# Không đảm bảo tối ưu nhưng thường nhanh hơn BFS vì hướng thẳng về đích
from utils import goal_test, actions, child_node, solution, in_frontier, heuristic

def greedy_search(initial_state):

    # Dùng heuristic làm chi phí ưu tiên thay cho g(n) thực
    node = {"state": initial_state,
            "parent": None,
            "action": None,
            "cost": heuristic(initial_state)
    }

    frontier = [node]
    reached = []

    while frontier:
        # Chọn node có heuristic nhỏ nhất (gần đích nhất theo ước lượng)
        frontier.sort(key=lambda x: x["cost"])
        node = frontier.pop(0)

        if goal_test(node["state"]):
            return solution(node)

        reached.append(node["state"])

        for action in actions(node["state"]):
            child = child_node(node, action)
            # Cập nhật chi phí của node con bằng heuristic của trạng thái con
            child["cost"] = heuristic(child["state"])

            # Chỉ thêm nếu chưa trong reached và chưa trong frontier
            if child["state"] not in reached and not in_frontier(frontier, child["state"]):
                frontier.append(child)

    return "Failure"