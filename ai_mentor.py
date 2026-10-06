import os
import streamlit as st

try:
    import anthropic
    _CLIENT = None

    def get_client():
        global _CLIENT
        if _CLIENT is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
            if not api_key:
                return None
            _CLIENT = anthropic.Anthropic(api_key=api_key)
        return _CLIENT

except ImportError:
    def get_client():
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


def stream_chat(messages: list[dict], lesson_context: str = None) -> str:
    client = get_client()
    if not client:
        yield "⚠️ Chưa cấu hình ANTHROPIC_API_KEY. Vào `.streamlit/secrets.toml` và thêm key nhé anh!"
        return

    system = SYSTEM_PROMPT
    if lesson_context:
        system += f"\n\nBài học hiện tại:\n{lesson_context}"

    try:
        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            system=system,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield text
    except anthropic.AuthenticationError:
        yield "❌ API key không hợp lệ. Kiểm tra lại ANTHROPIC_API_KEY trong secrets.toml nhé anh."
    except anthropic.RateLimitError:
        yield "⏳ Đang bận quá, thử lại sau 1 phút anh nhé!"
    except Exception as e:
        yield f"❌ Lỗi kết nối AI: {str(e)}"


def review_code(code: str, task_description: str) -> str:
    client = get_client()
    if not client:
        return "⚠️ Chưa cấu hình ANTHROPIC_API_KEY."

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
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    except Exception as e:
        return f"❌ Không thể review code: {str(e)}"


def explain_error(code: str, error_msg: str) -> str:
    client = get_client()
    if not client:
        return "⚠️ Chưa cấu hình ANTHROPIC_API_KEY."

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
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
    except Exception as e:
        return f"❌ Lỗi: {str(e)}"
