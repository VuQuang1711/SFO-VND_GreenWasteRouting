"""
Module Giải mã Hoán vị và Cắt tuyến (Decoder Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Cầu nối biểu diễn giữa không gian liên tục (SFO) và không gian tổ hợp rời rạc (VRP)

Tham chiếu học thuật:
- Mục 8.1 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 5.2 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Cơ chế Random-Key Encoding của Bean (1994) và Split Decoder cho bài toán CVRP.
"""

from typing import List, Dict, Union, Tuple
import numpy as np


class RouteDecoder:
    """
    Lớp đóng gói toàn bộ logic mã hóa và giải mã nghiệm định tuyến:
    1. Chuyển vector số thực liên tục của SFO thành thứ tự ưu tiên gom rác (Random-Key).
    2. Cắt chuỗi thứ tự ưu tiên thành các tuyến xe độc lập thỏa mãn tải trọng (Split Decoder).
    3. Mã hóa ngược (Re-encode) từ tuyến xe rời rạc về vector số thực để đồng bộ kết quả VND sang SFO.
    """

    def __init__(self, capacity_q_max: float = 1500.0, depot_index: int = 0):
        """
        Khởi tạo bộ giải mã tuyến xe.

        Giải thích tham số:
        - capacity_q_max: Sức chứa tối đa của thùng ép rác trên mỗi xe (kg). Dùng làm
          ngưỡng cắt để khép tuyến quay về Depot khi xe đã đầy.
        - depot_index: Chỉ số quy ước của trạm tập kết (mặc định là 0).
        """
        if capacity_q_max <= 0:
            raise ValueError(f"Lỗi khởi tạo: Sức chứa xe (capacity_q_max={capacity_q_max}) phải lớn hơn 0.")
        
        self.capacity_q_max = float(capacity_q_max)
        self.depot_index = int(depot_index)

    def random_key_to_tour(self, vector: Union[np.ndarray, List[float]]) -> np.ndarray:
        """
        Chuyển đổi vector số thực liên tục thành chuỗi thứ tự ghé thăm (Giant Tour).

        Nguyên lý (Random-Key Decoder):
        - SFO làm việc với các vector số thực trong không gian liên tục. Để biến các số thực
          này thành danh sách các điểm thu gom rời rạc, ta dùng phép sắp xếp vị trí (argsort).
        - Phần tử có giá trị nhỏ nhất trong vector sẽ có chỉ số index xuất hiện đầu tiên.
        - Kết quả tạo thành một hoán vị duy nhất của tất cả các điểm thu gom (từ 1 đến N).

        Tham số:
        - vector: Mảng 1D số thực liên tục có kích thước N (tương ứng N điểm thu gom rác).

        Trả về:
        - giant_tour: Mảng 1D chứa ID của các điểm thu gom rác (đánh số từ 1 đến N).
        """
        vec = np.asarray(vector, dtype=float)
        if vec.ndim != 1:
            raise ValueError(f"Lỗi giải mã: Vector vị trí phải là mảng 1 chiều, nhưng nhận được số chiều là {vec.ndim}.")
        if len(vec) == 0:
            raise ValueError("Lỗi giải mã: Vector vị trí rỗng, không có điểm nào để lập lộ trình.")

        # np.argsort sắp xếp các giá trị tăng dần và trả về thứ tự các chỉ số ban đầu.
        # Cộng thêm 1 để chỉ số điểm thu gom bắt đầu từ 1 (vì 0 được quy ước là Depot).
        giant_tour = np.argsort(vec) + 1
        return giant_tour

    def split_decoder(
        self,
        giant_tour: Union[np.ndarray, List[int]],
        demands: Union[np.ndarray, List[float], Dict[int, float]],
        capacity_q_max: float = None
    ) -> List[List[int]]:
        """
        Cắt chuỗi Giant Tour thành các tuyến xe hợp lệ có xét giới hạn tải trọng xe (Split Decoder).

        Nguyên lý hoạt động (Greedy First-Fit Split):
        - Thuật toán duyệt tuần tự từng điểm thu gom trong chuỗi Giant Tour.
        - Tích lũy lượng rác gom được trên xe hiện tại.
        - Nếu việc tiếp nhận thêm điểm tiếp theo làm tổng rác vượt quá sức chứa Q_max:
          -> Lập tức khép tuyến hiện tại bằng cách cho xe quay về Depot (thêm 0 vào cuối tuyến).
          -> Khởi tạo tuyến xe mới xuất phát từ Depot (bắt đầu bằng 0) để phục vụ điểm đó.
        - Đảm bảo 100% các tuyến sinh ra đều bắt đầu tại Depot 0, kết thúc tại Depot 0
          và không bao giờ bị quá tải.

        Tham số:
        - giant_tour: Danh sách hoặc mảng chứa thứ tự các điểm thu gom (không chứa Depot).
        - demands: Danh sách hoặc từ điển chứa lượng rác tại mỗi điểm (kg).
        - capacity_q_max: Tải trọng cho phép (nếu None sẽ dùng giá trị mặc định của lớp).

        Trả về:
        - routes: Danh sách các tuyến xe, mỗi tuyến là mảng các điểm: [0, c1, c2, ..., 0].
        """
        q_limit = float(capacity_q_max) if capacity_q_max is not None else self.capacity_q_max
        tour_list = [int(p) for p in giant_tour if int(p) != self.depot_index]

        if not tour_list:
            return []

        # Chuẩn hóa truy xuất lượng rác (demands)
        def get_demand(point_id: int) -> float:
            if isinstance(demands, dict):
                return float(demands.get(point_id, 0.0))
            else:
                if point_id >= len(demands):
                    raise IndexError(
                        f"Lỗi giải mã: Điểm thu gom ID={point_id} vượt quá số lượng phần tử của mảng demands ({len(demands)})."
                    )
                return float(demands[point_id])

        routes: List[List[int]] = []
        current_route: List[int] = [self.depot_index]
        current_load: float = 0.0

        for point in tour_list:
            point_demand = get_demand(point)

            if point_demand < 0:
                raise ValueError(f"Lỗi dữ liệu: Điểm thu gom {point} có lượng rác âm ({point_demand} kg).")
            if point_demand > q_limit:
                raise ValueError(
                    f"Lỗi bất khả thi: Điểm thu gom {point} có lượng rác {point_demand} kg, "
                    f"vượt quá sức chứa tối đa của xe ({q_limit} kg). Không xe nào có thể gom nổi điểm này một mình!"
                )

            # Kiểm tra nếu xe hiện tại còn đủ sức chứa để gom thêm điểm này không
            if current_load + point_demand <= q_limit:
                current_route.append(point)
                current_load += point_demand
            else:
                # Xe đầy tải: Khép tuyến về trạm tập kết Depot
                current_route.append(self.depot_index)
                routes.append(current_route)

                # Mở chuyến xe mới xuất phát từ Depot
                current_route = [self.depot_index, point]
                current_load = point_demand

        # Khép tuyến cho chiếc xe cuối cùng
        if len(current_route) > 1:
            current_route.append(self.depot_index)
            routes.append(current_route)

        return routes

    def decode(
        self,
        vector: Union[np.ndarray, List[float]],
        demands: Union[np.ndarray, List[float], Dict[int, float]],
        capacity_q_max: float = None
    ) -> List[List[int]]:
        """
        Hàm giải mã hoàn chỉnh từ vector số thực của SFO ra tập hợp các tuyến xe hợp lệ.
        Kết hợp 2 bước: random_key_to_tour -> split_decoder.
        """
        giant_tour = self.random_key_to_tour(vector)
        routes = self.split_decoder(giant_tour, demands, capacity_q_max)
        return routes

    def tour_to_random_key(self, routes: List[List[int]], dimension: int) -> np.ndarray:
        """
        Mã hóa ngược (Re-encoding): Chuyển tập hợp các tuyến xe rời rạc về vector số thực liên tục.

        Ý nghĩa sống còn trong thuật toán lai SFO-VND:
        - Khi thuật toán tìm kiếm cục bộ VND sửa đổi lộ trình (2-opt, Relocate, Swap), cấu trúc
          nghiệm rời rạc được cải thiện nhưng SFO lại hoạt động trên vector số thực liên tục.
        - Hàm này tạo ra một vector số thực mới có thứ tự tăng dần tương ứng với thứ tự các điểm
          vừa được tối ưu trong routes.
        - Nhờ đó, ta có thể cập nhật vị trí mới này trực tiếp cho cá thể Cá cờ ưu tú (Elite Sailfish),
          giúp toàn bộ quần thể SFO ở các vòng sau bơi về khu vực nghiệm mà VND vừa khai phá!

        Tham số:
        - routes: Danh sách các tuyến xe hiện tại (ví dụ: [[0, 3, 1, 0], [0, 2, 4, 0]]).
        - dimension: Số lượng điểm thu gom (số chiều của vector SFO).

        Trả về:
        - vector: Mảng 1D số thực trong khoảng [0.0, 1.0] phản ánh thứ tự tuyến mới.
        """
        ordered_points: List[int] = []
        for route in routes:
            for pt in route:
                if pt != self.depot_index and pt not in ordered_points:
                    ordered_points.append(pt)

        # Lập trình phòng thủ: nếu có điểm bị thiếu do rỗng, bổ sung các điểm còn lại
        all_points = set(range(1, dimension + 1))
        missing_points = list(all_points - set(ordered_points))
        ordered_points.extend(missing_points)

        # Tạo vector có giá trị phân bố đều tăng dần theo thứ tự ưu tiên
        vector = np.zeros(dimension, dtype=float)
        num_points = len(ordered_points)

        for rank, pt_id in enumerate(ordered_points):
            idx = pt_id - 1
            if 0 <= idx < dimension:
                # Gán giá trị tăng dần từ 0.05 đến 0.95 để giữ biên an toàn
                vector[idx] = (rank + 1) / (num_points + 1)

        return vector
