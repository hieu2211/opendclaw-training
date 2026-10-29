---
name: skk-collab
description: Hỏi người dùng nhập liệu, giao việc/chat giữa agent, báo tiến độ, đọc lại lượt cũ — thuần OpenClaw (thay ags form + ags chat + ags task + ags qa). Dùng khi người dùng nói "hỏi lại tôi", "dựng form", "giao việc cho agent khác", "báo tiến độ", "nãy nói gì", "tóm lại chuyện vừa bàn".
---

# SKK Collab — phối hợp người/agent thuần OpenClaw

## Cơ chế thật của 4 lệnh AGS gốc (để biết mình đang gộp cái gì)

- **`ags form <file>.jsonf`**: viết file JSON mô tả trang nhập liệu (field text/radio/checkbox/
  select/media/gallery/file, có `suggest`/`suggest_text` để agent gợi ý trước, có `show_if` để ẩn
  hiện field theo field khác). Lệnh **bung trang lên màn hình người dùng rồi THOÁT NGAY, không
  chờ**. Người dùng bấm "Lưu và gửi Agent" thì có tin nhắn báo quay lại đọc chính file `.jsonf`
  đó — mỗi field giờ có thêm khoá `value`.
- **`ags chat <conv_id|token> --title "<tên>" "<lời nhắn>"`**: nhắn cho MỘT AGENT KHÁC (cùng máy
  qua `conv_id`, khác máy qua `token` mã mời). `--title` bắt buộc (hiện tab ngắn cho người dùng
  theo dõi). Bên nhận là agent, không phải người — AGS dặn kèm mỗi lần giao việc: "đừng tự hỏi
  lại, đầu kia không ai bấm trả lời". Gửi xong không chờ đồng bộ, trả lời tự hiện khi bên kia rep.
- **`ags task log/done/fail/get/list <mã>`**: mỗi việc giao qua `ags chat` có MÃ VIỆC riêng để
  báo tiến độ (`log`), chốt xong (`done` kèm toàn bộ kết quả), báo thất bại (`fail`), hoặc bên
  giao xem lại (`get`/`list`). Im lâu hệ thống tự nhắc.
- **`ags qa conv/<mã prompt>/boc`**: đọc lại kho Hỏi–Đáp cũ của máy đó, host tự bóc từ nhật ký
  agent gắn theo mã prompt — dùng khi cần tóm lại lượt cũ mà không muốn cuộn cả nhật ký.

## Vì sao KHÔNG map 1:1 từng lệnh sang OpenClaw

4 lệnh AGS tách riêng vì AGS là **CLI chạy trên máy của mỗi agent độc lập, không chung một
transcript, không chung runtime** — nên cần: form riêng (vì không có lượt hội thoại trực tiếp
với người dùng để hỏi), mã việc riêng (`task`) để hai tiến trình độc lập theo dõi nhau, kho qa
riêng để bóc ngược lại nhật ký. OpenClaw thì ngược lại: session/subagent của cùng platform, có
`sessionKey`/`taskId` định danh sẵn, có transcript có cấu trúc sẵn, có hội thoại trực tiếp với
người dùng ngay trong turn — nên 4 việc đó chập lại thành 3 nhóm tool có sẵn, không cần dựng lại
UI popup / mã việc / kho qa riêng.

## 1. Hỏi người dùng nhập liệu (thay `ags form`)

AGS bung trang web rồi thoát ngay, chờ callback đọc lại file `.jsonf`. OpenClaw không có form
popup riêng — hỏi **trực tiếp trong lượt chat hiện tại**, chờ người dùng trả lời ở lượt kế tiếp.

- Nhiều câu hỏi cùng lúc: liệt kê gọn thành danh sách đánh số trong MỘT tin nhắn, nêu rõ gợi ý/
  mặc định cho từng câu (tương đương `suggest`/`suggest_text` của AGS) để người dùng chỉ cần xác
  nhận "đúng hết" hoặc sửa điểm cụ thể.
- OpenClaw có `AskUserQuestion` nhưng công cụ này **bị chặn/không khả dụng ở agent này** (xem
  danh sách tool đầu phiên) — nên hỏi thẳng bằng text, không giả vờ gọi được.
