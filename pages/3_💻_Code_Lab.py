import streamlit as st
import sys
import os
import io
import contextlib
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ai_mentor import review_code, explain_error

st.set_page_config(page_title="Code Lab — DevPath AI", page_icon="💻", layout="wide")

st.markdown("""
<style>
.code-output {
    background: #0D1117;
    border: 1px solid #1F2937;
    border-radius: 8px;
    padding: 14px 16px;
    font-family: monospace;
    font-size: 0.9rem;
    min-height: 80px;
    white-space: pre-wrap;
}
.output-ok { color: #10B981; border-left: 3px solid #10B981; }
.output-err { color: #EF4444; border-left: 3px solid #EF4444; }
.output-empty { color: #6B7280; }
.template-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 8px;
    padding: 12px 14px;
    margin: 6px 0;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

TEMPLATES = {
    "Hello World": {
        "code": '# Chương trình đầu tiên của anh!\nprint("Xin chào, tôi là lập trình viên!")\nprint("DevPath AI - Học lập trình mỗi ngày")',
        "desc": "Bài đầu tiên — in ra màn hình",
    },
    "Tính lương nhân viên": {
        "code": '''# Tính lương thực lãnh
luong_co_ban = 15_000_000
he_so = 1.5
phu_cap = 2_000_000
bao_hiem = 0.105  # 10.5%

luong_gross = luong_co_ban * he_so + phu_cap
khau_tru = luong_gross * bao_hiem
luong_net = luong_gross - khau_tru

print(f"Lương gross: {luong_gross:,.0f} đ")
print(f"Khấu trừ BH: {khau_tru:,.0f} đ")
print(f"Lương net:   {luong_net:,.0f} đ")''',
        "desc": "Tính lương thực lãnh — ví dụ HR",
    },
    "Lọc nhân viên": {
        "code": '''# Lọc nhân viên theo điều kiện
nhan_vien = [
    {"ten": "Nguyễn Văn A", "phong": "HR", "nam_kinh_nghiem": 5},
    {"ten": "Trần Thị B", "phong": "IT", "nam_kinh_nghiem": 3},
    {"ten": "Lê Văn C", "phong": "HR", "nam_kinh_nghiem": 8},
    {"ten": "Phạm Thị D", "phong": "Finance", "nam_kinh_nghiem": 2},
]

# Lọc nhân viên HR có >4 năm kinh nghiệm
hr_senior = [nv for nv in nhan_vien
             if nv["phong"] == "HR" and nv["nam_kinh_nghiem"] > 4]

print("Nhân viên HR Senior:")
for nv in hr_senior:
    print(f"  - {nv['ten']} ({nv['nam_kinh_nghiem']} năm KN)")''',
        "desc": "List comprehension lọc nhân viên",
    },
    "Vòng lặp For": {
        "code": '''# Tính tổng XP học viên
bai_hoc = {
    "Python cơ bản": 150,
    "Hàm và Module": 200,
    "List & Dict": 180,
    "OOP": 250,
}

tong_xp = 0
for bai, xp in bai_hoc.items():
    tong_xp += xp
    print(f"✅ {bai}: +{xp} XP")

print(f"\\nTổng XP: {tong_xp}")
print(f"Level: {'Intermediate' if tong_xp > 500 else 'Beginner'}")''',
        "desc": "Vòng lặp for với dict",
    },
    "Hàm tính thưởng": {
        "code": '''# Hàm tính thưởng cuối năm
def tinh_thuong(luong_co_ban, xep_loai, chuc_vu="NV"):
    """Tính thưởng theo xếp loại KPI"""
    he_so_chuc_vu = {"NV": 1.0, "TP": 1.5, "PGD": 2.0, "GD": 3.0}
    he_so_kpi = {"A": 3, "B": 2, "C": 1, "D": 0}

    he_so = he_so_chuc_vu.get(chuc_vu, 1.0)
    kpi = he_so_kpi.get(xep_loai, 0)

    thuong = luong_co_ban * he_so * kpi
    return thuong

# Test hàm
nhan_vien = [
    ("Nguyễn A", 15_000_000, "A", "TP"),
    ("Trần B",   12_000_000, "B", "NV"),
    ("Lê C",     20_000_000, "A", "PGD"),
]

print("BẢNG THƯỞNG CUỐI NĂM")
print("-" * 40)
for ten, luong, kpi, cv in nhan_vien:
    thuong = tinh_thuong(luong, kpi, cv)
    print(f"{ten} ({cv}-KPI {kpi}): {thuong:>15,.0f} đ")''',
        "desc": "Hàm Python thực tế HR",
    },
}


def run_code_safely(code: str) -> tuple[str, str, bool]:
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    error = None
    try:
        safe_globals = {
            "__builtins__": {
                "print": print, "range": range, "len": len, "int": int, "float": float,
                "str": str, "bool": bool, "list": list, "dict": dict, "tuple": tuple,
                "set": set, "sorted": sorted, "sum": sum, "min": min, "max": max,
                "abs": abs, "round": round, "enumerate": enumerate, "zip": zip,
                "map": map, "filter": filter, "input": lambda _="": "",
                "type": type, "isinstance": isinstance, "hasattr": hasattr,
                "getattr": getattr, "__import__": __builtins__.__import__,
            }
        }
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
            exec(code, safe_globals)
    except Exception:
        error = traceback.format_exc()

    output = stdout_buf.getvalue()
    stderr_out = stderr_buf.getvalue()
    full_error = (error or "") + (stderr_out or "")
    return output, full_error, error is None


def main():
    st.markdown("# 💻 Code Lab")
    st.markdown("*Viết code, chạy thử, nhận AI review — học bằng cách làm là nhanh nhất!*")
    st.markdown("---")

    col_editor, col_panel = st.columns([3, 2])

    with col_editor:
        starter = st.session_state.pop("code_lab_starter", None)
        task_desc = st.session_state.pop("code_lab_task", None)

        if "code_content" not in st.session_state:
            st.session_state.code_content = TEMPLATES["Hello World"]["code"]
        if starter:
            st.session_state.code_content = starter

        if task_desc:
            st.info(f"📌 **Bài tập:** {task_desc}")

        st.markdown("### ✏️ Editor")
        code = st.text_area(
            "Python code:",
            value=st.session_state.code_content,
            height=380,
            key="code_editor",
            label_visibility="collapsed",
            help="Viết code Python tại đây rồi nhấn Chạy",
        )
        st.session_state.code_content = code

        c1, c2, c3 = st.columns(3)
        with c1:
            run_btn = st.button("▶️ Chạy Code", type="primary", use_container_width=True)
        with c2:
            review_btn = st.button("🤖 AI Review", use_container_width=True)
        with c3:
            clear_btn = st.button("🗑️ Xóa", use_container_width=True)

        if clear_btn:
            st.session_state.code_content = "# Viết code tại đây\n"
            st.rerun()

        if run_btn:
            output, error, success = run_code_safely(code)
            st.session_state["run_output"] = output
            st.session_state["run_error"] = error
            st.session_state["run_success"] = success
            st.session_state["ai_review"] = None

        if review_btn and code.strip():
            with st.spinner("🤖 AI đang review code..."):
                task = task_desc or "Bài tập Python tự do"
                review = review_code(code, task)
                st.session_state["ai_review"] = review

        if "run_output" in st.session_state or "run_error" in st.session_state:
            st.markdown("### 📤 Kết quả")
            output = st.session_state.get("run_output", "")
            error = st.session_state.get("run_error", "")
            success = st.session_state.get("run_success", True)

            if success and output:
                st.markdown(f'<div class="code-output output-ok">{output}</div>', unsafe_allow_html=True)
            elif not success and error:
                st.markdown(f'<div class="code-output output-err">{error}</div>', unsafe_allow_html=True)
                if st.button("💡 AI giải thích lỗi này", key="explain_err"):
                    with st.spinner("Đang phân tích lỗi..."):
                        explanation = explain_error(code, error)
                        st.session_state["error_explanation"] = explanation
            else:
                st.markdown('<div class="code-output output-empty">(Không có output)</div>', unsafe_allow_html=True)

        if st.session_state.get("error_explanation"):
            with st.expander("💡 Giải thích lỗi từ AI", expanded=True):
                st.markdown(st.session_state["error_explanation"])

        if st.session_state.get("ai_review"):
            st.markdown("### 🤖 AI Review")
            st.markdown(st.session_state["ai_review"])

    with col_panel:
        st.markdown("### 📋 Template mẫu")
        for name, tmpl in TEMPLATES.items():
            if st.button(f"📄 {name}", key=f"tmpl_{name}", use_container_width=True,
                         help=tmpl["desc"]):
                st.session_state.code_content = tmpl["code"]
                st.rerun()

        st.markdown("---")
        st.markdown("### 📌 Chú thích nhanh")
        st.markdown("""
**In ra màn hình:**
```python
print("Hello!")
print(f"Số: {bien}")
```

**Biến và phép tính:**
```python
x = 10
y = 3.5
tong = x + y
```

**If/else:**
```python
if diem >= 8:
    print("Giỏi")
elif diem >= 6:
    print("Khá")
else:
    print("Trung bình")
```

**For loop:**
```python
for i in range(5):
    print(i)

for item in danh_sach:
    print(item)
```

**Hàm:**
```python
def tinh_tong(a, b):
    return a + b

ket_qua = tinh_tong(3, 4)
```
""")

        st.markdown("---")
        st.markdown("### ⚠️ Giới hạn")
        st.info("Code chạy trong môi trường an toàn. Một số thư viện (file I/O, network) bị giới hạn. Dùng để học lý thuyết Python cơ bản.")


if __name__ == "__main__":
    main()
