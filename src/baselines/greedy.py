"""
Thuật toán Cơ sở Láng giềng Gần nhất (Greedy Nearest Neighbor Baseline)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Phương án mốc cơ sở ("Before") để đối chứng hiệu quả với SFO và SFO-VND

Tham chiếu học thuật:
- Mục 7.2 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Chiến lược quy hoạch tuyến thu gom kinh nghiệm theo thứ tự vị trí địa lý lân cận.
"""

import time
from typing import List, Dict, Tuple, Optional, Any, Union
import numpy as np

from ..config import CAPACITY_Q_MAX, DEPOT_INDEX
from ..core.evaluator import RouteEvaluator
from ..core.validator import RouteValidator


class GreedyNearestNeighbor:
    """
    Thuật toán Tham ăn (Greedy Baseline):
    - Chiến lược: Tại mỗi bước, xe chọn điểm thu gom gần nhất chưa được phục vụ
      miễn là việc tiếp nhận điểm đó không làm vượt quá tải trọng tối đa Q_max.
    - Khi xe không thể gom thêm điểm nào nữa do giới hạn tải trọng, xe sẽ quay về Depot
      và một xe mới được điều động để tiếp tục lộ trình.
    - Vai trò: Đại diện cho phương án quy hoạch lộ trình theo thói quen/kinh nghiệm thực tế ("Before"),
      dùng để chứng minh mức tiết kiệm quãng đường và giảm phát thải CO2 của SFO-VND ("After").
    """

    def __init__(
        self,
        evaluator: RouteEvaluator,
        capacity_q_max: float = CAPACITY_Q_MAX,
        depot_index: int = DEPOT_INDEX
    ):
        """
        Khởi tạo thuật toán Tham ăn.
        """
        self.evaluator = evaluator
        self.capacity_q_max = float(capacity_q_max)
        self.depot_index = int(depot_index)
        self.validator = RouteValidator(self.capacity_q_max, self.depot_index)

    def _get_demand(self, point_id: int) -> float:
        """Lấy khối lượng rác an toàn của điểm thu gom."""
        if isinstance(self.evaluator.demands, dict):
            return float(self.evaluator.demands.get(point_id, 0.0))
        return float(self.evaluator.demands[point_id])

    def solve(self, total_customers: int) -> Dict[str, Any]:
        """
        Thực thi thuật toán Nearest Neighbor:

        Quy trình:
        1. Khởi tạo danh sách các điểm chưa thăm: unvisited = {1, 2, ..., N}.
        2. Vòng lặp chính: khi vẫn còn điểm chưa được phục vụ:
           - Khởi tạo xe mới: route = [0], current_load = 0.
           - Trong khi xe hiện tại vẫn còn gom thêm được:
             + Tìm trong tập unvisited điểm v có khoảng cách dist(current_node, v) nhỏ nhất
               sao cho current_load + demand(v) <= Q_max.
             + Nếu tìm thấy: Thêm v vào route, cập nhật load, xóa v khỏi unvisited.
             + Nếu không tìm thấy điểm nào vừa tải: Khép tuyến về Depot 0 và chuyển sang xe mới.
        3. Đánh giá toàn bộ phương án bằng RouteEvaluator và RouteValidator.
        """
        start_time = time.time()
        dist_matrix = self.evaluator.distance_matrix

        unvisited = set(range(1, total_customers + 1))
        routes: List[List[int]] = []

        while unvisited:
            current_route = [self.depot_index]
            current_load = 0.0
            current_node = self.depot_index

            while unvisited:
                best_next_node = None
                best_distance = float("inf")

                # Tìm điểm gần nhất thỏa mãn tải trọng
                for candidate in unvisited:
                    cand_demand = self._get_demand(candidate)
                    if current_load + cand_demand <= self.capacity_q_max:
                        dist = dist_matrix[current_node, candidate]
                        if dist < best_distance:
                            best_distance = dist
                            best_next_node = candidate

                # Nếu tìm thấy điểm hợp lệ
                if best_next_node is not None:
                    current_route.append(best_next_node)
                    current_load += self._get_demand(best_next_node)
                    unvisited.remove(best_next_node)
                    current_node = best_next_node
                else:
                    # Không còn điểm nào nhét vừa xe này -> Khép tuyến về Depot
                    break

            # Cho xe quay về trạm tập kết
            current_route.append(self.depot_index)
            routes.append(current_route)

        total_runtime = time.time() - start_time

        # Kiểm tra tính hợp lệ của phương án cơ sở
        is_valid, violation_count, messages = self.validator.validate_solution(
            routes=routes,
            demands=self.evaluator.demands,
            total_customers=total_customers,
            capacity_q_max=self.capacity_q_max
        )

        metrics = self.evaluator.evaluate_solution(routes)

        return {
            "algorithm": "Greedy Nearest Neighbor (Baseline Before)",
            "routes": routes,
            "metrics": metrics,
            "fitness": metrics["fitness"],
            "total_distance_km": metrics["total_distance_km"],
            "total_fuel_liters": metrics["total_fuel_liters"],
            "total_co2_kg": metrics["total_co2_kg"],
            "fuel_cost_vnd": metrics["fuel_cost_vnd"],
            "carbon_cost_vnd": metrics["carbon_cost_vnd"],
            "is_valid": is_valid,
            "violation_count": violation_count,
            "validation_messages": messages,
            "runtime_seconds": total_runtime
        }
