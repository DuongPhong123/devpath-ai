"""
DevPath AI — Curriculum Content
Nội dung khóa học từ zero đến developer.
"""

PHASES = {
    1: {"name": "Nền tảng Lập trình", "color": "#4F7CFF", "icon": "⚡"},
    2: {"name": "Lập trình Cốt lõi",  "color": "#22D3EE", "icon": "🔧"},
    3: {"name": "Chuyên môn hóa",      "color": "#A78BFA", "icon": "🚀"},
    4: {"name": "Senior & Pro",         "color": "#FCD34D", "icon": "🏆"},
}

MODULES = [
    # ── PHASE 1 ──────────────────────────────────────────────────────────────
    {
        "id": "m01", "phase": 1, "title": "Tư duy Lập trình", "icon": "🧠",
        "lessons": [
            {
                "id": "m01-l01", "title": "Máy tính hoạt động như thế nào?",
                "xp": 30, "minutes": 15,
                "content": """
## Máy tính hoạt động như thế nào?

Trước khi học code, hãy hiểu máy tính hoạt động ra sao.

### Các thành phần chính

- **CPU (Bộ xử lý)**: "Não" của máy tính, thực thi các lệnh
- **RAM (Bộ nhớ)**: Lưu dữ liệu đang dùng, nhanh nhưng mất khi tắt máy
- **Storage (Ổ cứng)**: Lưu dữ liệu lâu dài, chậm hơn RAM
- **I/O**: Bàn phím, màn hình, chuột để tương tác

### Lập trình là gì?

Lập trình là **viết tập hợp các lệnh** để máy tính thực thi.
Giống như viết công thức nấu ăn — máy tính sẽ làm theo từng bước.

```
# Ví dụ: Tính tiền lương
Đầu vào: Lương cơ bản = 15,000,000đ, số ngày làm = 22
Xử lý:  Lương ngày = 15,000,000 / 26
        Lương thực = Lương ngày × 22
Đầu ra: 12,692,307đ
```

### Ngôn ngữ lập trình

Máy tính chỉ hiểu 0 và 1. **Ngôn ngữ lập trình** là cầu nối giúp chúng ta viết lệnh bằng tiếng Anh thay vì 0/1.

> **Python** là ngôn ngữ đầu tiên chúng ta học — đơn giản, dễ đọc, dùng được cho web, AI, data.
""",
                "quiz": [
                    {
                        "q": "RAM khác ổ cứng ở điểm nào?",
                        "options": ["RAM nhanh hơn nhưng mất dữ liệu khi tắt máy",
                                    "RAM chậm hơn nhưng lưu được lâu",
                                    "RAM và ổ cứng giống nhau",
                                    "RAM chỉ dùng cho CPU"],
                        "correct": 0,
                        "explain": "RAM (Random Access Memory) rất nhanh nhưng là bộ nhớ tạm thời. Ổ cứng (HDD/SSD) lưu dữ liệu lâu dài nhưng chậm hơn."
                    }
                ]
            },
            {
                "id": "m01-l02", "title": "Thuật toán & Tư duy giải quyết vấn đề",
                "xp": 40, "minutes": 20,
                "content": """
## Thuật toán là gì?

**Thuật toán (Algorithm)** là tập hợp các bước có thứ tự để giải quyết một vấn đề.

### Ví dụ thực tế: Tìm ứng viên phù hợp

```
Bài toán: Tìm ứng viên có điểm cao nhất trong 100 hồ sơ

Bước 1: Đặt max_score = 0, best_candidate = "chưa có"
Bước 2: Lặp qua từng hồ sơ:
    - Nếu hồ sơ.điểm > max_score:
        - max_score = hồ sơ.điểm
        - best_candidate = hồ sơ.tên
Bước 3: In ra best_candidate
```

### 3 cấu trúc cơ bản

1. **Tuần tự (Sequence)**: Làm từng bước một
2. **Rẽ nhánh (Selection)**: Nếu điều kiện → làm A, không thì làm B
3. **Lặp (Loop)**: Làm đi làm lại cho đến khi thỏa điều kiện

### Luyện tư duy: Bài toán đơn giản

Viết thuật toán (bằng tiếng Việt) để:
- Tính thuế thu nhập cá nhân
- Tìm ngày có nhiều nhân viên vắng nhất trong tháng
""",
                "quiz": [
                    {
                        "q": "Trong 3 cấu trúc cơ bản, cấu trúc nào dùng để kiểm tra điều kiện?",
                        "options": ["Tuần tự", "Rẽ nhánh", "Lặp", "Tất cả đều được"],
                        "correct": 1,
                        "explain": "Rẽ nhánh (if/else) dùng để kiểm tra điều kiện và chọn hướng xử lý."
                    }
                ]
            },
        ]
    },
    {
        "id": "m02", "phase": 1, "title": "Python Cơ bản", "icon": "🐍",
        "lessons": [
            {
                "id": "m02-l01", "title": "Biến và Kiểu Dữ Liệu",
                "xp": 50, "minutes": 25,
                "content": """
## Biến và Kiểu Dữ Liệu trong Python

### Biến là gì?

**Biến** là "hộp" lưu dữ liệu. Đặt tên → gán giá trị → dùng lại.

```python
# Khai báo biến (không cần từ khóa đặc biệt như Java/C++)
ten = "Nguyễn Văn Phong"
tuoi = 34
luong = 15_000_000   # Dấu _ giúp đọc số dễ hơn
la_quan_ly = True

# In ra màn hình
print(ten)          # Nguyễn Văn Phong
print(tuoi)         # 34
print(f"Tên: {ten}, Tuổi: {tuoi}")   # f-string
```

### 4 Kiểu dữ liệu cơ bản

| Kiểu | Tên Python | Ví dụ |
|------|-----------|-------|
| Số nguyên | `int` | `34`, `-5`, `1000` |
| Số thực | `float` | `3.14`, `15.5` |
| Chuỗi | `str` | `"Xin chào"`, `'ABIC'` |
| Đúng/Sai | `bool` | `True`, `False` |

### Kiểm tra kiểu dữ liệu

```python
print(type(34))          # <class 'int'>
print(type("xin chào"))  # <class 'str'>
print(type(True))        # <class 'bool'>
```

### Chuyển đổi kiểu

```python
so_nguyen = int("25")        # "25" → 25
so_thuc   = float("3.14")    # "3.14" → 3.14
chuoi     = str(15000000)    # 15000000 → "15000000"
```

> 💡 **Ứng dụng thực tế**: Khi đọc dữ liệu từ Excel, mọi thứ đều là `str`. Phải chuyển sang `int`/`float` trước khi tính toán.
""",
                "quiz": [
                    {
                        "q": "Kết quả của `type(\"15000000\")` là gì?",
                        "options": ["<class 'int'>", "<class 'float'>",
                                    "<class 'str'>", "<class 'number'>"],
                        "correct": 2,
                        "explain": "Mọi thứ trong dấu nháy đều là str (string), dù trông giống số."
                    },
                    {
                        "q": "Cách nào đúng để in: Tên: Phong, Tuổi: 34?",
                        "options": [
                            'print("Tên: " + ten + ", Tuổi: " + tuoi)',
                            'print(f"Tên: {ten}, Tuổi: {tuoi}")',
                            'print(ten, tuoi)',
                            'printf("Tên: %s, Tuổi: %d", ten, tuoi)'
                        ],
                        "correct": 1,
                        "explain": "f-string là cách hiện đại và dễ đọc nhất trong Python."
                    }
                ],
                "exercise": {
                    "description": "Tạo biến lưu thông tin của bạn và in ra màn hình",
                    "starter": '# Tạo các biến sau:\n# ho_ten = "họ và tên của bạn"\n# nam_sinh = năm sinh\n# phong_ban = "tên phòng ban"\n# muc_luong = mức lương\n\n# TODO: Khai báo biến ở đây\n\n\n# In ra: "Xin chào, tôi là [tên], sinh năm [năm], phòng [phòng], lương [lương]đ"\n',
                }
            },
            {
                "id": "m02-l02", "title": "Toán tử và Biểu thức",
                "xp": 50, "minutes": 20,
                "content": """
## Toán tử trong Python

### Toán tử số học

```python
a, b = 10, 3

print(a + b)    # 13  — cộng
print(a - b)    # 7   — trừ
print(a * b)    # 30  — nhân
print(a / b)    # 3.333... — chia (kết quả float)
print(a // b)   # 3   — chia lấy nguyên
print(a % b)    # 1   — chia lấy dư (modulo)
print(a ** b)   # 1000 — lũy thừa
```

### Toán tử so sánh (trả về True/False)

```python
print(10 > 3)   # True
print(10 == 10) # True  (lưu ý: == không phải =)
print(10 != 5)  # True
print(10 >= 10) # True
```

### Ứng dụng HR thực tế

```python
luong_co_ban = 15_000_000
he_so_chuc_vu = 1.3
phu_cap = 500_000
so_ngay_lam = 20
tong_ngay = 26

# Tính lương
luong_ngay = luong_co_ban / tong_ngay
luong_thuc_te = luong_ngay * so_ngay_lam
luong_chuc_vu = luong_co_ban * he_so_chuc_vu
tong_thu_nhap = luong_thuc_te + phu_cap

print(f"Lương thực nhận: {tong_thu_nhap:,.0f}đ")
# Lương thực nhận: 12,192,308đ
```

> 💡 `{so:,.0f}` định dạng số có dấu phẩy ngăn cách hàng nghìn
""",
                "quiz": [
                    {
                        "q": "10 % 3 bằng bao nhiêu?",
                        "options": ["3", "1", "0.333", "3.33"],
                        "correct": 1,
                        "explain": "% là chia lấy dư. 10 = 3×3 + 1, vậy 10 % 3 = 1."
                    }
                ],
                "exercise": {
                    "description": "Tính lương tháng cho nhân viên theo công thức ABIC",
                    "starter": '# Tính lương cho nhân viên\nluong_co_ban = 18_000_000\nso_ngay_di_lam = 21\ntong_ngay_cong = 26\nphu_cap_xang_xe = 300_000\nphu_cap_an_trua = 600_000\n\n# TODO: Tính lương thực nhận\n# Công thức: (lương_cơ_bản / 26) × số_ngày_đi_làm + phụ_cấp\n\n\nprint(f"Lương tháng này: {luong_thuc_nhan:,.0f}đ")\n',
                }
            },
            {
                "id": "m02-l03", "title": "Điều kiện If/Else",
                "xp": 60, "minutes": 25,
                "content": """
## Câu lệnh điều kiện If/Else

### Cú pháp cơ bản

```python
if điều_kiện:
    # làm khi điều kiện đúng
elif điều_kiện_khác:
    # làm khi điều kiện này đúng
else:
    # làm khi không điều kiện nào đúng
```

### Ví dụ: Xếp loại nhân viên

```python
diem_danh_gia = 85

if diem_danh_gia >= 90:
    xep_loai = "Xuất sắc"
    thuong = 3_000_000
elif diem_danh_gia >= 80:
    xep_loai = "Tốt"
    thuong = 2_000_000
elif diem_danh_gia >= 70:
    xep_loai = "Khá"
    thuong = 1_000_000
else:
    xep_loai = "Trung bình"
    thuong = 0

print(f"Xếp loại: {xep_loai}, Thưởng: {thuong:,}đ")
# Xếp loại: Tốt, Thưởng: 2,000,000đ
```

### Toán tử logic

```python
and  # cả hai đều đúng
or   # ít nhất một đúng
not  # đảo ngược

# Ví dụ: Kiểm tra đủ điều kiện xét tuyển
tuoi = 28
kinh_nghiem_nam = 3
bang_cap = "Đại học"

du_dieu_kien = (tuoi >= 22 and tuoi <= 35) and \
               (kinh_nghiem_nam >= 2) and \
               (bang_cap in ["Đại học", "Thạc sĩ"])

if du_dieu_kien:
    print("✅ Đủ điều kiện vào vòng phỏng vấn")
else:
    print("❌ Chưa đủ điều kiện")
```
""",
                "quiz": [
                    {
                        "q": "Nếu điểm = 75, xếp loại và thưởng là gì (theo code ví dụ)?",
                        "options": [
                            "Xuất sắc, 3,000,000đ",
                            "Tốt, 2,000,000đ",
                            "Khá, 1,000,000đ",
                            "Trung bình, 0đ"
                        ],
                        "correct": 2,
                        "explain": "75 >= 70 (thỏa elif thứ 3) → Khá, 1,000,000đ"
                    }
                ],
                "exercise": {
                    "description": "Tính thưởng Tết dựa theo thâm niên và điểm đánh giá",
                    "starter": '# Thưởng Tết theo quy định ABIC\ntham_nien = 5      # năm\ndiem_danh_gia = 82  # 0-100\nluong_co_ban = 15_000_000\n\n# Quy tắc:\n# Thâm niên >= 10 năm: thưởng 3 tháng lương\n# Thâm niên >= 5 năm: thưởng 2 tháng lương\n# Thâm niên < 5 năm: thưởng 1 tháng lương\n# Thêm: nếu điểm >= 90, cộng thêm 50% thưởng\n\n# TODO: Viết code tính thuong_tet\n\n\nprint(f"Thưởng Tết: {thuong_tet:,.0f}đ")\n',
                }
            },
            {
                "id": "m02-l04", "title": "Vòng lặp For & While",
                "xp": 70, "minutes": 30,
                "content": """
## Vòng lặp — Làm đi làm lại

### Vòng lặp `for`

```python
# Lặp qua danh sách
nhan_vien = ["An", "Bình", "Chi", "Dũng"]

for ten in nhan_vien:
    print(f"Xin chào, {ten}!")

# Lặp với số (range)
for i in range(1, 6):      # 1, 2, 3, 4, 5
    print(f"Tháng {i}")

# range(start, stop, step)
for i in range(0, 100, 10):   # 0, 10, 20, ... 90
    print(i)
```

### Vòng lặp `while`

```python
so_thu = 0
max_thu = 3

while so_thu < max_thu:
    print(f"Lần thử {so_thu + 1}")
    so_thu += 1   # so_thu = so_thu + 1
```

### Ví dụ HR: Tính tổng lương phòng ban

```python
luong_nhan_vien = [15_000_000, 22_000_000, 18_500_000, 25_000_000]

tong_luong = 0
for luong in luong_nhan_vien:
    tong_luong += luong

tb_luong = tong_luong / len(luong_nhan_vien)
print(f"Tổng: {tong_luong:,.0f}đ")
print(f"Trung bình: {tb_luong:,.0f}đ")
```

### `break` và `continue`

```python
# break: dừng vòng lặp
for i in range(10):
    if i == 5:
        break          # Dừng tại i=5
    print(i)           # In 0,1,2,3,4

# continue: bỏ qua bước hiện tại
for i in range(10):
    if i % 2 == 0:
        continue       # Bỏ qua số chẵn
    print(i)           # In 1,3,5,7,9
```
""",
                "quiz": [
                    {
                        "q": "range(2, 10, 3) tạo ra dãy số nào?",
                        "options": ["2, 3, 4, 5, 6, 7, 8, 9",
                                    "2, 5, 8",
                                    "3, 6, 9",
                                    "2, 4, 6, 8"],
                        "correct": 1,
                        "explain": "range(start=2, stop=10, step=3): bắt đầu từ 2, bước nhảy 3, dừng trước 10 → 2, 5, 8"
                    }
                ],
                "exercise": {
                    "description": "Lọc và tính lương những NV làm đủ >= 20 ngày",
                    "starter": '# Dữ liệu chấm công tháng 10\nnhan_vien = [\n    {"ten": "Nguyễn An",   "ngay_lam": 22, "luong": 15_000_000},\n    {"ten": "Trần Bình",   "ngay_lam": 18, "luong": 20_000_000},\n    {"ten": "Lê Chi",      "ngay_lam": 25, "luong": 17_500_000},\n    {"ten": "Phạm Dũng",  "ngay_lam": 19, "luong": 22_000_000},\n    {"ten": "Hoàng Linh",  "ngay_lam": 26, "luong": 18_000_000},\n]\n\n# TODO: \n# 1. In ra tên những NV làm >= 20 ngày\n# 2. Tính tổng lương của những NV đó\n# 3. In: "Tổng lương NV làm đủ: X đ"\n',
                }
            },
            {
                "id": "m02-l05", "title": "List và Dictionary",
                "xp": 80, "minutes": 35,
                "content": """
## List và Dictionary — Hai cấu trúc dữ liệu quan trọng nhất

### List (Danh sách)

```python
# Tạo list
phong_ban = ["HR", "IT", "Kế toán", "Kinh doanh"]
luong_list = [15_000_000, 22_000_000, 18_000_000]

# Truy cập (index bắt đầu từ 0)
print(phong_ban[0])    # HR
print(phong_ban[-1])   # Kinh doanh (cuối cùng)

# Thêm/xóa
phong_ban.append("Pháp chế")    # thêm cuối
phong_ban.insert(1, "Hành chính")  # thêm tại vị trí 1
phong_ban.remove("IT")           # xóa theo giá trị

# Slicing
print(phong_ban[1:3])   # lấy từ index 1 đến 2

# Tìm kiếm
print("HR" in phong_ban)    # True
print(len(phong_ban))       # số phần tử
```

### Dictionary (Từ điển)

```python
# Cấu trúc: {key: value}
nhan_vien = {
    "ho_ten":     "Nguyễn Văn Phong",
    "phong_ban":  "HR",
    "chuc_vu":    "Chuyên viên",
    "luong":      15_000_000,
    "la_quan_ly": False
}

# Truy cập
print(nhan_vien["ho_ten"])          # Nguyễn Văn Phong
print(nhan_vien.get("email", "N/A"))  # Không lỗi nếu key không tồn tại

# Thêm/sửa
nhan_vien["email"] = "phong@abic.com"
nhan_vien["luong"] = 16_000_000    # cập nhật

# Duyệt
for key, value in nhan_vien.items():
    print(f"{key}: {value}")
```

### List of Dicts — Pattern phổ biến nhất

```python
# Kiểu dữ liệu thực tế nhất — giống một bảng Excel
danh_sach_nv = [
    {"ten": "An",   "phong": "HR",   "luong": 15_000_000},
    {"ten": "Bình", "phong": "IT",   "luong": 25_000_000},
    {"ten": "Chi",  "phong": "IT",   "luong": 22_000_000},
]

# Lọc NV phòng IT
nv_it = [nv for nv in danh_sach_nv if nv["phong"] == "IT"]

# Tổng lương
tong = sum(nv["luong"] for nv in danh_sach_nv)
```
""",
                "quiz": [
                    {
                        "q": 'phong_ban = ["HR","IT","KT"]. phong_ban[-1] là gì?',
                        "options": ["HR", "IT", "KT", "Lỗi"],
                        "correct": 2,
                        "explain": "Index -1 trỏ đến phần tử CUỐI CÙNG trong list → 'KT'"
                    }
                ],
                "exercise": {
                    "description": "Phân tích dữ liệu nhân sự bằng list và dict",
                    "starter": '# Dữ liệu nhân sự\nnhan_su = [\n    {"ten": "Nguyễn An",   "phong": "HR",  "luong": 15_000_000, "nam": 2019},\n    {"ten": "Trần Bình",   "phong": "IT",  "luong": 25_000_000, "nam": 2020},\n    {"ten": "Lê Chi",      "phong": "IT",  "luong": 22_000_000, "nam": 2018},\n    {"ten": "Phạm Dũng",  "phong": "KT",  "luong": 18_000_000, "nam": 2021},\n    {"ten": "Hoàng Em",   "phong": "HR",  "luong": 17_000_000, "nam": 2022},\n]\n\n# TODO:\n# 1. In ra tên và lương của NV phòng HR\n# 2. Tính lương trung bình toàn công ty\n# 3. Tìm người có lương cao nhất (tên + lương)\n# 4. Đếm số NV mỗi phòng ban (dùng dict)\n',
                }
            },
        ]
    },
    {
        "id": "m03", "phase": 1, "title": "Hàm (Functions)", "icon": "⚙️",
        "lessons": [
            {
                "id": "m03-l01", "title": "Định nghĩa và Gọi Hàm",
                "xp": 70, "minutes": 25,
                "content": """
## Hàm — Viết code một lần, dùng mãi mãi

### Tại sao cần hàm?

Thay vì copy-paste code, đặt nó vào hàm → gọi bất cứ khi nào cần.

### Cú pháp

```python
def ten_ham(tham_so_1, tham_so_2):
    # code xử lý
    return ket_qua
```

### Ví dụ thực tế

```python
# Hàm tính lương tháng
def tinh_luong(luong_co_ban, ngay_lam, tong_ngay=26, phu_cap=0):
    luong_thuc = (luong_co_ban / tong_ngay) * ngay_lam + phu_cap
    return round(luong_thuc)

# Gọi hàm
luong_phong = tinh_luong(15_000_000, 22)
luong_an    = tinh_luong(25_000_000, 20, phu_cap=500_000)

print(f"Lương Phong: {luong_phong:,}đ")
print(f"Lương An:   {luong_an:,}đ")


# Hàm xếp loại nhân viên
def xep_loai(diem):
    if diem >= 90:   return "Xuất sắc"
    elif diem >= 80: return "Tốt"
    elif diem >= 70: return "Khá"
    else:            return "Cần cải thiện"

# Test hàm
for diem in [95, 85, 72, 60]:
    print(f"Điểm {diem}: {xep_loai(diem)}")
```

### Hàm trả về nhiều giá trị

```python
def thong_ke_luong(danh_sach_luong):
    tong = sum(danh_sach_luong)
    tb   = tong / len(danh_sach_luong)
    cao  = max(danh_sach_luong)
    thap = min(danh_sach_luong)
    return tong, tb, cao, thap

t, tb, c, th = thong_ke_luong([15e6, 22e6, 18e6, 25e6])
print(f"Tổng: {t:,.0f}  TB: {tb:,.0f}")
```
""",
                "quiz": [
                    {
                        "q": "Trong `def tinh_luong(luong, ngay, phu_cap=0)`, gọi `tinh_luong(15e6, 22)` thì phu_cap bằng bao nhiêu?",
                        "options": ["Lỗi vì thiếu tham số", "0", "None", "Tự động tính"],
                        "correct": 1,
                        "explain": "phu_cap=0 là tham số mặc định (default parameter). Nếu không truyền, Python dùng giá trị 0."
                    }
                ],
                "exercise": {
                    "description": "Viết hàm tính thưởng cuối năm cho toàn bộ danh sách NV",
                    "starter": '# Viết hàm tính thưởng cuối năm\n# Quy tắc:\n# - Thâm niên >= 10 năm: 3 tháng lương\n# - Thâm niên >= 5 năm: 2 tháng lương\n# - Thâm niên < 5 năm: 1 tháng lương\n# - Nếu điểm KPI >= 90: nhân đôi thưởng\n\ndef tinh_thuong(luong_co_ban, tham_nien, diem_kpi):\n    # TODO: Viết code ở đây\n    pass\n\n\n# Test với dữ liệu thực\nnhan_vien = [\n    {"ten": "An",   "luong": 15_000_000, "tham_nien": 12, "kpi": 88},\n    {"ten": "Bình", "luong": 25_000_000, "tham_nien": 3,  "kpi": 95},\n    {"ten": "Chi",  "luong": 18_000_000, "tham_nien": 7,  "kpi": 76},\n]\n\nfor nv in nhan_vien:\n    thuong = tinh_thuong(nv["luong"], nv["tham_nien"], nv["kpi"])\n    print(f"{nv[\'ten\']}: Thưởng = {thuong:,.0f}đ")\n',
                }
            },
        ]
    },
    # ── PHASE 2 ──────────────────────────────────────────────────────────────
    {
        "id": "m04", "phase": 2, "title": "Python Nâng cao", "icon": "🔥",
        "lessons": [
            {
                "id": "m04-l01", "title": "List Comprehension & Lambda",
                "xp": 90, "minutes": 30,
                "content": """
## List Comprehension — Python thuần thục nhất

```python
# Cách cũ (for loop)
luong_tang = []
for luong in luong_list:
    luong_tang.append(luong * 1.1)

# List comprehension (1 dòng, Pythonic)
luong_tang = [luong * 1.1 for luong in luong_list]

# Có điều kiện lọc
nv_luong_cao = [nv for nv in ds_nv if nv["luong"] > 20_000_000]

# Dict comprehension
luong_dict = {nv["ten"]: nv["luong"] for nv in ds_nv}
```

### Lambda — Hàm ẩn danh

```python
# Thay vì def
tinh_thue = lambda luong: luong * 0.1 if luong > 10_000_000 else 0

# Dùng với sorted
ds_nv_sorted = sorted(ds_nv, key=lambda nv: nv["luong"], reverse=True)

# Dùng với map/filter
luong_list = [15e6, 22e6, 18e6, 25e6]
tong_thue = sum(map(lambda l: l * 0.1, filter(lambda l: l > 20e6, luong_list)))
```
""",
                "quiz": [
                    {
                        "q": "[x**2 for x in range(5) if x % 2 == 0] cho kết quả gì?",
                        "options": ["[0, 4, 16]", "[1, 9, 25]", "[0, 1, 4, 9, 16]", "[4, 16]"],
                        "correct": 0,
                        "explain": "range(5) = [0,1,2,3,4]. Lọc chẵn: [0,2,4]. Bình phương: [0,4,16]"
                    }
                ],
                "exercise": {
                    "description": "Dùng list comprehension xử lý bảng lương",
                    "starter": '# Dữ liệu\nds_nv = [\n    {"ten": "An",   "luong": 15_000_000, "phong": "HR"},\n    {"ten": "Bình", "luong": 25_000_000, "phong": "IT"},\n    {"ten": "Chi",  "luong": 22_000_000, "phong": "IT"},\n    {"ten": "Dũng", "luong": 13_000_000, "phong": "KT"},\n]\n\n# TODO dùng list comprehension:\n# 1. Tạo list tên của NV lương > 20 triệu\n# 2. Tạo dict {tên: lương_sau_tăng_10%} cho NV phòng IT\n# 3. Sắp xếp ds_nv theo lương giảm dần (dùng sorted + lambda)\n',
                }
            },
        ]
    },
]

# ── Helper functions ──────────────────────────────────────────────────────────

def get_all_lessons():
    """Trả về flat list tất cả lessons."""
    lessons = []
    for module in MODULES:
        for lesson in module["lessons"]:
            lesson["module_id"]    = module["id"]
            lesson["module_title"] = module["title"]
            lesson["module_icon"]  = module["icon"]
            lessons.append(lesson)
    return lessons

def get_lesson_by_id(lesson_id: str):
    for lesson in get_all_lessons():
        if lesson["id"] == lesson_id:
            return lesson
    return None

def get_module_lessons(module_id: str):
    for module in MODULES:
        if module["id"] == module_id:
            return module["lessons"]
    return []

def get_total_xp():
    return sum(l["xp"] for l in get_all_lessons())
