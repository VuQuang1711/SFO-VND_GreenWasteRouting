"""
Bộ Kiểm Thử Toàn Diện Cho Toy Instance 12 Điểm (test_toy_instance.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác đô thị bằng thuật toán lai SFO-VND
Quy chuẩn: Step 2 - Công việc 2.4 (Mục 13)

Kiểm tra nghiêm ngặt 8 trường hợp:
1. Trường hợp chuẩn (Valid Instance): Nghiệm khả thi qua toàn bộ các ràng buộc.
2. Trường hợp ID trùng (Duplicate ID).
3. Trường hợp Demand âm hoặc thiếu (Negative/Missing demand).
4. Trường hợp Nhu cầu tại một điểm vượt sức chứa q_i > Q (Demand exceeds capacity).
5. Trường hợp Thiếu trạm tập kết Depot (Missing depot).
6. Trường hợp Điểm không thể đến hoặc không thể về depot (Unreachable node/dead end).
7. Trường hợp Số xe sử dụng vượt quá K (Vehicles exceed fleet size).
8. Trường hợp Một điểm bị phục vụ lặp lại hoặc bị bỏ sót (Duplicate or omitted customer).
"""

import os
import sys
import json
import pytest
import numpy as np
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

TOY_DIR = os.path.join(root_dir, "data", "toy")


def load_toy_files():
    """Hàm phụ trợ tải dữ liệu toy instance gốc."""
    csv_path = os.path.join(TOY_DIR, "toy_12_points.csv")
    json_path = os.path.join(TOY_DIR, "toy_instance.json")
    routes_path = os.path.join(TOY_DIR, "toy_feasible_routes.json")

    df = pd.read_csv(csv_path)
    with open(json_path, "r", encoding="utf-8") as f:
        instance = json.load(f)
    with open(routes_path, "r", encoding="utf-8") as f:
        routes = json.load(f)

    return df, instance, routes


def validate_routes(df, instance, routes_payload):
    """
    Hàm kiểm định toàn diện một phương án định tuyến trên Toy Instance.
    Ném lỗi AssertionError/ValueError nếu vi phạm bất kỳ điều kiện nào.
    """
    points = df["point_id"].tolist()
    depot_id = instance["depot_id"]
    capacity_q = instance["capacity_q"]
    fleet_k = instance["fleet_k"]
    dist_matrix = np.array(instance["distance_matrix"])

    # 1. Kiểm tra ID trùng
    if len(points) != len(set(points)):
        raise ValueError("LỖI: Tồn tại point_id bị trùng lặp!")

    # 2. Kiểm tra Depot tồn tại
    if depot_id not in points:
        raise ValueError(f"LỖI: Không tìm thấy Depot ID {depot_id}!")

    # 3. Kiểm tra Demand
    demands = instance["demands"]
    for pid_str, d in demands.items():
        pid = int(pid_str)
        if pid == depot_id:
            if d != 0.0:
                raise ValueError(f"LỖI: Depot phải có demand bằng 0 (nhận {d})!")
        else:
            if d is None or np.isnan(d) or d < 0:
                raise ValueError(f"LỖI: Demand của điểm {pid} bị âm hoặc thiếu ({d})!")
            if d > capacity_q:
                raise ValueError(f"LỖI: Demand điểm {pid} ({d}) vượt quá sức chứa xe Q={capacity_q}!")

    # 4. Kiểm tra mạng đường đi và về depot
    n = len(points)
    for i in range(n):
        if i != depot_id:
            d_out = dist_matrix[depot_id, i]
            d_in = dist_matrix[i, depot_id]
            if np.isinf(d_out) or np.isnan(d_out) or d_out is None:
                raise ValueError(f"LỖI: Không có đường đi từ depot đến điểm {i}!")
            if np.isinf(d_in) or np.isnan(d_in) or d_in is None:
                raise ValueError(f"LỖI: Không có đường về từ điểm {i} tới depot!")

    # 5. Kiểm tra các tuyến xe (Routes)
    route_list = routes_payload["routes"]
    if len(route_list) > fleet_k:
        raise ValueError(f"LỖI: Số xe dùng ({len(route_list)}) vượt quá số xe cho phép K={fleet_k}!")

    visited_customers = []
    for r in route_list:
        custs = r["customer_ids"]
        # Kiểm tra tải trọng tuyến
        load = sum(demands[str(c)] for c in custs)
        if load > capacity_q:
            raise ValueError(f"LỖI: Tuyến xe {r['vehicle_id']} quá tải ({load} > {capacity_q})!")
        visited_customers.extend(custs)

    # 6. Kiểm tra phục vụ lặp hoặc bỏ sót
    expected_customers = set(p for p in points if p != depot_id)
    visited_set = set(visited_customers)

    if len(visited_customers) != len(visited_set):
        duplicates = [x for x in visited_set if visited_customers.count(x) > 1]
        raise ValueError(f"LỖI: Tồn tại điểm được phục vụ lặp lại: {duplicates}!")

    if visited_set != expected_customers:
        missing = expected_customers - visited_set
        raise ValueError(f"LỖI: Tồn tại điểm khách bị bỏ sót không được phục vụ: {missing}!")

    return True


