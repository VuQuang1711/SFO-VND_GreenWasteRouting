"""
Script Chuẩn hóa và Sinh Dữ liệu Thực tế Phường Tây Thạnh (Step 2)
Tuân thủ 100% Hướng dẫn của GVHD (Mục 14, 15, 17, 18, 19, 20):
- 1 Trạm trung chuyển Depot tại KCN Tân Bình (ID 0)
- 50 điểm thu gom rác nằm TRỰC TIẾP trên các trục đường của Phường Tây Thạnh trong SCC (snap = 0m)
- Phân tầng nhu cầu rác: 35 điểm dân cư (35-75kg), 15 điểm thương mại/kinh doanh (75-120kg)
- Cố định seed = 42
- Ma trận Dijkstra có hướng 51x51 (mét)
- Chứng minh nghiệm khả thi (Feasible Witness) K=4 xe, Q=1500kg
"""

import os
import json
import math
import numpy as np
import pandas as pd
import networkx as nx
import osmnx as ox

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

GRAPHML_PATH = os.path.join(ROOT_DIR, "data", "ward", "raw", "road_network.graphml")
PROC_DIR = os.path.join(ROOT_DIR, "data", "ward", "processed")
os.makedirs(PROC_DIR, exist_ok=True)

DEPOT_CSV = os.path.join(PROC_DIR, "depot.csv")
POINTS_CSV = os.path.join(PROC_DIR, "collection_points.csv")
MATRIX_CSV = os.path.join(PROC_DIR, "distance_matrix.csv")
VEHICLES_CSV = os.path.join(PROC_DIR, "vehicles.csv")
SCENARIO_JSON = os.path.join(PROC_DIR, "scenario.json")
FEASIBLE_JSON = os.path.join(PROC_DIR, "feasible_routes.json")


