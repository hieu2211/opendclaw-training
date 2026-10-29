---
name: skk-creative
description: Sinh ý tưởng viral/campaign, làm slide thuyết trình, dựng video giới thiệu ngắn từ brand/chủ đề. Dùng khi người dùng nói "ý tưởng viral", "làm slide", "video giới thiệu", "pitch deck", "campaign".
---

# SKK Creative — ý tưởng, slide, video trên OpenClaw

Gộp viral + video + slide vì cùng mục đích "sinh nội dung sáng tạo". OpenClaw không có server
cloud riêng để "nộp ý tưởng", không có addon canvas-motion-design riêng, không có trình duyệt ABA
mặc định (chỉ có nếu máy đã cài `skk-aba` — kiểm `which skk-aba` + file
`/home/node/.openclaw/workspace/skills/skk-aba/SKILL.md` tồn tại trước khi giả định có). Không
port nguyên AGS — thay bằng cơ chế OpenClaw thật: subagent brainstorm, file xuất qua exec, gửi
qua message.

## Cơ chế thật của AGS — để đối chiếu, không copy

- **`ags viral`**: một lệnh `ags online cat=idea prompt=...` chạy nền. AGS server tự "ốp" lại
  chính cuộc chat đang chạy, bắt agent hỏi hồ sơ thương hiệu (tên DN/sản phẩm/từ khoá, kiểm đếm
  chữ bằng mã), nộp prompt lên server AGS (agent không thấy nội dung xử lý), rồi AGS lại ốp dựng
  landing page từ dữ liệu trả về, kiểm bằng mã, đóng bản quyền, tự bung trang. Cấm gọi API thô
  (`/api/cloud/agent-jobs`) vì bỏ qua hết bước kiểm.
- **`ags video`**: dựng 1 file HTML canvas tự chứa — mọi khung hình là hàm thuần của thời gian
  `t` (pure function), player tự chứa (▶, tua, nút tải MP4 — người xem tự bấm, agent KHÔNG tự
  render MP4 trừ khi người dùng đòi rõ). Hỏi tối đa 2 màn `ags form` (kịch bản+kiểu, rồi
  storyboard từng cảnh). Nhạc agent tự tải từ Mixkit, phân tích BPM/beat phase để khớp nhịp.
  Ảnh/logo lấy qua trình duyệt thật (addon ABA), không `curl` thẳng link (tránh 403/hotlink
  block). Cần addon riêng "Xưởng video & slide" (`ags-studio`) + ABA mới chạy được. Có hàng chục
  luật cứng chống lặp motif, chống "cảm giác slide chạy" (cấm lượng tử hoá thời gian toàn cục),
  bắt buộc ít nhất 1 vật chủ morph xuyên cảnh, tự chụp stills soát tràn chữ/chồng lớp trước khi
  giao.
