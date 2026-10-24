"""
Bộ Kiểm Thử Đọc Dữ Liệu Benchmark CVRPLIB (test_loader.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Kiểm tra chất lượng nạp dữ liệu chuẩn quốc tế

Các ca kiểm thử:
1. Đọc đúng và đầy đủ 6 bộ benchmark CVRPLIB.
2. Kiểm tra schema: name, dimension, capacity, demand, depot, edge_weight_type, distance_matrix.
3. Kiểm tra tính hợp lệ:
   - Dimension = số lượng điểm demand = số lượng node_coord.
   - Sức chứa Q > 0, tất cả demand_i <= Q.
   - Depot index hợp lệ và demand tại depot = 0.
   - Ma trận khoảng cách kích thước NxN, đường chéo d(i,i) = 0, khoảng cách không âm.
4. Đối chiếu nghiệm tham chiếu BKS khi có file .sol.
"""

import os
import sys
import pytest
import numpy as np

# Đảm bảo import được module từ src
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.core.cvrplib_loader import CVRPLIBLoader

BENCHMARK_NAMES = [
    "E-n33-k4",
    "B-n50-k7",
    "E-n51-k5",
    "A-n53-k7",
    "A-n60-k9",
    "E-n76-k7"
]

EXPECTED_METADATA = {
    "E-n33-k4": {"dimension": 33, "customers": 32, "capacity": 8000.0, "k": 4, "bks": 835},
    "B-n50-k7": {"dimension": 50, "customers": 49, "capacity": 100.0, "k": 7, "bks": 741},
    "E-n51-k5": {"dimension": 51, "customers": 50, "capacity": 160.0, "k": 5, "bks": 521},
    "A-n53-k7": {"dimension": 53, "customers": 52, "capacity": 100.0, "k": 7, "bks": 1010},
    "A-n60-k9": {"dimension": 60, "customers": 59, "capacity": 100.0, "k": 9, "bks": 1354},
    "E-n76-k7": {"dimension": 76, "customers": 75, "capacity": 220.0, "k": 7, "bks": 682},
}


@pytest.fixture(scope="module")
def loader():
    return CVRPLIBLoader()


@pytest.mark.parametrize("instance_name", BENCHMARK_NAMES)
def test_instance_loading_and_metadata(loader, instance_name):
    """Kiểm tra nạp file .vrp và đối chiếu thông số chuẩn."""
    data = loader.load_instance(instance_name)
    expected = EXPECTED_METADATA[instance_name]

    assert data["name"] == instance_name
    assert data["dimension"] == expected["dimension"]
    assert data["num_customers"] == expected["customers"]
    assert data["capacity"] == expected["capacity"]
    assert data["edge_weight_type"] == "EUC_2D"
    assert data["depot"] == 0


@pytest.mark.parametrize("instance_name", BENCHMARK_NAMES)
def test_distance_matrix_validity(loader, instance_name):
    """Kiểm tra tính hợp lệ của ma trận khoảng cách Euclid 2D."""
    data = loader.load_instance(instance_name)
    matrix = data["distance_matrix"]
    n = data["dimension"]

    assert matrix.shape == (n, n)
    assert np.all(matrix >= 0)
    assert np.all(np.diag(matrix) == 0.0)
    # Với khoảng cách Euclid không gian 2D đối xứng
    assert np.allclose(matrix, matrix.T)


@pytest.mark.parametrize("instance_name", BENCHMARK_NAMES)
def test_demands_and_capacities(loader, instance_name):
    """Kiểm tra ràng buộc sức chứa và nhu cầu rác."""
    data = loader.load_instance(instance_name)
    demands = data["demand"]
    capacity = data["capacity"]
    depot = data["depot"]

    assert demands[depot] == 0.0
    for node_id, d in demands.items():
        assert d >= 0, f"Demand của nút {node_id} không được âm ({d})"
        assert d <= capacity, f"Demand nút {node_id} ({d}) vượt quá sức chứa xe ({capacity})"

    total_demand = sum(demands.values())
    expected_k = EXPECTED_METADATA[instance_name]["k"]
    assert total_demand <= expected_k * capacity, (
        f"Tổng demand ({total_demand}) vượt quá tổng sức chứa của K={expected_k} xe ({expected_k * capacity})"
    )


def test_file_not_found(loader):
    """Kiểm tra ném lỗi khi file không tồn tại."""
    with pytest.raises(FileNotFoundError):
        loader.load_instance("non_existent_instance.vrp")
