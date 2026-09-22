---
name: ags-memory
description: Bộ nhớ dài hạn của dự án AGS (AGSMem) — cây chủ đề, ghi nóng, tra cứu trước khi trả lời, viết lại snap, dọn bản ghi hỏng. Dùng khi người dùng hỏi "hôm trước chốt gì / đã bàn gì", khi vừa có quyết định/bài học đáng nhớ, hoặc khi phiên sắp đầy ngữ cảnh.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# AGSMem — bộ nhớ dự án dạng cây (lưu cloud, sống qua nhiều phiên)

Bộ nhớ là một **CÂY CHỦ ĐỀ** do người dùng dựng; mỗi nhánh có luật ghi riêng. Trong phiên bạn gần như không phải làm
gì: chỉ **ghi nóng** khi có chuyện đáng nhớ ngay, và **tra cây** khi cần biết chuyện cũ. Cuối phiên một agent phụ đọc lại
cuộc trò chuyện và chắt vào cây.

## 1. Ghi nóng — CHỈ khi đáng

```
ags mem hot "Admin chốt X, lý do Y"
```

**Đáng ghi:** người dùng CHỐT một điều (quyết định, luật, con số cuối) — nhất là khi nó lật cái đã chốt trước; một lỗi
đã trả giá (triệu chứng → nguyên nhân thật → cách chữa); một mốc thật (ra bản, đổi kiến trúc, ràng buộc mới).
**ĐỪNG ghi:** hỏi đáp thông thường, thao tác vụn, việc đang dở chưa ngã ngũ. Ghi mọi lượt = làm loãng kho.
Viết như nói cho người khác: một câu, có chủ ngữ, tự đủ nghĩa; KHÔNG chép nguyên văn, KHÔNG kèm mã dài.

## 2. Phiên sắp đầy (~85–90% ngữ cảnh, chưa bị nén)

```
ags mem cuoi-phien       # trả về ngay, chắt lọc chạy nền, bạn cứ làm tiếp
```
Với Claude, host đã cắm sẵn hook PreCompact nên thường khỏi gọi tay.

## 3. Tra TRƯỚC khi trả lời — theo thứ tự này, đủ là dừng

```
ags mem tim "<điều cần biết>"    # BƯỚC ĐẦU: soi cả bản tóm lẫn bản ghi, trả vài đoạn hợp nhất (--n 8 nếu cần nhiều)
ags mem snap                     # bản chắt lọc của MỌI nhánh
ags mem snap <mã nhánh | "Tên nhánh" | "A -> B">
ags mem tree                     # xem cây có nhánh nào, mã gì
ags mem entries --all --topic <mã nhánh> --limit 20    # CHỈ khi snap không đủ
ags mem snap --fr                # ép lấy nguyên văn (mặc định lặp lại sẽ chỉ báo "KHÔNG ĐỔI" — đó là câu trả lời ĐÚNG)
```

- ⛔ **TUYỆT ĐỐI đừng `ags mem entries --all` trần** — kéo hàng trăm bản, vừa tốn vừa dễ vớ phải điều đã bị quyết
  định sau lật (bản ghi chỉ THÊM, không sửa). Snap là bản đã chắt và dọn trùng.
- `ags mem tim` bắt được cả từ ghép tiếng Việt; grep thì chỉ khớp mặt chữ. Có lệnh tìm — đừng bảo người dùng là không có.
- Tên nhánh khớp nhiều chỗ → host liệt kê cho bạn chọn; đừng đoán, đừng tra cả cây rồi tự dò.
- Trong snap, `@543` = mã BẢN GHI đầy đủ; snap chỉ là mục lục, cần kỹ thì lần theo mã.
- Người dùng hỏi "ghi chú của tôi có gì" → `GET /api/quicknote/list?limit=50` (`/note` là của họ, bạn không ghi vào).

## 4. Ghi bản ghi (nạp có cấu trúc)