# =============================================================================
# CÁC TEST CASES ĐƯỢC CHUẨN HOÁ
# =============================================================================

def test_toy_valid_instance():
    """Test 1: Instance hợp lệ gốc phải vượt qua 100% kiểm định."""
    df, instance, routes = load_toy_files()
    assert validate_routes(df, instance, routes) is True


def test_duplicate_point_id():
    """Test 2: Phát hiện lỗi ID trùng lặp."""
    df, instance, routes = load_toy_files()
    # Tạo bản sao có ID trùng lặp
    df_dup = df.copy()
    df_dup.loc[len(df_dup)] = df_dup.iloc[1]  # Nhân đôi điểm 1
    with pytest.raises(ValueError, match="LỖI: Tồn tại point_id bị trùng lặp!"):
        validate_routes(df_dup, instance, routes)


def test_negative_or_missing_demand():
    """Test 3: Phát hiện lỗi Demand âm hoặc thiếu."""
    df, instance, routes = load_toy_files()
    instance_neg = json.loads(json.dumps(instance))
    instance_neg["demands"]["2"] = -10.0  # Gán demand âm
    with pytest.raises(ValueError, match="bị âm hoặc thiếu"):
        validate_routes(df, instance_neg, routes)


def test_demand_exceeds_capacity():
    """Test 4: Phát hiện lỗi demand tại một điểm vượt quá sức chứa q_i > Q."""
    df, instance, routes = load_toy_files()
    instance_over = json.loads(json.dumps(instance))
    instance_over["demands"]["3"] = 250.0  # Q = 200, demand = 250
    with pytest.raises(ValueError, match="vượt quá sức chứa xe Q"):
        validate_routes(df, instance_over, routes)


def test_missing_depot():
    """Test 5: Phát hiện lỗi thiếu depot."""
    df, instance, routes = load_toy_files()
    df_no_depot = df[df["point_id"] != 0].copy()
    with pytest.raises(ValueError, match="Không tìm thấy Depot ID"):
        validate_routes(df_no_depot, instance, routes)


def test_unreachable_node():
    """Test 6: Phát hiện điểm không thể đến hoặc không thể về depot."""
    df, instance, routes = load_toy_files()
    instance_unreach = json.loads(json.dumps(instance))
    # Giả lập điểm 4 bị đứt đường không thể quay về depot
    matrix = np.array(instance_unreach["distance_matrix"])
    matrix[4, 0] = np.inf
    instance_unreach["distance_matrix"] = matrix.tolist()

    with pytest.raises(ValueError, match="Không có đường về từ điểm 4 tới depot"):
        validate_routes(df, instance_unreach, routes)


def test_vehicles_exceed_fleet_size():
    """Test 7: Phát hiện lỗi số xe dùng vượt quá K."""
    df, instance, routes = load_toy_files()
    routes_over = json.loads(json.dumps(routes))
    # Tách thêm 1 xe thành 4 xe > K=3
    routes_over["routes"].append({
        "vehicle_id": "XE_04_EXTRA",
        "customer_ids": [4],
        "full_path": [0, 4, 0],
        "route_load_kg": 40.0
    })
    # Điều chỉnh xe 1 bớt điểm 4
    routes_over["routes"][0]["customer_ids"] = [1, 2, 3]

    with pytest.raises(ValueError, match="vượt quá số xe cho phép K=3"):
        validate_routes(df, instance, routes_over)


def test_duplicate_or_omitted_customer():
    """Test 8: Phát hiện điểm bị phục vụ lặp lại hoặc bị bỏ sót."""
    df, instance, routes = load_toy_files()

    # Bỏ sót điểm 12
    routes_omitted = json.loads(json.dumps(routes))
    routes_omitted["routes"][2]["customer_ids"] = [9, 10, 11]  # Thiếu 12
    with pytest.raises(ValueError, match="bị bỏ sót"):
        validate_routes(df, instance, routes_omitted)

    # Phục vụ lặp điểm 1 ở cả Xe 1 và Xe 2
    routes_dup = json.loads(json.dumps(routes))
    routes_dup["routes"][1]["customer_ids"].append(1)
    with pytest.raises(ValueError, match="phục vụ lặp lại"):
        validate_routes(df, instance, routes_dup)
