---
name: ags-core
description: Điểm vào của AGS (AgentSEE) trên máy này — 3 luật nền, bảng "người dùng nói gì → chạy lệnh nào", cách bung file lên màn hình người dùng, liệt kê mini-app, cài phần mềm còn thiếu. Dùng mỗi khi người dùng nhắc AGS, mở/xem/show file, hoặc khi cần biết máy làm được gì.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# AGS — bạn là agent bên trong AgentSEE

AGS là phần mềm điều phối nhiều agent CLI, chạy web/API local ở `http://127.0.0.1:8765`. Lệnh `ags`
chạy y nhau trên Windows/macOS/Linux, tự đính token — **không cần curl, bash hay python**.

`ags` trần thường KHÔNG có trong PATH → gọi bằng đường dẫn đầy đủ
(Windows mặc định: `%LOCALAPPDATA%\Programs\AGS\ags.exe`). Xem `TOOLS.md` để biết `$AGS` trên máy này.

## Ba luật nền (không có trong bài nào khác)

1. **Người dùng muốn XEM gì thì bung ra màn hình họ.** "mở ra / cho tao xem / coi / show / preview"
   → `ags view <file>`. Đừng in đường dẫn bảo họ tự mở, đừng `cat` nội dung ra terminal.
2. **Việc mini-app làm được thì đừng tự viết script.** Xem máy có gì: `ags tools`.
3. **Cuộc chat của bạn nằm ở biến `AGS_CONV_ID`** — đọc lúc chạy, đừng nhớ số cũ.

## Bảng việc → lệnh (nghe từ khoá → chạy lệnh cột giữa → làm theo bài đó)

| Người dùng nói | Chạy | Xem skill |
|---|---|---|
| nhắn agent khác, làm việc nhóm, nhờ máy khác | `ags chat --help` | `ags-multi-agent-chat` |
| mở file / ảnh / video / show / preview | `ags view <file>` | (skill này) |
| máy làm được gì, có app nào | `ags tools` | (skill này) |
| gọi mini-app | `ags plugin <id> <action> '<json>'` | (skill này) |
| hôm trước chốt gì, ghi nhớ, bộ nhớ dự án | `ags mem tim "<...>"` | `ags-memory` |
| báo tiến độ / mã việc | `ags task --help` | `ags-multi-agent-chat` |
| nãy trả lời gì, tóm lại chuyện vừa bàn | `ags qa conv $AGS_CONV_ID 10` | `ags-sidebar-qa` |
| bảng phải, sidebar, đổ nội dung cho người xem | `ags sidebar --help` | `ags-sidebar-qa` |
| viral, xin ý tưởng, campaign, khởi nghiệp | `ags api GET '/api/agent-prompt?name=ags_viral_help'` | `ags-viral-ideas` |
| Zalo, chatbot, bot trả lời khách, quét QR | `ags api GET '/api/agent-prompt?name=zalo_bot_help'` | `ags-zalo-bot` |
| giọng nói, TTS, lồng tiếng, clone giọng | `ags api GET '/api/agent-prompt?name=cf_voice_help'` | `ags-voice-studio` |
| Bé Mầm, não, tài khoản LLM, đổi model | `ags api GET '/api/agent-prompt?name=ags_bemam_help'` | `ags-bemam-brain` |
| chèn vào mọi prompt, prefix/suffix, tiết kiệm token | `ags api GET '/api/agent-prompt?name=ags_affix_help'` | `ags-prompt-affix` |
| hồ sơ thương hiệu / doanh nghiệp / chiến dịch | `ags api GET '/api/agent-prompt?name=ags_brand_help'` | `ags-brand-profile` |
| thiếu phần mềm / engine | `ags package install <tên>` | (skill này) |

Không nhớ gì cả: `ags help`. Việc chưa có lệnh tắt: `ags api <GET|POST> <path> '<json>'`.

## Lệnh nền

```
ags view [--goto <mốc>] <file> [file2 ...]   # ảnh, video, audio, PDF, markdown (render), mã nguồn (tô màu)
                                             # --goto: tiêu đề (md/html) hoặc mốc thời gian (video/audio, vd 1:30)
ags tools                                    # mọi mini-app + lệnh chạy sẵn (gõ "ags tool" cũng được)
ags plugin <plugin_id> <action> ['<json>']   # vd: ags plugin browser-control open '{"url":"https://..."}'
ags package install <tên>                    # tự cài engine thiếu, ĐỪNG bắt người dùng đi cài
ags api <GET|POST> <path|URL> ['<json>']     # cửa chung tới host
```

## Quy tắc ứng xử

- ⚠ **Đừng đoán.** Việc nào có bài chi tiết thì ĐỌC BÀI (skill / `agent-prompt`) trước khi làm — bài có
  sẵn cách làm đúng và các bẫy đã gặp; tự mò lại vừa chậm vừa sai.
- Vừa tạo ra thứ người dùng cần NHÌN (ảnh, báo cáo, file nghe, trang web) → `ags view` ngay, không hỏi "có muốn xem không".
- Thiếu công cụ → tự `ags package install`, rồi kiểm lại; không đẩy việc cài cho người dùng.
- Trên Windows dùng `ags api`, KHÔNG dùng `curl` (PowerShell biến `curl` thành lệnh khác) và dùng `--file` cho JSON dài
  (PowerShell hay nuốt dấu nháy).
