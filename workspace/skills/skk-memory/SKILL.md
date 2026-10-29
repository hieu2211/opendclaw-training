---
name: skk-memory
description: Bộ nhớ dự án dài hạn + hồ sơ thương hiệu, thuần OpenClaw (thay ags mem / ags brand / ags affix). Dùng khi người dùng nói "ghi nhớ", "bộ nhớ dự án", "hôm trước chốt gì", "hồ sơ thương hiệu/doanh nghiệp/sản phẩm", "chèn luật vào mọi prompt".
---

# SKK Memory — bộ nhớ dự án thuần OpenClaw (thay ags mem / ags brand / ags affix)

## AGS gốc làm gì (đọc từ `ags <lệnh> -h` thật, không suy đoán)

**`ags mem`** — bộ nhớ cloud dùng chung dự án, lưu theo CÂY nhánh:
- `tree` — in cây: mỗi nhánh NGỌN là một đường "A -> B -> C" kèm mô tả nhánh + cách viết bản ghi/snap.
- `save '<json>'` (hoặc `--file`/`-` để tránh PowerShell nuốt dấu nháy) — nạp bản ghi. `new_entry`
  là mảng object `{"prompt":"…","answer":"…","tags":[]}`, hoặc một chuỗi thuần (= phần đáp).
  **Chỉ ghi được vào nhánh NGỌN** — nhánh còn nhánh con bị từ chối thẳng. Có thể kèm
  `"da_chat":["#ff7","#ff9"]` đánh dấu lượt đã xem để khỏi bị nhắc lại. Ghi xong phải viết lại
  **SNAP** của nhánh vừa ghi.
- `entries [--all] [--limit N] [--topic '<nhánh>'] [--before <id>]` — đọc bộ nhớ cuộc chat này;
  `--all` = cả dự án.
- `counter` — tổng số prompt đã tích luỹ.

**`ags brand`** (addon content-factory) — hồ sơ thương hiệu qua `/api/cloud/brand` (GET/save/
link/delete): thực thể `t4` (kind/parent_id/name/mo_ta/gia/diem_doc_dao) → gắn vào `brand`
(ten/logo/slogan/category/pod/usp/hinh_mau/tinh_cach/su_menh/tam_nhin/gia_tri_cot_loi) → nhiều
`campaign` (muc_tieu_kinh_doanh/muc_tieu_truyen_thong/chien_luoc/chien_thuat/kpi) → `calendar`
(tu_ngay/den_ngay) → `content` (mo_ta_ngan/mo_ta_dai/kenh_phan_phoi/thumbnail/video). Thông điệp
RIÊNG theo nhóm công chúng nằm ở `link campaign-ta`. Ảnh/logo/video nằm trên máy người dùng nên
phải kèm `device_id`.

**`ags affix`** (addon riêng) — chèn `prefix`/`suffix` vào mọi prompt, theo `scope=conv` (mặc
định, theo conv hiện tại) hoặc `scope=project` (conv đè project). `tokenCutting`+`everyN` =
chỉ nhắc luật đầy đủ mỗi N câu; `smartRemind` (mặc định BẬT) chèn một dòng ngắn gọi tên luật
giữa hai lần nhắc đầy đủ. Tắt từng phần bằng `prefixOn:false`/`suffixOn:false` (nội dung vẫn
còn, bật lại là dùng ngay).

## Phản biện: vì sao không map 1:1

- `ags mem` là server cloud riêng với khái niệm "nhánh ngọn mới được ghi" + lệnh `snap` ràng buộc
  theo cây — OpenClaw không có cây nhánh hay khái niệm ngọn/snap ở tầng platform; đi xây lại y hệt
  là dựng thêm một hệ thống không ai yêu cầu (YAGNI).
- `ags brand` là CSDL quan hệ nhiều bảng có validate tên trường chặt (sai tên trường bị máy chủ
  báo lỗi) — OpenClaw không có server lưu entity/brand/campaign kiểu đó; file markdown tự do
  không validate, đổi lại là không cần cài addon/server riêng.
