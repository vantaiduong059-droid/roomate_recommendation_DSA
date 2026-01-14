import csv
import math

# =========================
# HÀM CHUẨN HÓA
# =========================
def norm_diff(a, b, max_val):
    """
    Chuẩn hóa độ chênh lệch về [0,1]
    """
    return abs(a - b) / max_val if max_val != 0 else 0


def binary_diff(a, b):
    """
    So sánh tiêu chí nhị phân (giống = 0, khác = 1)
    """
    return 0 if a == b else 1


# =========================
# TÍNH KHOẢNG CÁCH ĐỊA LÝ
# =========================
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    lat1, lon1, lat2, lon2 = map(math.radians,
                                 [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1) * math.cos(lat2) *
         math.sin(dlon / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# =========================
# LOAD CSV
# =========================
def load_students(csv_path):
    students = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append({
                "id": row["ID"],
                "name": row["Name"],
                "school": row["School_Full_Name"],   # ← sửa
                "budget": float(row["Budget"]),
                "sleep": float(row["Sleep_Time"]),  # ← sửa
                "personality": int(row["Personality"]),
                "pet": int(row["Pet"]),
                "clean": float(row["Cleanliness"]),
                "lat": float(row["Latitude"]),
                "lon": float(row["Longitude"])
            })
    return students


# =========================
# TÍNH WEIGHT (ĐỘ KHÔNG PHÙ HỢP)
# =========================
def calculate_weight(user, s, alpha,
                     max_budget, max_sleep, max_clean):

    weight = 0

    # Trường học
    weight += alpha["school"] * binary_diff(user["school"], s["school"])

    # Budget (phòng rẻ hơn budget → không bị phạt)
    if s["budget"] <= user["budget"]:
        budget_diff = 0
    else:
        budget_diff = norm_diff(s["budget"], user["budget"], max_budget)

    weight += alpha["budget"] * budget_diff

    # Giờ ngủ
    weight += alpha["sleep"] * norm_diff(user["sleep"], s["sleep"], max_sleep)

    # Độ sạch sẽ
    weight += alpha["clean"] * norm_diff(user["clean"], s["clean"], max_clean)

    # Tính cách
    weight += alpha["personality"] * binary_diff(
        user["personality"], s["personality"]
    )

    # Nuôi thú cưng
    weight += alpha["pet"] * binary_diff(user["pet"], s["pet"])

    return weight


# =========================
# RANKING (CÓ HARD DISTANCE)
# =========================
def rank_students(user, students, alpha, max_distance):
    results = []

    max_budget = max(s["budget"] for s in students)
    max_sleep = 24
    max_clean = 10

    for s in students:
        dist = haversine(
            user["lat"], user["lon"],
            s["lat"], s["lon"]
        )

        # HARD DISTANCE CONSTRAINT
        if dist > max_distance:
            continue

        w = calculate_weight(user, s, alpha,
                              max_budget, max_sleep, max_clean)

        results.append((s, round(w, 4), round(dist, 2)))

    results.sort(key=lambda x: x[1])
    return results


# =========================
# MAIN
# =========================
def main():
    print("=== NHẬP THÔNG TIN NGƯỜI DÙNG ===")
    user = {
        "school": input("Trường học: "),
        "budget": float(input("Ngân sách tối đa: ")),
        "sleep": float(input("Giờ ngủ (vd 23.5): ")),
        "personality": int(input("Hướng nội(0) / Hướng ngoại(1): ")),
        "pet": int(input("Nuôi thú cưng? Không(0) / Có(1): ")),
        "clean": float(input("Mức độ sạch sẽ (1–10): ")),
        "lat": float(input("Vĩ độ: ")),
        "lon": float(input("Kinh độ: "))
    }

    print("\n=== NHẬP TRỌNG SỐ ƯU TIÊN ===")
    alpha = {
        "school": float(input("Ưu tiên cùng trường: ")),
        "budget": float(input("Ưu tiên giá rẻ: ")),
        "sleep": float(input("Ưu tiên giờ ngủ: ")),
        "clean": float(input("Ưu tiên sạch sẽ: ")),
        "personality": float(input("Ưu tiên tính cách: ")),
        "pet": float(input("Ưu tiên thú cưng: "))
    }

    max_distance = float(input("\nKhoảng cách tối đa chấp nhận (km): "))

    students = load_students("students_sample.csv")

    ranked = rank_students(user, students, alpha, max_distance)

    print("\n=== SINH VIÊN PHÙ HỢP NHẤT ===")
    for s, w, d in ranked[:5]:
        print(f"{s['name']} | weight={w} | distance={d} km")


if __name__ == "__main__":
    main()

