# 🚀 DevPath AI — Học Lập Trình Cùng AI

Ứng dụng học lập trình Python từ cơ bản đến nâng cao, tích hợp AI Mentor (Claude), dành cho người Việt mới bắt đầu.

## Tính năng

- 🤖 **AI Mentor** — Chat hỏi đáp, giải thích code bằng tiếng Việt (Claude Haiku)
- 📚 **Bài Học** — 4 phase, nhiều module, nội dung + quiz + bài tập thực hành
- 💻 **Code Lab** — Viết và chạy Python trực tiếp, AI review code
- 📊 **Tiến Độ** — Theo dõi XP, level, streak, thành tích

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cấu hình API Key

Tạo file `.streamlit/secrets.toml` (KHÔNG commit lên GitHub):

```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

## Cấu trúc

```
devpath-ai/
├── app.py              # Dashboard chính
├── curriculum.py       # Nội dung bài học
├── progress.py         # Theo dõi tiến độ
├── ai_mentor.py        # Tích hợp Claude API
├── pages/
│   ├── 1_🤖_AI_Mentor.py
│   ├── 2_📚_Bài_Học.py
│   ├── 3_💻_Code_Lab.py
│   └── 4_📊_Tiến_Độ.py
└── .streamlit/
    └── config.toml     # Dark theme
```