- `ags affix` cấu hình per-cuộc-chat qua API riêng, bật/tắt độc lập từng conv — OpenClaw nạp
  `AGENTS.md`/`SOUL.md`/`MEMORY.md` lại ở **mọi turn** làm Project Context tự động, không cần
  gọi API bật/tắt; đổi lại không tách được theo từng cuộc chat riêng lẻ.

## Cách OpenClaw làm tương đương

### 1. Bộ nhớ dự án (thay `ags mem`)

Quy ước dùng trong workspace này — file `.md`, không có khái niệm nhánh ngọn/snap riêng:
- `knowledge/<chu-de>/MEMORY-<ten>.md` — tri thức dài hạn, cập nhật khi có quyết định/sự kiện mới.
- `knowledge/<chu-de>/memory-YYYY-MM-DD-<ten>.md` — nhật ký theo ngày khi cần mốc thời gian rõ
  (giữ MEMORY tổng không phình).
- `knowledge/INDEX.md` — mục lục trỏ tới từng thư mục chủ đề (tương đương `ags mem tree`, nhưng
  phẳng, không có ràng buộc "chỉ ghi vào ngọn").

**Đọc lại ("hôm trước chốt gì")**: `grep`/`cat` đúng file `knowledge/<chu-de>/MEMORY-*.md`, đừng
bịa khi không thấy — trả lời "chưa có ghi chép" trung thực hơn đoán.

**Ghi mới**: mở file đúng chủ đề, append đoạn mới có ngày (`## YYYY-MM-DD — <việc>`), không ghi
đè đoạn cũ. Chưa có chủ đề phù hợp thì tạo thư mục mới trong `knowledge/` + thêm dòng vào
`INDEX.md`. Bản ghi cần nguồn (AGS bắt buộc `tags`): ghi kèm "(nguồn: <việc/người yêu cầu>)"
cuối đoạn, đủ dùng, không cần hệ thống tag riêng.

### 2. Hồ sơ thương hiệu/doanh nghiệp/sản phẩm (thay `ags brand`)

Một file `knowledge/brand/<ten-thuong-hieu>.md` với các mục cố định:

```markdown
# <Tên thương hiệu>
## Thực thể liên quan
- <doanh nghiệp/sản phẩm>: <mô tả ngắn, điểm độc đáo>
## Hồ sơ thương hiệu
- Slogan / tính cách / sứ mệnh / tầm nhìn / giá trị cốt lõi
## Chiến dịch
### <Tên chiến dịch> (<từ ngày> → <đến ngày>)
- Mục tiêu kinh doanh / truyền thông:
- Thông điệp theo nhóm công chúng:
  - <Nhóm A>: <thông điệp riêng>
## Lịch nội dung
- <ngày> — <mô tả bài> — kênh: <...>
```

Không có API lưu ảnh/logo riêng — file media gửi qua `message` (attachment) hoặc đường dẫn tệp
trong workspace, ghi đường dẫn vào mục tương ứng (không cần `device_id` vì không có khái niệm
nhiều máy chia sẻ một kho cloud).

### 3. Luật chèn mọi prompt (thay `ags affix`) — ĐÃ CÓ SẴN, KHÔNG CẦN CODE

Muốn "chèn luật vào mọi prompt" → thêm dòng vào `AGENTS.md` (luật hành vi) hoặc `MEMORY.md`
(sự kiện/quyết định cần nhớ). Không toggle theo từng conv như AGS — luật áp dụng cho cả
workspace.

## Giới hạn / Giản lược có chủ đích

- Không có khái niệm "nhánh ngọn" / từ chối ghi vào nhánh còn con — file `.md` phẳng theo chủ
  đề, không validate cây.
- Không có lệnh `counter` đếm tổng prompt riêng, không có lệnh `snap` riêng theo nhánh.
- Không có CSDL quan hệ validate tên trường cho brand/campaign/calendar/content — sai tên mục
  trong markdown không bị máy báo lỗi, tự kiểm bằng mắt.
- Không toggle prefix/suffix bật/tắt theo từng cuộc chat, không có `tokenCutting`/`everyN`/
  `smartRemind` — `AGENTS.md`/`MEMORY.md` áp toàn workspace mọi turn, không chọn lọc theo conv.
- Không đoán khi thiếu thông tin — ghi rõ "chưa có" và hỏi người dùng.
