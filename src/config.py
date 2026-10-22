"""
Hệ thống Cấu hình Tham số Toàn cục (Global Configuration Module)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Phạm vi: Bài toán Green Capacitated Vehicle Routing Problem (GCVRP)

Mục đích module:
Tập trung toàn bộ siêu tham số của thuật toán SFO, cấu trúc lân cận VND,
thông số tải trọng xe thu gom, và các định mức tiêu thụ nhiên liệu/phát thải CO2
theo mô hình MEET và tiêu chuẩn kiểm kê khí nhà kính ISO 14064.
"""

from typing import Dict, Any


# =============================================================================
# 1. SIÊU THAM SỐ THUẬT TOÁN SAILFISH OPTIMIZER (SFO)
# Tham chiếu: Bài báo gốc Shadravan et al. (2019) và Báo cáo Step 1 (Mục 5.1 & 5.2)
# =============================================================================

# Số lượng cá mòi ban đầu trong quần thể con mồi (Sardine Population - NS)
# Giải thích: Quần thể cá mòi đóng vai trò đa dạng hóa (Exploration), giúp thuật toán
# rải đều các nghiệm trên toàn bộ không gian số thực để không bỏ sót vùng tối ưu.
DEFAULT_NUMBER_OF_SARDINES: int = 50
NUM_SARDINES: int = DEFAULT_NUMBER_OF_SARDINES

# Tỷ lệ phần trăm số lượng cá cờ so với cá mòi (Percentage of Population - PP)
# Giải thích: Số lượng cá cờ NSF = int(NS * PP). Thường chọn 0.1 đến 0.2 để số thợ săn
# chỉ chiếm 10-20% đàn mồi, giúp tập trung năng lực khai thác vào các cá thể tinh hoa.
DEFAULT_PERCENTAGE_OF_POPULATION: float = 0.1
PP: float = DEFAULT_PERCENTAGE_OF_POPULATION

# Hệ số sức mạnh tấn công ban đầu của cá cờ (Initial Attack Power - A)
# Giải thích: Giá trị A ban đầu đại diện cho cường độ tấn công cực đại (thường chọn 4.0).
# Trong các vòng lặp đầu, A lớn kích thích cá mòi chạy tán loạn để tăng độ bao phủ.
DEFAULT_INITIAL_ATTACK_POWER: float = 4.0
A_INITIAL: float = DEFAULT_INITIAL_ATTACK_POWER

# Bước giảm tuyến tính của sức mạnh tấn công (Attack Power Decrease Epsilon)
# Giải thích: Epsilon điều khiển tốc độ suy giảm của Attack Power theo từng thế hệ.
# Khi AP giảm xuống dưới 0.5, thuật toán sẽ thu hẹp phạm vi săn bắt để khai thác sâu.
DEFAULT_ATTACK_POWER_EPSILON: float = 0.001
EPSILON: float = DEFAULT_ATTACK_POWER_EPSILON

# Số vòng lặp tối đa của thuật toán SFO (Max Iterations)
# Giải thích: Ngân sách số thế hệ cho thuật toán tiến hóa. Với bài toán 40-100 điểm rác,
# 200 - 500 vòng lặp là khoảng cân bằng tốt giữa thời gian chạy và chất lượng nghiệm.
DEFAULT_MAX_ITERATIONS: int = 300
MAX_ITER: int = DEFAULT_MAX_ITERATIONS


# =============================================================================
# 2. THAM SỐ ĐỊNH TUYẾN XE THU GOM RÁC (VRP PARAMETERS)
# Tham chiếu: Báo cáo Step 1 (Mục 2.2, 4.2 & 4.3)
# =============================================================================

# Chỉ số quy ước của Trạm tập kết / Bãi xe (Depot Index)
# Giải thích: Theo chuẩn CVRPLIB và đồ thị định tuyến, điểm số 0 luôn là điểm xuất phát
# và kết thúc bắt buộc của mọi chuyến xe thu gom.
DEPOT_INDEX: int = 0

# Tải trọng tối đa cho phép của mỗi xe rác (Q_max - Đơn vị: kg)
# Giải thích: Với xe ép rác chuyên dụng cỡ nhỏ - vừa thu gom cấp phường tại TP.HCM,
# tải trọng thiết kế điển hình là 1,500 kg (1.5 tấn).
DEFAULT_CAPACITY_Q_MAX: float = 1500.0
CAPACITY_Q_MAX: float = DEFAULT_CAPACITY_Q_MAX

# Số lượng xe tối đa trong đội xe thu gom (Fleet Size - K)
# Giải thích: Ràng buộc trần số phương tiện sẵn có của đơn vị môi trường.
DEFAULT_MAX_VEHICLES: int = 6
MAX_VEHICLES: int = DEFAULT_MAX_VEHICLES


