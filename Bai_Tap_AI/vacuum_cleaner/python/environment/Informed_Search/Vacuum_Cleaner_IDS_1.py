# IDS: Iterative Deepening Search kết hợp ưu điểm của BFS (tối ưu) và DFS (ít bộ nhớ)
# Tăng dần giới hạn độ sâu từ 0 đến vô hạn cho đến khi tìm thấy đích
import sys
from utils import goal_test, actions, child_node, solution

def iterative_deepening_search(state):
    # Thử lần lượt từng mức giới hạn độ sâu
    for depth in range(sys.maxsize):
        result = depth_limit_search(state, depth)
        # Nếu kết quả không phải cutoff thì đã tìm thấy lời giải hoặc thất bại thực sự
        if result != 'cutoff':
            return result

def depth_limit_search(initial_state, limit):
    # Khởi tạo node gốc tại giới hạn độ sâu hiện tại
    node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }

    frontier = [node]
    result = 'failure'

    while frontier:
        node = frontier.pop()

        # Đạt đích thì trả về ngay chuỗi hành động
        if goal_test(node["state"]):
            return solution(node)

        if node["cost"] >= limit:
            # Đánh dấu cutoff: chưa tìm thấy đích nhưng bị cắt bởi giới hạn độ sâu
            result = 'cutoff'
        else:
            for action in reversed(actions(node["state"])):
                child = child_node(node, action)
                # Bỏ qua nếu quay ngược lại trạng thái cha trực tiếp (tránh chu trình đơn)
                if node["parent"] is not None and child["state"] == node["parent"]["state"]:
                    continue
                frontier.append(child)

    return result