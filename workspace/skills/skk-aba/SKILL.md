---
name: skk-aba
description: Điều khiển trình duyệt tự động qua addon ABA — mở/đọc/bấm tab, chụp màn, ghi âm/quay phim/chép lời, điều khiển chuột/phím thật, rút gọn link, dựng video demo. Dùng khi người dùng nói "skk aba", "duyệt web tự động", "lái trình duyệt", "ABA", "ghi màn hình", "quay video hướng dẫn".
metadata: {"openclaw":{"requires":{"bins":["skk-aba"]}}}
---

# SKK ABA — lái trình duyệt qua addon ABA

Không viết script Puppeteer/Playwright riêng. Addon ABA đã có sẵn CDP (Chrome DevTools Protocol)
nối vào trình duyệt thật của người dùng — gọi thẳng qua lệnh `skk-aba`, đường dẫn đầy đủ
`/home/node/.local/bin/skk-aba`.

## Việc gì dùng được

**Lệnh gốc cho addon** — `skk-aba do '{"action":"...","args":{...}}'` (chạy trên tab đang mở):
- Tab: `list_tabs`, `tab_new`, `window_new`, `tab_activate`, `tab_close`, `tab_state`.
- Đọc trang: `read_text`, `liet_ke` (liệt kê phần tử bấm được kèm mã ref), `js`, `screenshot`, `chup_ca_trang`.
- Thao tác: `open_url`, `real_click`, `real_type`, `real_key`, `real_drag`, `upload`, `paste`, `scroll`, `zoom`, `emulate`.
- Hiệu ứng: `tooltip`, `highlight`, `nguoi_that` (bấm lệch ngẫu nhiên như người, mặc định bật).

**Live / trình duyệt / addon**
- `skk-aba do '{"action":"live"}'`: mở cửa sổ Live xem + điều khiển màn hình host.
- `trinh_duyet` / `trinh_duyet_set`: xem/chọn trình duyệt chạy lệnh.
- `addon_path` / `mo_thu_muc_addon`: lấy/mở thư mục addon.

**Ghi âm / quay phim / chép lời**
- `audio`, `video`, `screen`: đều nhận `start | stop | status`.
- `tab_record_start`, `tab_record_stop`, `tab_record_status`: bản có tham số, ghi theo tab.
- Chrome có thể chặn ghi tới khi addon được gọi — chạy `skk-aba do '{"action":"os_key","args":{"keys":"alt+shift+."}}'` trước để mở khóa tab đang xem.
- `screen` luôn bắt người dùng tự chọn màn hình/cửa sổ, agent không qua được bước này.
- Nhóm lệnh `cheploi_*`: chép lời các đoạn đã ghi.

**Điều khiển cấp OS (chuột/phím thật)**
- `os_click`, `os_drag`, `os_key`, `os_shot` — chiếm chuột thật, cửa sổ trình duyệt phải ở trên cùng, trang zoom 100%.

**Việc khác**
- `skk-aba demo`: dựng video hướng dẫn từ kịch bản.
- `skk-aba link <url>`: rút gọn link thành `ags.sh/1...`.
- `shot`, `locate`: chụp tab đang mở, hoặc tìm ảnh mẫu trên màn hình rồi bấm.

## Lưu ý bắt buộc
- `open_url` tới http(s) công khai bắt buộc có `muc_dich`. Đổi domain khi còn bài học chờ nộp
  thì phải `nop_bai_hoc` trước (cập nhật/tạo mới/bỏ qua vì trùng).
- Toạ độ là điểm CSS của tab — đổi cỡ cửa sổ hoặc zoom là lệch, chạy lại `liet_ke` trước khi bấm.
- Trang web LLM mở ở tab nền không trả lời — dùng `window_new` mở cửa sổ riêng.
- Chạy prompt cố định/một lệnh: `skk-aba meta-prompt "câu hỏi"` (hoặc `@file.txt`, thêm `--noi-tiep`
  để hỏi tiếp cuộc chat cũ). Xem ABA có trên chợ/đã cài: `skk-aba aba_list`. Kiểm addon đã nối:
  `skk-aba health`.
- Luôn `skk-aba -h` lấy cú pháp mới nhất trước khi đoán tham số.
