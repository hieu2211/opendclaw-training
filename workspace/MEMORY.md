# MEMORY.md — Điều đã học được từ AGS (chắt lọc, có thể nạp thẳng làm bộ nhớ dài hạn)

## Nguyên tắc thiết kế của AGS (đáng bắt chước)
- **Một lệnh, phần còn lại do host lo.** `ags online cat=idea …` chạy nền, host tự ốp lại chính cuộc chat ở từng bước và **kiểm bằng mã**
  (đếm chữ, đủ trường, dựng trang xong mới cho qua). Đừng đi đường vòng bỏ qua phần kiểm.
- **Bài hướng dẫn nằm trên host, lấy theo tên** (`/api/agent-prompt?name=…`) — agent luôn đọc bản mới nhất; bảng "từ khoá → lệnh" chỉ là mục lục.
- **Nén bằng con trỏ, không gộp nghĩa** (snap + `@ID` → bản ghi gốc). Bản ghi chỉ thêm; snap là chỗ duy nhất được viết đè, và viết đè phải gộp.
- **Việc giữa các agent là bất đồng bộ**: gửi xong làm việc khác, kết quả tự bơm về; host nhắc hộ khi bên kia im.
- **Agent nhận việc không được hỏi lại** (không ai bấm) → gom câu hỏi vào log, chốt done kèm danh sách.
- **Dữ liệu riêng ở lại máy** (giọng clone, lịch sử chat, khoá API).

## Sự kiện & mốc (2026-09)
- 2026-09-16/17: dựng cầu đồng bộ lịch sử AGS → sidebar Claude Desktop bằng hook `Stop` + script quét `.jsonl` (5 bẫy: cp1252, UTC, lọc sai, app chỉ đọc lúc
  khởi động, app xoá thư mục sổ). Chiều ngược lại (Desktop → AGS) không có API sạch — đã chốt bỏ, không điều tra lại.
- 2026-09-18: dựng lại đồng bộ log thành tiến trình nền bền (Startup folder + supervisor + khoá PID). Lỗi thật đã sửa: `ds:null`, lượt không bao giờ `chot`,
  rò `CLAUDE_CODE_SESSION_ID`, dồn nhiều supervisor. Suýt sập app vì `taskkill ags.exe` — **cấm lặp lại**.
- Người dùng đã bác cách "hạ cấp im lặng": phải nghe đúng ý ("đừng bắt tôi nhờ thủ công" ≠ "cấm mọi chi phí").

## Sự thật cần nhớ
- AGS = điều phối agent CLI; nó gọi chính CLI (`claude`, …) trên máy → nhật ký agent nằm ở nơi CLI ghi (`~/.claude/projects/…jsonl`).
- `ags qa` bóc lời qua lại từ màn hình agent → có thể lẫn khung terminal; đó là bình thường, không phải bug parse.
- `zalo-bot` ≠ `zalo`. Gửi ảnh Zalo bị chặn. Nhóm trùng tên → dùng `thread_id`.
- Edge TTS ~65 s/1000 ký tự (không clone); OmniVoice ~740 s/1000 ký tự CPU (có clone, chạy tại máy).
- Snap tối đa `max_len`; điều mới lên đầu; mẩu `(!)` là ghim, giữ nguyên.
