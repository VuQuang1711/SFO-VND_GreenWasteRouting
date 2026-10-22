"""
Thuật toán Lai Ghép SFO-VND (Hybrid Sailfish Optimizer - Variable Neighborhood Descent)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Kiến trúc lai ghép hoàn chỉnh kết hợp Khám phá Toàn cục (SFO) và Khai thác Cục bộ (VND)

Tham chiếu học thuật:
- Mục 8 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 5.1 & 5.3 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Bảng ánh xạ code trong Viet so bo code.pdf (Trang 3 & 4)
"""

import time
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

from ..config import (
    DEFAULT_NUMBER_OF_SARDINES,
    DEFAULT_PERCENTAGE_OF_POPULATION,
    DEFAULT_INITIAL_ATTACK_POWER,
    DEFAULT_ATTACK_POWER_EPSILON,
    DEFAULT_MAX_ITERATIONS,
    CAPACITY_Q_MAX
)
from ..core.decoder import RouteDecoder
from ..core.evaluator import RouteEvaluator
from .vnd import VariableNeighborhoodDescent


class HybridSFOVND:
    """
    Thuật toán lai ghép hoàn chỉnh SFO-VND cho bài toán Green VRP:
    1. SFO: Tìm kiếm trên không gian số thực để khám phá đa dạng các cụm nghiệm tiềm năng.
    2. RouteDecoder: Chuyển vector số thực thành các tuyến xe hợp lệ thỏa mãn Q_max.
    3. VND: Can thiệp sâu vào cá thể Elite bằng 3 toán tử (2-opt -> Relocate -> Swap).
    4. Re-encoding: Mã hóa ngược tuyến xe tối ưu về vector số thực để đồng bộ lại cho quần thể SFO.
    """

    def __init__(
        self,
        evaluator: RouteEvaluator,
        decoder: RouteDecoder,
        dimension: int,
        number_of_sardines: int = DEFAULT_NUMBER_OF_SARDINES,
        percentage_of_population: float = DEFAULT_PERCENTAGE_OF_POPULATION,
        initial_attack_power: float = DEFAULT_INITIAL_ATTACK_POWER,
        epsilon: float = DEFAULT_ATTACK_POWER_EPSILON,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        vnd_trigger_interval: int = 5,
        random_seed: Optional[int] = 42
    ):
        """
        Khởi tạo thuật toán lai SFO-VND.

        Giải thích giáo dục:
        - vnd_trigger_interval: Chu kỳ kích hoạt VND (ví dụ: cứ mỗi 5 vòng lặp hoặc mỗi khi tìm thấy
          Elite mới). Việc giới hạn tần suất gọi VND giúp kiểm soát thời gian chạy (Runtime)
          như đã phân tích tại Mục 6.2 của Báo cáo Step 1, tránh tính toán quá tải cho hàm MEET.
        """
        if dimension <= 0:
            raise ValueError(f"Lỗi khởi tạo: Số chiều bài toán ({dimension}) phải lớn hơn 0.")

        self.evaluator = evaluator
        self.decoder = decoder
        self.dimension = int(dimension)
        self.number_of_sardines = int(number_of_sardines)
        self.percentage_of_population = float(percentage_of_population)
        self.initial_attack_power = float(initial_attack_power)
        self.epsilon = float(epsilon)
        self.max_iterations = int(max_iterations)
        self.vnd_trigger_interval = int(vnd_trigger_interval)
        self.random_seed = random_seed

        # Khởi tạo bộ tìm kiếm cục bộ VND đi kèm
        self.vnd = VariableNeighborhoodDescent(
            evaluator=self.evaluator,
            capacity_q_max=self.decoder.capacity_q_max,
            depot_index=self.decoder.depot_index,
            strategy="first_improvement"
        )

        # Số lượng cá cờ trong quần thể
        self.number_of_sailfish = max(1, int(self.number_of_sardines * self.percentage_of_population))
        self.lower_bound = 0.0
        self.upper_bound = 1.0

        # Biến lưu trữ kết quả tốt nhất
        self.best_solution_vector: Optional[np.ndarray] = None
        self.best_routes: Optional[List[List[int]]] = None
        self.best_fitness: float = float("inf")
        self.best_metrics: Optional[Dict[str, Any]] = None

        # Lịch sử hội tụ phục vụ XAI Dashboard
        self.convergence_curve: List[float] = []
        self.vnd_improvements: List[Dict[str, Any]] = []

        # Cờ kiểm soát trạng thái
        self.is_optimized: bool = False

    def optimize(self) -> Dict[str, Any]:
        """
        Thực thi toàn bộ quy trình tối ưu hóa lai ghép SFO-VND:

        Luồng xử lý:
        1. Khởi tạo 2 quần thể Cá cờ và Cá mòi.
        2. Vòng lặp tiến hóa qua t = 1..max_iterations:
           - SFO cập nhật vị trí Cá cờ (Eq. 6) và Cá mòi (Eq. 9, 11, 12).
           - SFO thế chỗ cá thể theo cơ chế săn bắt (Eq. 13).
           - Khi đến chu kỳ kích hoạt VND hoặc khi cá cờ đầu đàn tìm được kỷ lục mới:
             -> Giải mã tuyến xe của Elite Sailfish.
             -> Gọi VND (2-opt -> Relocate -> Swap) tinh chỉnh sâu lộ trình.
             -> Nếu VND cải thiện được:
                + Cập nhật Best Routes và Best Fitness.
                + Mã hóa ngược (Re-encode) tuyến mới thành vector số thực.
                + Ghi đè vector mới này vào cá thể Elite trong quần thể SFO!
           - Ghi nhận lịch sử hội tụ qua từng thế hệ.
        """
        start_time = time.time()

        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        # Khởi tạo quần thể ngẫu nhiên
        sailfish = np.random.uniform(
            self.lower_bound, self.upper_bound, (self.number_of_sailfish, self.dimension)
        )
        sardines = np.random.uniform(
            self.lower_bound, self.upper_bound, (self.number_of_sardines, self.dimension)
        )

        # Đánh giá fitness ban đầu của Cá cờ
        sf_fitness = np.zeros(self.number_of_sailfish, dtype=float)
        sf_routes: List[List[List[int]]] = []
        for i in range(self.number_of_sailfish):
            rts = self.decoder.decode(sailfish[i], self.evaluator.demands)
            fit = self.evaluator.calculate_fitness(rts)
            sf_fitness[i] = fit
            sf_routes.append(rts)

        # Đánh giá fitness ban đầu của Cá mòi
        s_fitness = np.zeros(self.number_of_sardines, dtype=float)
        for j in range(self.number_of_sardines):
            rts = self.decoder.decode(sardines[j], self.evaluator.demands)
            s_fitness[j] = self.evaluator.calculate_fitness(rts)

        # Tìm Elite Sailfish và Injured Sardine
        elite_idx = int(np.argmin(sf_fitness))
        elite_sailfish = sailfish[elite_idx].copy()
        elite_fitness = float(sf_fitness[elite_idx])

        injured_idx = int(np.argmin(s_fitness))
        injured_sardine = sardines[injured_idx].copy()

        self.best_solution_vector = elite_sailfish.copy()
        self.best_routes = sf_routes[elite_idx]
        self.best_fitness = elite_fitness
        self.best_metrics = self.evaluator.evaluate_solution(self.best_routes)

        self.convergence_curve.append(self.best_fitness)

        # Vòng lặp tiến hóa chính
        for t in range(self.max_iterations):
            # 1. Tính toán Mật độ con mồi (PD) và Sức mạnh tấn công (AP)
            total_pop = self.number_of_sailfish + self.number_of_sardines
            pd = 1.0 - (self.number_of_sailfish / total_pop)
            ap = max(0.0, self.initial_attack_power * (1.0 - 2.0 * (t + 1) * self.epsilon))

            # 2. Cập nhật vị trí Cá cờ (Eq. 6)
            for i in range(self.number_of_sailfish):
                lambda_i = 2.0 * np.random.rand() * pd - pd
                target_center = (elite_sailfish + injured_sardine) / 2.0
                rand_vec = np.random.rand(self.dimension)
                step = lambda_i * (rand_vec * target_center - sailfish[i])
                sailfish[i] = np.clip(elite_sailfish - step, self.lower_bound, self.upper_bound)

            # 3. Cập nhật vị trí Cá mòi (Eq. 9, 11, 12)
            if ap >= 0.5:
                for j in range(self.number_of_sardines):
                    rand_scale = np.random.rand()
                    sardines[j] = np.clip(
                        rand_scale * (elite_sailfish - sardines[j] + ap),
                        self.lower_bound,
                        self.upper_bound
                    )
            else:
                alpha = max(1, int(self.number_of_sardines * ap))
                beta = max(1, int(self.dimension * ap))
                chosen_sardines = np.random.choice(self.number_of_sardines, alpha, replace=False)
                for j_idx in chosen_sardines:
                    chosen_dims = np.random.choice(self.dimension, beta, replace=False)
                    rand_scale = np.random.rand()
                    for d in chosen_dims:
                        sardines[j_idx, d] = rand_scale * (elite_sailfish[d] - sardines[j_idx, d] + ap)
                    sardines[j_idx] = np.clip(sardines[j_idx], self.lower_bound, self.upper_bound)

            # 4. Đánh giá lại toàn bộ quần thể
            for i in range(self.number_of_sailfish):
                rts = self.decoder.decode(sailfish[i], self.evaluator.demands)
                fit = self.evaluator.calculate_fitness(rts)
                sf_fitness[i] = fit
                sf_routes[i] = rts

            for j in range(self.number_of_sardines):
                rts = self.decoder.decode(sardines[j], self.evaluator.demands)
                s_fitness[j] = self.evaluator.calculate_fitness(rts)

            # 5. Săn bắt và Thế chỗ (Catching & Replacement - Eq. 13)
            for i in range(self.number_of_sailfish):
                for j in range(self.number_of_sardines):
                    if s_fitness[j] < sf_fitness[i]:
                        sailfish[i] = sardines[j].copy()
                        sf_fitness[i] = s_fitness[j]
                        sf_routes[i] = self.decoder.decode(sailfish[i], self.evaluator.demands)

            # 6. Kiểm tra xem có kỷ lục SFO mới không
            current_best_idx = int(np.argmin(sf_fitness))
            found_new_best = sf_fitness[current_best_idx] < self.best_fitness

            if found_new_best:
                self.best_fitness = float(sf_fitness[current_best_idx])
                self.best_solution_vector = sailfish[current_best_idx].copy()
                self.best_routes = sf_routes[current_best_idx]
                elite_sailfish = sailfish[current_best_idx].copy()

            # 7. KÍCH HOẠT LAI GHÉP VND (LOCAL EXPLOITATION TRÊN ELITE)
            # Kích hoạt khi tìm thấy kỷ lục mới hoặc theo chu kỳ định kỳ
            should_run_vnd = found_new_best or ((t + 1) % self.vnd_trigger_interval == 0)

            if should_run_vnd and self.best_routes:
                vnd_res = self.vnd.optimize(self.best_routes)
                vnd_fit = float(vnd_res["final_fitness"])

                # Nếu VND tìm được lộ trình tốt hơn cả SFO
                if vnd_fit < self.best_fitness - 1e-6:
                    improve_amount = self.best_fitness - vnd_fit
                    self.vnd_improvements.append({
                        "iteration": t + 1,
                        "before_fitness": self.best_fitness,
                        "after_fitness": vnd_fit,
                        "improvement": improve_amount
                    })

                    self.best_fitness = vnd_fit
                    self.best_routes = vnd_res["best_routes"]

                    # ĐỒNG BỘ NGƯỢC (RE-ENCODING): Biến tuyến rời rạc thành vector liên tục
                    # và cập nhật trực tiếp vào cá thể Elite của SFO!
                    reencoded_vector = self.decoder.tour_to_random_key(self.best_routes, self.dimension)
                    sailfish[current_best_idx] = reencoded_vector.copy()
                    sf_fitness[current_best_idx] = self.best_fitness
                    sf_routes[current_best_idx] = self.best_routes
                    elite_sailfish = reencoded_vector.copy()

            # Cập nhật Injured Sardine
            injured_idx = int(np.argmin(s_fitness))
            injured_sardine = sardines[injured_idx].copy()

            # Ghi nhận đường cong hội tụ
            self.convergence_curve.append(self.best_fitness)

        total_runtime = time.time() - start_time
        self.best_metrics = self.evaluator.evaluate_solution(self.best_routes)
        self.is_optimized = True

        return {
            "algorithm": "Hybrid SFO-VND",
            "best_fitness": self.best_fitness,
            "best_routes": self.best_routes,
            "metrics": self.best_metrics,
            "convergence_curve": self.convergence_curve,
            "vnd_improvements": self.vnd_improvements,
            "runtime_seconds": total_runtime,
            "total_iterations": self.max_iterations
        }

    def shutdown_resources(self) -> None:
        """Giải phóng bộ nhớ và dọn dẹp tài nguyên."""
        self.best_solution_vector = None
        self.best_routes = None
        self.convergence_curve.clear()
        self.vnd_improvements.clear()
        self.vnd.shutdown_resources()
        self.is_optimized = False