```
ags mem save '<json>' | ags mem save --file duong-dan.json | ags mem save -     # PowerShell: dùng --file
{"topic_id":"6552","new_entry":[{"prompt":"…","answer":"…","tags":[]}]}          # new_entry là MẢNG
```
- Chắt theo câu nhắc thì kèm `"da_chat":["#ff7","#ff9"]` để host thôi nhắc lại các lượt đó.
- Nhánh CÒN nhánh con thì bị từ chối — gắn xuống nhánh NGỌN. `ags mem save` trần in ra khuôn JSON đầy đủ.
- **Ghi xong NHỚ viết lại snap của nhánh vừa ghi.**

## 5. Cách chọn nhánh & viết lại snap (việc của agent chắt lọc)

1. Hỏi: điều này NÓI VỀ chuyện gì? 2. Dò bảng nhánh (`topic` + `gom` + `ban_ghi_cach_viet`), chọn nhánh CỤ THỂ NHẤT.
3. Không nhánh nào đúng → **BỎ HẲN**, đừng nhét nhánh gần gần. MỘT điều chỉ vào MỘT nhánh (cấm chép y nguyên sang hai chỗ).
Sai hay gặp: chuyện đời sống (ăn uống, du lịch) ném vào nhánh kỹ thuật; một câu bình thường xé thành nhiều bản ghi.

Tin mới chọi tin cũ → theo lối nhánh khai: **Giữ mới** (bỏ cũ) · **Tổng hợp** (gom cả hai) · **Hỏi lại** (ĐỪNG tự quyết —
ghi vào snap một dòng cần xác nhận).

Viết lại snap: `GET /api/agsmem/snap?topic=<mã>` (trả `snap`, `kind`, `max_len`, `rule_distill`, `rule_important`).
**BẮT BUỘC đọc bản hiện có rồi GỘP** — viết đè bằng bản ngắn hơn = xoá tri thức cũ, host chặn cả đợt.
- Trùng ý >40% với snap hiện có → THÔI.
- Điều mới đặt **LÊN TRÊN** (đầu đoạn / đầu danh sách), không nối cuối.
- Mỗi ý một gạch đầu dòng ngắn kèm `@ID`: `- AGS có prefix để nhắc nhớ Agent @543`.
- Vượt `max_len` thì NÉN: mẩu có `(!)` (người dùng ghim) GIỮ; mới giữ, cũ nhường; đoạn dài → TÁCH thành bản ghi mới, để
  lại một gạch đầu dòng + `@ID`. **Nén bằng con trỏ, đừng gộp nghĩa** (gộp "phở, bún bò, miến" → "món nước" là mất
  "ghét miến").
- Nộp: `POST /api/agsmem/snap {"topic_id":"…","conv_id":<AGS_CONV_ID>,"snap":"…"}` — thiếu `conv_id` là bị từ chối.
- Gặp câu bắt đầu bằng **CHẶN QUYỀN** → nhánh chỉ được đọc: DỪNG, đừng thử đường khác, báo người dùng.

## 6. Dọn bản ghi hỏng (chỉ thứ CHÍNH BẠN vừa ghi hỏng, hoặc khi người dùng bảo)

```
ags mem xoa 137 | --ids 12,15,20 | --tu 100 --den 120 | --moi 5 | --cu 5 | --ngay 2026-09-03 | --tu-ngay A --den-ngay B
        [--topic <mã>]     # chọn theo lô chỉ LIỆT KÊ; phải thêm --that mới xoá thật (gõ đích danh 1 mã thì xoá luôn)
ags mem thung-rac ; ags mem khoi-phuc 137      # khôi phục = ghi lại thành bản MỚI (mã mới)
```
Xoá bản ghi KHÔNG đụng snap; muốn snap thôi nhắc chuyện cũ thì viết lại snap. Đừng tự dọn bản ghi cũ của người khác.
