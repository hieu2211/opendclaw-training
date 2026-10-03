# Bộ "huấn luyện" OpenClaw từ tri thức AGS

Chắt từ: skill `ags` + `agsmem`, 8 bài `agent-prompt` trên host AGS (`viral`, `zalo_bot`, `cf_voice`, `bemam`, `affix`, `brand`,
`form`, `aba`), help các lệnh `ags`, và các bài học vận hành đã ghi trong bộ nhớ dự án. Đây là **gói sống** — mỗi khi AGS
thêm năng lực mới hoặc có bài học mới đáng nhớ thì cập nhật tiếp, không phải làm một lần rồi xong (xem `workspace/MEMORY.md`).
Đã bỏ sạch tên/email/tài khoản/đường dẫn cá nhân (`ags` gọi thẳng hoặc qua `$AGS`).

```
openclaw-training/
├─ workspace/                     ← thả vào workspace của OpenClaw (mặc định ~/.openclaw/workspace)
│  ├─ AGENTS.md                   nguyên tắc làm việc kiểu AGS
│  ├─ TOOLS.md                    bảng tra nhanh lệnh/endpoint
│  ├─ MEMORY.md                   bộ nhớ dài hạn: nguyên tắc thiết kế, mốc, sự thật cần nhớ
│  ├─ TOKEN-OPTIMIZATION.md       cơ chế tiết kiệm token của AGS (affix) + nếp nghĩ tương tự ở nơi khác trong hệ thống
│  └─ skills/
│     ├─ ags-core/                điểm vào + 4 luật nền (gồm luật mã lượt #a1b2c) + bảng từ khoá → lệnh
│     ├─ ags-multi-agent-chat/    ags chat + ags task (giao/nhận việc, luật "đừng hỏi lại")
│     ├─ ags-memory/              AGSMem: ghi nóng, tra, snap, dọn
│     ├─ ags-zalo-bot/            chatbot Zalo cá nhân
│     ├─ ags-voice-studio/        TTS + clone giọng
│     ├─ ags-viral-ideas/         dây chuyền `online cat=idea`
│     ├─ ags-brand-profile/       hồ sơ thương hiệu/chiến dịch
│     ├─ ags-bemam-brain/         Bé Mầm Mini
│     ├─ ags-prompt-affix/        prefix/suffix/tiết kiệm token (chi tiết lệnh — xem thêm TOKEN-OPTIMIZATION.md)
│     ├─ ags-sidebar-qa/          sidebar + ags qa
│     ├─ ags-form/                `ags form` — dựng trang nhập liệu thay vì hỏi từng câu trong chat
│     ├─ ags-browser-automation/  `ags aba` — ABA/META.ai, lái trình duyệt, quay màn hình
│     └─ ags-ops-lessons/         bẫy đã dính thật (Windows, đồng bộ, tiến trình nền)
└─ dataset/
   ├─ build_dataset.py            sinh dataset (thêm ví dụ = nối `add(ex(...))`)
   ├─ ags_sft.jsonl               90 ví dụ, chat + tool-calling (messages / tool_calls)
   └─ ags_sft_alpaca.jsonl        cùng nội dung, dạng instruction/input/output
```

## Cách dùng

**Cách 1 — nạp tri thức (không cần train, hiệu quả ngay):**
chép `workspace/*` vào workspace OpenClaw (giữ nguyên thư mục `skills/`), mở phiên **mới** (skill mới không nạp vào phiên đang chạy).
Skill dùng định dạng `SKILL.md` (frontmatter `name` + `description`); `metadata.openclaw.requires.bins: ["ags"]` chỉ hiện skill khi máy có `ags`.

**Cách 2 — fine-tune mô hình:** dùng `dataset/ags_sft.jsonl` làm SFT (chat template có `tool_calls`), hoặc `ags_sft_alpaca.jsonl` nếu trainer
chỉ nhận instruction/input/output. 90 ví dụ đủ để dạy *hành vi* (định tuyến skill, đúng lệnh, đúng luật) — muốn tăng độ phủ thì nhân bản mỗi
tình huống bằng cách diễn đạt khác và lấy thêm lượt thật từ `ags qa` (nhớ lọc thông tin nhạy cảm trước).

## Lưu ý

- Các skill gọi lệnh `ags` nên chỉ **chạy được khi OpenClaw nằm cùng máy với AGS**. Phần nguyên tắc (`AGENTS.md`, `MEMORY.md`, `TOKEN-OPTIMIZATION.md`,
  `ags-ops-lessons`) dùng được ở bất kỳ đâu.
- Kết quả tool trong dataset là **mẫu minh hoạ** (mã việc, id, số liệu là ví dụ), không phải dữ liệu thật của máy nào.
- Bài `agent-prompt` nằm trên host và có thể đổi theo phiên bản AGS; skill chỉ là bản chụp (lần cuối xác nhận: 2026-10-03). Khi lệch,
  `ags api GET '/api/agent-prompt?name=…'` là nguồn đúng. `ags-form` chưa có `--help` đầy đủ lúc viết (host không phản hồi) — lấy mẫu spec
  thật trước khi dùng.
- Cố ý **không đưa vào**: lịch sử chat thô (`ags_sync_log.md`, `.ags-prompts/`) — có tên, SĐT, tài khoản; `CVS-Insight-Tool/` — dự án khác, không phải
  kiến thức AGS; `ai_trends_research_report.md` — báo cáo tin tức, không phải năng lực agent.
