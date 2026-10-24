"""
Ứng dụng Web Demo Quản lý Định tuyến Xanh (GreenWaste Route AI Dashboard)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Giao diện Streamlit tích hợp Bản đồ tương tác, Green Impact Dashboard và XAI Inspector

Tham chiếu:
- Mục 9 của Bản mô tả đề tài (GVHD/01_Mo_ta_de_tai_SFO_VND_Green_Waste_Routing.docx)
- Mục 8.1 - 8.4 của Báo cáo Step 1 (Báo cáo SFO - VND Step 1.docx)
- Universal XAI & 3-Tier Blueprint (Data Layer - Model Layer - Presentation Layer)
"""

import sys
import os
import time
import numpy as np
import pandas as pd
import streamlit as st

# Thêm thư mục gốc Source vào sys.path để import các module nội bộ
current_dir = os.path.dirname(os.path.abspath(__file__))
source_root = os.path.dirname(current_dir)
if source_root not in sys.path:
    sys.path.insert(0, source_root)

from src.config import (
    CAPACITY_Q_MAX,
    DEPOT_INDEX,
    DEFAULT_MAX_ITERATIONS,
    DEFAULT_NUMBER_OF_SARDINES,
    DEFAULT_PERCENTAGE_OF_POPULATION,
    EMISSION_FACTOR_CO2_PER_LITER,
    FUEL_PRICE_VND_PER_LITER
)
from src.core.data_loader import DataLoader
from src.core.decoder import RouteDecoder
from src.core.evaluator import RouteEvaluator
from src.core.validator import RouteValidator
from src.algorithms.sfo import SailfishOptimizer
from src.algorithms.vnd import VariableNeighborhoodDescent
from src.algorithms.hybrid_sfo_vnd import HybridSFOVND
from src.baselines.greedy import GreedyNearestNeighbor


