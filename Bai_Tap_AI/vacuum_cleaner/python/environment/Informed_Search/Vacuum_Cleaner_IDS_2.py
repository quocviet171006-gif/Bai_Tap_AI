# IDS sớm kiểm tra đích: goal_test được gọi ngay khi sinh node con
# Thoát sớm hơn IDS_1 mà không cần đợi pop ra mới kiểm tra
import sys
from utils import goal_test, actions, child_node, solution, in_frontier, heuristic

def iterative_deepening_search(state):
    # Tăng dần giới hạn độ sâu từ 0 đến vô hạn
    for depth in range(sys.maxsize):
        result = depth_limit_search(state, depth)
        if result != 'cutoff':
            return result

def depth_limit_search(initial_state, limit):
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

        if node["cost"] >= limit:
            # Chạm giới hạn độ sâu, đánh dấu cutoff và tiếp tục
            result = 'cutoff'
        else:
            for action in reversed(actions(node["state"])):
                child = child_node(node, action)
                # Bỏ qua nếu quay lại trạng thái cha trực tiếp
                if node["parent"] is not None and child["state"] == node["parent"]["state"]:
                    continue
                # Kiểm tra đích ngay khi vừa sinh ra node con
                if goal_test(child["state"]):
                    return solution(child)
                frontier.append(child)

    return result