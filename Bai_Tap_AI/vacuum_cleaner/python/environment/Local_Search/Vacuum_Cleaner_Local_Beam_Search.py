from utils import actions, child_node, goal_test, solution, find_robot

GUI_LOGGER = None

# Hàm heuristic đánh giá trạng thái dựa trên số ô bẩn còn lại
# và khoảng cách từ robot đến ô bẩn gần nhất
def get_heuristic(state):
    rx, ry = find_robot(state)
    dirt_count = 0
    min_dist = float('inf')
    
    for r in range(len(state)):
        for c in range(len(state[0])):
            if state[r][c] in (1, 3):
                dirt_count += 1
                dist = abs(r - rx) + abs(c - ry)
                if dist < min_dist:
                    min_dist = dist
                    
    # Nếu không còn ô bẩn thì đã đạt trạng thái mục tiêu
    if dirt_count == 0:
        return 0

    # Ưu tiên giảm số ô bẩn trước, sau đó giảm khoảng cách
    return (dirt_count * 1000) + min_dist


# Thuật toán Local Beam Search
# k là số trạng thái tốt nhất được giữ lại ở mỗi bước
def local_beam_search(initial_state, k=3):

    # Khởi tạo beam với trạng thái ban đầu
    initial_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": get_heuristic(initial_state)
    }
    beam = [initial_node]
    
    while True:
        candidates = []

        # Duyệt các trạng thái hiện tại trong beam
        for node in beam:

            # Kiểm tra điều kiện đích
            if goal_test(node["state"]):
                return solution(node)

            # Gửi dữ liệu cho giao diện nếu có
            if GUI_LOGGER:
                GUI_LOGGER(node, beam, [])
            
            # Sinh các trạng thái kế tiếp
            for action in actions(node["state"]):
                child = child_node(node, action)
                child["cost"] = get_heuristic(child["state"])
                candidates.append(child)
        
        # Không còn trạng thái để mở rộng
        if not candidates:
            return "Failure"
        
        # Chọn k trạng thái tốt nhất cho vòng lặp tiếp theo
        candidates.sort(key=lambda x: x["cost"])
        beam = candidates[:k]