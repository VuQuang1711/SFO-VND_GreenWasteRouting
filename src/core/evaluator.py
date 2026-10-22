"""
Module Đánh giá Hàm Mục tiêu & Phát thải Môi trường (Evaluator Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Tính toán Quãng đường, Nhiên liệu theo MEET, Phát thải CO2 theo ISO 14064, Chi phí và Fitness

Tham chiếu học thuật:
- Mục 6.2 của Bản mô tả đề tài (Mô hình MEET - GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 4.3 & 4.4 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Khuyến nghị của GVHD về mô hình tiêu thụ nhiên liệu phụ thuộc tải trọng tuyến tính (Load-dependent Model)
"""

from typing import List, Dict, Tuple, Union, Any
import numpy as np

from ..config import (
    DEPOT_INDEX,
    EMPTY_FUEL_RATE_L_PER_KM,
    LOAD_FUEL_FACTOR_L_PER_KM_PER_KG,
    EMISSION_FACTOR_CO2_PER_LITER,
    FUEL_PRICE_VND_PER_LITER,
    CARBON_COST_VND_PER_KG,
    PENALTY_WEIGHT,
    CAPACITY_Q_MAX
)


class RouteEvaluator:
    """
    Lớp đánh giá chất lượng nghiệm định tuyến (Evaluation Layer):
    1. Tính tổng quãng đường di chuyển thực tế của đội xe (km).
    2. Tính lượng nhiên liệu tiêu hao theo tải trọng tích lũy động (mô hình MEET).
    3. Tính lượng khí nhà kính CO2 xả ra môi trường (chuẩn ISO 14064).
    4. Tính chi phí kinh tế vận hành và điểm số thích nghi (Fitness Score).
    """

    def __init__(
        self,
        distance_matrix: Union[np.ndarray, List[List[float]]],
        demands: Union[np.ndarray, List[float], Dict[int, float]],
        capacity_q_max: float = CAPACITY_Q_MAX,
        depot_index: int = DEPOT_INDEX,
        empty_fuel_rate: float = EMPTY_FUEL_RATE_L_PER_KM,
        load_fuel_factor: float = LOAD_FUEL_FACTOR_L_PER_KM_PER_KG,
        co2_emission_factor: float = EMISSION_FACTOR_CO2_PER_LITER,
        fuel_price: float = FUEL_PRICE_VND_PER_LITER,
        carbon_cost: float = CARBON_COST_VND_PER_KG,
        penalty_weight: float = PENALTY_WEIGHT,
        benchmark_mode: bool = False
    ):
        """
        Khởi tạo bộ đánh giá hàm mục tiêu.

        Giải thích tham số:
        - distance_matrix: Ma trận khoảng cách N x N giữa tất cả các điểm (đơn vị: km hoặc mét quy đổi).
        - demands: Danh sách lượng rác tại từng điểm thu gom (kg).
        - benchmark_mode: Nếu True, hàm mục tiêu ưu tiên tối ưu khoảng cách thuần túy để đối chiếu
          với Best Known Solution (BKS) của CVRPLIB; nếu False, tối ưu chi phí xanh tổng hợp (Nhiên liệu + CO2).
        """
        self.distance_matrix = np.asarray(distance_matrix, dtype=float)
        if self.distance_matrix.ndim != 2 or self.distance_matrix.shape[0] != self.distance_matrix.shape[1]:
            raise ValueError(
                f"Lỗi ma trận: Ma trận khoảng cách phải là ma trận vuông 2 chiều, nhận được shape {self.distance_matrix.shape}."
            )

        self.demands = demands
        self.capacity_q_max = float(capacity_q_max)
        self.depot_index = int(depot_index)
        self.empty_fuel_rate = float(empty_fuel_rate)
        self.load_fuel_factor = float(load_fuel_factor)
        self.co2_emission_factor = float(co2_emission_factor)
        self.fuel_price = float(fuel_price)
        self.carbon_cost = float(carbon_cost)
        self.penalty_weight = float(penalty_weight)
        self.benchmark_mode = bool(benchmark_mode)

    def _get_demand(self, point_id: int) -> float:
        """Truy xuất khối lượng rác tại điểm thu gom an toàn."""
        if isinstance(self.demands, dict):
            return float(self.demands.get(point_id, 0.0))
        return float(self.demands[point_id])

    def evaluate_route(self, route: List[int]) -> Dict[str, float]:
        """
        Đánh giá chi tiết từng chỉ số vận hành cho một tuyến xe đơn lẻ:
        Lộ trình mẫu: [0, c1, c2, ..., cm, 0]

        Bản chất vật lý của mô hình MEET (Load-dependent Consumption):
        - Đoạn 0 -> c1: Xe chạy từ bãi tập kết với thùng rỗng, tải gom = 0.
        - Đoạn c1 -> c2: Xe đã thu gom điểm c1, tải trọng trên xe = demand(c1).
        - Đoạn ci -> ci+1: Tải trọng tích lũy tăng dần = sum(demand(c1..ci)).
        - Đoạn cm -> 0: Xe chở toàn bộ rác gom được chạy về trạm trung chuyển, đây là chặng
          nặng nhất và tiêu hao nhiên liệu trên mỗi km lớn nhất.
        """
        if not route or len(route) < 2:
            return {
                "distance": 0.0,
                "fuel_liters": 0.0,
                "co2_kg": 0.0,
                "total_load_kg": 0.0,
                "overload_kg": 0.0
            }

        total_distance = 0.0
        total_fuel = 0.0
        current_load = 0.0

        for i in range(len(route) - 1):
            u = route[i]
            v = route[i + 1]

            # Khoảng cách giữa 2 điểm liên tiếp trên mạng đường bộ
            dist = self.distance_matrix[u, v]
            total_distance += dist

            # Nếu điểm xuất phát u là điểm thu gom (khác Depot), cộng dồn rác vừa bốc lên xe
            if u != self.depot_index:
                current_load += self._get_demand(u)

            # Suất tiêu thụ nhiên liệu biến thiên theo tải trọng tích lũy (Lít / km)
            # f(L) = f_empty + alpha * L
            fuel_rate = self.empty_fuel_rate + self.load_fuel_factor * current_load
            segment_fuel = dist * fuel_rate
            total_fuel += segment_fuel

        # Tổng khối lượng gom trên cả chuyến xe
        total_load = current_load
        overload = max(0.0, total_load - self.capacity_q_max)

        # Lượng phát thải CO2 theo tiêu chuẩn ISO 14064 (kg CO2)
        co2_emitted = total_fuel * self.co2_emission_factor

        return {
            "distance": total_distance,
            "fuel_liters": total_fuel,
            "co2_kg": co2_emitted,
            "total_load_kg": total_load,
            "overload_kg": overload
        }

    def evaluate_solution(self, routes: List[List[int]]) -> Dict[str, Any]:
        """
        Đánh giá tổng hợp toàn bộ phương án định tuyến của đội xe:
        - Tổng quãng đường (km)
        - Tổng nhiên liệu tiêu thụ (Lít)
        - Tổng phát thải carbon CO2 (kg)
        - Tổng chi phí tài chính (VNĐ)
        - Hệ số sử dụng tải trọng bình quân (%)
        - Giá trị hàm mục tiêu (Fitness Score)
        """
        total_distance = 0.0
        total_fuel = 0.0
        total_co2 = 0.0
        total_overload = 0.0
        total_load = 0.0
        active_vehicles = 0

        route_details = []

        for r in routes:
            # Bỏ qua các tuyến xe rỗng chỉ có [0, 0] hoặc [0]
            non_depot_nodes = [pt for pt in r if pt != self.depot_index]
            if not non_depot_nodes:
                continue

            active_vehicles += 1
            metrics = self.evaluate_route(r)
            total_distance += metrics["distance"]
            total_fuel += metrics["fuel_liters"]
            total_co2 += metrics["co2_kg"]
            total_overload += metrics["overload_kg"]
            total_load += metrics["total_load_kg"]
            route_details.append(metrics)

        # 1. Chi phí vận hành tài chính (tiền dầu)
        fuel_cost = total_fuel * self.fuel_price

        # 2. Chi phí phát thải môi trường (thuế/trọng số carbon)
        carbon_cost = total_co2 * self.carbon_cost

        # 3. Tiền phạt vi phạm tải trọng (Penalty)
        penalty_cost = total_overload * self.penalty_weight

        # 4. Tính toán hàm mục tiêu Fitness
        if self.benchmark_mode:
            # Ở chế độ Benchmark CVRPLIB: Mục tiêu chính là tổng khoảng cách (để khớp BKS)
            fitness = total_distance + penalty_cost
        else:
            # Ở chế độ Case Study Xanh: Mục tiêu chính là tổng chi phí tài chính + phát thải + phạt
            fitness = fuel_cost + carbon_cost + penalty_cost

        # Hệ số sử dụng tải trọng trung bình (%)
        max_possible_load = active_vehicles * self.capacity_q_max
        capacity_utilization = (total_load / max_possible_load * 100.0) if max_possible_load > 0 else 0.0

        return {
            "fitness": fitness,
            "total_distance_km": total_distance,
            "total_fuel_liters": total_fuel,
            "total_co2_kg": total_co2,
            "fuel_cost_vnd": fuel_cost,
            "carbon_cost_vnd": carbon_cost,
            "penalty_cost_vnd": penalty_cost,
            "active_vehicles": active_vehicles,
            "capacity_utilization_pct": capacity_utilization,
            "is_feasible": (total_overload == 0.0),
            "route_details": route_details
        }

    def calculate_fitness(self, routes: List[List[int]]) -> float:
        """Hàm rút gọn trả về điểm số thích nghi (Fitness) cho thuật toán tối ưu."""
        result = self.evaluate_solution(routes)
        return float(result["fitness"])
