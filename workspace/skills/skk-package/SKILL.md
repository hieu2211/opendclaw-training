---
name: skk-package
description: Cài phần mềm/addon mới, tích hợp khả năng chưa có, hoặc kiểm tra công cụ đã cài trên máy. Dùng khi người dùng nói "cài phần mềm", "thiếu công cụ", "cài addon", "tích hợp", "cài thêm skill", "máy có cái này chưa".
---

# SKK Package — cài & kiểm tra công cụ trên OpenClaw

## Cơ chế thật của AGS (`ags package -h` / `ags tools -h`) — để đối chiếu, không copy

- `ags package install/uninstall <id>`: CHỈ nhận id trong danh sách cố định AGS tự khai: agent CLI
  (`claude codex cursor kiro grok antigravity opencode` — cài xong tự tích hợp đăng ký vào AGS) và
  phần mềm (`edge-tts omnivoice zca-js`). Gõ sai id → lệnh tự trả danh sách id đúng. Trả về job
  chạy nền `{"job":{"id":"pkg-…"}}`, theo dõi qua `ags api GET /api/package/job?id=...`;
  `already:true` = máy có sẵn, khỏi làm.
- `ags tools`: chỉ in bảng tĩnh tool do addon trên máy khai báo sẵn (nhãn + lệnh), không cài gì.

## Vì sao không map 1:1

AGS giới hạn cố định ~10 id vì đó là server/host riêng của AGS tự quản lý job cài + tự tích hợp
agent CLI vào chính nó. OpenClaw không có whitelist id cố định kiểu đó, cũng không có cơ chế
"job cài nền" riêng — OpenClaw có ClawHub (chợ skill/plugin mở, không giới hạn danh sách cứng) và
`exec` (package manager hệ thống thật, không giả lập job). Copy "bảng id cố định" vào đây là bịa
— OpenClaw không hỗ trợ đúng những id đó. Thay bằng 2 đường thật dưới.

## Thứ tự ưu tiên khi cần "khả năng mới"

1. **Tìm trên ClawHub trước** — dùng `message(action="send", clawhub={query:"<tên khả năng>"})`.
   Chợ skill/plugin chính thức của OpenClaw, trả card cài đặt cho người dùng bấm chọn. Luôn thử
   bước này trước khi nghĩ tới cài tay.
2. **ClawHub không có** → hỏi người dùng xác nhận có thực sự cần công cụ hệ thống thuần (ffmpeg,
   yt-dlp, 1 binary CLI...) không. Xác nhận xong mới `exec` cài qua package manager sẵn có của hệ
   (apt/pip/npm) — viết rõ lệnh sẽ chạy trước khi chạy, không âm thầm cài.
   Ví dụ xin xác nhận: "Máy chưa có ffmpeg, chạy `apt-get install -y ffmpeg` có đồng ý không?"
3. **Không bao giờ** tự `openclaw update`, tự cài global npm/pip làm đổi hệ thống lớn, hay bypass
   approval exec — theo đúng luật "OpenClaw Control" trong AGENTS.md nền tảng. Cần update OpenClaw
   thì chỉ hướng dẫn người dùng gõ `/update` trong chat (nếu là owner) hoặc nhờ operator chạy
   `openclaw update` ngoài terminal.

## Kiểm tra addon/tool đã có trên máy (thay `ags tools`)

Không có bảng liệt kê tĩnh — dò bằng lệnh thật qua `exec`:
```
which ffmpeg yt-dlp pandoc libreoffice node python3 2>/dev/null
ls /home/node/.openclaw/workspace/skills/
cat /home/node/.openclaw/workspace/skills/<tên-skill>/SKILL.md   # đọc metadata.requires.bins
```
`metadata.openclaw.requires.bins` trong frontmatter mỗi SKILL.md (vd skk-aba yêu cầu bin
`skk-aba`) là nguồn thật cho biết skill đó cần gì — kiểm `which <bin>` để biết addon có hoạt
động thật hay chỉ là file skill rỗng không có backend.

## Giản lược có chủ đích

- Không build catalog JSON riêng để track "đã cài gì" → skipped: state phân tán theo
  `which`/`ls` thật, add khi có >20 addon cần tra cứu nhanh và cần index tập trung.
- Không tự động hoá bước cài apt/pip → skipped: luôn cần người xác nhận trước, add bước
  tự động chỉ khi có whitelist lệnh an toàn rõ ràng từ operator.
