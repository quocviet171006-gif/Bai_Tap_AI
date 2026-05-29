import sys
from utils import goal_test, actions, child_node, solution, heuristic

def ida_star_search(initial_state):
    # Khởi tạo node gốc
    start_h = heuristic(initial_state)
    root = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0,        # g(n)
        "f": start_h      # f(n) = g(n) + h(n)
    }

    # Ngưỡng f-limit ban đầu chính là f(n) của trạng thái khởi đầu
    f_limit = root["f"]

    while f_limit < sys.maxsize:
        # Gọi hàm tìm kiếm theo chiều sâu có giới hạn ngưỡng f
        result, next_f_limit = f_limit_search(root, f_limit)
        
        # Nếu tìm thấy đích (trả về một node giải pháp chứa đường đi)
        if isinstance(result, dict):
            return solution(result)
        
        # Nếu không tìm thấy và không thể mở rộng thêm (bị kẹt hoàn toàn)
        if next_f_limit == sys.maxsize:
            return "Failure"
        
        # Cập nhật ngưỡng f-limit mới bằng giá trị f nhỏ nhất vượt quá ngưỡng cũ
        f_limit = next_f_limit

    return "Failure"


def f_limit_search(root_node, f_limit):
    """
    Tìm kiếm bằng DFS sử dụng một Stack cho frontier.
    Trả về (node_đích, next_f_limit) hoặc ('cutoff', next_f_limit)
    """
    frontier = [root_node]
    min_overflow_f = sys.maxsize  # Lưu giá trị f nhỏ nhất lớn hơn f_limit để làm ngưỡng tiếp theo

    while frontier:
        node = frontier.pop()

        # Kiểm tra nếu trạng thái hiện tại là đích
        if goal_test(node["state"]):
            return node, f_limit

        # Duyệt qua các hành động có thể (đảo ngược list hành động để thứ tự duyệt giống DFS thông thường)
        for action in reversed(actions(node["state"])):
            child = child_node(node, action)
            
            # Tính f(n) cho nút con
            g_child = child["cost"]
            f_child = g_child + heuristic(child["state"])
            child["f"] = f_child

            # Tránh đi ngược lại trạng thái của nút cha ngay trước đó (chu trình đơn giản)
            if node["parent"] is not None and child["state"] == node["parent"]["state"]:
                continue

            # Nếu f vượt quá ngưỡng hiện tại, ghi nhận lại giá trị để tăng f-limit ở vòng lặp sau
            if child["f"] > f_limit:
                if child["f"] < min_overflow_f:
                    min_overflow_f = child["f"]
            else:
                # Nếu thỏa mãn nằm trong ngưỡng, thêm vào frontier để tiếp tục đào sâu
                frontier.append(child)

    return "cutoff", min_overflow_f