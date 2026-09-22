---
name: ags-sidebar-qa
description: Điều khiển bốn mép màn hình người dùng trong AGS (ags sidebar — bảng phải, dải trên, dải đáy, cột trái) và đọc lại lịch sử hỏi–đáp của chính cuộc chat (ags qa). Dùng khi cần báo tiến độ/đổ bảng biểu cho người xem, hoặc khi người dùng hỏi "nãy mày trả lời gì", "tóm lại chuyện vừa bàn".
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# `ags sidebar` — bốn mép màn hình

```
ags sidebar dir=<top|left|right|bottom> act=<show|hide|toggle> [content=<...>] [title="..."]
```
- **right**: bảng bên phải, MỖI CUỘC CHAT MỘT TAB riêng (không đè tab agent khác). Chỗ báo tiến độ, đổ bảng biểu, kết quả dài.
- **left**: cột danh sách cuộc chat — chỉ đóng/mở, không nhận nội dung.
- **top**: dải trên toàn màn hình, mặc định XANH kiểu "đã xong". Báo một câu ngắn nổi bật.
- **bottom**: dải ghim mép dưới khung dòng lệnh. Thông tin bám theo lúc làm ("đang chạy bước 2/4…").

`content` nhận 4 dạng (tự nhận): chữ thường · đoạn HTML · đường dẫn file `.md/.html/.js` · `-` (đọc từ stdin:
`cat trang.html | ags sidebar dir=right act=show content=-`). Ép kiểu: `text:` / `html:` / `js:`.

```
ags sidebar dir=top act=show content="Đã dựng xong landing page — bấm vào cửa sổ vừa mở"
ags sidebar dir=bottom act=show content="Đang chạy bước 2/4: biên tập nội dung…"
ags sidebar dir=bottom act=hide
ags sidebar dir=right act=show content=ket-qua.html
```
Lưu ý: HTML bị lọc sạch phần chạy được. Cần chạy mã thì khai `content=js:...` và chỉ dùng được ở dải TRÊN và dải ĐÁY (bảng phải
không chạy mã). Tiến độ việc do agent khác giao (`ags chat`) thì hệ thống TỰ vẽ — đừng vẽ lại. Cú pháp cũ
`ags sidebar show|hide` / `html <file>` tương đương `dir=right`.

# `ags qa` — kho hỏi–đáp của máy này

Câu người dùng đã gõ + câu agent đã trả lời, gắn bằng mã prompt; host tự bóc từ nhật ký agent. **Rẻ hơn nhiều so với cuộn màn hình / đọc cả
nhật ký phiên.**

```
ags qa conv <mã cuộc chat> [N]         # N lượt gần nhất (mặc định 20), cũ → mới. Mã chat = $AGS_CONV_ID
ags qa <mã prompt>                     # đúng một lượt
ags qa boc <mã cuộc chat> <mã prompt>  # bóc lại lượt còn thiếu câu trả lời
… --json                               # nguyên gói JSON
```
- "(chưa bóc được)" → host chưa lần ra câu trả lời, thử `ags qa boc`.
- "(bóc chưa chắc tay)" → lấy bằng cách đọc ngược màn hình, **đọc kỹ trước khi tin**.
- Kho nằm trên MÁY NÀY, không đồng bộ lên mây.
- `ags qa conv <id> --json` có thể trả `{"ds":null,"so":0}` (không phải `[]`) khi chat chưa có lượt nào → luôn `(qa.ds || [])`.
  Mỗi lượt có cờ `chot` (đã chốt); lượt bị bỏ dở có thể KHÔNG BAO GIỜ `chot:1` — đừng để nó chặn các lượt mới hơn.
