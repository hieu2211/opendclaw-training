---
name: ags-browser-automation
description: ABA — duyệt web tự động qua trình duyệt đã đăng nhập (ags aba): hỏi/nhờ META.ai trả lời hoặc vẽ ảnh, hoặc tự lái trang (mở, bấm, gõ, dán, cuộn, chụp, đọc chữ, liệt kê nút kèm toạ độ, chạy JS), quay/ghi âm tab đang xem, cài addon trình duyệt. Dùng khi người dùng nhắc "ags aba", "ABA", "META.ai", "nhờ Meta vẽ ảnh", duyệt web tự động, lái trình duyệt.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# ABA (`ags aba`) — lái trình duyệt đã đăng nhập của người dùng

ABA chạy kịch bản trên **trình duyệt thật đã đăng nhập** của người dùng — không mở phiên ẩn danh riêng, nên dùng
được các dịch vụ cần đăng nhập (vd META.ai) mà không cần agent tự đăng nhập hộ.

## TRƯỚC KHI chạy bất kỳ lệnh aba nào: kiểm addon đã nối chưa

```
ags aba health
```

- Addon chưa nối → **DẠY người dùng tự cài** (KHÔNG tự làm hộ được): mở trang tiện ích trình duyệt
  (`edge://extensions` hay `chrome://extensions`) → bật "Chế độ nhà phát triển / Developer mode" →
  "Tải tiện ích đã giải nén / Load unpacked" → trỏ vào thư mục addon mà `health` trả về (`thu_muc_addon`,
  thường `~/ABA-addon`). Nạp xong addon TỰ nối, khỏi khoá gì thêm — rồi mới chạy kịch bản.
- Addon từ bản 1.5.0 **tự tải lại** khi mô-đun lên bản mới, không cần làm gì thêm.
- Chỉ khi `health` vẫn trả `can_reload_addon:true` (addon cũ bản 1.4.x) mới cần bảo người dùng vào trang tiện
  ích bấm nút ⟳ "Tải lại addon" **một lần**, rồi mới chạy tiếp.

## Lệnh hay dùng

```
ags aba meta-prompt "câu hỏi"            # chạy một ABA — hỏi/nhờ META.ai trả lời hoặc vẽ ảnh
ags aba meta-prompt @cau-hoi.txt         # prompt dài lấy từ tệp thay vì gõ thẳng
ags aba meta-prompt "…" --noi-tiep       # hỏi tiếp trong CÙNG cuộc chat META.ai cũ (giữ ngữ cảnh)
ags aba aba_list                         # các kịch bản ABA có sẵn trên chợ / đã cài trên máy
ags aba do '{"action":"read_text"}'      # lệnh gốc cho addon — xem đủ action bằng `ags aba help`
ags aba help                             # bảng đầy đủ mọi lệnh + cách dùng — ĐỌC trước khi tự lái trang
```

Lệnh gốc (`ags aba do`) tự lái trang ở mức thao tác: mở trang, bấm, gõ, dán, cuộn, chụp màn hình, đọc chữ trên
trang, liệt kê nút bấm kèm toạ độ, chạy JS, cài/gỡ kịch bản… — đừng đoán tên action, chạy `ags aba help` để lấy
bảng đủ trước khi ghép lệnh.

## Ghi lại phiên duyệt web

```
ags aba audio start / stop     # ghi tiếng của tab đang xem
ags aba video start / stop     # quay cả hình; stop trả về đường dẫn tệp
```

Lệnh tự bấm phím mở khoá addon nếu Chrome chặn ghi hình/tiếng; **cửa sổ trình duyệt phải đang ở trên cùng**
(không bị che/thu nhỏ) khi chạy.

## Lưu ý

- `ags aba meta-prompt` là lối tắt phổ biến nhất — dùng khi chỉ cần hỏi/nhờ META.ai một câu, không cần tự lái
  từng bước. Dùng `ags aba do` (lệnh gốc) khi cần điều khiển chi tiết một trang web bất kỳ, không riêng META.ai.
- Việc xong có file/ảnh/video cần người dùng xem → `ags view <file>` theo đúng luật của `ags-core`, đừng chỉ báo
  đường dẫn.
