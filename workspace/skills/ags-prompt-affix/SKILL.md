---
name: ags-prompt-affix
description: Cấu hình câu AGS tự chèn vào mỗi prompt của người dùng — prefix (đầu), suffix (đuôi), tiết kiệm token (everyN), bộ nhớ tăng cường (smartRemind), phạm vi cuộc chat/dự án. Dùng khi người dùng nói "thêm câu này vào tất cả prompt", "chèn vào đầu/đít mỗi câu", "lúc nào cũng nhắc tôi…", "bật tiết kiệm token", "nhắc lại mỗi 3 câu".
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Luật kèm mỗi prompt (affix)

AGS tự chèn câu vào lời người dùng; **lịch sử chat vẫn lưu câu gốc sạch**. Người dùng khỏi gõ lại.

- `scope=conv` (mặc định; `id` lấy ở `AGS_CONV_ID`): chỉ cuộc chat này.
- `scope=project` (`id` = mã dự án): cả dự án. **Cuộc chat có đặt thì ĐÈ dự án.**

```
ags api GET  '/api/affix?scope=conv&id='"$AGS_CONV_ID"                                   # xem đang đặt gì
ags api POST /api/affix '{"scope":"conv","id":"<id>","prefix":"<câu chèn TRƯỚC prompt>"}'
ags api POST /api/affix '{"scope":"conv","id":"<id>","suffix":"<câu chèn SAU prompt>"}'
ags api POST /api/affix '{"scope":"conv","id":"<id>","tokenCutting":true,"everyN":3}'
```

- Field không gửi thì **giữ nguyên**. Đặt nội dung mà không nói gì thêm là **tự bật**.
- Tắt: `{"prefixOn":false}` / `{"suffixOn":false}` — nội dung còn nguyên, bật lại là dùng.
- **Tiết kiệm token** (`tokenCutting`): chỉ nhắc luật đầy đủ ở câu đầu, rồi cứ `everyN` câu một lần (mặc định 3).
- **Bộ nhớ tăng cường** (`smartRemind`, MẶC ĐỊNH BẬT, chỉ có tác dụng khi tiết kiệm token bật): giữa hai lần nhắc đầy đủ,
  AGS cài một dòng rất ngắn gọi tên luật để agent không quên. Tắt: `{"smartRemind":false}`.
  Người dùng gọi nó đủ kiểu ("nhắc thông minh", "cho nó nhớ luật", "đừng quên luật") — đều là công tắc này.
