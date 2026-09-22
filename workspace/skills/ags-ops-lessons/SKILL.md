---
name: ags-ops-lessons
description: Bài học vận hành đã trả giá thật khi làm việc với AGS + Claude trên Windows — đồng bộ lịch sử chat AGS↔Claude Desktop, tiến trình nền tự hồi sinh, bẫy encoding/múi giờ/lọc phiên, không giết ags.exe, hiểu đúng lời người dùng. Dùng khi debug đồng bộ AGS, viết script chạy nền trên Windows, hoặc trước khi làm việc có rủi ro làm sập AGS.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Bài học vận hành (đã dính thật, đừng dính lại)

## A. Đồng bộ lịch sử chat AGS → sidebar Claude Desktop
- AGS gọi chính CLI `claude` trên máy nên mọi chat đã nằm ở `~/.claude/projects/<khoá-thư-mục>/<id-phiên>.jsonl`.
  Sidebar app Claude **không đọc** thư mục đó; nó có sổ riêng: `%APPDATA%\Claude\claude-code-sessions\<GUID-A>\<GUID-B>\local_<uuid>.json`,
  trỏ sang chat bằng `cliSessionId` (= tên file .jsonl bỏ đuôi). **2 GUID khác nhau trên từng máy — phải tự dò, không chép cứng.**
- Cơ chế đang chạy: hook `Stop` gọi script quét `.jsonl` chưa có sổ rồi ghi file sổ (mặc định chỉ xem thử, cờ `--that` mới ghi). Sao lưu thư mục sổ trước khi ghi.
- **5 cái bẫy:**
  1. Cửa sổ lệnh Windows mặc định cp1252 → tiêu đề tiếng Việt làm script sập, hook báo lỗi đỏ. Đầu script:
     `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` (cả stderr). Chạy tay ổn ≠ chứng minh — thử trong shell SẠCH.
  2. Timestamp trong `.jsonl` là **UTC**; phải gắn `tzinfo=timezone.utc` không thì lệch 7 tiếng, phiên sáng nay nằm đáy sidebar.
  3. Đừng lọc "phiên < 2 lượt thì bỏ" (chat mới nào cũng bắt đầu 1 lượt). Dấu hiệu đúng của chat có người ngồi: bản ghi
     `{"type":"mode"}` trong ~8 dòng đầu; phần mềm gọi `-p` thì không có.
  4. App chỉ đọc sổ **lúc khởi động** → mục mới lên ở lần mở app kế tiếp. Đó là giới hạn nền tảng, nói rõ cho người dùng, đừng cố làm "tức thì".
  5. App xoá rồi dựng lại thư mục sổ lúc khởi động → `os.makedirs(..., exist_ok=True)` + bọc TOÀN BỘ phần ghi trong try/except.
     Hook TUYỆT ĐỐI không được làm gãy lượt chat.
- **KHÔNG làm:** đẩy lịch sử chat lên GitHub/dịch vụ ngoài (có số lợi nhuận, SĐT khách, khoá API — không lùi được); ghi thẳng vào
  LevelDB/IndexedDB của app; tự đăng nhập hộ người dùng.
- **Không làm được (đừng mất công):** đồng bộ lịch sử Antigravity (nằm trên server Google); dùng GitHub làm cầu; sửa `cwd` dự án AGS
  qua API (`/api/projects` chỉ GET/POST); làm sidebar cập nhật tức thì; Claude Desktop → AGS không có API sạch (`ags chat` là giao việc
  thật cho agent chứ không phải sao chép thụ động).
- CLI `claude` báo "not compatible with the version of Windows" thường là file `claude.exe` chỉ là mẩu giữ chỗ vài trăm byte →
  `npm install -g @anthropic-ai/claude-code --include=optional`. Đăng ký CLI với AGS phải trỏ file `.exe` thật, không phải `.cmd`.

## B. Tiến trình nền bền vững trên Windows
- Tách 2 lớp: **collector bền** (đúng 1 instance, độc lập phiên) + **lớp hiển thị theo phiên** (`tail -f` file log qua Monitor, tối đa 30 phút, hết thì arm lại). Đừng nhập lại thành một.
- Single-instance bằng file khoá chứa PID (kiểm bằng `tasklist`); supervisor `.bat` vòng lặp relaunch sau 3 giây; khởi động cùng Windows bằng file
  trong thư mục **Startup** (Task Scheduler bị "Access is denied" trong sandbox).
- Chạy lại `wscript` mỗi lần debug mà không diệt supervisor cũ → dồn nhiều vòng lặp song song. Luôn kiểm bằng
  `Get-CimInstance Win32_Process | Where CommandLine -like '*<tên supervisor>*'`, diệt HẾT (cả cmd.exe cha) rồi mới chạy lại MỘT lần.
- Chạy launcher từ trong một phiên Claude sẽ **rò biến môi trường** `CLAUDE_CODE_SESSION_ID` sang tiến trình con → tự lọc mất chat của chính phiên đó.
  Dùng `env -u CLAUDE_CODE_SESSION_ID wscript.exe …`.
- Mọi `execSync` phải có `timeout`; mỗi cuộc chat xử lý trong try/catch riêng để một chat lỗi không chặn cả lượt quét.
- **Lượt không bao giờ chốt:** nếu lượt chưa `chot` cũ hơn 120 giây → coi là bỏ dở, bỏ qua; không thì nó chặn vĩnh viễn mọi lượt mới hơn.

## C. ⛔ Đừng bao giờ `taskkill` `ags.exe` khi debug
`ags.exe` (cửa sổ tên "claude") chính là **app AGS + API `127.0.0.1:8765`**. Giết nhầm là sập cả app vài phút.
Chậm/treo thì chờ hoặc test có giới hạn (`timeout N ags.exe …`). Lỡ sập: `Start-Process "<đường dẫn>\ags.exe" -WindowStyle Minimized`.

## D. Cài plugin/skill mới
Skill/lệnh mới cài **không nạp** vào cuộc trò chuyện đang tiếp diễn (`--continue`/resume). Bảo người dùng thoát hẳn và mở phiên **mới hoàn toàn**;
đừng thử đi thử lại lệnh hay bắt họ "mở lại" nhiều lần. (Áp dụng cho AGS/Claude Code; với OpenClaw thì mở phiên mới sau khi thêm skill.)

## E. Hiểu đúng lời người dùng
Câu kiểu "đừng dùng tới token" thường nghĩa là **"đừng bắt tôi phải nhờ thủ công mỗi lần"**, không phải "cấm mọi chi phí backend". Đừng
âm thầm hạ cấp tính năng đang chạy theo nghĩa hẹp nhất — nói rõ mình hiểu theo nghĩa nào hoặc hỏi một câu, nhất là khi hai cách hiểu cho
hành vi khác hẳn nhau. Người dùng phải nhắc hai lần mới là dấu hiệu bạn đã không nghe.

## F. Kiểm chứng trước khi báo "xong"
Không báo xong khi chưa đo: chạy đúng dòng lệnh của hook trong shell sạch, xác nhận mã thoát 0, cho script ghi log mỗi lần chạy để biết hook có nổ
thật, rồi mở một chat mới kiểm tra kết quả thật.
