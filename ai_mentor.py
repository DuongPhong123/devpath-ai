import os
import streamlit as st

try:
    import google.generativeai as genai
    _MODEL = None

    def get_model():
        global _MODEL
        if _MODEL is None:
            api_key = os.environ.get("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
            if not api_key:
                return None
            genai.configure(api_key=api_key)
            _MODEL = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_PROMPT,
            )
        return _MODEL

except ImportError:
    def get_model():
        return None


SYSTEM_PROMPT = """Bạn là DevPath AI — trợ lý dạy lập trình thông minh, thân thiện dành cho người Việt Nam mới bắt đầu học code.

Phong cách:
- Giải thích bằng tiếng Việt, đơn giản, dễ hiểu như đang nói chuyện với bạn bè
- Dùng ví dụ thực tế từ công việc văn phòng, HR, kế toán — gần gũi với người không biết code
- Khuyến khích, tích cực, không phán xét khi học viên mắc lỗi
- Khi giải thích code, luôn có phần "Tại sao lại như vậy?" và ví dụ chạy được
- Format câu trả lời: dùng markdown với headers, bullet points, code blocks

Quy tắc:
- Nếu học viên hỏi ngoài chủ đề lập trình, nhẹ nhàng hướng về bài học
- Luôn kết thúc bằng một câu hỏi gợi mở hoặc bài tập nhỏ để học viên thực hành
- Khi giải thích lỗi code, chỉ rõ VÀ giải thích TẠI SAO lỗi đó xảy ra
"""


def _to_gemini_history(messages: list[dict]) -> list[dict]:
    history = []
    for m in messages:
        role = "model" if m["role"] == "assistant" else "user"
        history.append({"role": role, "parts": [m["content"]]})
    return history


def stream_chat(messages: list[dict], lesson_context: str = None) -> str:
    model = get_model()
    if not model:
        yield "⚠️ Chưa cấu hình GEMINI_API_KEY. Vào Streamlit Cloud → Settings → Secrets và thêm key nhé anh!"
        return

    system_extra = ""
    if lesson_context:
        system_extra = f"\n\nBài học hiện tại:\n{lesson_context}"

    history = _to_gemini_history(messages[:-1])
    last_msg = messages[-1]["content"] + system_extra

    try:
        chat = model.start_chat(history=history)
        response = chat.send_message(last_msg, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        err = str(e)
        if "API_KEY" in err.upper() or "403" in err:
            yield "❌ API key không hợp lệ. Kiểm tra lại GEMINI_API_KEY trong Secrets nhé anh."
        elif "quota" in err.lower() or "429" in err:
            yield "⏳ Đang bận quá (quota), thử lại sau 1 phút anh nhé!"
        else:
            yield f"❌ Lỗi kết nối AI: {err}"


def review_code(code: str, task_description: str) -> str:
    model = get_model()
    if not model:
        return "⚠️ Chưa cấu hình GEMINI_API_KEY."

    prompt = f"""Anh vừa viết đoạn code Python sau để giải bài tập:

**Yêu cầu bài tập:** {task_description}

**Code của anh:**
```python
{code}
```

Hãy review code theo 3 phần:
1. ✅ **Điểm tốt** — những gì anh làm đúng
2. 🔧 **Cải thiện** — code có chạy không, lỗi gì không, tối ưu hơn được không
3. 💡 **Gợi ý** — cách viết Pythonic hơn (nếu có)

Giải thích đơn giản, thân thiện nhé!"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Không thể review code: {str(e)}"


def explain_error(code: str, error_msg: str) -> str:
    model = get_model()
    if not model:
        return "⚠️ Chưa cấu hình GEMINI_API_KEY."

    prompt = f"""Code Python của anh bị lỗi:

```python
{code}
```

**Thông báo lỗi:**
```
{error_msg}
```

Giải thích:
1. Lỗi này là lỗi gì, tại sao xảy ra
2. Cách sửa cụ thể
3. Cách tránh lỗi này trong tương lai"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"
