# Uniform Cost Search: luôn mở rộng node có chi phí tích lũy g(n) thấp nhất
# Dùng heap để lấy node chi phí thấp nhất với độ phức tạp O(log n) mỗi lần
import heapq
from utils import goal_test, actions, child_node, solution

def uniform_cost_search(initial_state):

    # count dùng làm tie-breaker khi hai node có cùng chi phí
    count = 0
    node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0,
        "id": count
    }

    frontier = []
    # Heap lưu theo (chi phí, id, node) để so sánh đúng khi chi phí bằng nhau
    heapq.heappush(frontier, (node["cost"], node["id"], node))

    # reached lưu chi phí thấp nhất đã tìm thấy tới mỗi trạng thái
    reached = {str(initial_state): 0}

    while frontier:
        cost, node_id, node = heapq.heappop(frontier)

        # Kiểm tra đích khi lấy ra node có chi phí thấp nhất
        if goal_test(node["state"]):
            return solution(node)

        for action in actions(node["state"]):
            child = child_node(node, action)
            s_str = str(child["state"])

            # Chỉ thêm vào frontier nếu tìm được đường đi rẻ hơn đến trạng thái này
            if s_str not in reached or child["cost"] < reached[s_str]:
                reached[s_str] = child["cost"]
                count += 1
                child["id"] = count
                heapq.heappush(frontier, (child["cost"], child["id"], child))

    return "Failure"