---
name: skk-voice
description: Đọc văn bản thành giọng nói (TTS), gửi voice note, thuần OpenClaw (thay ags voice). Dùng khi người dùng nói "đọc thành giọng nói", "gửi voice", "lồng tiếng", "giọng nói", "TTS", "clone giọng".
---

# SKK Voice — TTS thuần OpenClaw (thay AGS Voice Studio)

## Cơ chế thật của AGS (để biết mình đang giản lược cái gì)

`ags voice` không phải 1 lệnh đơn — là cả một hệ: 2 engine tích hợp dùng chung job queue qua
`ags api`:

| Engine | Tốc độ | Clone giọng | Riêng tư |
|---|---|---|---|
| `edge` (Microsoft Edge TTS, mặc định) | ~65 giây/1000 ký tự | KHÔNG | gửi văn bản lên server Microsoft |
| `omni` (OmniVoice) | ~740 giây/1000 ký tự (CPU) | CÓ, cần file mẫu .wav 5–30s + `ref_text` | chạy 100% local |

Quy trình thật: `ags api GET /api/voice/voices` (kiểm engine sẵn sàng) → ước lượng thời gian đọc
= `(số_ký_tự/1000) × sec_per_1000 / 60` phút; **vượt 5 phút thì DỪNG, hỏi người dùng** cắt nhỏ
job hay chạy một mạch → `ags api POST /api/voice/synth {...}` (job chạy NỀN, trả `job-id` ngay)
→ poll `ags api GET /api/voice/job/<id>` mỗi 3–5s tới khi `status:"done"` lấy `path` file .wav →
`ags view <path>` bung cho người dùng nghe. Clone giọng là API riêng: `POST /api/voice/clone`
với `sample_path` (.wav 5–30s) + `ref_text` (lời thoại mẫu, giúp giống hơn).

## Vì sao KHÔNG map 1:1 sang OpenClaw

- Toàn bộ "2 engine + job queue + poll trạng thái + ước lượng phút" tồn tại vì AGS là **app
  lưu trữ file** chạy trên máy người dùng (model tự host, CPU chậm, phải canh treo máy). OpenClaw
  gọi provider TTS qua tool `message` — không tự chạy model, không có khái niệm "máy mình chậm
  nên phải ước lượng/cắt job".
- Clone giọng của AGS (`omni`) là model chạy local xử lý file .wav mẫu — OpenClaw không có path
  tương đương native; đây là **giới hạn thật, không giả lập**.

## Cách dùng (một bước, không cần job/polling)

```
message(action="send", target="<đích>", voiceText="<nội dung cần đọc>", asVoice=true)
```

- `voiceText`: văn bản cần đọc — tool tự tổng hợp giọng và gửi như voice note, xử lý đồng bộ
  trong một lệnh gửi.
- `asVoice: true`: bắt buộc để gửi dạng voice note (không phải file âm thanh thường).
- `voiceId` / `voiceProvider`: override giọng/nhà cung cấp nếu channel cho chọn (tuỳ kênh, không
  chắc có nhiều giọng như AGS edge/omni).

## Khác biệt chính (so AGS thật, không phải bản đoán cũ)

- **Không có bước "chọn engine edge/omni"**: OpenClaw không lộ 2-engine; nhà cung cấp TTS do
  platform/channel quyết, agent không tự chọn nhanh/chậm/riêng-tư như AGS.
- **Không có job-id + poll**: `message` xử lý đồng bộ, không trả `job-id` để `GET job/<id>`.
  Không có khái niệm "ước lượng phút đọc rồi hỏi cắt nhỏ" vì không chạy model local chậm.
- **KHÔNG có clone giọng từ file mẫu người dùng** (giới hạn thật, không bịa cách giả): AGS
  `omni` nhận .wav 5–30s + `ref_text` để clone. OpenClaw qua `message` không có API này. Người
  dùng cần đúng giọng họ → nói rõ giới hạn; nếu bắt buộc phải có, chỉ cách là addon/dịch vụ
  ngoài qua `exec` (tự cài TTS clone ngoài, không phải tính năng OpenClaw có sẵn) — không tự chế
  pipeline giả danh "clone".
- **Văn bản rất dài**: không có cơ chế cắt-job-ghép-ffmpeg như AGS (AGS cắt vì sợ job model local
  treo giữa chừng). Cần đọc văn bản dài thì agent tự cắt theo câu, gọi `message` nhiều lần theo
  thứ tự — mỗi lần là một voice note độc lập trong chat, không cần ghép file.
- **Đọc số/ngày tháng**: giữ nguyên lưu ý của AGS — viết ra dạng đọc được ("hai mươi ba tháng
  tám") thay vì "23/8" để giọng tự nhiên hơn, áp dụng cho mọi engine TTS.

## Giản lược có chủ đích

- Bỏ bước "kiểm engine sẵn sàng / cài edge-tts / omnivoice": OpenClaw không tự host engine, nhà
  cung cấp luôn sẵn sàng qua tool platform.
- Bỏ ước lượng `sec_per_1000` và ngưỡng 5 phút: không áp dụng vì không chạy model local trên máy
  người dùng.
- Bỏ `ags qa`/`ags view`-style bung file riêng: voice note gửi thẳng vào kênh chat, người dùng
  nghe ngay trong app chat, không cần lệnh mở file.

## Không làm

- Không tự dựng server TTS riêng, không cài `edge-tts`/`omnivoice`/VieNeu thủ công qua `exec` —
  dùng thẳng `message(asVoice, voiceText)` đã có sẵn trong platform.
- Không bịa ra API clone giọng không tồn tại trong OpenClaw native.
