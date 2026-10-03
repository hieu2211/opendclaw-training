# TOKEN-OPTIMIZATION.md — Cách AGS tiết kiệm token, chắt lại để huấn luyện

AGS có một tính năng **gọi thẳng là "tiết kiệm token"** (prefix/suffix/affix), và ngoài ra còn nhiều chỗ khác
trong thiết kế của nó theo cùng một triết lý: đừng nhắc lại cái đã nói, đừng kéo cái không cần, đừng để agent tự
đi lục lại những gì host đã có sẵn bản rút gọn. Tài liệu này gom cả hai, để OpendClaw học được không chỉ MỘT
tính năng mà cả NẾP NGHĨ đằng sau nó.

## 1. Cơ chế rõ ràng: "tiết kiệm token" trong `ags api /api/affix` (chi tiết đủ ở skill `ags-prompt-affix`)

AGS tự chèn một câu luật vào **mỗi** lời người dùng gửi đi (prefix/suffix), để agent không quên một quy tắc cố
định — nhưng nhắc đủ câu đó ở MỌI lượt thì tốn token oan. Nên AGS tách hai công tắc:

- **`tokenCutting` (tiết kiệm token):** chỉ nhắc luật ĐẦY ĐỦ ở câu đầu tiên, rồi cứ `everyN` câu (mặc định 3)
  mới nhắc lại đầy đủ một lần — các câu ở giữa KHÔNG kèm gì cả.
- **`smartRemind` (bộ nhớ tăng cường, mặc định BẬT, chỉ có tác dụng khi `tokenCutting` đang bật):** giữa hai lần
  nhắc đầy đủ, AGS vẫn cài một dòng RẤT NGẮN gọi tên luật (không nhắc lại toàn văn) để agent không quên mất luật
  đang áp dụng. Đây là phần khéo nhất: không phải "tắt nhắc để tiết kiệm" (agent quên luật giữa chừng), mà là
  "nhắc tối thiểu vừa đủ để không quên, không nhắc thừa".

```
ags api POST /api/affix '{"scope":"conv","id":"<id>","tokenCutting":true,"everyN":3}'
ags api POST /api/affix '{"scope":"conv","id":"<id>","smartRemind":true}'
```

**Bài học khi áp dụng nếp này ở nơi khác:** đừng hiểu "tiết kiệm" là "cắt hẳn" — cắt hẳn thì mất tác dụng ban đầu
(agent quên luật). Cách đúng là nén tần suất nhắc đầy đủ xuống mức vừa đủ, và chèn một "mỏ neo" cực ngắn ở giữa
hai lần nhắc để không rơi mất ngữ cảnh. Việc hiểu sai "tiết kiệm token" thành "cắt luôn tính năng" từng xảy ra
thật (xem `ags-ops-lessons`, mục E) — luôn hỏi lại người dùng muốn nghĩa nào trước khi hạ cấp.

## 2. Nếp nghĩ tương tự ở những chỗ khác trong AGS

Đây không phải tính năng cùng tên, nhưng cùng một nguyên tắc: **đưa agent bản đã chắt lọc/đã có sẵn trước, chỉ
lục bản gốc khi bản chắt không đủ.**

- **Bộ nhớ dự án (`ags-memory`):** `ags mem tim "<câu hỏi>"` trả vài đoạn đã chấm điểm — RẺ. `ags mem snap` là
  bản đã chắt, đã dọn trùng của một nhánh. Chỉ khi cả hai không đủ mới đụng tới `ags mem entries --topic <mã>
  --limit 20` (bản gốc). **Tuyệt đối tránh** `ags mem entries --all` trần — kéo hàng trăm bản ghi thô, vừa tốn
  hàng nghìn chữ vừa dễ vớ nhầm điều đã bị quyết định sau lật (bản ghi chỉ THÊM, không sửa).
- **Tra lại y nguyên = trả lời một chữ:** `ags mem snap` gọi lại với nội dung bên dưới KHÔNG đổi thì host chỉ trả
  "KHÔNG ĐỔI" thay vì gửi lại toàn bộ đoạn — nhận câu đó nghĩa là đúng, đừng gọi lại trừ khi thật sự cần bản
  nguyên văn (`--fr`).
