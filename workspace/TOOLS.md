# TOOLS.md — Bảng tra nhanh lệnh `ags`

> Đặt `AGS` = đường dẫn đầy đủ tới `ags` trên máy này. Windows mặc định: `%LOCALAPPDATA%\Programs\AGS\ags.exe`.
> API host: `http://127.0.0.1:8765` (đã có `ags api` lo token). Biến môi trường quan trọng: `AGS_CONV_ID` (mã cuộc chat của bạn).

| Nhóm | Lệnh | Ghi chú |
|---|---|---|
| Khám phá | `ags help` · `ags tools` · `ags plugin <id> <action> '<json>'` | mini-app là nơi tìm trước khi tự viết script |
| Hiển thị | `ags view [--goto <mốc>] <file…>` | ảnh/video/audio/PDF/md/mã nguồn |
| | `ags sidebar dir=<top\|left\|right\|bottom> act=<show\|hide\|toggle> content=<…>` | tab phải = mỗi chat một tab |
| Chat agent | `ags chat setup` · `ags chat <conv\|token> --title "<<5 chữ>" "<lời>"` · `ags chat invite` · `ags chat --peers` | `--title` bắt buộc |
| Việc | `ags task log\|done\|fail\|get\|list <mã> "<…>"` | báo từng bước |
| Hỏi–đáp | `ags qa conv $AGS_CONV_ID [N]` · `ags qa <mã prompt>` · `ags qa boc <chat> <prompt>` · `--json` | kho local |
| Bộ nhớ | `ags mem tim "<…>"` · `snap [mã\|tên]` · `tree` · `hot "<…>"` · `save '<json>'\|--file f\|-` · `entries --topic <mã> --limit 20` · `cuoi-phien` · `xoa …` · `thung-rac` · `khoi-phuc <id>` · `counter` | `tim` trước, đừng `entries --all` trần |
| Cài đặt | `ags package install <tên>` (vd `edge-tts`, `omnivoice`) | trả `{"already":true}` hoặc `{"job":…}` |
| Ý tưởng | `ags online cat=idea prompt="<nguyên văn>"` | đừng gọi `/api/cloud/agent-jobs` |
| Cửa chung | `ags api <GET\|POST\|DELETE> <path\|URL> ['<json>']` | |
| Bài chi tiết | `ags api GET '/api/agent-prompt?name=<tên>'` với tên ∈ `ags_viral_help` `zalo_bot_help` `cf_voice_help` `ags_bemam_help` `ags_affix_help` `ags_brand_help` | bài luôn mới nhất từ host |

## Endpoint hay dùng
`/api/projects` (GET/POST) · `/api/conversations` · `/api/chat/peers` · `/api/cloud/brand[/save|/link|/delete]` · `/api/affix` ·
`/api/voice/{voices,synth,job/<id>,recent,clone,clones}` · `/api/plugins/{install,install-status}` ·
`/api/agsmem/snap` · `/api/quicknote/list` · `/reg?agent=<tên>&path=<exe>` (đăng ký CLI agent — trỏ `.exe` thật, không `.cmd`)

## Mini-app đã gặp
`zalo-bot` (Zalo cá nhân) · `zalo` (Bot Platform/OA — KHÁC) · `bemam-mini` (não gom LLM) · `browser-control` · Voice Studio (edge / omni)
