import math
import random
from utils import goal_test, actions, child_node, solution, heuristic

GUI_LOGGER = None

# Cho phép chấp nhận trạng thái xấu hơn với một xác suất nhất định
# để tránh mắc kẹt tại cực trị cục bộ
def simulated_annealing(initial_state):
    current_node = {
        "state": initial_state,
        "parent": None,
        "action": None,
        "cost": 0
    }
    
    # Khởi tạo các tham số nhiệt độ
    T = 100.0
    Tmin = 0.01
    alpha = 0.95
    
    while T > Tmin:

        # Kiểm tra trạng thái đích
        if goal_test(current_node["state"]):
            return solution(current_node)
            
        possible_actions = actions(current_node["state"])

        # Không còn hành động để thực hiện
        if not possible_actions:
            return solution(current_node)
            
        # Chọn ngẫu nhiên một trạng thái lân cận
        action = random.choice(possible_actions)
        next_node = child_node(current_node, action)
        
        current_h = heuristic(current_node["state"])
        next_h = heuristic(next_node["state"])
        delta = next_h - current_h
        
        # Luôn chấp nhận trạng thái tốt hơn
        if delta < 0:
            current_node = next_node

        # Có thể chấp nhận trạng thái xấu hơn theo xác suất e^(-Δ/T)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_node = next_node
                
        if GUI_LOGGER:
            GUI_LOGGER(current_node, None, None)
            
        # Giảm nhiệt độ theo lịch làm lạnh
        T = alpha * T
        
    return solution(current_node)