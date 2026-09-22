---
name: ags-zalo-bot
description: Đọc/gửi tin Zalo cá nhân và dựng chatbot trả lời tự động bằng mini-app zalo-bot của AGS (cài, quét QR, chọn chat lắng nghe, đặt rule chuyển tin sang agent, hook lọc, duyệt vào nhóm). Dùng khi người dùng nói "Zalo", "tạo chatbot", "bot trả lời khách", "trực nhóm", "kết nối Zalo".
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Zalo Bot — tin nhắn Zalo CÁ NHÂN + chatbot tự trả lời

"Tạo chatbot cho tôi / làm con bot trả lời khách / kết nối Zalo / cho bot trực nhóm" đều là VIỆC NÀY —
**đừng viết bot mới từ đầu**. Bộ máy có sẵn, bạn chỉ ráp:

`zalo-bot` bắt tin → **rule** bơm tin sang một cuộc chat agent → agent trả lời → `send` gửi ngược lại Zalo.

`zalo-bot` = Zalo CÁ NHÂN (lái trình duyệt đã đăng nhập Zalo Web, lưu tin vào kho local). **KHÁC** mini-app `zalo`
(Bot Platform/OA).

## Bước 0 — LUÔN kiểm tra, đừng giả định

```
ags plugin zalo-bot status
```
Chưa cài → TỰ cài từ Chợ (đừng bảo người dùng đi cài):
```
ags api POST /api/plugins/install '{"id":"zalo-bot"}'
ags api GET  /api/plugins/install-status      # lặp tới khi xong rồi mới dùng tiếp
```

## Đăng nhập — chỉ quét QR (không có user/pass)

```
ags plugin zalo-bot start          # mở trình duyệt + bắt đầu đọc tin
ags plugin zalo-bot screenshot     # PNG base64 màn Zalo — QR nằm ở đây
ags plugin zalo-bot status         # need_relogin=true → phải quét lại
```
Chụp xong ĐƯA ẢNH cho người dùng (ghi ra file → `ags view <file>.png`) để họ quét bằng điện thoại. Đừng mô tả suông.

## Chọn chat được lắng nghe (chỉ tin trong danh sách này mới tới agent)

```
ags plugin zalo-bot sync_groups
ags plugin zalo-bot threads_get
ags plugin zalo-bot threads_set '{"selected":["<thread_id>","<thread_id2>"]}'
```
⚠ Nhóm TRÙNG TÊN là chuyện thường → luôn định danh bằng `thread_id`, không bằng tên.

## Rule điều phối — tin của nhóm nào bơm sang cuộc chat agent nào

```
ags plugin zalo-bot rules_get
ags plugin zalo-bot rule_save '{"groups":["<thread_id>"],"all_private":false,"conv":<conv_id agent nhận>,"batch":20,"nicks":[],"format":""}'
ags plugin zalo-bot rule_delete '{"id":"<rule_id>"}'
```
- `batch` = số giây gom tin trước khi bơm (đừng để mỗi tin đánh thức agent một lần).
- `nicks` rỗng = mọi người. `format` là mẫu tin với `{nick} {group} {message} {thread_id}`.
- Nâng cao — hook Python lọc/biến đổi tin: `rule_set_hook '{"id":"…","filter_script":"/đường/dẫn/hook.py"}'`,
  `hook_context '{"id":"…"}'` (id/tên nhóm + UID/nick lịch sử để viết hook), `sender_identities`, `senders`.

## Đọc / gửi / trả lời

```
ags plugin zalo-bot messages '{"ThreadID":"<id>","Limit":30}'       # kho local, chạy cả khi trình duyệt tắt
ags plugin zalo-bot send '{"thread_id":"<id>","group":false,"message":"<nội dung>"}'
ags plugin zalo-bot inbox_feed          # tin của chat ĐÃ tick — thứ thực sự đưa agent xử lý
ags plugin zalo-bot recent              # tin vừa bắt được (RAM) — soi khi nghi sót tin
ags plugin zalo-bot batches             # các lô đang gom
ags plugin zalo-bot reply '{"batch_id":"<id>","send":true}'      # send | skip
ags plugin zalo-bot forward_pending     # tin đang chờ bơm, chưa trả lời
```

## Duyệt người xin vào nhóm (cần quyền trưởng/phó nhóm)

```
ags plugin zalo-bot group_pending '{"group_id":"<id>"}'
ags plugin zalo-bot group_review '{"group_id":"<id>","members":["<uid>"],"approve":true}'
```

## Cấu hình & vận hành

```
ags plugin zalo-bot config_get
ags plugin zalo-bot config_set '{"autostart":true,"store":true,"headless":false}'
ags plugin zalo-bot stop | pause | kill_browsers | browsers | avatars | check_zca
```

## Cảnh báo

- **GỬI ẢNH hiện bị Zalo chặn theo tài khoản** (đọc ảnh vẫn được) — đừng hứa với người dùng là gửi được.
- Khi giao việc cho agent trả lời: dặn kèm "ĐỪNG dùng công cụ hỏi lại — không ai bấm trả lời → treo" (xem `ags-multi-agent-chat`).