# Cấu hình giao diện trang web
st.set_page_config(
    page_title="GreenWaste Route AI - Urban Waste Routing",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tiêu đề chính của ứng dụng
st.title("🚛 GreenWaste Route AI: Hệ Thống Tối Ưu Tuyến Thu Gom Rác Đô Thị")
st.markdown(
    "> **Đề tài Nghiên cứu Khoa học Sinh viên:** Tối ưu hóa lộ trình thu gom rác thải đô thị "
    "nhằm giảm chi phí và phát thải carbon bằng thuật toán **Sailfish Optimizer lai Variable Neighborhood Descent (SFO-VND)**.<br>"
    "> **Khu vực thử nghiệm:** Phường Sơn Kỳ, Quận Tân Phú, TP. Hồ Chí Minh.",
    unsafe_allow_html=True
)

st.divider()

# =============================================================================
# THANH ĐIỀU KHIỂN BÊN TRÁI (SIDEBAR CONTROLS)
# =============================================================================
st.sidebar.header("⚙️ Cấu Hình Tham Số Vận Hành")

# 1. Chọn nguồn dữ liệu
data_source = st.sidebar.selectbox(
    "📁 Chọn Nguồn Dữ Liệu:",
    ["Case Study Phường Sơn Kỳ (60 điểm)", "Tùy chỉnh tải file CSV"]
)

points_file_path = os.path.join(source_root, "data", "case_study", "collection_points.csv")
matrix_file_path = os.path.join(source_root, "data", "case_study", "distance_matrix.csv")

loader = DataLoader(depot_index=DEPOT_INDEX)

if data_source == "Case Study Phường Sơn Kỳ (60 điểm)":
    if os.path.exists(points_file_path):
        dataset = loader.load_case_study(points_file_path, matrix_file_path)
    else:
        st.error(f"Chưa tìm thấy file dữ liệu: {points_file_path}")
        st.stop()
else:
    st.sidebar.info("Vui lòng đặt file collection_points.csv vào thư mục data/case_study/")
    st.stop()

# 2. Cấu hình đội xe & thuật toán
st.sidebar.subheader("🚚 Thông Số Đội Xe")
truck_capacity = st.sidebar.slider(
    "Tải trọng tối đa mỗi xe (Q_max - kg):",
    min_value=500.0,
    max_value=3000.0,
    value=CAPACITY_Q_MAX,
    step=100.0
)

st.sidebar.subheader("🧬 Siêu Tham Số SFO-VND")
max_iters = st.sidebar.slider("Số vòng lặp tối đa (Max Iterations):", min_value=20, max_value=500, value=100, step=20)
num_sardines = st.sidebar.slider("Số lượng cá mòi (Prey NS):", min_value=20, max_value=100, value=40, step=10)
vnd_interval = st.sidebar.slider("Chu kỳ kích hoạt VND (vòng):", min_value=1, max_value=20, value=5, step=1)
rand_seed = st.sidebar.number_input("Hạt giống ngẫu nhiên (Random Seed):", value=42, step=1)

# Lựa chọn thuật toán chạy
selected_algo = st.sidebar.radio(
    "🎯 Chọn Thuật Toán Thực Thi:",
    ["Chạy Toàn Bộ (So Sánh Before / After)", "Chỉ SFO thuần", "Chỉ Hybrid SFO-VND", "Chỉ Baseline Tham Ăn (Greedy)"]
)

run_button = st.sidebar.button("🚀 BẮT ĐẦU TỐI ƯU HÓA", type="primary", use_container_width=True)


# =============================================================================
# KHU VỰC HIỂN THỊ KẾT QUẢ & CÁC TAB CHỨC NĂNG
# =============================================================================

tab_summary, tab_map, tab_dashboard, tab_xai = st.tabs([
    "📋 Tổng Quan Dữ Liệu",
    "🗺️ Bản Đồ Lộ Trình",
    "🌱 Green Impact Dashboard",
    "🔍 Góc Giải Thích XAI"
])

# TAB 1: TỔNG QUAN DỮ LIỆU
with tab_summary:
    st.subheader("📍 Dữ Liệu Điểm Thu Gom Rác Tại Địa Bàn")
    points_df = dataset["points_df"]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số điểm thu gom", f"{len(points_df) - 1} điểm")
    col2.metric("Tổng lượng rác phát sinh", f"{points_df['demand'].sum():,.1f} kg")
    col3.metric("Lượng rác bình quân/điểm", f"{points_df[points_df['point_id'] != 0]['demand'].mean():.1f} kg")
    col4.metric("Sức chứa thiết kế xe", f"{truck_capacity:,.0f} kg")

    st.dataframe(
        points_df[['point_id', 'name', 'lat', 'lon', 'demand', 'node_type', 'service_time_min']],
        use_container_width=True,
        height=300
    )

# Chuẩn bị bộ đánh giá và giải mã
decoder = RouteDecoder(capacity_q_max=truck_capacity, depot_index=DEPOT_INDEX)
evaluator = RouteEvaluator(
    distance_matrix=dataset["distance_matrix"],
    demands=dataset["demands"],
    capacity_q_max=truck_capacity,
    depot_index=DEPOT_INDEX
)
validator = RouteValidator(capacity_q_max=truck_capacity, depot_index=DEPOT_INDEX)

# Biến session_state để lưu kết quả chạy
if "results" not in st.session_state:
    st.session_state["results"] = None

if run_button:
    with st.spinner("Đang thực thi mô hình tối ưu hóa định tuyến..."):
        total_cust = dataset["dimension"]

        results = {}

        # 1. Chạy Baseline Tham ăn (Before)
        greedy = GreedyNearestNeighbor(evaluator=evaluator, capacity_q_max=truck_capacity)
        t0 = time.time()
        res_greedy = greedy.solve(total_cust)
        res_greedy["runtime"] = time.time() - t0
        results["greedy"] = res_greedy

        # 2. Chạy SFO thuần nếu được chọn
        if selected_algo in ["Chạy Toàn Bộ (So Sánh Before / After)", "Chỉ SFO thuần"]:
            sfo = SailfishOptimizer(
                evaluator=evaluator,
                decoder=decoder,
                dimension=total_cust,
                number_of_sardines=num_sardines,
                max_iterations=max_iters,
                random_seed=rand_seed
            )
            res_sfo = sfo.optimize()
            results["sfo"] = res_sfo

        # 3. Chạy Hybrid SFO-VND nếu được chọn
        if selected_algo in ["Chạy Toàn Bộ (So Sánh Before / After)", "Chỉ Hybrid SFO-VND"]:
            hybrid = HybridSFOVND(
                evaluator=evaluator,
                decoder=decoder,
                dimension=total_cust,
                number_of_sardines=num_sardines,
                max_iterations=max_iters,
                vnd_trigger_interval=vnd_interval,
                random_seed=rand_seed
            )
            res_hybrid = hybrid.optimize()
            results["hybrid"] = res_hybrid

        st.session_state["results"] = results
        st.success("Tối ưu hóa hoàn tất thành công!")

# Lấy kết quả từ session state
res = st.session_state["results"]

if res is not None:
    # TAB 3: GREEN IMPACT DASHBOARD (SO SÁNH BEFORE / AFTER)
    with tab_dashboard:
        st.subheader("📊 Bảng So Sánh Hiệu Quả Xanh (Green Impact: Before vs After)")

        greedy_res = res.get("greedy")
        hybrid_res = res.get("hybrid") or res.get("sfo")

        if greedy_res and hybrid_res:
            g_dist = greedy_res["total_distance_km"]
            h_dist = hybrid_res["metrics"]["total_distance_km"]
            dist_diff_pct = (g_dist - h_dist) / g_dist * 100.0

            g_fuel = greedy_res["total_fuel_liters"]
            h_fuel = hybrid_res["metrics"]["total_fuel_liters"]
            fuel_diff_pct = (g_fuel - h_fuel) / g_fuel * 100.0

            g_co2 = greedy_res["total_co2_kg"]
            h_co2 = hybrid_res["metrics"]["total_co2_kg"]
            co2_diff_pct = (g_co2 - h_co2) / g_co2 * 100.0

            g_cost = greedy_res["fuel_cost_vnd"]
            h_cost = hybrid_res["metrics"]["fuel_cost_vnd"]
            cost_diff_pct = (g_cost - h_cost) / g_cost * 100.0

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Tổng Quãng Đường", f"{h_dist:.2f} km", f"-{dist_diff_pct:.1f}%")
            col_m2.metric("Nhiên Liệu Tiêu Thụ", f"{h_fuel:.2f} Lít", f"-{fuel_diff_pct:.1f}%")
            col_m3.metric("Phát Thải CO2 (ISO 14064)", f"{h_co2:.2f} kg", f"-{co2_diff_pct:.1f}%")
            col_m4.metric("Chi Phí Nhiên Liệu", f"{h_cost:,.0f} đ", f"-{cost_diff_pct:.1f}%")

            st.write("### Chi tiết đối chứng số liệu:")
            comparison_table = pd.DataFrame({
                "Chỉ Số Đánh Giá": [
                    "Tổng quãng đường di chuyển (km)",
                    "Lượng dầu Diesel tiêu thụ (Lít)",
                    "Lượng phát thải CO2 (kg)",
                    "Chi phí nhiên liệu vận hành (VNĐ)",
                    "Số lượng xe sử dụng",
                    "Hệ số lấp đầy tải trọng bình quân (%)",
                    "Thời gian tính toán CPU (giây)"
                ],
                "Phương án Before (Kinh nghiệm/Tham ăn)": [
                    f"{g_dist:.2f}",
                    f"{g_fuel:.2f}",
                    f"{g_co2:.2f}",
                    f"{g_cost:,.0f}",
                    f"{greedy_res['metrics']['active_vehicles']} xe",
                    f"{greedy_res['metrics']['capacity_utilization_pct']:.1f}%",
                    f"{greedy_res['runtime_seconds']:.3f} s"
                ],
                "Phương án After (Đề xuất SFO-VND)": [
                    f"{h_dist:.2f}",
                    f"{h_fuel:.2f}",
                    f"{h_co2:.2f}",
                    f"{h_cost:,.0f}",
                    f"{hybrid_res['metrics']['active_vehicles']} xe",
                    f"{hybrid_res['metrics']['capacity_utilization_pct']:.1f}%",
                    f"{hybrid_res['runtime_seconds']:.2f} s"
                ],
                "Mức độ cải thiện (%)": [
                    f"Giảm {dist_diff_pct:.2f}%",
                    f"Tiết kiệm {fuel_diff_pct:.2f}%",
                    f"Cắt giảm {co2_diff_pct:.2f}%",
                    f"Tiết kiệm {cost_diff_pct:.2f}%",
                    "-",
                    f"+{(hybrid_res['metrics']['capacity_utilization_pct'] - greedy_res['metrics']['capacity_utilization_pct']):.1f}%",
                    "-"
                ]
            })
            st.table(comparison_table)

    # TAB 2: BẢN ĐỒ LỘ TRÌNH
    with tab_map:
        st.subheader("🗺️ Bản Đồ Trực Quan Hóa Tuyến Đường và Chi Tiết Lộ Trình")
        best_routes = (res.get("hybrid") or res.get("sfo") or res.get("greedy"))["best_routes"] if "best_routes" in (res.get("hybrid") or res.get("sfo") or res.get("greedy")) else res["greedy"]["routes"]

        # 1. Tự động sinh bản đồ tương tác và nhúng trực tiếp vào giao diện
        from src.map.route_mapper import RouteMapper
        import streamlit.components.v1 as components

        points_df = dataset["points_df"]
        points_info = {}
        for _, row in points_df.iterrows():
            pid = int(row["point_id"])
            points_info[pid] = {
                "lat": float(row["lat"]),
                "lon": float(row["lon"]),
                "demand": float(row["demand"]),
                "name": str(row["name"]),
                "node_type": str(row.get("node_type", "Dân cư"))
            }

        depot_coords = (points_info[0]["lat"], points_info[0]["lon"])
        mapper = RouteMapper(depot_coords=depot_coords, zoom_start=15)
        html_map_path = os.path.join(source_root, "green_waste_routing_map.html")
        mapper.generate_map(best_routes, points_info, html_map_path)

        if os.path.exists(html_map_path):
            with open(html_map_path, "r", encoding="utf-8") as f:
                map_html = f.read()
            components.html(map_html, height=520, scrolling=True)

        # 2. Chi tiết từng xe với tên địa danh rõ ràng
        st.markdown("### 🚚 Chi Tiết Danh Sách Điểm Dừng Từng Xe:")
        color_labels = ["Đỏ", "Xanh dương", "Xanh ngọc", "Cam đất", "Tím", "Đỏ cam", "Xanh lam"]
        active_veh = 0

        for r_idx, r in enumerate(best_routes):
            pts = [p for p in r if p != 0]
            if not pts:
                continue
            active_veh += 1
            load = sum(dataset["demands"][p] for p in pts)
            c_label = color_labels[(active_veh - 1) % len(color_labels)]

            with st.expander(f"🚚 Tuyến Xe #{active_veh} (Màu {c_label}) | Tải gom: {load:,.1f} / {truck_capacity:.0f} kg ({load/truck_capacity*100:.1f}%) | {len(pts)} điểm thu gom", expanded=(active_veh == 1)):
                st.write(f"**Bắt đầu:** 🏁 {points_info[0]['name']}")
                stop_rows = []
                for step, pt in enumerate(pts, 1):
                    info = points_info.get(pt, {})
                    stop_rows.append({
                        "Thứ tự ghé": f"#{step}",
                        "Tên địa điểm / Đầu hẻm": info.get("name", f"Điểm #{pt}"),
                        "Khối lượng rác (kg)": f"{info.get('demand', 0.0):.1f} kg",
                        "Loại hình": info.get("node_type", "Dân cư")
                    })
                st.table(pd.DataFrame(stop_rows))
                st.write(f"**Kết thúc:** 🏁 Quay về {points_info[0]['name']} (Xả rác hoàn tất tuyến)")

    # TAB 4: GÓC GIẢI THÍCH XAI (EXPLAINABLE AI INSPECTOR)
    with tab_xai:
        st.subheader("🔍 XAI Inspector: Minh Bạch Hóa Cơ Chế Tối Ưu")

        col_x1, col_x2 = st.columns(2)

        with col_x1:
            st.markdown("#### 1. Mô hình Tiêu thụ Nhiên liệu Động MEET")
            st.latex(r"f(L_{ij}) = f_{\text{empty}} + \alpha \cdot L_{ij}")
            st.latex(r"\text{Fuel}_{\text{total}} = \sum_{(i,j)} d_{ij} \cdot f(L_{ij})")
            st.caption("Suất tiêu thụ nhiên liệu biến thiên theo tải trọng rác tích lũy dọc tuyến.")

            st.markdown("#### 2. Kiểm kê Phát thải Carbon ISO 14064")
            st.latex(r"\text{CO}_2\text{ (kg)} = \text{Fuel (Lít)} \times 2.68\text{ (kg CO}_2\text{/Lít)}")

        with col_x2:
            st.markdown("#### 3. Cường độ Tấn công SFO (Attack Power)")
            st.latex(r"AP = A \cdot (1 - 2 \cdot t \cdot \epsilon)")
            st.caption("AP giảm dần giúp thuật toán chuyển từ Exploration (khám phá) sang Exploitation (tinh chỉnh).")

            st.markdown("#### 4. Ba Toán tử Lân cận của VND")
            st.markdown("- **2-opt:** Đảo ngược đoạn con trong xe để gỡ đường cắt chéo.")
            st.markdown("- **Relocate:** Rút 1 điểm từ xe này chèn sang xe khác.")
            st.markdown("- **Swap:** Hoán đổi 2 điểm giữa 2 xe để thu gọn bán kính phục vụ.")

        if "hybrid" in res and res["hybrid"].get("convergence_curve"):
            st.write("#### 📈 Đường cong hội tụ theo thời gian:")
            conv_df = pd.DataFrame({
                "Iteration": list(range(len(res["hybrid"]["convergence_curve"]))),
                "Fitness Score": res["hybrid"]["convergence_curve"]
            }).set_index("Iteration")
            st.line_chart(conv_df)