- **`ags slide`**: tương tự nhưng ra bộ slide — xuất PNG từng trang + PDF + PPTX (dạng ảnh, không
  sửa chữ được) + ghi chú người nói, 2 chế độ dựng ("một style chung" hoặc "xoay vòng kiểu/bộ
  lớn" dùng kit 23 kiểu có sẵn), cũng 2 màn `ags form`, cũng cần `ags-studio` + ABA, cũng tự soát
  tràn chữ bằng mã trước khi xuất (bắt buộc 0 cảnh báo tràn).

## Vì sao không map 1:1

`ags video` và `ags slide` là hai hệ thống rất lớn: addon riêng biên dịch/chạy HTML-canvas động,
thư viện kỹ thuật morph/beat-sync riêng, pipeline lấy ảnh qua trình duyệt thật (không phải HTTP
fetch), hàng chục luật cứng chống lặp và chống tràn chữ được kiểm bằng mã (đếm số lần gọi `kf(`,
đếm cảnh dùng lượng tử hoá thời gian...), cơ chế "ốp lại chat" để ép đúng quy trình nhiều bước.
OpenClaw không có addon canvas-motion-design, không có server tự ốp lại chat, không có pipeline
nhạc-beat-sync hay trình duyệt mặc định để lấy ảnh né hotlink-block. Copy kiến trúc đó vào đây là
giả lập độ phức tạp không cần thiết và không ai bảo trì nổi (YAGNI) — nếu copy nửa vời sẽ tạo ảo
giác "làm được như AGS" trong khi thực chất chỉ ra file tĩnh đơn giản, gây hiểu lầm. Thay bằng bản
giản lược rõ giới hạn: nếu người dùng cần đúng y như `ags video`/`ags slide` (nhạc khớp beat, morph
chuyên nghiệp, PPTX edit được...), **nói thẳng OpenClaw không có addon đó**, và đề xuất 2 hướng:
(a) nếu máy có sẵn AGS cài đặt, gọi thẳng `ags video`/`ags slide` qua `exec`; (b) nếu không, làm
bản tĩnh giản lược theo mục 2/3 dưới.

## 1. Ý tưởng viral/campaign (thay `ags viral`)

Không nộp lên server cloud nào hết, không có landing-page-pipeline tự động. Spawn 1 subagent
brainstorm:
```
sessions_spawn(
  task: "Nghĩ N ý tưởng viral/campaign cho [brand/sản phẩm/từ khoá]. Trả markdown có cấu trúc:
         tiêu đề, insight, concept, kênh phù hợp, gợi ý hook.",
  context: "isolated"
)
```
Dùng model mặc định; chỉ đổi model mạnh hơn nếu người dùng cần chiều sâu sáng tạo cao.
Trả kết quả dạng markdown thẳng trong chat là đủ trong đa số trường hợp.
Chỉ dựng thành "trang web"/landing page khi người dùng yêu cầu rõ ràng muốn 1 trang xem được:
- Đang ở webchat → `[embed ...]` qua Control UI.
- Không thì ghi file `.md`/`.html` qua `exec` rồi gửi qua `message` dạng attachment.

## 2. Video (thay `ags video`)

Việc NẶNG — trước khi làm, hỏi lại người dùng có thực sự cần video động không, hay slide
tĩnh/ảnh là đủ đáp ứng mục đích (YAGNI). **Không tự viết canvas-motion-design phức tạp kiểu AGS**
(không beat-sync, không morph object xuyên cảnh, không hệ luật chống lặp) — nếu người dùng đòi
đúng mức đó, xem mục "Vì sao không map 1:1" ở trên.

Chọn theo thứ tự công cụ đã có, không ép buộc trình duyệt:
1. `which ffmpeg` có → viết code render từng frame ảnh tĩnh (HTML→ảnh qua công cụ đã có, hoặc
   canvas/SVG → PNG) rồi `ffmpeg` ghép frame thành video. Đây là đường mặc định cho nhu cầu
   đơn giản (slideshow có chữ, chuyển cảnh fade cơ bản).
2. Nếu đã có Remotion hay công cụ HTML→video khác cài sẵn trong môi trường → dùng thẳng, không
   cài thêm công cụ nặng mới nếu không bắt buộc.
3. Chỉ khi cần render HTML/CSS động thật (animation phức tạp JS-driven) và máy có addon
   `skk-aba` kết nối thật (`which skk-aba` + `skk-aba health` xác nhận) → dùng `skk-aba` để quay
   màn hình tab render. Không giả định ABA luôn có.

## 3. Slide thuyết trình (thay `ags slide`)

Ưu tiên đơn giản nhất đáp ứng được, không dựng engine canvas/kit 23 kiểu riêng:
1. Markdown có cấu trúc (mỗi `## ` là 1 slide) — xuất thẳng, convert khi cần bằng công cụ có sẵn.
2. HTML tĩnh đơn giản (không cần JS động) — xem qua `message` attachment, hoặc `[embed ...]`
   nếu webchat.
3. **Chỉ** xuất PPTX/PDF thật khi người dùng cần đúng định dạng file đó:
   - `which pandoc` có → convert markdown → pptx/pdf trực tiếp.
   - `which libreoffice` có → convert HTML/odp → pptx/pdf.
   - Không có cả hai → hỏi xác nhận trước khi cài qua package manager (xem skill `skk-package`),
     không tự ý cài công cụ nặng nếu markdown/HTML đã đáp ứng được nhu cầu.
   - Lưu ý: PPTX xuất kiểu này là slide ảnh/text thường, không có hiệu ứng morph/bước từng ý như
     AGS — nói rõ giới hạn nếu người dùng kỳ vọng trình chiếu động.

## Giản lược có chủ đích

- Không dựng landing page/server riêng cho mọi ý tưởng → skipped: chỉ cần khi người dùng đòi
  trang web, add qua `[embed]`/file HTML lúc đó.
- Không ép buộc pipeline trình duyệt cho video → skipped: ffmpeg ghép frame đủ cho hầu hết case,
  add route `skk-aba` khi cần animation CSS/JS thật mà máy có addon.
- Không tự cài pandoc/libreoffice mặc định → skipped: phần lớn yêu cầu dừng ở markdown/HTML,
  add cài đặt khi người dùng xác nhận cần file PPTX/PDF thật.
- Không tự viết engine canvas-motion-design/beat-sync kiểu AGS → skipped: quá lớn để giản lược
  đúng, add bằng cách gọi thẳng `ags video`/`ags slide` qua exec nếu máy có AGS cài sẵn.
