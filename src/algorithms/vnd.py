"""
Thuật toán Tìm kiếm Lân cận Biến đổi (Variable Neighborhood Descent - VND)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Khai thác cục bộ chuyên sâu (Local Exploitation) trên cấu trúc tuyến rời rạc

Tham chiếu học thuật:
- Mladenović, N., & Hansen, P. (1997). Variable neighborhood search. Computers & Operations Research.
- Mục 8.2 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 5.3 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Algorithm 1 trong Analysis-of-variable-neighborhood-descent...pdf
"""

import copy
import time
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

from ..config import CAPACITY_Q_MAX, DEPOT_INDEX
from ..core.evaluator import RouteEvaluator


class VariableNeighborhoodDescent:
    """
    Thuật toán Variable Neighborhood Descent (VND) tinh chỉnh lộ trình thu gom rác.

    Nguyên lý 3 cấu trúc lân cận (k = 1, 2, 3):
    - k=1 (2-opt - Intra-route): Đảo ngược một đoạn con trong cùng một tuyến xe để gỡ
      các cung đường cắt chéo nhau trên bản đồ, giúp rút ngắn quãng đường nội tuyến.
    - k=2 (Relocate - Inter/Intra-route): Rút 1 điểm từ xe này chèn sang vị trí của xe khác
      (có kiểm tra sức chứa Q_max), giúp sửa lỗi phân chia điểm bị lệch vùng.
    - k=3 (Swap - Inter-route): Hoán đổi vị trí của 2 điểm giữa 2 xe khác nhau
      (có kiểm tra sức chứa Q_max), giúp cả hai xe cùng thu hẹp phạm vi gom rác.
    """

    def __init__(
        self,
        evaluator: RouteEvaluator,
        capacity_q_max: float = CAPACITY_Q_MAX,
        depot_index: int = DEPOT_INDEX,
        max_no_improve: int = 50,
        strategy: str = "first_improvement"
    ):
        """
        Khởi tạo bộ tối ưu cục bộ VND.

        Giải thích giáo dục:
        - evaluator: Bộ đánh giá tính Fitness dựa trên mô hình tải trọng động MEET và ISO 14064.
        - capacity_q_max: Giới hạn tải trọng xe để sàng lọc các nghiệm vi phạm khi Relocate/Swap.
        - strategy: 'first_improvement' (chấp nhận ngay khi thấy nghiệm tốt hơn, chạy rất nhanh,
          cực kỳ phù hợp khi ghép vào vòng lặp của SFO) hoặc 'best_improvement' (quét hết lân cận).
        """
        if capacity_q_max <= 0:
            raise ValueError(f"Lỗi khởi tạo VND: Sức chứa xe ({capacity_q_max}) phải lớn hơn 0.")

        self.evaluator = evaluator
        self.capacity_q_max = float(capacity_q_max)
        self.depot_index = int(depot_index)
        self.max_no_improve = int(max_no_improve)
        self.strategy = strategy.lower()

        if self.strategy not in ["first_improvement", "best_improvement"]:
            raise ValueError(f"Lỗi chiến lược VND: Chỉ hỗ trợ 'first_improvement' hoặc 'best_improvement', nhận: {strategy}.")

        # Lưu lịch sử cải thiện
        self.history: List[Dict[str, Any]] = []

    def _get_demand(self, point_id: int) -> float:
        """Lấy khối lượng rác an toàn của một điểm thu gom."""
        if isinstance(self.evaluator.demands, dict):
            return float(self.evaluator.demands.get(point_id, 0.0))
        return float(self.evaluator.demands[point_id])

    def _get_route_load(self, route: List[int]) -> float:
        """Tính tổng tải trọng gom được của một tuyến xe."""
        return sum(self._get_demand(pt) for pt in route if pt != self.depot_index)

    def operator_2opt(self, routes: List[List[int]], current_fitness: float) -> Tuple[List[List[int]], float, bool]:
        """
        Toán tử Lân cận k=1: 2-opt (Gỡ đường chéo nội tuyến - Intra-route).

        Nguyên lý hình học:
        - Giả sử một xe có lộ trình [0, ..., A, B, ..., C, D, ..., 0] bị giao cắt giữa đoạn (A->B) và (C->D).
        - Toán tử 2-opt sẽ cắt bỏ 2 cạnh này và đảo ngược toàn bộ chuỗi điểm ở giữa: [B, ..., C] thành [C, ..., B].
        - Vì tất cả các điểm vẫn nằm trong xe đó, tổng tải trọng gom KHÔNG THAY ĐỔI -> bảo toàn 100% tính hợp lệ tải trọng!
        """
        best_routes = copy.deepcopy(routes)
        best_fit = current_fitness
        improved = False

        for r_idx in range(len(best_routes)):
            route = best_routes[r_idx]
            n = len(route)
            # Một tuyến cần tối thiểu 4 điểm (Depot, 2 điểm gom rác, Depot) để áp dụng 2-opt
            if n < 4:
                continue

            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    # Thử nghiệm đảo đoạn con từ i đến j
                    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
                    candidate_routes = [r.copy() for r in best_routes]
                    candidate_routes[r_idx] = new_route

                    candidate_fit = self.evaluator.calculate_fitness(candidate_routes)

                    if candidate_fit < best_fit - 1e-6:
                        best_fit = candidate_fit
                        best_routes = candidate_routes
                        improved = True

                        if self.strategy == "first_improvement":
                            return best_routes, best_fit, True

        return best_routes, best_fit, improved

    def operator_relocate(self, routes: List[List[int]], current_fitness: float) -> Tuple[List[List[int]], float, bool]:
        """
        Toán tử Lân cận k=2: Relocate (Rút và chèn một điểm - Intra/Inter-route).

        Nguyên lý tối ưu:
        - Rút 1 điểm thu gom u khỏi vị trí hiện tại trong Tuyến 1 và thử chèn vào Tuyến 2.
        - Lập trình phòng thủ: Kiểm tra xem Tuyến 2 sau khi nhận thêm u có vượt quá Q_max không.
          Nếu vượt tải trọng, lập tức bỏ qua phép thử này để tránh sinh nghiệm bất khả thi!
        - Bảo toàn tuyệt đối cấu trúc Depot: Mọi tuyến luôn bắt đầu bằng Depot (0) và kết thúc bằng Depot (0).
        """
        best_routes = copy.deepcopy(routes)
        best_fit = current_fitness
        improved = False

        num_routes = len(best_routes)

        for src_r in range(num_routes):
            route_src = best_routes[src_r]
            src_customers = [pt for pt in route_src if pt != self.depot_index]
            if not src_customers:
                continue

            for src_idx, node_to_move in enumerate(src_customers):
                node_demand = self._get_demand(node_to_move)

                for dst_r in range(num_routes):
                    route_dst = best_routes[dst_r]
                    dst_customers = [pt for pt in route_dst if pt != self.depot_index]

                    # Chèn nội tuyến (cùng 1 xe)
                    if src_r == dst_r:
                        if len(src_customers) <= 1:
                            continue
                        temp_customers = [p for p in src_customers]
                        temp_customers.pop(src_idx)

                        for dst_idx in range(len(temp_customers) + 1):
                            if dst_idx == src_idx:
                                continue

                            new_pts = [p for p in temp_customers]
                            new_pts.insert(dst_idx, node_to_move)

                            cand_routes = copy.deepcopy(best_routes)
                            cand_routes[src_r] = [self.depot_index] + new_pts + [self.depot_index]

                            cand_fit = self.evaluator.calculate_fitness(cand_routes)
                            if cand_fit < best_fit - 1e-6:
                                best_fit = cand_fit
                                best_routes = cand_routes
                                improved = True
                                if self.strategy == "first_improvement":
                                    return best_routes, best_fit, True

                    # Chèn liên tuyến (sang xe khác)
                    else:
                        dst_load = sum(self._get_demand(p) for p in dst_customers)
                        if dst_load + node_demand > self.capacity_q_max:
                            continue  # Vượt tải trọng xe đích

                        new_src_pts = [p for p in src_customers]
                        new_src_pts.pop(src_idx)

                        for dst_idx in range(len(dst_customers) + 1):
                            new_dst_pts = [p for p in dst_customers]
                            new_dst_pts.insert(dst_idx, node_to_move)

                            cand_routes = copy.deepcopy(best_routes)
                            cand_routes[src_r] = [self.depot_index] + new_src_pts + [self.depot_index]
                            cand_routes[dst_r] = [self.depot_index] + new_dst_pts + [self.depot_index]

                            cand_fit = self.evaluator.calculate_fitness(cand_routes)
                            if cand_fit < best_fit - 1e-6:
                                best_fit = cand_fit
                                best_routes = cand_routes
                                improved = True
                                if self.strategy == "first_improvement":
                                    return best_routes, best_fit, True

        return best_routes, best_fit, improved

    def operator_swap(self, routes: List[List[int]], current_fitness: float) -> Tuple[List[List[int]], float, bool]:
        """
        Toán tử Lân cận k=3: Swap (Hoán đổi vị trí hai điểm giữa hai xe khác nhau - Inter-route).

        Nguyên lý tối ưu:
        - Chọn 1 điểm u thuộc Xe 1 và 1 điểm v thuộc Xe 2, đổi chỗ trực tiếp 2 điểm này cho nhau.
        - Lập trình phòng thủ: Kiểm tra đồng thời cả 2 xe sau khi đổi có thỏa mãn Q_max không.
        - Bảo toàn tuyệt đối cấu trúc Depot ở 2 đầu tuyến.
        """
        best_routes = copy.deepcopy(routes)
        best_fit = current_fitness
        improved = False

        num_routes = len(best_routes)
        if num_routes < 2:
            return best_routes, best_fit, False

        for r1 in range(num_routes - 1):
            route1 = best_routes[r1]
            customers1 = [p for p in route1 if p != self.depot_index]
            if not customers1:
                continue
            load1 = sum(self._get_demand(p) for p in customers1)

            for r2 in range(r1 + 1, num_routes):
                route2 = best_routes[r2]
                customers2 = [p for p in route2 if p != self.depot_index]
                if not customers2:
                    continue
                load2 = sum(self._get_demand(p) for p in customers2)

                for pos1, node1 in enumerate(customers1):
                    demand1 = self._get_demand(node1)

                    for pos2, node2 in enumerate(customers2):
                        demand2 = self._get_demand(node2)

                        # Kiểm tra ràng buộc tải trọng cho cả 2 xe sau khi hoán đổi
                        new_load1 = load1 - demand1 + demand2
                        new_load2 = load2 - demand2 + demand1

                        if new_load1 > self.capacity_q_max or new_load2 > self.capacity_q_max:
                            continue  # Một trong hai xe bị quá tải -> Bỏ qua

                        new_c1 = [p for p in customers1]
                        new_c2 = [p for p in customers2]
                        new_c1[pos1] = node2
                        new_c2[pos2] = node1

                        cand_routes = copy.deepcopy(best_routes)
                        cand_routes[r1] = [self.depot_index] + new_c1 + [self.depot_index]
                        cand_routes[r2] = [self.depot_index] + new_c2 + [self.depot_index]

                        cand_fit = self.evaluator.calculate_fitness(cand_routes)

                        if cand_fit < best_fit - 1e-6:
                            best_fit = cand_fit
                            best_routes = cand_routes
                            improved = True

                            if self.strategy == "first_improvement":
                                return best_routes, best_fit, True

        return best_routes, best_fit, improved

    def optimize(self, initial_routes: List[List[int]]) -> Dict[str, Any]:
        """
        Vòng lặp điều khiển luân chuyển của thuật toán VND (Algorithm 1):
        1. Bắt đầu với k = 1 (toán tử 2-opt).
        2. Nếu k tìm được nghiệm tốt hơn:
           -> Chấp nhận nghiệm mới và quay về k = 1 ngay lập tức.
        3. Nếu k không tìm được cải thiện:
           -> Chuyển sang cấu trúc lân cận tiếp theo (k = k + 1).
        4. Thuật toán kết thúc khi k vượt quá 3 (đã thử hết cả 3 lân cận mà không còn cải thiện).
        """
        start_time = time.time()
        current_routes = copy.deepcopy(initial_routes)
        current_fitness = self.evaluator.calculate_fitness(current_routes)

        initial_fitness = current_fitness
        k = 1
        step_count = 0

        # Lọc bỏ các tuyến rỗng trước khi tinh chỉnh
        current_routes = [r for r in current_routes if len(r) > 2]

        while k <= 3 and step_count < self.max_no_improve:
            improved = False
            step_count += 1

            if k == 1:
                # Lân cận k=1: 2-opt
                new_routes, new_fit, improved = self.operator_2opt(current_routes, current_fitness)
            elif k == 2:
                # Lân cận k=2: Relocate
                new_routes, new_fit, improved = self.operator_relocate(current_routes, current_fitness)
            elif k == 3:
                # Lân cận k=3: Swap
                new_routes, new_fit, improved = self.operator_swap(current_routes, current_fitness)

            if improved:
                current_routes = new_routes
                current_fitness = new_fit
                # Quay về lân cận nhỏ nhất để tiếp tục đào sâu (VND core principle)
                k = 1
            else:
                # Chuyển sang lân cận tiếp theo có mức độ xáo trộn lớn hơn
                k += 1

        total_runtime = time.time() - start_time
        metrics = self.evaluator.evaluate_solution(current_routes)

        return {
            "algorithm": "Variable Neighborhood Descent (VND)",
            "initial_fitness": initial_fitness,
            "final_fitness": current_fitness,
            "improvement_pct": ((initial_fitness - current_fitness) / initial_fitness * 100.0) if initial_fitness > 0 else 0.0,
            "best_routes": current_routes,
            "metrics": metrics,
            "runtime_seconds": total_runtime,
            "total_steps": step_count
        }

    def shutdown_resources(self) -> None:
        """Giải phóng bộ nhớ và dọn dẹp tài nguyên."""
        self.history.clear()
