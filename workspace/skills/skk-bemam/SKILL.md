---
name: skk-bemam
description: Ghi chú giới hạn - ags bemam (addon bemam-mini gom nhiều tài khoản LLM) KHÔNG có tương đương trực tiếp trong OpenClaw. Dùng khi người dùng hỏi "bé Mầm", "bé mầm mini", "gom tài khoản LLM", "đổi model", "API key" để trả lời đúng cách OpenClaw làm.
---

# SKK Bemam — model/API key thuần OpenClaw (không map 1:1 từ `ags bemam`)

## AGS gốc làm gì (đọc từ `ags bemam -h` thật, không suy đoán)

`ags bemam` giao diện tới addon **`bemam-mini`**: một proxy chạy ngay trên máy, gom nhiều tài
khoản LLM (Google/Antigravity, Claude, Codex, xAI, Kimi…) + kho API key, xoay vòng
**round-robin** giữa các tài khoản, rồi cho dùng như một agent trong AGS.

Lệnh chính: `status` (đang chạy chưa, cổng nào, dùng model gì), `accounts` (kho tài khoản đã
đăng nhập: email/provider/hạn), `models` (model dùng được + đang chọn), `model_set
'{"model":"..."}'`, `apikeys` (kho API key + provider nhận key, có OpenRouter), `login_start
'{"provider":"..."}'` + `login_status` (lấy link đăng nhập — phải mở TRÊN MÁY CHẠY NÃO vì
callback về localhost máy đó). Còn có `install`/`install_status`/`uninstall`,
`service {"op":"restart"}`, `apikey_add`/`apikey_delete`, `account_delete`,
`optimize_get`/`optimize_set`.

## Phản biện: vì sao không map 1:1

`bemam-mini` là kiến trúc **multi-account-pool** gắn chặt vào app AGS: nhiều tài khoản LLM cùng
provider xoay vòng round-robin để né rate-limit/hết quota, gắn thẳng vào tiến trình chạy trên
một máy cụ thể (đăng nhập phải mở link TRÊN MÁY CHẠY NÃO).

OpenClaw có mô hình khác hẳn: mỗi session/agent gắn với một model + provider cấu hình sẵn ở
tầng platform (gateway/models/agents trong config), không có khái niệm "pool nhiều tài khoản
xoay vòng trong 1 agent". Tự giả lập round-robin tài khoản bằng code riêng là dựng thêm một hệ
thống KHÔNG ai yêu cầu, lệch khỏi kiến trúc quản lý model/credential đã có của platform — vi
phạm YAGNI và dễ dựng vùng quản lý thông tin đăng nhập không ai audit.

## Cách dùng trong OpenClaw khi người dùng cần việc tương tự

- "Đổi model đang dùng" → `session_status(model="...")` override theo session hiện tại, hoặc
  sửa cấu hình `models`/`agents` ở tầng platform (việc của operator, không phải agent tự sửa
  file cấu hình hệ thống qua chat).
- "Thêm/xoá API key của provider" → thuộc nhóm thiết lập credential, theo đúng luật platform:
  qua `openclaw configure` ở terminal (prompt tự che secret) — agent KHÔNG thu thập API key qua
  chat, không tự ghi vào file config.
- "Dùng nhiều provider khác nhau cho các việc khác nhau" → đã có sẵn ở tầng OpenClaw: mỗi
  agent/session có thể cấu hình model riêng; `sessions_spawn(model="...")` override model cho
  một subagent cụ thể theo việc, không cần proxy pool riêng.

## Giới hạn / Giản lược có chủ đích

- Không viết proxy/round-robin nhiều tài khoản LLM riêng.
- Không tự lưu trữ/xoay API key trong workspace, không có lệnh `accounts`/`apikeys` liệt kê kho
  tài khoản (không có kho tài khoản nào để liệt kê).
- Không có `login_start`/`login_status` tự động đăng nhập provider qua link callback localhost —
  đăng nhập/API key luôn qua `openclaw configure` ở terminal.
- Người dùng cần đúng tính năng "pool nhiều tài khoản xoay vòng" như AGS → nói rõ OpenClaw chưa
  có tính năng này ở tầng platform, không giả lập bằng code tạm.
