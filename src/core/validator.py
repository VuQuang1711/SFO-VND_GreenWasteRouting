"""
Module Kiểm tra Tính Hợp lệ của Nghiệm (Solution Validator Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Thẩm định 4 ràng buộc cứng (Hard Constraints) của bài toán Green VRP

Tham chiếu học thuật:
- Mục 4.2 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 4.2 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
"""

from typing import List, Dict, Tuple, Union, Set
import numpy as np


class RouteValidator:
    """
    Lớp thẩm định tính hợp lệ của phương án định tuyến (Validation Layer).
    Đảm bảo một giải pháp chỉ được chấp nhận khi vượt qua toàn bộ 4 ràng buộc cứng.
    """

    def __init__(self, capacity_q_max: float = 1500.0, depot_index: int = 0):
        """
        Khởi tạo bộ kiểm tra ràng buộc.

        Giải thích tham số:
        - capacity_q_max: Ngưỡng tải trọng tối đa của xe (kg).
        - depot_index: Chỉ số trạm tập kết Depot (mặc định là 0).
        """
        self.capacity_q_max = float(capacity_q_max)
        self.depot_index = int(depot_index)

    def check_full_and_unique_coverage(
        self, routes: List[List[int]], total_customers: int
    ) -> Tuple[bool, str]:
        """
        Ràng buộc 1 & 2: Phục vụ đầy đủ 100% và duy nhất mỗi điểm đúng 1 lần.

        Giải thích bản chất:
        - Đơn vị thu gom môi trường không được phép bỏ sót bất kỳ thùng rác nào trên địa bàn (Full Coverage).
        - Đồng thời không được để hai xe cùng đến thu gom một thùng rác (Unique Visit), vì gây lãng phí
          nhiên liệu và xung đột lộ trình vận hành.

        Tham số:
        - routes: Danh sách các tuyến xe.
        - total_customers: Tổng số điểm thu gom cần phục vụ (N điểm, đánh số từ 1 đến N).

        Trả về:
        - (is_valid, message): True nếu thỏa mãn; False kèm lý do vi phạm chi tiết bằng Tiếng Việt.
        """
        visited_points: List[int] = []
        for r_idx, route in enumerate(routes):
            for pt in route:
                if pt != self.depot_index:
                    visited_points.append(pt)

        # Kiểm tra trùng lặp (trùng điểm)
        seen: Set[int] = set()
        duplicates: Set[int] = set()
        for pt in visited_points:
            if pt in seen:
                duplicates.add(pt)
            seen.add(pt)

        if duplicates:
            return False, f"Vi phạm tính duy nhất: Các điểm thu gom {sorted(list(duplicates))} bị ghé thăm nhiều hơn 1 lần."

        # Kiểm tra bỏ sót điểm
        required_points = set(range(1, total_customers + 1))
        missing_points = required_points - seen
        if missing_points:
            return False, f"Vi phạm độ bao phủ: Bỏ sót {len(missing_points)} điểm thu gom chưa phục vụ: {sorted(list(missing_points))}."

        # Kiểm tra xuất hiện điểm lạ ngoài danh sách
        extra_points = seen - required_points
        if extra_points:
            return False, f"Vi phạm dữ liệu: Xuất hiện các điểm lạ không có trong danh sách thu gom: {sorted(list(extra_points))}."

        return True, "Thỏa mãn: Toàn bộ 100% các điểm thu gom được phục vụ đầy đủ và duy nhất đúng 1 lần."

    def check_depot_start_and_end(self, routes: List[List[int]]) -> Tuple[bool, str]:
        """
        Ràng buộc 3: Xuất phát từ Depot và quay về đúng Depot (Depot Return Constraint).

        Giải thích bản chất:
        - Xe rác sau ca làm việc bắt buộc phải quay về bãi tập kết/trạm trung chuyển để xả rác và bảo dưỡng.
        - Mọi tuyến xe hợp lệ phải có điểm đầu tiên là Depot (0) và điểm kết thúc là Depot (0).
        """
        for r_idx, route in enumerate(routes):
            if not route:
                continue
            if route[0] != self.depot_index:
                return False, f"Vi phạm Depot ở Tuyến xe #{r_idx + 1}: Tuyến xe không bắt đầu tại Depot {self.depot_index} (bắt đầu tại {route[0]})."
            if route[-1] != self.depot_index:
                return False, f"Vi phạm Depot ở Tuyến xe #{r_idx + 1}: Tuyến xe không kết thúc quay về Depot {self.depot_index} (kết thúc tại {route[-1]})."

        return True, "Thỏa mãn: Tất cả các tuyến xe đều xuất phát từ Depot và kết thúc quay về đúng Depot."

    def check_capacity(
        self,
        routes: List[List[int]],
        demands: Union[np.ndarray, List[float], Dict[int, float]],
        capacity_q_max: float = None
    ) -> Tuple[bool, str]:
        """
        Ràng buộc 4: Không có xe nào bị vượt quá tải trọng cho phép (Capacity Constraint).

        Giải thích bản chất:
        - Thùng chứa xe rác có dung tích và tải trọng giới hạn vật lý. Nếu chở quá tải trọng,
          xe sẽ vi phạm luật giao thông đường bộ và gây mất an toàn cơ học khi ép rác.
        """
        q_limit = float(capacity_q_max) if capacity_q_max is not None else self.capacity_q_max

        def get_demand(point_id: int) -> float:
            if isinstance(demands, dict):
                return float(demands.get(point_id, 0.0))
            return float(demands[point_id])

        for r_idx, route in enumerate(routes):
            total_load = sum(get_demand(pt) for pt in route if pt != self.depot_index)
            if total_load > q_limit:
                return (
                    False,
                    f"Vi phạm tải trọng ở Tuyến xe #{r_idx + 1}: Tổng khối lượng rác gom là {total_load:.2f} kg, "
                    f"vượt quá sức chứa tối đa {q_limit:.2f} kg (vượt {(total_load - q_limit):.2f} kg)."
                )

        return True, "Thỏa mãn: Không có xe nào bị vượt quá tải trọng thiết kế."

    def validate_solution(
        self,
        routes: List[List[int]],
        demands: Union[np.ndarray, List[float], Dict[int, float]],
        total_customers: int,
        capacity_q_max: float = None,
        max_vehicles: int = None
    ) -> Tuple[bool, int, List[str]]:
        """
        Tổng hợp kiểm tra toàn diện cả 4 điều kiện cứng của phương án lộ trình.

        Trả về:
        - is_valid (bool): True nếu phương án hoàn toàn khả thi (feasible).
        - violation_count (int): Số lượng lỗi vi phạm phát hiện được.
        - messages (List[str]): Danh sách báo cáo chi tiết từng vi phạm.
        """
        violations: List[str] = []

        # 1. Kiểm tra bao phủ và duy nhất
        ok_cov, msg_cov = self.check_full_and_unique_coverage(routes, total_customers)
        if not ok_cov:
            violations.append(msg_cov)

        # 2. Kiểm tra Depot
        ok_depot, msg_depot = self.check_depot_start_and_end(routes)
        if not ok_depot:
            violations.append(msg_depot)

        # 3. Kiểm tra tải trọng
        ok_cap, msg_cap = self.check_capacity(routes, demands, capacity_q_max)
        if not ok_cap:
            violations.append(msg_cap)

        # 4. Kiểm tra giới hạn số lượng xe (nếu có cấu hình)
        if max_vehicles is not None and len(routes) > max_vehicles:
            violations.append(
                f"Vi phạm số lượng xe: Sử dụng {len(routes)} xe, vượt quá số lượng xe sẵn có của đội ({max_vehicles} xe)."
            )

        is_valid = (len(violations) == 0)
        return is_valid, len(violations), violations
