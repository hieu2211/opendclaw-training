---
name: ags-multi-agent-chat
description: Phối hợp nhiều agent trong AGS — nhắn/giao việc cho agent khác (cùng máy hoặc máy khác), lập nhóm agent với tên gọi tắt, nhận việc và báo tiến độ bằng mã việc (ags task). Dùng khi người dùng bảo "kêu A1 làm…", "nhờ agent kia…", "lập nhóm", hoặc khi bạn được giao một việc có mã.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Nói chuyện với agent khác (`ags chat`) & nhận/báo việc (`ags task`)

## Giao việc

```
ags chat setup                                     # KỊCH BẢN lập nhóm — bắt đầu từ đây
ags chat <conv_id> --title "<tên việc>" "<lời nhắn>"   # agent CÙNG MÁY (khỏi mật khẩu)
ags chat <token>   --title "<tên việc>" "<lời nhắn>"   # agent MÁY KHÁC (token trong mã mời)
ags chat invite                                    # lấy mã mời <conv_id>@<token>.ags của cuộc chat này
ags chat --peers                                   # = ags peers
```

- `--title` **BẮT BUỘC**, ngắn dưới 5 chữ. Bảng phải của người dùng chia mỗi việc một TAB; bạn cầm nội dung
  việc nên bạn đặt tên — hệ thống không tự tóm tắt hộ.
- Gửi xong **cứ làm việc khác**. Trả lời của bên kia tự hiện trong cuộc chat của bạn; họ im lâu thì host tự nhắc hộ.
  Đừng ngồi canh, đừng poll.
- Mỗi lần nhắn nói rõ *mình là ai, cần gì* — bên kia là một agent độc lập, không có ngữ cảnh của bạn.

### DẶN KÈM MỖI LẦN GIAO VIỆC (viết thẳng vào lời nhờ)

> "Đừng dùng công cụ hỏi lại của bạn — đầu bên kia là agent, không phải người ngồi trước màn hình, không ai bấm
> trả lời nên hỏi là treo. Cần hỏi thì gom hết câu hỏi thành danh sách, ghi vào log việc rồi chốt done luôn kèm
> danh sách đó; tôi đọc được và sẽ giao lại kèm câu trả lời."

**Vì sao:** agent nhận việc hay bật hộp hỏi/xác nhận rồi đứng chờ vô tận — người dùng không thấy, không rep được,
việc chết cứng tới lúc hết giờ.

## Kịch bản khi người dùng nhờ lập nhóm

Hỏi TỪNG câu một, chờ họ trả lời:

1. "Anh/chị muốn tôi nói chuyện với agent TRONG MÁY NÀY hay Ở MÁY KHÁC?"
2. **Trong máy** → đọc danh sách cuộc chat (đọc *tên*, đừng đọc số), hỏi chọn cuộc nào (chọn được nhiều), rồi hỏi
   "đặt tên gọi tắt cho từng bạn là gì?" (A1, A2, Bếp, Thợ…). GHI NHỚ bảng *tên gọi tắt ↔ conv_id* suốt phiên. Từ đó
   "kêu A1 làm X, A2 làm Y" → tự chạy `ags chat <conv A1> --title "…" "X"` và `… <conv A2> … "Y"`, báo lại khi có
   kết quả. KHÔNG hỏi lại conv_id nữa.
3. **Máy khác** → `ags chat invite` lấy mã mời (dạng `123@xyz.ags`), đưa người dùng câu:
   "Chat với tôi qua 123@xyz.ags" để họ gửi sang máy kia. Muốn chủ động nhắn sang máy khác: xin mã mời bên đó, lấy
   phần sau `@` (bỏ đuôi `.ags`) làm token.

## Khi BẠN là bên nhận việc — luôn có mã việc

```
ags task log  <mã> "<đang làm gì>"    # báo từng bước xong — bên giao đang nhìn tiến độ, ĐỪNG im
ags task done <mã> "<kết quả>"        # chốt xong, kèm TOÀN BỘ kết quả
ags task fail <mã> "<lý do>"          # làm không được thì nói thẳng
ags task get  <mã>                    # bên giao dùng để theo dõi
ags task list                         # việc liên quan cuộc chat này
```

- Im quá lâu hệ thống sẽ nhắc. `ags task done` TRẦN (không mã) là việc của stop hook, không phải lệnh này.
- **Không dùng công cụ hỏi lại người dùng** khi đang làm việc được giao (không ai bấm trả lời). Gom câu hỏi → ghi
  vào log → `ags task done` kèm danh sách câu hỏi.
- Tiến độ việc do agent khác giao thì hệ thống TỰ vẽ ở bảng phải — đừng tự vẽ lại.
