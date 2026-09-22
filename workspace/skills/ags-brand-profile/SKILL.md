---
name: ags-brand-profile
description: Xem/sửa hồ sơ thương hiệu & truyền thông trong AGS (thực thể người/doanh nghiệp/sản phẩm → thương hiệu → chiến dịch → lịch nội dung → bài đăng). Dùng khi người dùng chỉ muốn XEM hoặc SỬA hồ sơ, không xin ý tưởng viral.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Hồ sơ thương hiệu & truyền thông

Chỉ dùng khi người dùng muốn XEM/SỬA hồ sơ. Xin ý tưởng → `ags-viral-ideas`.

```
ags api GET  /api/cloud/brand                                   # lấy trọn hồ sơ một lần
ags api POST /api/cloud/brand/save   '{"bang":"t4","kind":"business","name":"..."}'      # tạo
ags api POST /api/cloud/brand/save   '{"bang":"t4","id":<id>,"name":"tên mới"}'          # sửa
ags api POST /api/cloud/brand/link   '{"loai":"t4-brand","t4_id":<id>,"brand_id":<id>}'
ags api POST /api/cloud/brand/delete '{"bang":"t4","id":<id>}'
```

## Cấu trúc
Người / doanh nghiệp / sản phẩm đều là **thực thể** (cha–con qua `parent_id`) → gắn vào **thương hiệu** → thương hiệu có nhiều
**chiến dịch** → chiến dịch có **lịch nội dung** → lịch có **bài đăng**. MỘT thương hiệu dùng chung cho nhiều thực thể được.

## Bảng nhận trường nào
- `t4`: kind · parent_id · name · mo_ta · gia · diem_doc_dao
- `brand`: ten · logo · logo_don_sac · logo_rut_gon · device_id · slogan · category · pod · usp · hinh_mau · tinh_cach ·
  su_menh · tam_nhin · gia_tri_cot_loi
- `ta` / `channel`: ten · mo_ta
- `campaign`: brand_id · ten · muc_tieu_kinh_doanh · muc_tieu_truyen_thong · thong_tin_can_truyen · chien_luoc ·
  chien_thuat · kpi
- `calendar`: campaign_id · ten · tu_ngay · den_ngay
- `content`: calendar_id · mo_ta_ngan · mo_ta_dai · kenh_phan_phoi · device_id · thumbnail · hinh_dinh_kem · video

Gửi sai tên trường thì máy chủ báo rõ bảng đó nhận cột nào — **đọc lời báo mà sửa**, đừng đoán.

## Thông điệp riêng cho từng nhóm công chúng nằm ở chỗ nối
```
ags api POST /api/cloud/brand/link '{"loai":"campaign-ta","campaign_id":<id>,"ta_id":<id>,"thong_diep":"..."}'
```

## Ảnh / logo / video nằm trên MÁY NGƯỜI DÙNG
→ gửi kèm `device_id` của máy đang chạy. Thiếu nó thì mở ở máy khác là gãy.