# =============================================================================
# 3. ĐỊNH MỨC MÔ HÌNH MÔI TRƯỜNG MEET & CHUẨN ISO 14064
# Tham chiếu: Mô hình MEET (Methodologies for Estimating Air Pollutant Emissions)
# và Tiêu chuẩn ISO 14064 về kiểm kê khí nhà kính.
# =============================================================================

# Trọng lượng bản thân của xe rác khi chưa chở hàng (Curb/Empty Weight - kg)
# Giải thích: Khối lượng khung gầm và thùng ép rác rỗng (khoảng 2,500 kg).
VEHICLE_EMPTY_WEIGHT_KG: float = 2500.0

# Định mức tiêu thụ nhiên liệu cơ sở khi xe chạy rỗng (Empty Fuel Rate - Lít/km)
# Giải thích: Khi không tải, động cơ diesel tiêu tốn khoảng 0.12 lít/km (12 lít/100km).
EMPTY_FUEL_RATE_L_PER_KM: float = 0.12

# Hệ số gia tăng tiêu thụ nhiên liệu theo khối lượng rác chở thêm (Load Fuel Factor)
# Đơn vị: Lít / km / kg rác
# Giải thích: Mỗi 1,000 kg rác gom thêm sẽ làm tăng mức tiêu hao khoảng 0.04 lít/km.
# Hệ số này thể hiện bản chất động: chở càng nặng đi đường càng hao dầu.
LOAD_FUEL_FACTOR_L_PER_KM_PER_KG: float = 0.00004

# Hệ số phát thải CO2 của dầu Diesel theo chuẩn ISO 14064 (Emission Factor)
# Đơn vị: kg CO2 / Lít dầu Diesel
# Giải thích: Đốt cháy hoàn toàn 1 lít dầu diesel sinh ra trung bình 2.68 kg CO2.
EMISSION_FACTOR_CO2_PER_LITER: float = 2.68

# Đơn giá nhiên liệu dầu Diesel ước tính (VNĐ / Lít)
# Giải thích: Dùng để tính toán trực tiếp chi phí kinh tế vận hành của đội xe.
FUEL_PRICE_VND_PER_LITER: float = 22500.0

# Đơn giá quy đổi chi phí môi trường phát thải carbon (VNĐ / kg CO2)
# Giải thích: Trọng số quy đổi thuế carbon/chi phí xã hội, giúp hàm mục tiêu cân bằng
# giữa lợi ích kinh tế (tiền xăng) và trách nhiệm môi trường (giảm phát thải).
CARBON_COST_VND_PER_KG: float = 500.0

# Hệ số phạt cực lớn cho nghiệm không hợp lệ (Penalty Weight)
# Giải thích: Đặt giá trị 1,000,000 VNĐ cho mỗi điểm vi phạm (vượt tải trọng, sót điểm)
# để thuật toán tự động triệt tiêu các nghiệm vi phạm ràng buộc cứng.
PENALTY_WEIGHT: float = 1000000.0


# =============================================================================
# 4. HÀM KIỂM TRA TÍNH TOÀN VẸN CỦA CẤU HÌNH (DEFENSIVE PROGRAMMING)
# =============================================================================

def validate_config(config_dict: Dict[str, Any] = None) -> bool:
    """
    Kiểm tra tính hợp lệ của toàn bộ tham số cấu hình hệ thống.
    Nếu phát hiện giá trị bất hợp lý, hàm lập tức ném lỗi bằng Tiếng Việt.
    """
    num_sardines = config_dict.get('num_sardines', NUM_SARDINES) if config_dict else NUM_SARDINES
    pp_val = config_dict.get('pp', PP) if config_dict else PP
    q_max = config_dict.get('capacity_q_max', CAPACITY_Q_MAX) if config_dict else CAPACITY_Q_MAX
    penalty = config_dict.get('penalty_weight', PENALTY_WEIGHT) if config_dict else PENALTY_WEIGHT

    if num_sardines <= 0:
        raise ValueError(f"Lỗi cấu hình: Số lượng cá mòi (num_sardines={num_sardines}) phải lớn hơn 0.")
    if not (0.0 < pp_val <= 1.0):
        raise ValueError(f"Lỗi cấu hình: Tỷ lệ cá cờ (pp={pp_val}) phải nằm trong khoảng (0, 1].")
    if q_max <= 0:
        raise ValueError(f"Lỗi cấu hình: Tải trọng tối đa của xe (capacity_q_max={q_max}) phải lớn hơn 0.")
    if penalty <= 0:
        raise ValueError(f"Lỗi cấu hình: Hệ số phạt (penalty_weight={penalty}) phải là số dương lớn.")

    return True


# Tự động kiểm tra tính hợp lệ khi import module
validate_config()