- **Hỏi–đáp trong phiên (`ags-sidebar-qa`):** `ags qa conv <id> [N]` lấy lại N lượt gần nhất từ kho đã bóc sẵn,
  rẻ hơn nhiều so với việc agent tự cuộn/đọc lại toàn bộ nhật ký phiên để nhớ "nãy mình nói gì".
  `ags qa <mã prompt>` tra đúng MỘT lượt thay vì kéo cả đoạn quanh nó.
  Mã lượt `#a1b2c` ở đầu mỗi lời người dùng (xem `ags-core`, luật 0) chính là chìa khoá cho lối tra rẻ này — agent
  không cần tự đoán xem "lượt nào trước" nữa, chỉ cần có mã là tra thẳng.
- **Chắt lọc bộ nhớ theo lô, không theo từng lượt:** skill `agsmem` dặn thẳng "đừng chắt lọc gì sau mỗi lượt" —
  chỉ ghi NÓNG khi thật sự đáng (chốt quyết định, lỗi đã trả giá, mốc thật), còn việc chia vào nhánh dồn lại làm
  một lượt cuối phiên. Ghi mọi lượt là tốn token oan mà kho cũng loãng, không giúp tra cứu tốt hơn.
- **Đợt "Chưng cất khi được nhắc" không bị nhắc lại vô ích:** mỗi bản ghi mới kèm `from_qa_ids`/`da_chat` — danh
  sách mã lượt agent ĐÃ XEM, dù lượt đó chẳng có gì đáng ghi. Nhờ vậy lần sau host không nhắc lại đúng những lượt
  đã xử lý xong — khỏi tốn thêm một vòng xem lại từ đầu (bài học thật: một agent từng bị nhắc lại tám lượt liền
  chỉ vì quên khai `da_chat`).
- **Việc dài đẩy ra màn hình, không đẩy vào chat:** kết quả dài (bảng biểu, báo cáo, trang web) đi qua
  `ags sidebar` hoặc `ags view` thay vì dán nguyên văn vào lời đáp trong chat — vừa dễ đọc hơn cho người dùng,
  vừa không kéo dài ngữ cảnh hội thoại bằng nội dung mà người dùng sẽ xem trên màn hình chứ không đọc lại trong
  chat nữa.
- **Việc nền thì báo một câu rồi im, không poll dày:** `ags chat`/`ags task` là bất đồng bộ — gửi việc xong làm
  việc khác, hệ thống tự nhắc khi bên kia trả lời hoặc im quá lâu. Poll liên tục để "canh" là tốn lượt gọi vô ích
  mà không đổi được gì nhanh hơn.
- **Số thứ tự lượt (`#a1b2c`) không phải nội dung cần xử lý (`ags-core`, luật 0):** AGS tự thêm mã này vào đầu
  lời người dùng; agent phải BỎ QUA nó, không được dừng lại suy luận xem mã nghĩa là gì — mất công tốn cả token
  lẫn thời gian cho một việc không ra kết quả gì (ghi nhận thật: một agent "lùng" mã này mất hơn mười phút).

## 3. Rút lại nếp chung cho OpendClaw

1. **Luôn có một bản RẺ trước khi đụng tới bản ĐẮT**: tóm tắt/snap/cache trước, bản gốc/toàn bộ lịch sử chỉ khi
   bản rẻ không đủ trả lời.
2. **Nhắc lại luật/ngữ cảnh theo nhịp, không theo từng lượt** — đủ để không quên, không thừa để khỏi tốn.
3. **Đánh dấu cái đã xử lý** (mã lượt, `da_chat`, "KHÔNG ĐỔI") để không phải xử lý lại từ đầu.
4. **Đẩy nội dung dài ra kênh hiển thị phù hợp** (màn hình/sidebar/file) thay vì nhét hết vào ngữ cảnh hội thoại.
5. **"Tiết kiệm" không có nghĩa là "cắt bỏ"** — khi một yêu cầu tiết kiệm có thể hiểu thành "giảm chi phí" hoặc
   "giảm công sức người dùng", làm rõ nghĩa trước khi hạ cấp tính năng (xem thêm `ags-ops-lessons`, mục E).

## Nguồn

`ags api GET '/api/agent-prompt?name=ags_affix_help'` (xác nhận còn đúng tới 2026-10-03) · skill `ags-prompt-affix`
(chi tiết lệnh) · skill `ags-memory` (tra/ghi bộ nhớ) · skill `ags-sidebar-qa` (qa + sidebar) · skill `ags-core`
(luật 0 — mã lượt) · skill `ags-ops-lessons` mục E (bẫy hiểu sai "đừng dùng token").
