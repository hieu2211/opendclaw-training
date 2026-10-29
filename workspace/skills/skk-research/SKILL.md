---
name: skk-research
description: Điều phối nghiên cứu đa ngữ thuần OpenClaw — tìm kiếm nhiều ngôn ngữ, ghi file .md có dẫn nguồn, cho AI khác phản biện, dựng báo cáo HTML xem được. Dùng khi người dùng nói "skk research", "nghiên cứu vấn đề", "research kèm <chủ đề>", "điều tra", "tra cứu sâu".
---

# SKK Research — nghiên cứu đa ngữ có nguồn + phản biện (thuần OpenClaw)

Không phụ thuộc công cụ ngoài (như AGS). Chỉ dùng tool OpenClaw sẵn có: `sessions_spawn`,
`sessions_send`, `sessions_yield`, `subagents`, `message`, `exec`, `WebSearch`/`WebFetch` (nếu tool
policy cấp).

## Bước 0 — Hỏi cấu hình
Hỏi người dùng nghiên cứu vấn đề gì trước khi bắt đầu (ngôn ngữ cần tra, số trang đọc mỗi
ngôn ngữ N, AI nào phản biện — mặc định dùng model mạnh nhất có sẵn).

## Bước 1 — Mở phiên Research
- Thay cho "conv RID" của AGS: dùng `taskName` dạng `skk-research-<slug>` làm handle cố định.
- Tìm phiên cũ qua `sessions_list` (lọc `label` chứa `[SKK Research]`); còn hoạt động thì dùng
  lại, không có thì `sessions_spawn` tạo mới (`context: "isolated"`, `label: "[SKK Research] <slug>"`).

## Bước 2 — Giao nghiên cứu
- Giao việc tìm kiếm cho subagent qua `sessions_spawn`/`sessions_send`: dùng `WebSearch`/`WebFetch`
  nếu agent có; không có thì dùng `exec` (curl, trình duyệt CLI sẵn trên máy) để tra từng ngôn ngữ.
- Đọc top N trang, dịch yêu cầu sang các ngôn ngữ đã chọn, lặp lại cho mỗi ngôn ngữ.
- Ghi kết quả vào `skk-research-<slug>.md` trong workspace, luôn dẫn URL nguồn; mâu thuẫn ghi
  cả hai phía.
- Subagent không được hỏi lại người dùng giữa đường (đầu kia cũng là agent).
- Dùng `subagents(action="wait")` chờ xong, kiểm file `.md` tồn tại và có ít nhất 1 URL trước
  khi qua bước 3.

## Bước 3 — AI phản biện
- Model có sẵn trong OpenClaw: `sessions_spawn` subagent với `model` override tương ứng, giao
  đọc file `.md` và phản biện.
- AI ngoài có bot/account đã cấu hình (theo danh bạ `MEMORY.md`): gửi file qua
  `message(action="send")` tới bot đó, chờ trả lời. Chưa cấu hình thì báo người dùng cần làm
  thủ công, không tự bịa kết nối.
- Cập nhật `.md` theo phản biện, kèm nguồn (session key / chat đã phản biện).

## Bước 4 — Sinh HTML và dọn dẹp
- Tạo `skk-research-<slug>.html` tự chứa (CSS + JS inline, không phụ thuộc file ngoài).
- Hiện cho người dùng ngay: webchat/Control UI dùng `[embed ...]`, kênh khác đính kèm
  `MEDIA:<path>`. Không chỉ in đường dẫn.
- Dọn dẹp: phiên subagent spawn ở bước 1 dùng `cleanup: "delete"`; nếu là session visible thì
  `sessions(action="delete")` khi xong.

## Bước 5 — Báo người dùng
Tóm tắt ngắn: đường dẫn `.md` + `.html`, số nguồn đã dẫn, AI nào đã phản biện, phiên đã dọn.

## Lưu ý
- Không giả định có binary ngoài; luôn dùng tool OpenClaw đã cấp trong tool policy.
- Tool OpenClaw đã làm được việc gì (spawn, gửi tin, đính file) thì dùng, đừng tự viết script
  thay thế.