def generate_dataset():
    print("[1/5] Đang nạp đồ thị mạng đường và trích xuất thành phần liên thông mạnh SCC...")
    np.random.seed(42)
    G = ox.load_graphml(GRAPHML_PATH)
    scc_nodes = max(nx.strongly_connected_components(G), key=len)
    G_scc = G.subgraph(scc_nodes)
    nodes, edges = ox.graph_to_gdfs(G_scc)

    depot_node = 4225472861
    depot_lat = 10.8122
    depot_lon = 106.6215

    # 1. Thu thập các nút theo tên đường trong SCC
    street_nodes = {}
    for (u, v, k), row in edges.iterrows():
        name = row.get("name")
        if isinstance(name, list):
            name = name[0]
        if pd.isna(name):
            continue
        if name not in street_nodes:
            street_nodes[name] = []
        if u != depot_node and u not in street_nodes[name]:
            street_nodes[name].append(u)
        if v != depot_node and v not in street_nodes[name]:
            street_nodes[name].append(v)

    # 2. Phân bổ 50 điểm trên 13 trục đường chính của Phường Tây Thạnh
    target_streets = [
        ("Đường Tây Thạnh", 6),
        ("Lê Trọng Tấn", 6),
        ("Chế Lan Viên", 4),
        ("Lưu Chí Hiếu", 4),
        ("Nguyễn Hữu Tiến", 4),
        ("Dương Đức Hiền", 4),
        ("Bùi Xuân Phái", 4),
        ("Phạm Ngọc Thảo", 3),
        ("Nguyễn Hữu Dật", 3),
        ("Đường CN13", 3),
        ("Đường CN1", 3),
        ("Đường Kênh 19/5", 3),
        ("Đường số 15", 3)
    ]

    chosen_nodes = []
    chosen_street_map = {}

    for st, count in target_streets:
        available = [n for n in street_nodes.get(st, []) if n not in chosen_nodes]
        if len(available) >= count:
            selected = np.random.choice(available, count, replace=False).tolist()
        else:
            selected = available
        chosen_nodes.extend(selected)
        for n in selected:
            chosen_street_map[n] = st

    print(f" -> Đã chọn thành công {len(chosen_nodes)} điểm trên các trục đường Phường Tây Thạnh.")

    # 3. Phân tầng nhu cầu rác (35 dân cư: 35-75kg; 15 thương mại: 80-120kg)
    # 35 điểm đầu tiên là dân cư, 15 điểm tiếp theo là thương mại
    point_types = ["residential"] * 35 + ["commercial"] * 15
    np.random.shuffle(point_types)

    residential_demands = [35.0, 40.0, 45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 75.0]
    commercial_demands = [80.0, 85.0, 90.0, 95.0, 100.0, 105.0, 110.0, 115.0, 120.0]

    points_data = []

    # Điểm 0: Depot
    points_data.append({
        "point_id": 0,
        "name": "Trạm trung chuyển chất thải Tây Thạnh (Depot)",
        "latitude": depot_lat,
        "longitude": depot_lon,
        "demand_kg": 0.0,
        "point_type": "depot",
        "source_type": "trạm trung chuyển chất thải quy hoạch",
        "snapped_node": depot_node,
        "snap_distance_m": 0.0
    })

    for idx, node_id in enumerate(chosen_nodes, 1):
        pt_type = point_types[idx - 1]
        street_name = chosen_street_map[node_id]
        lat = float(nodes.loc[node_id]["y"])
        lon = float(nodes.loc[node_id]["x"])

        if pt_type == "residential":
            dmd = float(np.random.choice(residential_demands))
            side = "Lề phải" if np.random.rand() > 0.5 else "Lề trái"
            num = (idx * 7 + 13) % 250 + 1
            name = f"Số {num} {street_name} ({side})"
        else:
            dmd = float(np.random.choice(commercial_demands))
            commercial_labels = [
                "Cụm thương mại - dịch vụ", "Chợ dân sinh Tây Thạnh", "Siêu thị tiện lợi",
                "Cụm nhà hàng - quán ăn", "Khu dịch vụ KCN", "Cửa hàng bán lẻ tổng hợp"
            ]
            c_tag = np.random.choice(commercial_labels)
            num = (idx * 11 + 5) % 180 + 1
            name = f"{c_tag} - Số {num} {street_name}"

        points_data.append({
            "point_id": idx,
            "name": name,
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "demand_kg": dmd,
            "point_type": pt_type,
            "source_type": "điểm thu gom giả lập trên mạng đường OSM",
            "snapped_node": node_id,
            "snap_distance_m": 0.0
        })

    df_points = pd.DataFrame(points_data)
    df_points.to_csv(POINTS_CSV, index=False, encoding="utf-8")
    print(f"[2/5] Đã lưu {len(df_points)} điểm (1 Depot + 50 điểm thu gom) vào: {POINTS_CSV}")
    total_demand = df_points["demand_kg"].sum()
    print(f" -> Tổng nhu cầu rác thải toàn mạng: {total_demand:.1f} kg")

    # Lưu depot.csv
    depot_row = df_points.iloc[[0]][["point_id", "name", "latitude", "longitude", "source_type", "snapped_node", "snap_distance_m"]]
    depot_row.rename(columns={"point_id": "depot_id"}, inplace=True)
    depot_row.to_csv(DEPOT_CSV, index=False, encoding="utf-8")

    # Lưu vehicles.csv (K=4 xe, Q=1500kg)
    vehicles_data = [
        {"vehicle_id": 1, "capacity_kg": 1500.0, "available": True},
        {"vehicle_id": 2, "capacity_kg": 1500.0, "available": True},
        {"vehicle_id": 3, "capacity_kg": 1500.0, "available": True},
        {"vehicle_id": 4, "capacity_kg": 1500.0, "available": True}
    ]
    pd.DataFrame(vehicles_data).to_csv(VEHICLES_CSV, index=False, encoding="utf-8")

    # 4. Tính ma trận khoảng cách có hướng Dijkstra 51 x 51
    print("[3/5] Đang tính ma trận khoảng cách có hướng 51x51 bằng thuật toán Dijkstra trên SCC...")
    all_snapped_nodes = [row["snapped_node"] for row in points_data]
    n = len(all_snapped_nodes)
    dist_matrix = np.zeros((n, n), dtype=float)

    for i, u_node in enumerate(all_snapped_nodes):
        lengths = nx.single_source_dijkstra_path_length(G_scc, u_node, weight="length")
        for j, v_node in enumerate(all_snapped_nodes):
            if i == j:
                dist_matrix[i, j] = 0.0
            else:
                dist_matrix[i, j] = round(lengths[v_node], 1)

    np.savetxt(MATRIX_CSV, dist_matrix, delimiter=",", fmt="%.1f")
    print(f" -> Đã lưu ma trận khoảng cách vào: {MATRIX_CSV}")
    print(f" -> Kiểm tra: Đường chéo d(i,i) = {np.max(np.diag(dist_matrix))}m, Vô cực: {np.isinf(dist_matrix).sum()} ô.")

    # 5. Xây dựng Nghiệm Khả Thi (Feasible Witness)
    print("[4/5] Đang thiết lập phương án phân tuyến khả thi (Feasible Witness)...")
    # Chia 50 điểm khách (1..50) vào 4 xe sao cho mỗi xe <= 1500kg
    demands_dict = {row["point_id"]: row["demand_kg"] for row in points_data}

    # Gom tuần tự thỏa mãn Q <= 1500
    routes_customers = [[], [], [], []]
    routes_loads = [0.0, 0.0, 0.0, 0.0]

    current_veh = 0
    for p_id in range(1, 51):
        dmd = demands_dict[p_id]
        if routes_loads[current_veh] + dmd > 1500.0:
            current_veh += 1
            if current_veh >= 4:
                raise ValueError("Không thể chia vào 4 xe! Tổng demand vượt quá dự kiến.")
        routes_customers[current_veh].append(p_id)
        routes_loads[current_veh] += dmd

    routes_witness = []
    total_dist = 0.0
    for v_idx in range(4):
        custs = routes_customers[v_idx]
        load = routes_loads[v_idx]
        # Tính cự ly chu trình: 0 -> c1 -> c2 ... -> 0
        cycle = [0] + custs + [0]
        c_dist = sum(dist_matrix[cycle[k], cycle[k+1]] for k in range(len(cycle) - 1))
        total_dist += c_dist
        routes_witness.append({
            "vehicle_id": v_idx + 1,
            "route": cycle,
            "customer_ids": custs,
            "route_load_kg": round(load, 1),
            "capacity_kg": 1500.0,
            "route_distance_m": round(c_dist, 1),
            "validation_status": "PASS"
        })
        print(f"   Xe #{v_idx + 1}: {len(custs)} điểm, tải {load:.1f} / 1500 kg ({load/1500.0*100:.1f}%), cự ly {c_dist/1000.0:.2f} km")

    feasible_witness_payload = {
        "status": "FEASIBLE",
        "ward": "Phường Tây Thạnh",
        "district": "Quận Tân Phú",
        "seed": 42,
        "number_of_vehicles": 4,
        "total_capacity_kg": 6000.0,
        "total_demand_kg": round(total_demand, 1),
        "capacity_utilization_pct": round(total_demand / 6000.0 * 100.0, 2),
        "total_distance_km": round(total_dist / 1000.0, 3),
        "routes": routes_witness
    }

    with open(FEASIBLE_JSON, "w", encoding="utf-8") as f:
        json.dump(feasible_witness_payload, f, indent=2, ensure_ascii=False)
    print(f" -> Đã lưu Feasible Witness vào: {FEASIBLE_JSON}")

    # 6. Cập nhật scenario.json
    scenario_payload = {
        "ward_name": "Phường Tây Thạnh",
        "district_name": "Quận Tân Phú",
        "city_name": "Thành phố Hồ Chí Minh",
        "admin_source": "OpenStreetMap Nominatim Overpass API (admin_level=8)",
        "seed": 42,
        "demand_rule": "35 điểm dân cư (35-75kg) + 15 điểm kinh doanh/thương mại (80-120kg)",
        "K": 4,
        "Q": 1500.0,
        "units": {
            "demand": "kg",
            "capacity": "kg",
            "distance": "meter",
            "fuel": "liter",
            "co2": "kg",
            "cost": "VND"
        },
        "road_network_source": "OpenStreetMap drive network with 400m buffer, filtered largest SCC (868 nodes)",
        "created_at": "2026-11-07T15:00:00+07:00",
        "version": "1.1"
    }

    with open(SCENARIO_JSON, "w", encoding="utf-8") as f:
        json.dump(scenario_payload, f, indent=2, ensure_ascii=False)
    print(f" -> Đã lưu Scenario vào: {SCENARIO_JSON}")
    print("\n[5/5] HOÀN TẤT CHUẨN HÓA BỘ DỮ LIỆU TÂY THẠNH!")


if __name__ == "__main__":
    generate_dataset()

