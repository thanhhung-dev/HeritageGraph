"""
Danh sách địa điểm văn hóa Huế - Đà Nẵng.
Mỗi địa điểm sẽ được crawl từ Wikipedia và sinh training data.
"""

HUE_LOCATIONS = {
    "Di tích lịch sử": [
        "Hoàng thành Huế",
        "Lăng Tự Đức",
        "Lăng Minh Mạng",
        "Lăng Khải Định",
        "Lăng Gia Long",
        "Chùa Thiên Mụ",
        "Điện Hòn Chén",
        "Cầu Trường Tiền",
        "Đàn Nam Giao",
        "Bảo tàng Cổ vật Cung đình Huế",
    ],
    "Làng nghề": [
        "Làng nghề đúc đồng Phường Đúc",
        "Làng nghề làm lụa Mỹ Xuyên",
        "Làng nghề hoa giấy Thanh Tiên",
        "Làng nghề làm hương Thủy Xuân",
        "Làng nghề đan nón Phú Cam",
    ],
    "Lễ hội": [
        "Festival Huế",
        "Lễ hội Cầu Ngư",
        "Lễ hội đua thuyền sông Hương",
        "Lễ hội đền Huyền Trân",
    ],
    "Nghệ thuật": [
        "Nhã nhạc cung đình Huế",
        "Ca Huế",
        "Múa bóng",
        "Hát tuồng",
    ],
    "Ẩm thực": [
        "Cơm hến",
        "Bún bò Huế",
        "Bánh khoái",
        "Chè bắp Huế",
        "Mè xửng",
    ],
}

DANANG_LOCATIONS = {
    "Danh thắng": [
        "Ngũ Hành Sơn",
        "Bà Nà Hills",
        "Sông Hàn",
        "Biển Mỹ Khê",
        "Bán đảo Sơn Trà",
        "Đèo Hải Vân",
    ],
    "Làng nghề": [
        "Làng đá Non Nước",
        "Làng La Hường",
        "Làng gốm Thanh Hà",
        "Làng chiếu Cẩm Nê",
        "Làng nghề nước mắm Nam Ô",
    ],
    "Lễ hội": [
        "Lễ hội Quan Thế Âm",
        "Lễ hội đua thuyền sông Hàn",
        "Lễ hội đình làng Cẩm Lệ",
    ],
    "Nghệ thuật": [
        "Bài chòi miền Trung",
        "Múa xứ Dừa",
    ],
    "Ẩm thực": [
        "Mì Quảng",
        "Bún chả cá Đà Nẵng",
        "Bánh tráng cuốn thịt heo",
        "Bánh xèo",
        "Cao lầu",
    ],
}


def get_all_locations():
    """Trả về list tất cả địa điểm kèm region."""
    all_locs = []
    for category, items in HUE_LOCATIONS.items():
        for item in items:
            all_locs.append({
                "region": "Huế",
                "category": category,
                "name": item,
            })
    for category, items in DANANG_LOCATIONS.items():
        for item in items:
            all_locs.append({
                "region": "Đà Nẵng",
                "category": category,
                "name": item,
            })
    return all_locs


if __name__ == "__main__":
    locs = get_all_locations()
    print(f"Total: {len(locs)} địa điểm")
    print(f"  Huế: {sum(1 for l in locs if l['region'] == 'Huế')}")
    print(f"  Đà Nẵng: {sum(1 for l in locs if l['region'] == 'Đà Nẵng')}")
