---
name: ags-form
description: Dựng trang nhập liệu cho người dùng điền (text/textarea/number/checkbox/radio/select/date…) bằng `ags form`, host bung TRANG NHẬP LIỆU lên màn hình họ và trả lại đường dẫn JSON kết quả. Dùng khi cần NGƯỜI DÙNG nhập thông tin, dựng khảo sát, thu thập dữ liệu, điền thông tin — thay vì tự hỏi từng câu trong chat.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# `ags form` — thu thập dữ liệu bằng trang nhập liệu, không hỏi từng câu trong chat

Khi cần nhiều trường thông tin cùng lúc (khảo sát, đăng ký, cấu hình) thay vì hỏi-đáp từng câu trong chat, gửi một
spec JSON mô tả form, AGS tự bung **trang nhập liệu** lên màn hình người dùng.

```
ags form <spec.json>
```

- Agent soạn spec JSON các trường (`text`, `textarea`, `number`, `checkbox`, `radio`, `select`, `date`, …).
- Host bung trang nhập liệu lên màn hình người dùng dựa trên spec đó.
- Người dùng điền và nộp → host lưu kết quả vào `data/forms/<id>.json`.
- `ags form` **in ra đường dẫn** file kết quả đó để agent đọc và xử lý tiếp.

⚠ Chưa có thêm chi tiết field-by-field của spec (cú pháp đúng từng loại field) — khi cần dựng form thật, chạy
`ags form --help` trên máy đang có AGS để lấy mẫu spec đầy đủ trước khi soạn JSON, đừng đoán cấu trúc.

Dùng việc này thay vì tự hỏi từng câu trong chat khi: cần nhiều trường cùng lúc, cần kiểu dữ liệu có ràng buộc
(số, ngày, chọn một trong nhiều lựa chọn), hoặc người dùng rõ ràng muốn "điền form" chứ không muốn trả lời hội thoại.
