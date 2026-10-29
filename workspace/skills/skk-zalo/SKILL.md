---
name: skk-zalo
description: Đọc/gửi tin Zalo cá nhân, chatbot trả lời khách qua kênh Zalo, thuần OpenClaw (thay ags zalo / addon zalo-bot). Dùng khi người dùng nói "Zalo", "chatbot Zalo", "bot trả lời khách", "trực nhóm Zalo".
---

# SKK Zalo — Zalo cá nhân thuần OpenClaw (thay addon `zalo-bot` của AGS)

## AGS gốc làm gì (đọc từ `ags zalo -h` thật, không suy đoán)

`ags zalo` giao diện tới addon **`zalo-bot`** = tin nhắn Zalo **CÁ NHÂN** của người dùng (KHÁC
hẳn addon `zalo` là Bot Platform/OA — hai thứ khác nhau, không lẫn). Cơ chế: lái một trình duyệt
đã đăng nhập Zalo Web, lưu tin vào kho **SQLite local** (`~/.config/ags/zalo_bridge.db`, bảng
`zalo_bridge_messages`/`zalo_batches`), rồi bơm tin của các chat được chọn sang một cuộc chat
agent theo "rule".

Luồng: `status` (kiểm trước khi làm gì) → `start` (mở trình duyệt, bắt tin) → `screenshot`
(ảnh PNG có QR, đăng nhập CHỈ bằng quét QR, không user/pass) → `threads_get`/`threads_set`
(chọn thread_id lắng nghe, tên trùng là chuyện thường nên luôn định danh bằng thread_id) →
`rule_save`/`rule_delete`/`rule_set_hook` (nhóm nào bơm sang conv agent nào, `batch`=giây gom
tin, hook Python lọc/biến đổi) → `messages`/`send`/`reply`/`forward_pending`/`inbox_feed`/
`recent`/`batches` (đọc/gửi/trả lời/theo dõi lô đang gom) → `group_pending`/`group_review`
(duyệt người xin vào nhóm) → `config_get`/`config_set`, `stop`/`pause`/`kill_browsers`.
Gắn thẻ trong nhóm bằng `@<mã người>` hoặc `@All`, ảnh/file gửi kèm là đường dẫn tuyệt đối tối
đa 25MB.

## Phản biện: vì sao không map 1:1

- `zalo-bot` tự lái một trình duyệt Zalo Web + tự quét QR qua ảnh chụp màn hình — OpenClaw không
  tự động hoá đăng nhập Zalo qua chat (không thu thập QR/cookie/session riêng); xác thực kênh
  là việc cấu hình platform một lần, không phải việc lặp lại trong mỗi turn của agent.
- `zalo-bot` tự quản kho SQLite riêng + bảng rule/batch/hook để quyết định tin nào bơm vào conv
  nào — OpenClaw đã có tầng channel + binding channel→agent/session ở platform; viết lại một
  tầng rule/batch riêng trong workspace là trùng lặp kiến trúc có sẵn (YAGNI).
- Hai addon `zalo` (OA/Bot Platform) và `zalo-bot` (cá nhân) tách biệt bên AGS; OpenClaw gộp cả
  hai kiểu Zalo vào `message` tool qua hai channel id khác nhau (`zalo` cho OA, `zalouser` cho cá
  nhân) — không nhầm lẫn khi chọn target.

## Cách OpenClaw làm tương đương

### Thiết lập kênh (một lần, do operator làm qua terminal, KHÔNG qua chat)

```
openclaw channels add zalo
```
hoặc `openclaw configure` — prompt tự hỏi/che thông tin đăng nhập. Agent **không** tự quét QR,
không tự thu thập cookie/token qua chat. Người dùng đưa QR/token trong chat → nhắc họ dùng lệnh
terminal trên, không nhận hộ.

Channel `zalo` = Zalo Bot Platform/OA; channel `zalouser` = Zalo cá nhân (tương ứng `zalo-bot`
của AGS). Chọn đúng channel theo nhu cầu người dùng.

### Đọc / gửi tin (sau khi channel đã cấu hình)

```
message(action="send", channel="zalouser", target="<id hội thoại/số điện thoại>", message="<nội dung>")
message(action="read", channel="zalouser", channelId="<id>")
```

- Gửi kèm ảnh/file: thêm `attachments` (type `image`/`file`, `media` là đường dẫn/base64).
- Group chat: `target` dùng đúng id nhóm theo định dạng channel trả về, không suy đoán theo
  tên (tên trùng là chuyện thường — AGS cũng cảnh báo y vậy với `thread_id`).

### Chatbot tự động trả lời khách

AGS cần "rule" riêng + `batch` giây gom tin bơm vào 1 conv. OpenClaw: binding channel→agent/
session có sẵn ở tầng platform — tin tới là một turn bình thường, agent trả lời bằng
`message(action="send")`, không cần tầng rule/batch/hook riêng.

- "Gom nhiều tin trước khi trả lời" (= `batch` của AGS): để agent tự đọc các tin gần nhất trong
  turn hiện tại trước khi trả lời, không cần cấu hình batch-N-giây.

## Giới hạn / Giản lược có chủ đích

- Không tự lái trình duyệt Zalo Web, không tự chụp/đọc QR qua chat — xác thực kênh luôn qua
  `openclaw channels add`/`openclaw configure` ở terminal.
- Không có kho SQLite riêng để query trực tiếp lịch sử tin — đọc lịch sử qua
  `message(action="read")`, không có truy vấn SQL tuỳ ý như AGS.
- Không có khái niệm `rule`/`hook` Python lọc tin theo nhóm riêng — lọc/xử lý nằm trong logic
  agent khi nhận turn, không phải cấu hình riêng trước đó.
- Không có lệnh duyệt người xin vào nhóm (`group_pending`/`group_review`) — ngoài phạm vi
  `message` tool hiện có; thiếu, cần nêu rõ nếu người dùng hỏi tới.
