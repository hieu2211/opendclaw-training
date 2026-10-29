---
name: skk-timeline
description: Dựng lại lịch sử một dự án từ mọi dấu vết (git, file memory, prompt cũ, máy thật) rồi ghi vào knowledge/ + dựng trang timeline xem được, thuần OpenClaw. Dùng khi người dùng nói "timeline", "lịch sử dự án", "nhìn lại dự án", "hành trình phát triển", "dựng lịch sử".
---

# SKK Timeline — lịch sử dự án thuần OpenClaw (thay ags-timeline)

AGS gốc dựa vào server cloud riêng (AGSMem cloud API, kho prompt riêng của AGS) để lưu mốc và
dựng trang. OpenClaw không có hai thứ đó — thay bằng file trong `knowledge/` (đã là bộ nhớ dự án
thật của workspace này, xem skill `skk-memory`) và dựng trang bằng file HTML tĩnh đơn giản.

## Khác biệt chính so với AGS gốc — đọc trước khi làm

- **Không có "kho prompt AGS cloud"** (`ags api GET /api/cloud/prompts`) để đào lịch sử — nguồn
  đào thay bằng: `git log`, file `.md` lịch sử/memory sẵn có trong `knowledge/`, transcript các
  session cũ (`sessions_list` + đọc lại nếu cần), SSH/exec chỉ-đọc vào máy thật nếu có.
- **Không ghi vào "AGSMem cloud"** — ghi thẳng vào `knowledge/<chu-de>/MEMORY-*.md` theo đúng
  quy ước đã dùng trong workspace (xem `skk-memory`), không cần API riêng, không cần "nhánh ngọn".
- **Không dựng qua "Content Factory Landing Page"** — dựng 1 file `.html` tĩnh tự chứa (không
  phụ thuộc server ngoài), lưu trong thư mục dự án, xem qua `message` attachment hoặc
  `[embed ...]` nếu đang ở webchat Control UI.
- **Không chia việc theo "model nhẹ nhất/trung bình"** như AGS ép buộc — OpenClaw dùng
  `sessions_spawn` với `model` override nếu cần tiết kiệm chi phí cho bước đào dữ liệu (nhiều
  đọc, ít suy luận), nhưng không bắt buộc — tuỳ ngân sách/model đang cấu hình.

## Luật an toàn (giữ nguyên từ AGS, vẫn đúng)

- Không đưa IP, MAC, mật khẩu, khoá API, DSN vào trang hay bản ghi — thấy trong nguồn thì bỏ qua/
  thay bằng placeholder, không in ra.
- SSH/exec vào máy thật chỉ ĐỌC — không sửa, không restart service khi đang làm việc này.
- Không đoán: thiếu nguồn thì ghi "chưa rõ", thiếu thông tin để quyết thì hỏi thẳng trong chat
  (không có form popup riêng như AGS).

## Bước 0 — chốt dự án

Biết tên dự án, thư mục code, máy chạy thật (nếu có) thì làm luôn. Thiếu thì hỏi thẳng trong
lượt chat hiện tại: tên dự án, thư mục/repo, máy chạy, khoảng thời gian cần dựng.

## Bước 1 — đào lịch sử (có thể giao subagent nếu khối lượng lớn)

Việc đọc nhiều/nghĩ ít này giao được cho `sessions_spawn` (model nhẹ nếu muốn tiết kiệm), đưa
cho nó: tên dự án, thư mục/repo, nguồn cần đào, đường dẫn file kết quả, nguyên văn mục "Luật an
toàn" trên. Subagent chỉ đọc + ghi file dữ liệu tạm, KHÔNG ghi `knowledge/`, KHÔNG dựng trang.

Nguồn đào (không giới hạn, thấy nguồn khác có dấu vết thì đào thêm):
- `git log --date=iso --stat` trong thư mục dự án.
- File lịch sử/memory sẵn có: `knowledge/<chu-de>/MEMORY-*.md`, `knowledge/<chu-de>/memory-*.md`.
- Session cũ liên quan: `sessions_list(search="<tên dự án>")`.
- Máy thật (nếu SSH có): `ls -la --time-style=long-iso`, `systemctl status`, log file `.bak_*`.

Mỗi mốc gom: ngày (giờ VN), loại (`feat`/`infra`/`bug`/`incident`/`idea`), tiêu đề ngắn, nội
dung, trạng thái (`open`/`fixed`), nguồn. Lưu ra `timeline-<slug>.json` + 1 file `.md` lịch sử
đầy đủ cạnh code.

## Bước 2 — ghi vào knowledge/

Nhánh đích: file `knowledge/<chu-de>/MEMORY-<ten>.md` phù hợp dự án. Chưa có chủ đề phù hợp thì
tạo mới (xem `skk-memory`), không cần hỏi xin tạo "nhánh" như AGS vì đây chỉ là file, không phải
cấu trúc cây cố định cần đồng bộ.

## Bước 3 — dựng trang timeline (HTML tĩnh, tự chứa)

Một file `.html` trong thư mục dự án, có:
- Tiêu đề + vài số liệu tổng (số mốc, số tháng).
- Timeline chia theo năm, lọc theo loại mốc (JS thuần, không cần framework).
- Mỗi mốc dẫn nguồn ngắn (git hash / tên file memory).
- Mục "Còn treo": lỗi/nợ kỹ thuật chưa xử lý.
- Font đủ dấu tiếng Việt, chạy được không cần mạng (không gọi CDN ngoài nếu tránh được).

Xem bằng `message` (gửi file đính kèm) hoặc `[embed url="/__openclaw__/canvas/..." ...]` nếu
đã stage vào hosted root và đang ở Control UI webchat — không ép buộc dùng embed nếu kênh khác.

## Bước 4 — báo kết quả

Báo ngắn: đã ghi vào file `knowledge/` nào, đường dẫn trang `.html`, các mốc chính. Có mốc mới
sau này: thêm vào file memory + sửa số liệu/mảng dữ liệu trang, không cần dựng lại từ đầu.
