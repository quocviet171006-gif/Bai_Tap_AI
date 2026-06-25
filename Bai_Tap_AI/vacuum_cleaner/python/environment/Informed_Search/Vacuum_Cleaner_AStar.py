from utils import goal_test, actions, child_node, solution, heuristic

def a_star_search(initial_state):

    # f(n) = g(n) + h(n)
    start_h = heuristic(initial_state)
    node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0,        # g(n)
        "f": start_h      # f(n)
    }

    if goal_test(node["state"]):
        return solution(node)

    frontier = [node]
    # reached lưu trữ trạng thái và chi phí g(n) thấp nhất tìm thấy đến trạng thái đó
    reached = {str(initial_state): 0}

    while frontier:
        # Chọn nút có f(n) thấp nhất (A* ưu tiên nút có tổng chi phí thấp nhất)
        frontier.sort(key=lambda x: x["f"])
        node = frontier.pop(0)

        # Kiểm tra đích khi lấy ra khỏi frontier
        if goal_test(node["state"]):
            return solution(node)

        for action in actions(node["state"]):
            child = child_node(node, action)
            state_str = str(child["state"])
            
            # g(n) của nút con
            g_child = child["cost"]
            # f(n) = g(n) + h(n)
            f_child = g_child + heuristic(child["state"])
            child["f"] = f_child

            # Nếu trạng thái chưa từng tới, hoặc tìm thấy đường đi tới trạng thái này với chi phí g(n) thấp hơn
            if state_str not in reached or g_child < reached[state_str]:
                reached[state_str] = g_child
                frontier.append(child)

    return "Failure"