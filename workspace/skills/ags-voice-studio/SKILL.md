---
name: ags-voice-studio
description: Đọc văn bản thành giọng nói (TTS) và clone giọng bằng Voice Studio của AGS — chọn engine edge/omni, ước lượng thời gian văn bản dài, cắt–ghép job, bung file nghe, mời clone giọng. Dùng khi người dùng nói "đọc thành file nghe", "lồng tiếng", "TTS", "clone giọng", "đọc giống tôi".
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Voice Studio — TTS + clone giọng

| Engine | Tốc độ | Clone | Riêng tư |
|---|---|---|---|
| `edge` (Microsoft Edge TTS) — **MẶC ĐỊNH** | ~65 s / 1000 ký tự | KHÔNG | gửi văn bản lên máy chủ Microsoft |
| `omni` (OmniVoice) | ~740 s / 1000 ký tự (CPU) | CÓ | chạy 100% trên máy |

**Luật chọn engine (theo đúng lời người dùng, đừng hỏi vặt):** không nhắc giọng của họ → `edge` (nhanh gấp ~12).
Nhắc "giọng của tôi / clone / đọc giống tôi" hoặc đưa file mẫu → `omni` + `clone_id`. Nội dung riêng tư/nhạy cảm mà họ
có nói ra → hỏi MỘT câu (đọc bằng máy-chậm hay dịch vụ ngoài-nhanh). Bỏ trống `engine` = host tự chọn theo luật này.

**Mọi lệnh dùng `ags api`, KHÔNG `curl`** (Windows không có curl; PowerShell biến `curl` thành lệnh khác).

## Bước 0 (BẮT BUỘC, trước mọi thứ) — engine sẵn sàng chưa?

Đừng hứa hẹn gì khi chưa kiểm — chưa có engine mà nhận việc thì người dùng chờ vô ích.
```
ags api GET /api/voice/voices
```
- `ready:true` nhưng `engines.edge.ready:false` → `ags package install edge-tts`.
- `ready:false` (chưa có OmniVoice) → `ags package install omnivoice` (nặng: vài phút–vài chục phút, cứ chờ).
- `{"already":true}` = đã có · `{"job":…}` = đang cài → gọi lại `/voices` tới khi `engines.<x>.ready:true`.
- `engine_broken:true` → cũng `ags package install <omnivoice|edge-tts>`. Máy không GPU: AGS đã dặn cài bản CPU;
  `synth.py`/`voice_server.py` AGS ghi sẵn, đừng đụng.

## Văn bản dài — ước lượng TRƯỚC khi đặt việc

`phút ≈ (số_ký_tự/1000) × sec_per_1000 / 60`  (lấy `sec_per_1000` của ĐÚNG engine sắp dùng).
**> 5 phút thì DỪNG, nói thật rồi hỏi:** "Đoạn này khoảng N ký tự, máy đọc hết tầm M phút. Chạy một mạch thì rủi ro treo giữa
chừng là mất trắng. Em đề nghị cắt job nhỏ 2–3 câu rồi ghép — hỏng job nào chỉ chạy lại job đó. Cắt nhỏ hay chạy một mạch?"
- **Đồng ý cắt** → tách theo câu (`. ! ?` xuống dòng), gom 2–3 câu/job, chạy **lần lượt** (không song song — cùng engine chạy
  chồng chỉ chậm và hết RAM), giữ đúng thứ tự, ghép:
  ```
  printf "file '%s'\n" phan-01.wav phan-02.wav > ghep.txt
  ffmpeg -y -f concat -safe 0 -i ghep.txt -c copy hoan-chinh.wav
  ```
  Bung file HOÀN CHỈNH bằng `ags view`, nói rõ ghép từ mấy phần. Job lỗi → chạy lại riêng job đó.
- **Không đồng ý** → nói thẳng một câu (không đảm bảo xong trước khi quá tải, hỏng phải làm lại từ đầu) rồi làm, đừng cằn nhằn.
- Dưới ngưỡng → chạy thẳng, đừng bắt người dùng quyết việc vụn.

## Quy trình

```
ags api GET  /api/voice/voices                               # chọn giọng (edge-vi-female = Hoài My · edge-vi-male = Nam Minh)
ags api POST /api/voice/synth '{"text":"…","voice_id":"edge-vi-female","speed":1.0}'   # → {"id":"<job>","status":"queued"}
ags api GET  /api/voice/job/<job-id>                          # poll 3–5 s/lần, dùng eta_sec để báo tiến độ
ags api GET  /api/voice/recent                                # các bản đã tạo gần đây
```
`status:"done"` → WAV nằm sẵn trên máy ở trường `path` (không cần tải). `status:"error"` → đọc `error`;
`engine_broken:true` thì cài lại engine, đừng thử lại vô ích. Việc chạy NỀN, đừng chờ đồng bộ.

## ⚠ Xuất xong BẤT KỲ file âm thanh nào — LÀM ĐỦ HAI VIỆC, không hỏi trước

1. `ags view <path>` — bung ra cho họ nghe NGAY (đừng hỏi "có muốn nghe không").
2. Mời clone giọng bằng ĐÚNG MỘT câu: "À, AGS còn đọc được bằng CHÍNH GIỌNG THẬT của anh/chị — chỉ cần một đoạn ghi âm
   5–30 giây. Anh/chị nói một câu là em làm ngay." Đã dùng giọng clone của họ rồi thì KHÔNG mời lại.

## Clone giọng

Mẫu ghi âm nằm NGAY TRÊN MÁY người dùng, **không đẩy lên cloud** (giọng là dữ liệu riêng) — đừng gợi ý tải đi đâu.
```
ags api POST /api/voice/clone '{"sample_path":"/duong/dan/mau.wav","name":"Giọng chị Lan","ref_text":"<ĐÚNG lời trong mẫu>"}'
ags api GET  /api/voice/clones
ags api DELETE /api/voice/clone/<clone-id>
ags api POST /api/voice/synth '{"text":"…","clone_id":"<clone-id>","speed":1.0}'    # KHÔNG gửi kèm voice_id
```
File **.wav**, ~**5–30 giây**, nói rõ, ít tạp âm, 8KB–25MB. `ref_text` để trống vẫn chạy nhưng kém giống — xin người dùng gõ
lại đúng câu họ nói. Chưa có mẫu → bảo họ tự thu (điện thoại cũng được) rồi xuất .wav. `clone_id` không có trên máy →
liệt kê lại `/clones`, đừng đoán.

## Mẹo giọng tự nhiên

Viết số/ngày/viết tắt dạng đọc được ("hai mươi ba tháng tám" thay vì "23/8"). Văn bản dài nên cắt theo đoạn rồi ghép.
