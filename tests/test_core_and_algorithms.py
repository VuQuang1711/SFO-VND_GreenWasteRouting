"""
Bộ Kiểm thử Toàn diện cho Lớp Core và Lõi Thuật toán (Test Suite)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Kiểm thử Unit Test, Kiểm thử Công thức Toán học và Kiểm thử Ứng suất Bộ nhớ
"""

import sys
import unittest
import numpy as np

# Thêm đường dẫn Source vào sys.path để import trực tiếp
sys.path.insert(0, ".")

from src.config import CAPACITY_Q_MAX, DEPOT_INDEX
from src.core.decoder import RouteDecoder
from src.core.validator import RouteValidator
from src.core.evaluator import RouteEvaluator
from src.algorithms.sfo import SailfishOptimizer
from src.algorithms.vnd import VariableNeighborhoodDescent
from src.algorithms.hybrid_sfo_vnd import HybridSFOVND
from src.baselines.greedy import GreedyNearestNeighbor


class TestGreenVRPCoreAndAlgorithms(unittest.TestCase):
    """Lớp kiểm thử các thành phần cốt lõi của hệ thống."""

    def setUp(self):
        """Khởi tạo môi trường dữ liệu mẫu cho bài toán thu gom rác mini (1 Depot + 6 điểm rác)."""
        self.num_customers = 6
        self.capacity_q_max = 100.0
        self.depot_index = 0

        # Lượng rác tại từng điểm (kg)
        self.demands = {
            0: 0.0,   # Depot
            1: 30.0,
            2: 40.0,
            3: 50.0,
            4: 25.0,
            5: 35.0,
            6: 45.0
        }

        # Tọa độ 2D đơn giản
        self.coords = {
            0: (0.0, 0.0),   # Depot
            1: (1.0, 1.0),
            2: (1.0, 3.0),
            3: (2.0, 5.0),
            4: (-2.0, 1.0),
            5: (-3.0, 3.0),
            6: (-1.0, 4.0)
        }

        # Ma trận khoảng cách Euclid 2D
        n = len(self.coords)
        self.dist_matrix = np.zeros((n, n), dtype=float)
        for i in range(n):
            for j in range(n):
                if i != j:
                    dx = self.coords[i][0] - self.coords[j][0]
                    dy = self.coords[i][1] - self.coords[j][1]
                    self.dist_matrix[i, j] = np.sqrt(dx * dx + dy * dy)

        self.decoder = RouteDecoder(capacity_q_max=self.capacity_q_max, depot_index=self.depot_index)
        self.validator = RouteValidator(capacity_q_max=self.capacity_q_max, depot_index=self.depot_index)
        self.evaluator = RouteEvaluator(
            distance_matrix=self.dist_matrix,
            demands=self.demands,
            capacity_q_max=self.capacity_q_max,
            depot_index=self.depot_index
        )

    def test_01_decoder_logic(self):
        """Kiểm tra tính đúng đắn của bộ giải mã Random-Key và Split Decoder."""
        # 1. Test Random-Key
        vector = np.array([0.7, 0.1, 0.9, 0.2, 0.5, 0.3])
        tour = self.decoder.random_key_to_tour(vector)
        # Kỳ vọng thứ tự tăng dần: idx 1 (pt 2), idx 3 (pt 4), idx 5 (pt 6), idx 4 (pt 5), idx 0 (pt 1), idx 2 (pt 3)
        expected_tour = np.array([2, 4, 6, 5, 1, 3])
        np.testing.assert_array_equal(tour, expected_tour)

        # 2. Test Split Decoder cắt tuyến theo sức chứa 100 kg
        routes = self.decoder.split_decoder(tour, self.demands, capacity_q_max=100.0)
        self.assertTrue(len(routes) >= 2)
        for r in routes:
            self.assertEqual(r[0], 0)
            self.assertEqual(r[-1], 0)
            load = sum(self.demands[pt] for pt in r if pt != 0)
            self.assertLessEqual(load, 100.0)

        # 3. Test Re-encoding (mã hóa ngược)
        reencoded = self.decoder.tour_to_random_key(routes, dimension=self.num_customers)
        self.assertEqual(len(reencoded), self.num_customers)
        self.assertTrue(np.all(reencoded >= 0.0) and np.all(reencoded <= 1.0))

    def test_02_validator_constraints(self):
        """Kiểm tra bộ thẩm định 4 ràng buộc cứng (Hard Constraints)."""
        valid_routes = [[0, 1, 2, 0], [0, 3, 4, 0], [0, 5, 6, 0]]
        is_valid, viol_count, msgs = self.validator.validate_solution(
            routes=valid_routes,
            demands=self.demands,
            total_customers=self.num_customers,
            capacity_q_max=100.0
        )
        self.assertTrue(is_valid)
        self.assertEqual(viol_count, 0)

        # Cố tình tạo vi phạm bỏ sót điểm 6 và thăm điểm 1 hai lần
        invalid_routes = [[0, 1, 2, 0], [0, 1, 3, 4, 0], [0, 5, 0]]
        is_valid2, viol_count2, msgs2 = self.validator.validate_solution(
            routes=invalid_routes,
            demands=self.demands,
            total_customers=self.num_customers,
            capacity_q_max=100.0
        )
        self.assertFalse(is_valid2)
        self.assertGreater(viol_count2, 0)

    def test_03_evaluator_meet_and_co2(self):
        """Kiểm tra công thức tính tiêu thụ nhiên liệu MEET và phát thải CO2 theo ISO 14064."""
        route = [0, 1, 2, 0]
        metrics = self.evaluator.evaluate_route(route)
        self.assertGreater(metrics["distance"], 0.0)
        self.assertGreater(metrics["fuel_liters"], 0.0)
        self.assertGreater(metrics["co2_kg"], 0.0)
        self.assertEqual(metrics["overload_kg"], 0.0)

        # Kiểm tra tỷ lệ CO2 theo ISO 14064 (2.68 kg CO2 / lít dầu)
        expected_co2 = metrics["fuel_liters"] * self.evaluator.co2_emission_factor
        self.assertAlmostEqual(metrics["co2_kg"], expected_co2, places=4)

    def test_04_greedy_baseline(self):
        """Kiểm tra thuật toán tham ăn Nearest Neighbor."""
        greedy = GreedyNearestNeighbor(evaluator=self.evaluator, capacity_q_max=100.0)
        res = greedy.solve(total_customers=self.num_customers)
        self.assertTrue(res["is_valid"])
        self.assertGreater(res["fitness"], 0.0)
        self.assertGreater(len(res["routes"]), 0)

    def test_05_vnd_local_search(self):
        """Kiểm tra khả năng cải thiện của thuật toán tìm kiếm cục bộ VND (2-opt, Relocate, Swap)."""
        # Tuyến khởi đầu hơi vòng vèo
        initial_routes = [[0, 3, 1, 2, 0], [0, 6, 4, 5, 0]]
        vnd = VariableNeighborhoodDescent(evaluator=self.evaluator, capacity_q_max=100.0)
        res = vnd.optimize(initial_routes)
        self.assertLessEqual(res["final_fitness"], res["initial_fitness"])

    def test_06_sfo_optimization(self):
        """Kiểm tra tiến trình hội tụ của thuật toán Sailfish Optimizer."""
        sfo = SailfishOptimizer(
            evaluator=self.evaluator,
            decoder=self.decoder,
            dimension=self.num_customers,
            number_of_sardines=20,
            max_iterations=15,
            random_seed=42
        )
        res = sfo.optimize()
        self.assertTrue(sfo.is_optimized)
        self.assertLess(res["best_fitness"], float("inf"))
        self.assertEqual(len(res["convergence_curve"]), 16)  # Khởi tạo + 15 vòng
        sfo.shutdown_resources()
        self.assertFalse(sfo.is_optimized)

    def test_07_hybrid_sfo_vnd(self):
        """Kiểm tra thuật toán lai ghép hoàn chỉnh Hybrid SFO-VND."""
        hybrid = HybridSFOVND(
            evaluator=self.evaluator,
            decoder=self.decoder,
            dimension=self.num_customers,
            number_of_sardines=20,
            max_iterations=15,
            vnd_trigger_interval=3,
            random_seed=42
        )
        res = hybrid.optimize()
        self.assertTrue(hybrid.is_optimized)
        self.assertLess(res["best_fitness"], float("inf"))
        self.assertGreater(len(res["convergence_curve"]), 0)
        hybrid.shutdown_resources()
        self.assertFalse(hybrid.is_optimized)


if __name__ == "__main__":
    unittest.main()
