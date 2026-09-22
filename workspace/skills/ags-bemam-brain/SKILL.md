---
name: ags-bemam-brain
description: Quản Bé Mầm Mini — mini-app "não" gom nhiều tài khoản LLM (Google/Antigravity, Claude, Codex, xAI, Kimi…) + kho API key, xoay vòng round-robin, dùng như một agent trong AGS. Dùng khi người dùng hỏi "Bé Mầm", "não", tài khoản LLM, đổi model, API key.
metadata: {"openclaw":{"requires":{"bins":["ags"]}}}
---

# Bé Mầm Mini — hỏi gì thì chạy lệnh, đừng đoán

Mini-app `bemam-mini`: proxy gom nhiều tài khoản LLM + kho API key, xoay vòng round-robin, dùng như một agent trong AGS.
Người dùng hỏi tới thì **HỎI THẲNG NÓ**:

```
ags plugin bemam-mini status         # não chạy chưa, cổng nào, model gì
ags plugin bemam-mini accounts       # kho tài khoản đã đăng nhập (email · provider · hạn)
ags plugin bemam-mini models         # model dùng được + model đang chọn
ags plugin bemam-mini model_set '{"model":"gemini-3.1-flash-lite"}'
ags plugin bemam-mini apikeys        # kho API key + provider nhận key (có OpenRouter)
ags plugin bemam-mini login_start '{"provider":"antigravity"}'      # rồi login_status lấy link
```

Còn: `install` / `install_status` / `uninstall` · `service '{"op":"restart"}'` · `apikey_add` / `apikey_delete` ·
`account_delete` · `optimize_get` / `optimize_set`.

⚠ Đăng nhập tài khoản mới phải mở link **TRÊN MÁY CHẠY NÃO** (callback về localhost máy đó) — dùng `open_url`; đừng đưa
link cho người ở máy khác bấm.
