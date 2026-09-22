---
name: ags-viral-ideas
description: Xin ý tưởng viral / campaign / ý tưởng kinh doanh qua dây chuyền AGS "online cat=idea" — hỏi hồ sơ (doanh nghiệp, sản phẩm, từ khoá) có kiểm bằng mã, nộp máy chủ, dựng trang, bung lên màn hình. Dùng khi người dùng nói "xin ý tưởng viral", "idea", "plan/campaign viral", "kinh doanh gì", "khởi nghiệp", "cho tao vài ý tưởng".
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Xin ý tưởng viral — MỘT LỆNH DUY NHẤT

Người dùng xin ý tưởng ("xin ý tưởng viral", "idea viral", "plan viral", "campaign viral", "xin idea", "ý tưởng kinh doanh",
"kinh doanh gì", "khởi nghiệp", "startup idea") → gõ **đúng một lệnh**, rồi thôi:

```
ags online cat=idea prompt="<nguyên văn câu người dùng vừa nói>"
```

Lệnh trả về NGAY, việc chạy nền. AGS tự làm trọn dây chuyền và **ốp lại chính cuộc chat này** ở từng bước:

1. **Hỏi hồ sơ.** AGS bơm một lời nhờ: tra `ags api GET /api/cloud/brand` xem người dùng đã có doanh nghiệp/sản phẩm chưa.
   - Có → LIỆT KÊ cho họ CHỌN, rồi hỏi lại một câu: "Lần này làm cho [DN] – [sản phẩm], nhấn vào [từ khoá]. Còn đúng không?"
     Họ nói cần sửa → HỎI RÕ SỬA CHỖ NÀO.
   - Chưa có → hỏi gọn một lượt.
   - Xong in ra đúng MỘT khối JSON: `{"ten_doanh_nghiep":"...","san_pham":"...","keyword_viral":"..."}`
   AGS **kiểm bằng mã**: đủ 3 trường; đếm chữ theo khoảng trắng — doanh nghiệp **1–5 chữ**, sản phẩm **1–5 chữ**,
   từ khoá **2–4 chữ** ("chó mèo"=2, "tiệm spa chó"=3). Chưa đạt → nó bơm lại KÈM LÝ DO (thừa/thiếu mấy chữ ở đâu) →
   hỏi lại người dùng rồi in lại JSON.
   ⚠ Quá dài thì bảo người dùng RÚT GỌN. **Đừng tự cắt hộ, đừng bịa cho đủ.**
2. **Nộp việc lên máy chủ** — bài prompt nằm trên máy chủ, bạn không thấy và không cần thấy.
3. **Dựng trang** — AGS ốp bạn dựng trang giới thiệu từ dữ liệu nhận về; kiểm bằng mã, chưa đạt thì bắt làm lại.
4. **Đóng dấu bản quyền rồi tự bung trang lên màn hình.**

⛔ **ĐỪNG tự gọi `/api/cloud/agent-jobs`.** Đi đường đó là bỏ qua hết phần kiểm bằng mã — hồ sơ thiếu vẫn lọt, trang dựng
ẩu vẫn qua. Cứ `online cat=idea` rồi làm theo thứ nó nhờ.

**Người dùng thấy gì:** bảng phải tự hiện tab tiến độ. Nói họ khỏi ngồi canh — đóng chat đi làm việc khác, lát mở bảng phải
vẫn thấy.
