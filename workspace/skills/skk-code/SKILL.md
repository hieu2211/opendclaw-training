---
name: skk-code
description: "Điều phối tính năng lớn qua 3 vai subagent (Planner/Debater/Coder) với 1 file plan-<slug>.md làm nguồn sự thật. Kích hoạt khi người dùng nói: ags code, lên plan rồi code, planner coder, lập plan để code tính năng."
---

# skk-code — Điều phối Planner → Debater → Coder

Bản chất AGS `ags code` giữ lại: 3 vai cố định, debate theo mức độ việc, 1 nguồn
sự thật cho plan, vai nhận việc không hỏi lại, điều phối không tự code.
Khác AGS: dùng subagent OpenClaw thật (`sessions_spawn`/`sessions_send`/
`sessions_yield`/`subagents`) thay vì app chat riêng + convid + form popup.

## Workflow

1. **Hiểu việc & chốt mức độ.**
   Tóm tắt việc cần làm trong 1-2 câu. Hỏi thẳng trong chat (không có form):
   `"Việc này mức Nhỏ / Trung bình / Lớn? (gợi ý: <mức đề xuất dựa trên quy mô>)"`.
   Mức quyết số vòng debate: Nhỏ=0, Trung bình=1, Lớn=3. Việc chạm bảo mật/auth
   luôn tối thiểu 1 vòng debate dù mức Nhỏ.
   **Done when:** đã có slug (kebab-case, vd `fix-login-timeout`) và mức độ.

2. **Khởi tạo file plan.**
   `exec`: tạo `plan-<slug>.md` ở gốc dự án (cwd phiên hiện tại, hoặc thư mục
   người dùng chỉ định) với khung:
   ```
   # Plan: <slug>
   ## Bối cảnh
   ## Mức độ
   ## Plan
   ## Nghiệm thu
   ## Lịch sử
   ```
   **Done when:** file tồn tại, đã điền Bối cảnh + Mức độ.

3. **Spawn Planner.**
   ```json
   sessions_spawn({
     "task": "Lên plan cho: <mô tả việc>. Đọc/ghi trực tiếp file <path>/plan-<slug>.md bằng exec, điền mục Plan (các bước cụ thể, file sẽ đụng, rủi ro) và append vào Lịch sử. Mức độ: <mức>. KHÔNG hỏi lại người dùng — nếu thiếu thông tin, liệt kê câu hỏi ở cuối báo cáo trả về.",
     "taskName": "<slug>_planner",
     "label": "<slug>-Planner",
     "context": "isolated",
     "visible": false
   })
   ```
   Giữ lại `childSessionKey` trả về — dùng lại cho các lần sửa plan ở bước 4.
   `sessions_yield` chờ kết quả nếu cần (không busy-poll).
   **Done when:** Planner báo xong, mục Plan trong file có nội dung.

4. **Debate (bỏ qua nếu mức Nhỏ & không chạm bảo mật).** Lặp N vòng (Lớn=3,
   Trung bình=1):
   - Spawn Debater đọc file, soi plan, không sửa file — chỉ trả phản biện:
     ```json
     sessions_spawn({
       "task": "Đọc plan-<slug>.md tại <path>. Phản biện: thiếu bước, rủi ro, sai tiếp cận, test case bỏ sót. KHÔNG sửa file. Trả danh sách góp ý ngắn gọn trong kết quả.",
       "taskName": "<slug>_debate_<n>",
       "label": "<slug>-Debater-<n>",
       "context": "isolated",
       "visible": false
     })
     ```
   - Gửi góp ý cho Planner sửa, dùng lại session Planner (không respawn mất ngữ cảnh):
     ```json
     sessions_send({
       "sessionKey": "<childSessionKey của Planner>",
       "message": "Sửa plan-<slug>.md theo góp ý: <tóm tắt góp ý>. Append vào Lịch sử.",
       "mode": "followup"
     })
     ```
   **Done when:** đã chạy đủ N vòng, Lịch sử có mục ghi từng vòng debate.

5. **Duyệt plan với người dùng.** Tóm tắt plan (không dán nguyên file), hỏi
   thẳng: `"Duyệt plan này để code không? (OK / sửa chỗ nào)"`. Nếu sửa, quay
   lại bước 3/4 với `sessions_send` tới Planner.
   **Done when:** người dùng xác nhận OK.

6. **Spawn Coder.**
   ```json
   sessions_spawn({
     "task": "Code theo đúng plan sau (toàn văn từ plan-<slug>.md):\n<nội dung mục Plan>\n\nSau khi code xong: tự chạy test/kiểm tra liên quan, ghi kết quả + evidence vào mục Nghiệm thu của <path>/plan-<slug>.md. KHÔNG hỏi lại — nếu bí, liệt kê blocker trong báo cáo trả về.",
     "taskName": "<slug>_coder",
     "label": "<slug>-Coder",
     "context": "isolated",
     "visible": false
   })
   ```
   **Done when:** Coder báo xong, mục Nghiệm thu có kết quả test thật (không phải lời hứa).

7. **Duyệt nghiệm thu & báo người dùng.** Đọc mục Nghiệm thu, xác nhận có
   bằng chứng thật (log test, output lệnh) rồi mới báo người dùng là xong.
   Không tự coi "đã code xong" là đủ nếu thiếu bằng chứng chạy được.
   **Done when:** đã báo người dùng kèm tóm tắt + đường dẫn `plan-<slug>.md`.

## Luật cứng (giữ từ AGS)

- Subagent (Planner/Debater/Coder) **không được hỏi lại người dùng** — đầu
  kia không ai bấm trả lời. Thiếu gì thì liệt kê câu hỏi trong kết quả trả
  về cho điều phối xử lý.
- Điều phối (agent đang chat) **không tự lên plan, không tự code** — chỉ
  điều phối, duyệt plan, duyệt nghiệm thu.
- `plan-<slug>.md` là nguồn sự thật DUY NHẤT — mọi vai đọc/ghi qua `exec`,
  không có hệ thống convid/manifest riêng.

## Giản lược có chủ đích so với AGS gốc

- Không có "model_tier" chọn CLI khác nhau mỗi vai → dùng `model` param của
  `sessions_spawn` khi cần override model cho 1 vai cụ thể.
- Không có ask-mode riêng theo vai, không có form popup → hỏi thẳng trong
  chat với gợi ý mặc định.
- Không có app/conv_id riêng → `sessions_spawn` tự quản lý định danh session,
  `taskName`/`label` đủ để theo dõi trong `subagents` list.