- Không có field "media"/"gallery" riêng — gửi ảnh/video minh họa qua `message` attachment kèm
  trong cùng câu hỏi nếu cần cho người dùng xem trước khi chọn. Đây là giới hạn thật: không có
  form multi-field phức hợp (`show_if`, gallery thẻ ảnh chọn) như AGS.

## 2. Giao việc / chat giữa agent (thay `ags chat`)

```
sessions_spawn(task="<việc>", label="<tên ngắn>", taskName="<handle ổn định>")  # tạo worker mới
sessions_yield(waitFor="message")                                               # chờ kết quả, không busy-poll
```

- **Luật bắt buộc giữ nguyên từ AGS** (vẫn đúng với OpenClaw): subagent nhận việc **không được
  dùng công cụ hỏi lại người dùng** — đầu kia không có người ngồi chờ. Cần hỏi gì thì subagent
  liệt kê câu hỏi vào kết quả trả về (completion event), agent chính đọc và quyết, không để treo
  việc. Tương đương câu dặn "đừng tự hỏi lại" của `ags chat`.
- `label`/`taskName` thay cho `--title` của AGS: đặt tên ngắn để người dùng/agent cha theo dõi.
- `sessions_list` để tìm lại session đã giao trước đó (tương đương AGS `ags chat --peers`/`ghep`).

## 3. Báo tiến độ việc (thay `ags task`)

AGS có mã việc riêng tách biệt khỏi `ags chat`. OpenClaw không cần mã việc riêng — `taskId`/
`sessionKey` sinh ra khi `sessions_spawn` đã là định danh đó:

- "Báo một bước đã xong" (thay `ags task log`) → progress message trong lúc subagent chạy, hoặc
  dòng tiến độ ngay trong phản hồi hiện tại nếu cùng turn.
- "Chốt xong kèm kết quả" (thay `ags task done`) → subagent kết final reply đầy đủ kết quả, trả
  qua completion event mà `sessions_yield` đang chờ.
- "Làm không được, báo lý do" (thay `ags task fail`) → final reply nói rõ lý do thất bại, vẫn
  qua đường completion event, không cần trạng thái `fail` riêng.
- "Xem lại tiến độ/liệt kê việc" (thay `ags task get`/`list`) → `subagents(action="list"|"wait",
  taskId=...)`.

## 4. Đọc lại lượt cũ (thay `ags qa`)

AGS phải bóc ngược từ nhật ký vì CLI của nó không giữ transcript có cấu trúc kèm sẵn. OpenClaw:
lịch sử hội thoại **nằm ngay trong context phiên hiện tại** — không cần lệnh tra cứu riêng.

- Người dùng hỏi "nãy nói gì"/"tóm lại chuyện vừa bàn" → trả lời thẳng từ context đang có trong
  transcript, không gọi tool nào.
- Cần xem lại một **session khác** (không phải phiên hiện tại) → `sessions_list` tìm session đó
  (có `includeLastMessage` để xem preview), đây là khác biệt thật: AGS tra theo "mã prompt", 
  OpenClaw tra theo `sessionKey`/`sessionId`.

## Giản lược có chủ đích

- Không dựng lại UI popup `.jsonf` (field media/gallery/show_if phức hợp) — hỏi thẳng trong văn
  bản chat vì agent-người ở chung một transcript, không cần trang riêng.
- Không dựng mã việc (`task code`) riêng song song với `sessionId`/`taskId` đã có sẵn — tránh hai
  hệ định danh trùng việc.
- Không dựng kho Q&A riêng để "bóc lại" — dùng transcript context sẵn có của phiên; chỉ khi cần
  tra session khác mới gọi `sessions_list`.

## Không làm

- Không bịa field `media`/`gallery`/`show_if` giả lập bằng text — nói rõ giới hạn không có form
  multi-field thật, không giả vờ làm được.
- Không gọi `AskUserQuestion` nếu nó không có trong danh sách tool khả dụng của phiên — hỏi thẳng
  bằng text thay thế.
