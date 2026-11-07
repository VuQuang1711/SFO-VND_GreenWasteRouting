"""
Script Tự Động Tải Bộ Nghiệm Chuẩn (.sol) từ CVRPLIB (download_cvrplib_solutions.py)
Đề tài: Tối ưu hóa lộ trình thu gom rác thải đô thị bằng thuật toán lai SFO-VND
Mục đích: Tải các file nghiệm tham chiếu (.sol) cho 6 bộ benchmark quốc tế về thư mục data/benchmarks/raw/
"""

import os
import sys
import urllib.request
from typing import Dict

# Đảm bảo mã hóa console UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Danh mục 6 instance và nhóm phân loại trong CVRPLIB
INSTANCES: Dict[str, str] = {
    "E-n33-k4": "E",
    "B-n50-k7": "B",
    "E-n51-k5": "E",
    "A-n53-k7": "A",
    "A-n60-k9": "A",
    "E-n76-k7": "E",
}

# Các máy chủ chính thức của CVRPLIB (PUC-Rio, Brazil)
BASE_URLS = [
    "http://vrp.atd-lab.inf.puc-rio.br/media/com_vrp/instances",
    "http://vrp.galgos.inf.puc-rio.br/media/com_vrp/instances",
]


def download_benchmark_solutions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(current_dir, "..", "data", "benchmarks", "raw"))
    os.makedirs(target_dir, exist_ok=True)

    print("=" * 70)
    print("  BẮT ĐẦU TẢI 6 FILE NGHIỆM THAM CHIẾU (.sol) TỪ CVRPLIB (PUC-RIO)")
    print("=" * 70)
    print(f"Thư mục lưu trữ: {target_dir}\n")

    success_count = 0

    for inst_name, group in INSTANCES.items():
        sol_filename = f"{inst_name}.sol"
        dst_path = os.path.join(target_dir, sol_filename)

        downloaded = False
        for base_url in BASE_URLS:
            url = f"{base_url}/{group}/{sol_filename}"
            print(f"[*] Đang tải {sol_filename} từ: {url} ...", end=" ", flush=True)

            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/120.0.0.0 Safari/537.36"
                        )
                    },
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    content = resp.read()
                    with open(dst_path, "wb") as f:
                        f.write(content)

                print(" THÀNH CÔNG!")
                downloaded = True
                success_count += 1
                break
            except Exception as e:
                print(f" Thất bại ({e})")

        if not downloaded:
            print(f"[-] Cảnh báo: Không thể tải {sol_filename} từ các mirror.")

    print("\n" + "=" * 70)
    print(f"  HOÀN TẤT: Đã tải thành công {success_count}/{len(INSTANCES)} file .sol")
    print("=" * 70)


if __name__ == "__main__":
    download_benchmark_solutions()

