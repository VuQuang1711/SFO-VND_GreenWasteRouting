"""
Thuật toán Tối ưu hóa Cá Cờ (Sailfish Optimizer - SFO) cho Định tuyến Thu gom Rác VRP
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Khám phá toàn cục (Global Exploration) trên không gian số thực liên tục

Tham chiếu học thuật:
- Bài báo gốc: Shadravan, S., Naji, H. R., & Bardsiri, V. K. (2019). The Sailfish Optimizer:
  A novel nature-inspired metaheuristic algorithm for solving constrained engineering problems.
  Engineering Applications of Artificial Intelligence, 80, 20-34.
- Báo cáo Step 1: Mục 5.1 & 5.2 (GVHD/02_Mau_bao_cao_STEP1_SFO_VND_Green_Waste_Routing.docx)
- Mô hình Toán học: Eq. 1 đến Eq. 13 trong tài liệu SailFish.docx
"""

import time
from typing import List, Dict, Tuple, Optional, Any, Union
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


class SailfishOptimizer:
    """
    Thuật toán Sailfish Optimizer (SFO) giải bài toán Green VRP:
    - Quần thể cá cờ (Sailfish - NSF): Đóng vai trò các thợ săn tinh anh, tập trung khai thác (Intensification).
    - Quần thể cá mòi (Sardines - NS): Đóng vai trò con mồi số lượng lớn, di chuyển tán loạn để khám phá (Diversification).
    - Cầu nối giải mã: Sử dụng RouteDecoder (Random-Key + Split) để ánh xạ vector liên tục sang tuyến xe.
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
        random_seed: Optional[int] = 42
    ):
        """
        Khởi tạo thuật toán SFO.

        Giải thích giáo dục về các tham số:
        - evaluator: Bộ đánh giá tính quãng đường, nhiên liệu MEET, phát thải CO2 và chi phí.
        - decoder: Bộ giải mã chuyển vector số thực liên tục thành tuyến xe hợp lệ theo Q_max.
        - dimension: Số chiều của bài toán, tương ứng đúng bằng số lượng điểm thu gom rác (N).
        - number_of_sardines (NS): Số lượng cá mòi (con mồi). NS lớn giúp quét rộng không gian.
        - percentage_of_population (PP): Tỷ lệ cá cờ so với cá mòi (NSF = int(NS * PP)). Thường là 10-20%.
        - initial_attack_power (A): Cường độ tấn công cực đại ban đầu (mặc định A=4.0 theo Eq. 10).
        - epsilon: Hệ số suy giảm của Attack Power qua các thế hệ.
        - max_iterations: Số vòng lặp tối đa để thuật toán hội tụ.
        - random_seed: Hạt giống ngẫu nhiên cố định để đảm bảo tính tái lập (Fair Comparison).
        """
        if dimension <= 0:
            raise ValueError(f"Lỗi khởi tạo: Số chiều không gian tìm kiếm (dimension={dimension}) phải lớn hơn 0.")
        if number_of_sardines <= 0:
            raise ValueError(f"Lỗi khởi tạo: Số lượng cá mòi (number_of_sardines={number_of_sardines}) phải lớn hơn 0.")
        if not (0.0 < percentage_of_population <= 1.0):
            raise ValueError(f"Lỗi khởi tạo: Tỷ lệ cá cờ (percentage_of_population={percentage_of_population}) phải thuộc (0, 1].")
        if max_iterations <= 0:
            raise ValueError(f"Lỗi khởi tạo: Số vòng lặp (max_iterations={max_iterations}) phải lớn hơn 0.")

        self.evaluator = evaluator
        self.decoder = decoder
        self.dimension = int(dimension)
        self.number_of_sardines = int(number_of_sardines)
        self.percentage_of_population = float(percentage_of_population)
        self.initial_attack_power = float(initial_attack_power)
        self.epsilon = float(epsilon)
        self.max_iterations = int(max_iterations)
        self.random_seed = random_seed

        # Số lượng cá cờ: NSF = max(1, int(NS * PP)) theo Eq. 1 & 4
        self.number_of_sailfish = max(1, int(self.number_of_sardines * self.percentage_of_population))

        # Miền giá trị chuẩn hóa của vector Random-Key [0.0, 1.0]
        self.lower_bound = 0.0
        self.upper_bound = 1.0

        # Biến trạng thái lưu trữ nghiệm tối ưu toàn cục
        self.best_solution_vector: Optional[np.ndarray] = None
        self.best_routes: Optional[List[List[int]]] = None
        self.best_fitness: float = float("inf")
        self.best_metrics: Optional[Dict[str, Any]] = None

        # Lịch sử hội tụ (Convergence History) phục vụ XAI Dashboard
        self.convergence_curve: List[float] = []
        self.attack_power_history: List[float] = []
        self.prey_density_history: List[float] = []

        # Cờ trạng thái kiểm soát luồng (Defensive Programming)
        self.is_optimized: bool = False

    def _initialize_populations(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Khởi tạo ngẫu nhiên vị trí cho 2 quần thể trong không gian [0.0, 1.0]^d:
        - Quần thể cá cờ: Ma trận (number_of_sailfish x dimension) - Eq. 1
        - Quần thể cá mòi: Ma trận (number_of_sardines x dimension) - Eq. 4
        """
        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        sailfish = np.random.uniform(
            self.lower_bound, self.upper_bound, (self.number_of_sailfish, self.dimension)
        )
        sardines = np.random.uniform(
            self.lower_bound, self.upper_bound, (self.number_of_sardines, self.dimension)
        )
        return sailfish, sardines

    def _evaluate_individual(self, vector: np.ndarray) -> Tuple[float, List[List[int]], Dict[str, Any]]:
        """
        Hàm cầu nối đánh giá một cá thể:
        1. Giải mã vector số thực -> các tuyến xe (Split Decoder).
        2. Tính toán điểm Fitness, nhiên liệu, CO2 và chi phí (Evaluator).
        """
        routes = self.decoder.decode(vector, self.evaluator.demands)
        metrics = self.evaluator.evaluate_solution(routes)
        fitness = float(metrics["fitness"])
        return fitness, routes, metrics

    def _calculate_prey_density(self, n_sf: int, n_s: int) -> float:
        """
        Tính toán Mật độ con mồi (Prey Density - PD) theo Eq. 8 trong SailFish.pdf:
        PD = 1 - (NSF / (NSF + NS))

        Giải thích bản chất:
        - Khi tỷ lệ thợ săn ít so với con mồi, PD cao -> cá cờ có nhiều mục tiêu để săn.
        - Khi cá mòi bị bắt dần, tỷ lệ thay đổi làm giảm PD, điều hướng thuật toán chuyển
          từ thăm dò diện rộng sang co cụm săn bắt.
        """
        total = n_sf + n_s
        if total <= 0:
            return 0.0
        return 1.0 - (n_sf / total)

    def _calculate_attack_power(self, current_iter: int) -> float:
        """
        Tính toán Sức mạnh tấn công (Attack Power - AP) theo Eq. 10 trong SailFish.pdf:
        AP = A * (1 - 2 * (t + 1) * epsilon)

        Giải thích bản chất:
        - Ở các thế hệ đầu: t nhỏ -> AP >= 0.5. Toàn bộ đàn cá mòi hoảng loạn lẩn trốn,
          vị trí thay đổi trên tất cả các chiều (Exploration mạnh mẽ).
        - Ở các thế hệ sau: t lớn -> AP < 0.5. Cá cờ đã dồn cá mòi vào vòng vây, chỉ một
          số ít con mồi và một số chiều bị thay đổi (Exploitation tập trung tinh chỉnh).
        """
        ap = self.initial_attack_power * (1.0 - 2.0 * (current_iter + 1) * self.epsilon)
        return max(0.0, float(ap))

    def optimize(self) -> Dict[str, Any]:
        """
        Thực thi toàn bộ chu trình tối ưu của thuật toán Sailfish Optimizer (SFO).

        Các bước tiến hóa:
        Bước 1: Khởi tạo 2 quần thể Cá cờ và Cá mòi.
        Bước 2: Tìm cá thể Cá cờ ưu tú (Elite Sailfish) và Cá mòi bị thương (Injured Sardine).
        Bước 3: Lặp qua từng thế hệ:
          a) Cập nhật Mật độ mồi PD và hệ số lambda (Eq. 7 & 8).
          b) Cập nhật vị trí đàn Cá cờ (Eq. 6).
          c) Tính Sức mạnh tấn công AP và cập nhật đàn Cá mòi (Eq. 9, 10, 11, 12).
          d) Cơ chế Săn bắt & Chiếm lĩnh vị trí (Catching & Replacement - Eq. 13).
          e) Cập nhật lại nghiệm tốt nhất toàn cục và ghi nhận lịch sử hội tụ.
        """
        start_time = time.time()

        # Bước 1: Khởi tạo quần thể
        sailfish, sardines = self._initialize_populations()

        # Đánh giá quần thể cá cờ ban đầu
        sf_fitness = np.zeros(self.number_of_sailfish, dtype=float)
        sf_routes: List[List[List[int]]] = []
        sf_metrics: List[Dict[str, Any]] = []

        for i in range(self.number_of_sailfish):
            fit, rts, mtr = self._evaluate_individual(sailfish[i])
            sf_fitness[i] = fit
            sf_routes.append(rts)
            sf_metrics.append(mtr)

        # Đánh giá quần thể cá mòi ban đầu
        s_fitness = np.zeros(self.number_of_sardines, dtype=float)
        for j in range(self.number_of_sardines):
            fit, _, _ = self._evaluate_individual(sardines[j])
            s_fitness[j] = fit

        # Bước 2: Xác định Elite Sailfish và Injured Sardine ban đầu
        elite_idx = int(np.argmin(sf_fitness))
        elite_sailfish = sailfish[elite_idx].copy()
        elite_fitness = float(sf_fitness[elite_idx])

        injured_idx = int(np.argmin(s_fitness))
        injured_sardine = sardines[injured_idx].copy()

        # Lưu lại nghiệm tốt nhất toàn cục
        self.best_solution_vector = elite_sailfish.copy()
        self.best_routes = sf_routes[elite_idx]
        self.best_fitness = elite_fitness
        self.best_metrics = sf_metrics[elite_idx]

        self.convergence_curve.append(self.best_fitness)

        # Bước 3: Vòng lặp tiến hóa qua các thế hệ
        for t in range(self.max_iterations):
            # Tính Mật độ mồi PD (Eq. 8)
            pd = self._calculate_prey_density(self.number_of_sailfish, self.number_of_sardines)
            self.prey_density_history.append(pd)

            # Tính Sức mạnh tấn công AP (Eq. 10)
            ap = self._calculate_attack_power(t)
            self.attack_power_history.append(ap)

            # --- A. CẬP NHẬT VỊ TRÍ CÁ CỜ (PREDATORS UPDATE - Eq. 6 & 7) ---
            for i in range(self.number_of_sailfish):
                # Hệ số lambda_i điều khiển bước nhảy thích nghi theo mật độ con mồi PD
                lambda_i = 2.0 * np.random.rand() * pd - pd
                # Trọng tâm giữa thợ săn đầu đàn và con mồi bị thương nặng nhất
                target_center = (elite_sailfish + injured_sardine) / 2.0
                rand_vec = np.random.rand(self.dimension)
                
                # Eq. 6: Cá cờ bơi bao vây con mồi
                step = lambda_i * (rand_vec * target_center - sailfish[i])
                sailfish[i] = elite_sailfish - step
                sailfish[i] = np.clip(sailfish[i], self.lower_bound, self.upper_bound)

            # --- B. CẬP NHẬT VỊ TRÍ CÁ MÒI (PREY UPDATE - Eq. 9, 11, 12) ---
            if ap >= 0.5:
                # Trường hợp 1: AP >= 0.5 - Đàn cá mòi hoảng loạn, tất cả thay đổi vị trí
                for j in range(self.number_of_sardines):
                    rand_scale = np.random.rand()
                    # Eq. 9: Cá mòi di chuyển tránh xa cá cờ tinh anh có tính đến lực tấn công AP
                    sardines[j] = rand_scale * (elite_sailfish - sardines[j] + ap)
                    sardines[j] = np.clip(sardines[j], self.lower_bound, self.upper_bound)
            else:
                # Trường hợp 2: AP < 0.5 - Vòng vây siết chặt, chỉ alpha cá mòi và beta chiều cập nhật
                alpha = max(1, int(self.number_of_sardines * ap))
                beta = max(1, int(self.dimension * ap))
                
                # Chọn ngẫu nhiên alpha con cá mòi
                chosen_sardines_indices = np.random.choice(self.number_of_sardines, alpha, replace=False)
                for j_idx in chosen_sardines_indices:
                    # Chọn ngẫu nhiên beta chiều để thay đổi
                    chosen_dims = np.random.choice(self.dimension, beta, replace=False)
                    rand_scale = np.random.rand()
                    for d in chosen_dims:
                        sardines[j_idx, d] = rand_scale * (elite_sailfish[d] - sardines[j_idx, d] + ap)
                    sardines[j_idx] = np.clip(sardines[j_idx], self.lower_bound, self.upper_bound)

            # --- C. ĐÁNH GIÁ LẠI QUẦN THỂ ---
            for i in range(self.number_of_sailfish):
                fit, rts, mtr = self._evaluate_individual(sailfish[i])
                sf_fitness[i] = fit
                sf_routes[i] = rts
                sf_metrics[i] = mtr

            for j in range(self.number_of_sardines):
                fit, _, _ = self._evaluate_individual(sardines[j])
                s_fitness[j] = fit

            # --- D. SĂN BẮT VÀ THAY THẾ (CATCHING & REPLACEMENT - Eq. 13) ---
            # Nếu cá mòi có vị trí tốt hơn cá cờ, cá cờ chiếm vị trí đó
            for i in range(self.number_of_sailfish):
                for j in range(self.number_of_sardines):
                    if s_fitness[j] < sf_fitness[i]:
                        sailfish[i] = sardines[j].copy()
                        sf_fitness[i] = s_fitness[j]
                        sf_routes[i] = self.decoder.decode(sailfish[i], self.evaluator.demands)
                        sf_metrics[i] = self.evaluator.evaluate_solution(sf_routes[i])

            # Cập nhật Elite Sailfish (nghiệm tốt nhất hiện tại)
            current_best_idx = int(np.argmin(sf_fitness))
            if sf_fitness[current_best_idx] < self.best_fitness:
                self.best_fitness = float(sf_fitness[current_best_idx])
                self.best_solution_vector = sailfish[current_best_idx].copy()
                self.best_routes = sf_routes[current_best_idx]
                self.best_metrics = sf_metrics[current_best_idx]
                elite_sailfish = sailfish[current_best_idx].copy()

            # Cập nhật Injured Sardine (con mòi có fitness tốt nhất trong đàn mồi)
            injured_idx = int(np.argmin(s_fitness))
            injured_sardine = sardines[injured_idx].copy()

            # Lưu lại vào đường cong hội tụ
            self.convergence_curve.append(self.best_fitness)

        total_runtime = time.time() - start_time
        self.is_optimized = True

        return {
            "algorithm": "Sailfish Optimizer (SFO)",
            "best_fitness": self.best_fitness,
            "best_routes": self.best_routes,
            "metrics": self.best_metrics,
            "convergence_curve": self.convergence_curve,
            "runtime_seconds": total_runtime,
            "total_iterations": self.max_iterations,
            "attack_power_history": self.attack_power_history,
            "prey_density_history": self.prey_density_history
        }

    def shutdown_resources(self) -> None:
        """
        Giải phóng bộ nhớ và dọn dẹp tài nguyên (Resource Management).
        Tuân thủ quy chuẩn Universal Blueprint để tránh rò rỉ bộ nhớ khi chạy nhiều lần.
        """
        self.best_solution_vector = None
        self.best_routes = None
        self.convergence_curve.clear()
        self.attack_power_history.clear()
        self.prey_density_history.clear()
        self.is_optimized = False
