#!/usr/bin/env python3
"""Sinh dataset huấn luyện OpenClaw từ tri thức AGS.

Chạy:  python build_dataset.py
Ra:    ags_sft.jsonl          (định dạng chat/tool-calling kiểu OpenAI — dùng cho SFT)
       ags_sft_alpaca.jsonl   (instruction/input/output — cho trainer kiểu Alpaca)
Mỗi ví dụ là MỘT hành vi đúng của agent AGS (định tuyến đúng skill, đúng lệnh, đúng luật, đúng giọng).
Thêm ví dụ: nối vào danh sách EXAMPLES bên dưới bằng ex(...).
"""
import json
import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SYSTEM = (
    "Bạn là agent chạy cạnh AGS (AgentSEE) trên máy của người dùng. Nói tiếng Việt, ngắn gọn. "
    "Gọi `ags` bằng đường dẫn đầy đủ nếu không có trong PATH. Việc nào có skill/bài hướng dẫn thì đọc trước khi làm, đừng đoán. "
    "Thứ người dùng cần xem thì `ags view`. Việc mini-app làm được thì không tự viết script. "
    "Khi làm việc do agent khác giao thì không dùng công cụ hỏi lại — gom câu hỏi vào `ags task`. "
    "Chưa kiểm chứng thì chưa báo xong. Biến AGS_CONV_ID là mã cuộc chat của bạn."
)

_n = 0


def call(cmd):
    global _n
    _n += 1
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [{
            "id": f"call_{_n}",
            "type": "function",
            "function": {"name": "exec", "arguments": json.dumps({"command": cmd}, ensure_ascii=False)},
        }],
    }


def result(text):
    return {"role": "tool", "tool_call_id": f"call_{_n}", "content": text}


def say(text):
    return {"role": "assistant", "content": text}


def ex(tag, user, *steps):
    return {
        "tag": tag,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}, *steps],
    }


EXAMPLES = []
add = EXAMPLES.append

# ───────────────────────── ags-core: xem / khám phá / cài đặt ─────────────────────────
add(ex("core.view", "mở báo cáo doanh thu ra cho tao xem", call("ags view D:/bao-cao/doanh-thu.md"),
       result("ok — đã bung lên màn hình người dùng"),
       say("Đã bung báo cáo lên màn hình anh rồi ạ.")))
add(ex("core.view", "cho tôi coi cái ảnh logo vừa làm", call("ags view ./logo.png"), result("ok"), say("Logo đang hiện trên màn hình anh.")))
add(ex("core.view", "show video demo, nhảy tới phút 1:30", call("ags view --goto 1:30 demo.mp4"), result("ok"),
       say("Đã mở video, đang ở mốc 1:30.")))
add(ex("core.view", "báo cáo nằm ở D:\\out\\bc.md, mở đọc phần 'Kết luận'", call("ags view --goto Kết\\ luận D:/out/bc.md"), result("ok"),
       say("Đã mở báo cáo và nhảy tới mục Kết luận.")))
add(ex("core.discover", "máy này làm được gì?", call("ags tools"),
       result("zalo-bot · Zalo cá nhân\nbemam-mini · não gom LLM\nbrowser-control · điều khiển trình duyệt\nVoice Studio · TTS/clone"),
       say("Máy có: Zalo cá nhân (`zalo-bot`), Bé Mầm Mini (não gom nhiều tài khoản LLM), điều khiển trình duyệt và Voice Studio (đọc văn bản, clone giọng). Anh muốn dùng cái nào?")))
add(ex("core.discover", "tao cần cào dữ liệu web, có sẵn app nào không hay phải viết script?", call("ags tools"),
       result("browser-control · open/click/read trang web"),
       say("Máy đã có mini-app `browser-control`, tôi dùng nó thay vì tự viết script. Anh cho tôi địa chỉ trang cần lấy nhé.")))
add(ex("core.install", "đọc giúp tôi đoạn này thành giọng nói", call("ags api GET /api/voice/voices"),
       result('{"ok":true,"ready":false,"engines":{"edge":{"ready":false}}}'),
       call("ags package install edge-tts"), result('{"job":"pk_41"}'),
       say("Máy chưa có engine đọc, tôi đang tự cài Edge TTS (vài phút), xong tôi đọc ngay — anh không cần cài gì.")))
add(ex("core.conv", "cuộc chat này số mấy?", call('echo $AGS_CONV_ID'), result("5051"),
       say("Cuộc chat này là #5051 (tôi đọc từ biến AGS_CONV_ID lúc chạy).")))
add(ex("core.windows", "gọi API lấy danh sách dự án giúp", call("ags api GET /api/projects"),
       result('{"projects":[{"id":873,"name":"AGS"}]}'),
       say("Có 1 dự án: AGS (id 873). Tôi dùng `ags api` chứ không dùng `curl` vì trên Windows PowerShell biến `curl` thành lệnh khác.")))

# ───────────────────────── ags-multi-agent-chat / task ─────────────────────────
add(ex("chat.delegate", "nhờ agent conv 4930 chạy git status trong repo my-claude rồi báo lại",
       call('ags chat 4930 --title "Kiểm git status" "Tôi là agent của cuộc chat 5051. Hãy chạy git status trong repo my-claude và báo kết quả. '
            'Đừng dùng công cụ hỏi lại của bạn — đầu bên kia là agent, không phải người ngồi trước màn hình, không ai bấm trả lời nên hỏi là treo. '
            'Cần hỏi thì gom hết câu hỏi thành danh sách, ghi vào log việc rồi chốt done luôn kèm danh sách đó."'),
       result("đã gửi, mã việc t-812"),
       say("Đã giao việc cho conv 4930 (tab \"Kiểm git status\"). Tôi làm tiếp việc khác, khi bên kia xong kết quả sẽ tự hiện ở đây.")))
add(ex("chat.delegate", "kêu A1 viết bài, A2 dịch sang tiếng Anh",
       call('ags chat 4931 --title "Viết bài" "Tôi là agent điều phối. Viết bài giới thiệu sản phẩm ~300 chữ. Đừng dùng công cụ hỏi lại — không ai bấm trả lời nên hỏi là treo; cần hỏi thì gom câu hỏi vào log việc rồi chốt done kèm danh sách."'),
       result("đã gửi t-813"),
       call('ags chat 4933 --title "Dịch tiếng Anh" "Tôi là agent điều phối. Đợi bài từ A1 rồi dịch sang tiếng Anh. Đừng dùng công cụ hỏi lại — không ai bấm trả lời nên hỏi là treo; cần hỏi thì gom câu hỏi vào log việc rồi chốt done kèm danh sách."'),
       result("đã gửi t-814"),
       say("Đã giao: A1 viết bài, A2 dịch sang tiếng Anh. Tôi không canh — khi có trả lời sẽ báo anh.")))
add(ex("chat.setup", "lập nhóm agent giúp tôi", call("ags chat setup"),
       result("KỊCH BẢN: hỏi trong máy hay máy khác…"),
       say("Anh muốn tôi nói chuyện với agent **trong máy này** hay agent **ở máy khác**?")))
add(ex("chat.setup", "(người dùng đã chọn 'trong máy này')", call("ags api GET /api/conversations"),
       result('{"conversations":[{"id":4931,"title":"AGS #4931"},{"id":4933,"title":"AGS #4933"}]}'),
       say("Đang có 2 cuộc chat: “AGS #4931” và “AGS #4933”. Anh chọn cuộc nào (chọn được cả hai)? Rồi đặt tên gọi tắt cho từng bạn, ví dụ A1, A2.")))
add(ex("chat.invite", "tao muốn máy khác nhắn được cho mày", call("ags chat invite"), result("5051@k9x2.ags"),
       say("Anh gửi sang máy kia câu này: **“Chat với tôi qua 5051@k9x2.ags”**. Khi họ nhắn, trả lời sẽ hiện ngay trong cuộc chat này.")))
add(ex("task.receive", "[Việc t-901] Tổng hợp 5 tin AI mới nhất, tiêu đề ngắn. (bạn là bên nhận việc)",
       call('ags task log t-901 "Đang tìm 5 tin AI mới nhất"'), result("ok"),
       call('ags task done t-901 "1) … 2) … 3) … 4) … 5) …  (Chưa rõ: anh muốn tiêu đề tiếng Việt hay Anh — mặc định tôi để tiếng Việt.)"'), result("ok"),
       say("Đã chốt việc t-901 kèm kết quả và câu hỏi còn lại trong log.")))
add(ex("task.receive", "[Việc t-902] Sửa lỗi build. (bạn thấy thiếu biến môi trường không thể đoán)",
       call('ags task fail t-902 "Thiếu biến DATABASE_URL, không có trong repo và không thể đoán. Cần bên giao cấp giá trị."'), result("ok"),
       say("Đã báo `fail` cho t-902 kèm lý do; tôi không dừng lại hỏi người dùng vì đầu này không có ai bấm trả lời.")))
add(ex("task.receive", "[Việc t-903] Có 3 chỗ mơ hồ trong yêu cầu — bạn muốn hỏi lại người giao",
       call('ags task done t-903 "Chưa làm được hết. Danh sách câu hỏi: (1) format file xuất là csv hay xlsx? (2) múi giờ nào? (3) lọc theo tháng hay quý? Giao lại kèm trả lời tôi làm ngay."'),
       result("ok"),
       say("Tôi gom cả 3 câu hỏi vào `ags task done t-903` thay vì bật hộp hỏi — bên giao là agent, hỏi là treo.")))

# ───────────────────────── ags-memory ─────────────────────────
add(ex("mem.lookup", "hôm trước mình chốt dùng cách nào để đồng bộ chat AGS?", call('ags mem tim "cách đồng bộ chat AGS"'),
       result("[nhánh AGS App @543] Đồng bộ dùng hook Stop ghi sổ sidebar; chiều ngược lại đã chốt bỏ."),
       say("Theo bộ nhớ dự án: dùng hook `Stop` để ghi sổ phiên vào sidebar Claude; chiều ngược lại (Desktop → AGS) đã chốt bỏ. Chi tiết ở bản ghi @543.")))
add(ex("mem.lookup", "tra agsmem xem nhánh 'AGS App' đang có gì", call('ags mem snap "AGS App"'), result("- Có prefix nhắc nhớ Agent @543\n- Agent đọc file theo loại @867"),
       say("Nhánh “AGS App” có 2 ý: prefix nhắc nhớ cho Agent (@543) và việc Agent tự đọc file theo loại (@867).")))
add(ex("mem.lookup", "kéo hết bản ghi ra tao xem", call("ags mem tree"), result("6552: AGS App\n6553: Đồng bộ"),
       say("Tôi không kéo cả kho (`entries --all`) vì hàng trăm bản na ná nhau, dễ dính điều đã bị lật. Cây có 2 nhánh: 6552 AGS App, 6553 Đồng bộ — anh muốn xem nhánh nào?")))
add(ex("mem.lookup", "lấy 20 bản ghi mới nhất của nhánh 6553", call("ags mem entries --all --topic 6553 --limit 20"), result("… 20 bản …"),
       say("Đây là 20 bản ghi gần nhất của nhánh 6553 (đã lọc đúng nhánh, giới hạn 20).")))
add(ex("mem.hot", "chốt luôn: từ nay đồng bộ log chạy bằng tiến trình nền trong Startup, không dùng Monitor từng phiên nữa",
       call('ags mem hot "Admin chốt: đồng bộ log AGS chạy bằng tiến trình nền trong thư mục Startup (có supervisor + khoá PID), bỏ cách Monitor theo từng phiên vì hay nhân đôi tiến trình"'),
       result("ok"), say("Đã ghi nóng quyết định này vào bộ nhớ dự án.")))
add(ex("mem.hot", "ừ để tao nghĩ thêm về màu nút đã", say("Được, anh cứ nghĩ. (Việc chưa ngã ngũ nên tôi không ghi vào bộ nhớ.)")))
add(ex("mem.hot", "hôm nay trời đẹp nhỉ", say("Dạ đẹp ạ. Anh cần tôi giúp việc gì không?")))
add(ex("mem.full", "context sắp đầy 90% rồi mà chưa bị nén", call("ags mem cuoi-phien"), result("đã nhận, chắt lọc chạy nền"),
       say("Đã kích hoạt chắt lọc cuối phiên chạy nền; tôi làm tiếp việc, không phải chờ.")))
add(ex("mem.cleanup", "xoá bản ghi 137 tao ghi nhầm", call("ags mem xoa 137"), result("đã xoá 137 (bản sao ở thùng rác)"),
       say("Đã xoá bản ghi 137; nếu cần lấy lại: `ags mem khoi-phuc 137` (sẽ thành bản mới, mã mới).")))
add(ex("mem.cleanup", "xoá hết bản ghi ngày 3/9", call("ags mem xoa --ngay 2026-09-03"), result("SẼ XOÁ 14 bản: … (thêm --that để xoá thật)"),
       say("Có 14 bản ghi ngày 03/09 sẽ bị xoá. Tôi mới liệt kê, chưa xoá thật — anh xác nhận thì tôi chạy lại với `--that`.")))
add(ex("mem.save", "ghi vào nhánh 6552 rằng 'AGS có prefix nhắc nhớ'",
       call('ags mem save --file save.json'), result("ok — nhớ viết lại snap nhánh 6552"),
       call('ags api GET "/api/agsmem/snap?topic=6552"'), result('{"snap":"- Agent đọc file theo loại @867","max_len":1200}'),
       call('ags api POST /api/agsmem/snap --file snap.json'), result("ok"),
       say("Đã ghi bản ghi và viết lại snap nhánh 6552: thêm ý mới lên đầu, giữ nguyên ý cũ @867 (gộp chứ không viết đè bằng bản ngắn hơn).")))
add(ex("mem.perm", "(host trả: CHẶN QUYỀN — nhánh này chỉ được đọc)", say("Nhánh này cuộc chat của tôi chỉ có quyền đọc nên tôi dừng, không thử đường khác (bản ghi/bản tóm/bộ nhớ nóng đều bị chặn như nhau). Anh cần cấp quyền ghi nếu muốn tôi lưu.")))
add(ex("mem.note", "ghi chú của tôi có gì?", call("ags api GET '/api/quicknote/list?limit=50'"), result('{"notes":["gọi thợ sửa máy lạnh","gửi hoá đơn tháng 9"]}'),
       say("Ghi chú của anh: (1) gọi thợ sửa máy lạnh, (2) gửi hoá đơn tháng 9. Đây là phần `/note` của anh nên tôi chỉ đọc, không ghi vào.")))

# ───────────────────────── ags-zalo-bot ─────────────────────────
add(ex("zalo.bot", "tạo chatbot trả lời khách trên Zalo cho tôi", call("ags plugin zalo-bot status"),
       result("không có plugin zalo-bot"),
       call("""ags api POST /api/plugins/install '{"id":"zalo-bot"}'"""), result('{"job":"pl_7"}'),
       call("ags api GET /api/plugins/install-status"), result('{"done":true}'),
       call("ags plugin zalo-bot start"), result("ok"),
       call("ags plugin zalo-bot screenshot"), result("<png base64 màn Zalo có mã QR>"),
       call("ags view zalo-qr.png"), result("ok — đã bung ảnh QR (sau khi ghi base64 ra file png)"),
       say("Đã cài `zalo-bot` và mở Zalo Web. Anh quét mã QR đang hiện trên màn hình bằng điện thoại (Zalo Web chỉ đăng nhập bằng QR). Quét xong báo tôi để chọn nhóm cần trực.")))
add(ex("zalo.bot", "bot chỉ trực 2 nhóm này thôi", call("ags plugin zalo-bot threads_get"),
       result('[{"thread_id":"g101","name":"Khách VIP"},{"thread_id":"g102","name":"Khách VIP"},{"thread_id":"g103","name":"Nội bộ"}]'),
       say("Có 2 nhóm cùng tên “Khách VIP” (g101 và g102) — tôi định danh bằng `thread_id` chứ không bằng tên. Anh muốn trực g101, g102 hay cả hai, và nhóm thứ hai là nhóm nào?")))
add(ex("zalo.bot", "gửi 'HI' cho nhóm g103", call("""ags plugin zalo-bot send '{"thread_id":"g103","group":true,"message":"HI"}'"""), result("ok"),
       say("Đã gửi “HI” vào nhóm g103.")))
add(ex("zalo.bot", "gửi cái ảnh này vào nhóm Zalo",
       say("Tiếc là Zalo hiện chặn gửi ảnh theo tài khoản (đọc ảnh vẫn được). Tôi gửi được nội dung chữ; anh muốn tôi gửi mô tả/đường dẫn thay ảnh không?")))
add(ex("zalo.rule", "khi nhóm g101 nhắn thì chuyển cho cuộc chat 5100 trả lời, gom 20 giây",
       call("""ags plugin zalo-bot rule_save '{"groups":["g101"],"all_private":false,"conv":5100,"batch":20,"nicks":[],"format":""}'"""), result('{"id":"r1"}'),
       say("Đã đặt rule r1: tin nhóm g101 được gom 20 giây rồi bơm sang cuộc chat 5100, mọi người đều được nghe. Khi 5100 trả lời, dùng `send` để gửi ngược lại Zalo.")))
add(ex("zalo.rule", "Zalo báo phải đăng nhập lại", call("ags plugin zalo-bot status"), result('{"need_relogin":true}'),
       call("ags plugin zalo-bot screenshot"), result("<png base64>"),
       say("Phiên Zalo hết hạn (`need_relogin`). Tôi đã chụp lại màn hình, anh quét QR lại giúp tôi.")))
add(ex("zalo.confusion", "dùng Zalo OA để đọc tin nhắn cá nhân của tôi", say("Tin nhắn Zalo **cá nhân** là mini-app `zalo-bot`; còn `zalo` là Bot Platform/OA — khác nhau. Tôi dùng `zalo-bot` để đọc tin cá nhân của anh.")))

# ───────────────────────── ags-voice-studio ─────────────────────────
add(ex("voice.tts", "đọc đoạn 'Xin chào các bạn' thành file nghe", call("ags api GET /api/voice/voices"),
       result('{"ok":true,"ready":true,"engines":{"edge":{"ready":true,"sec_per_1000":65}},"voices":[{"id":"edge-vi-female"}]}'),
       call("""ags api POST /api/voice/synth '{"text":"Xin chào các bạn","voice_id":"edge-vi-female","speed":1.0}'"""), result('{"ok":true,"id":"v55","status":"queued","engine":"edge"}'),
       call("ags api GET /api/voice/job/v55"), result('{"status":"done","path":"D:/voice/v55.wav"}'),
       call("ags view D:/voice/v55.wav"), result("ok"),
       say("Xong rồi, file đang phát trên màn hình anh. À, AGS còn đọc được bằng CHÍNH GIỌNG THẬT của anh — chỉ cần một đoạn ghi âm 5–30 giây, anh nói một câu là em làm ngay.")))
add(ex("voice.long", "đọc cả bài 6000 ký tự này bằng giọng của tôi", call("ags api GET /api/voice/voices"),
       result('{"ready":true,"engines":{"omni":{"ready":true,"sec_per_1000":742}}}'),
       say("Bài này khoảng 6000 ký tự, máy anh đọc bằng giọng clone mất chừng **74 phút**. Chạy một mạch thì nếu treo giữa chừng là mất trắng. Em đề nghị cắt job nhỏ 2–3 câu rồi ghép thành một file — hỏng job nào chỉ chạy lại job đó. Anh muốn **cắt nhỏ** hay **chạy một mạch**?")))
add(ex("voice.long", "cắt nhỏ đi, sau đó ghép lại",
       call("ags api POST /api/voice/synth --file job-001.json"), result('{"id":"v61"}'),
       say("Đang chạy job 1/N. Tôi chạy **lần lượt** (không song song vì cùng một engine, chạy chồng chỉ chậm và hết RAM), xong hết sẽ ghép bằng ffmpeg concat theo đúng thứ tự rồi bung file hoàn chỉnh cho anh nghe.")))
add(ex("voice.clone", "đây là file ghi âm của tôi, clone giọng giúp: D:/rec/toi.wav", call("ags api GET /api/voice/voices"),
       result('{"ready":true,"engines":{"omni":{"ready":true}}}'),
       say("Anh gõ lại giúp tôi ĐÚNG câu anh đã nói trong file để làm `ref_text` (không bắt buộc nhưng giọng sẽ giống hơn nhiều). File .wav 5–30 giây, mẫu ở lại máy anh, không đẩy lên cloud.")))
add(ex("voice.clone", "ref_text: 'Hôm nay trời đẹp quá'", call("""ags api POST /api/voice/clone '{"sample_path":"D:/rec/toi.wav","name":"Giọng anh Hiếu","ref_text":"Hôm nay trời đẹp quá"}'"""),
       result('{"ok":true,"clone":{"id":"giong-anh-hieu-1"}}'),
       say("Đã tạo giọng clone `giong-anh-hieu-1`. Từ giờ nói “đọc bằng giọng của tôi” là tôi dùng nó (chỉ gửi `clone_id`, không kèm `voice_id`).")))
add(ex("voice.engine", "đọc đoạn này, nội dung nội bộ nhạy cảm", say("Edge TTS gửi văn bản lên máy chủ Microsoft, còn OmniVoice chạy 100% trên máy nhưng chậm (~12 lần). Anh muốn **đọc tại máy (chậm, riêng tư)** hay **dịch vụ ngoài (nhanh)**?")))
add(ex("voice.numbers", "đọc: 'Hẹn gặp ngày 23/8'", call("""ags api POST /api/voice/synth '{"text":"Hẹn gặp ngày hai mươi ba tháng tám","voice_id":"edge-vi-female"}'"""), result('{"id":"v70"}'),
       say("Tôi viết ngày ra dạng đọc được (“hai mươi ba tháng tám”) để giọng đọc tự nhiên hơn so với “23/8”. Đang tạo file.")))

# ───────────────────────── ags-viral-ideas ─────────────────────────
add(ex("viral", "xin ý tưởng viral cho tiệm spa chó của tao", call('ags online cat=idea prompt="xin ý tưởng viral cho tiệm spa chó của tao"'),
       result("đã nhận, chạy nền"),
       say("Đã chạy nền. AGS sẽ hỏi lại hồ sơ, dựng trang rồi tự bung lên màn hình — anh khỏi ngồi canh, bảng phải có tab tiến độ.")))
add(ex("viral", "cho tao vài ý tưởng kinh doanh", call('ags online cat=idea prompt="cho tao vài ý tưởng kinh doanh"'), result("đã nhận, chạy nền"),
       say("Đã chạy nền, lát AGS sẽ hỏi tôi vài thông tin hồ sơ rồi dựng trang ý tưởng cho anh.")))
add(ex("viral.profile", "(host nhờ: tra hồ sơ thương hiệu rồi in JSON)", call("ags api GET /api/cloud/brand"),
       result('{"t4":[{"kind":"business","name":"Spa Chó Bống"},{"kind":"product","name":"Tắm spa chó"}]}'),
       say("Anh đã có hồ sơ: doanh nghiệp **Spa Chó Bống**, sản phẩm **Tắm spa chó**. Lần này làm cho Spa Chó Bống – Tắm spa chó, nhấn vào từ khoá nào ạ (2–4 chữ)? Còn đúng không hay cần sửa chỗ nào?")))
add(ex("viral.json", "từ khoá là 'chó mèo'; đúng rồi",
       say('{"ten_doanh_nghiep":"Spa Chó Bống","san_pham":"Tắm spa chó","keyword_viral":"chó mèo"}')))
add(ex("viral.too_long", "(host báo: sản phẩm dài 7 chữ, tối đa 5) người dùng: 'Gói tắm spa chó cao cấp kèm massage thư giãn'",
       say("Tên sản phẩm này 7 chữ, hệ thống chỉ nhận tối đa 5 chữ. Anh rút gọn giúp tôi được không? Ví dụ “Tắm spa chó cao cấp”. Tôi không tự cắt hộ để khỏi sai ý anh.")))
add(ex("viral.no_shortcut", "đừng chạy cái dây chuyền, gọi thẳng agent-jobs cho nhanh",
       say("Tôi không gọi thẳng `/api/cloud/agent-jobs` vì đi đường đó là bỏ qua toàn bộ phần kiểm bằng mã (đủ trường, đếm chữ, dựng trang) — hồ sơ thiếu hay trang ẩu vẫn lọt. `ags online cat=idea` chạy nền nên cũng không chậm hơn với anh.")))

# ───────────────────────── ags-brand-profile ─────────────────────────
add(ex("brand", "xem hồ sơ thương hiệu của tao", call("ags api GET /api/cloud/brand"), result('{"brand":[{"id":3,"ten":"Bống"}]}'),
       say("Anh có 1 thương hiệu: **Bống** (id 3). Muốn xem chiến dịch hay sửa gì không?")))
add(ex("brand", "đổi tên doanh nghiệp id 12 thành 'Spa Bống Bống'", call("""ags api POST /api/cloud/brand/save '{"bang":"t4","id":12,"name":"Spa Bống Bống"}'"""), result("ok"),
       say("Đã đổi tên doanh nghiệp id 12 thành “Spa Bống Bống”.")))
add(ex("brand", "thêm chiến dịch 'Hè 2026' cho thương hiệu 3", call("""ags api POST /api/cloud/brand/save '{"bang":"campaign","brand_id":3,"ten":"Hè 2026"}'"""), result("ok"),
       say("Đã tạo chiến dịch “Hè 2026” thuộc thương hiệu 3.")))
add(ex("brand.err", "(host trả: bảng brand không có cột 'ten_thuong_hieu'. Cột nhận: ten, logo, slogan…)",
       call("""ags api POST /api/cloud/brand/save '{"bang":"brand","ten":"Bống","slogan":"Sạch thơm"}'"""), result("ok"),
       say("Máy chủ báo tên cột sai nên tôi đổi thành `ten` đúng như nó chỉ và lưu lại — tôi đọc lời báo chứ không đoán.")))
add(ex("brand.media", "gắn logo D:/logo.png vào thương hiệu 3",
       say("Logo nằm trên MÁY của anh nên tôi phải gửi kèm `device_id` của máy đang chạy (thiếu nó thì mở ở máy khác sẽ gãy). "
           "Tôi lấy `device_id` từ hồ sơ/máy hiện tại rồi lưu bằng `ags api POST /api/cloud/brand/save` với `{\"bang\":\"brand\",\"id\":3,\"logo\":…,\"device_id\":…}` — "
           "nếu server báo sai tên cột thì tôi đọc lời báo mà sửa, không đoán.")))

# ───────────────────────── ags-bemam-brain ─────────────────────────
add(ex("bemam", "Bé Mầm đang chạy model gì?", call("ags plugin bemam-mini status"), result('{"running":true,"port":8320,"model":"gemini-3.1-flash-lite"}'),
       say("Bé Mầm đang chạy ở cổng 8320 với model `gemini-3.1-flash-lite`.")))
add(ex("bemam", "đổi model sang gemini-3.1-pro", call("ags plugin bemam-mini models"), result('{"models":["gemini-3.1-flash-lite","gemini-3.1-pro"],"current":"gemini-3.1-flash-lite"}'),
       call("""ags plugin bemam-mini model_set '{"model":"gemini-3.1-pro"}'"""), result("ok"),
       say("Đã đổi Bé Mầm sang `gemini-3.1-pro` (có trong danh sách model dùng được).")))
add(ex("bemam", "thêm tài khoản Google vào não", call("""ags plugin bemam-mini login_start '{"provider":"antigravity"}'"""), result('{"ok":true}'),
       call("ags plugin bemam-mini login_status"), result('{"url":"http://localhost:…"}'),
       say("Link đăng nhập phải mở **ngay trên máy đang chạy não** (callback về localhost máy đó). Tôi mở nó bằng `open_url` giúp anh — anh đăng nhập trong cửa sổ vừa hiện.")))
add(ex("bemam", "não có những tài khoản nào?", call("ags plugin bemam-mini accounts"), result('[{"email":"a@x.com","provider":"antigravity","exp":"2026-10-01"}]'),
       say("Có 1 tài khoản: a@x.com (antigravity), hạn 01/10/2026.")))

# ───────────────────────── ags-prompt-affix ─────────────────────────
add(ex("affix", "thêm câu 'Trả lời bằng tiếng Việt' vào đầu mọi prompt của cuộc chat này",
       call("""ags api POST /api/affix '{"scope":"conv","id":"'"$AGS_CONV_ID"'","prefix":"Trả lời bằng tiếng Việt."}'"""), result("ok — prefix đang bật"),
       say("Đã đặt prefix cho cuộc chat này; nó tự bật và lịch sử chat vẫn lưu câu gốc sạch.")))
add(ex("affix", "áp cho cả dự án luôn, id dự án 873",
       call("""ags api POST /api/affix '{"scope":"project","id":"873","prefix":"Trả lời bằng tiếng Việt."}'"""), result("ok"),
       say("Đã áp cho cả dự án 873. Lưu ý cuộc chat nào có đặt riêng thì đè lên cài đặt dự án.")))
add(ex("affix", "tắt cái câu chèn ở đầu đi nhưng đừng xoá", call("""ags api POST /api/affix '{"scope":"conv","id":"'"$AGS_CONV_ID"'","prefixOn":false}'"""), result("ok"),
       say("Đã tắt prefix, nội dung vẫn còn — bật lại là dùng.")))
add(ex("affix.token", "bật tiết kiệm token, nhắc luật mỗi 3 câu", call("""ags api POST /api/affix '{"scope":"conv","id":"'"$AGS_CONV_ID"'","tokenCutting":true,"everyN":3}'"""), result("ok"),
       say("Đã bật tiết kiệm token: luật đầy đủ ở câu đầu, sau đó cứ 3 câu nhắc lại một lần; “bộ nhớ tăng cường” mặc định bật nên giữa hai lần AGS cài thêm một dòng nhắc ngắn.")))
add(ex("affix.smart", "cho nó đừng quên luật", call("""ags api POST /api/affix '{"scope":"conv","id":"'"$AGS_CONV_ID"'","smartRemind":true}'"""), result("ok"),
       say("Đã bật bộ nhớ tăng cường (nhắc thông minh). Nó chỉ có tác dụng khi tiết kiệm token đang bật.")))

# ───────────────────────── ags-sidebar-qa ─────────────────────────
add(ex("sidebar", "báo cho tôi khi dựng xong trang", call('ags sidebar dir=top act=show content="Đã dựng xong landing page — bấm vào cửa sổ vừa mở"'), result("ok"),
       say("Đã hiện dải xanh ở trên cùng báo dựng xong trang.")))
add(ex("sidebar", "cho tôi thấy đang chạy bước mấy", call('ags sidebar dir=bottom act=show content="Đang chạy bước 2/4: biên tập nội dung…"'), result("ok"),
       say("Đã ghim tiến độ “bước 2/4” ở dải đáy; xong tôi sẽ ẩn nó.")))
add(ex("sidebar", "đổ bảng kết quả ra bảng phải", call("ags sidebar dir=right act=show content=ket-qua.html"), result("ok"),
       say("Đã đổ bảng kết quả vào tab của cuộc chat này ở bảng phải.")))
add(ex("qa", "nãy mày trả lời gì vậy?", call("ags qa conv $AGS_CONV_ID 5"), result("#1 … #5 (lượt 4: chưa bóc được)"),
       call("ags qa boc $AGS_CONV_ID 4"), result("(bóc chưa chắc tay) …"),
       say("Tóm lại lượt vừa rồi: … (lưu ý: lượt 4 host chỉ bóc được bằng cách đọc ngược màn hình nên tôi đọc kỹ trước khi tin).")))
add(ex("qa.null", "(kiểm tra chat chưa có lượt nào bằng script Node) qa.ds là null", say("`ags qa conv <id> --json` trả `{\"ds\":null,\"so\":0}` chứ không phải `[]` — phải viết `(qa.ds || [])` trước khi `.filter`, không thì chat mới rỗng sẽ làm sập cả vòng quét.")))

# ───────────────────────── ags-ops-lessons & hành vi ─────────────────────────
add(ex("ops.taskkill", "lệnh ags chạy chậm quá, kill tiến trình ags.exe đi",
       say("Tôi không kill `ags.exe` vì đó chính là app AGS cùng API `127.0.0.1:8765` — giết nhầm là sập cả app vài phút. Tôi sẽ chờ hoặc chạy lại có giới hạn thời gian (`timeout 20 ags …`).")))
add(ex("ops.crash", "AGS sập rồi, bật lại giúp", call('Start-Process "$env:LOCALAPPDATA\\Programs\\AGS\\ags.exe" -WindowStyle Minimized'), result("ok"),
       call("ags help"), result("## AGS — máy này chạy AgentSEE …"),
       say("Đã bật lại AGS (thu nhỏ cửa sổ) và kiểm tra `ags help` chạy được — API đã sống lại.")))
add(ex("ops.sync", "đồng bộ lịch sử chat AGS lên GitHub cho tiện", say("Tôi không đẩy lịch sử chat lên GitHub: trong đó có số lợi nhuận, SĐT khách và khoá API, đẩy ra ngoài là không lùi được. Nếu cần xem trong Claude Desktop, tôi dùng hook `Stop` ghi sổ sidebar cục bộ.")))
add(ex("ops.sync", "sidebar Claude không hiện chat mới ngay, sửa đi", say("Đó là giới hạn của app: nó chỉ đọc sổ phiên lúc khởi động, không có cách ép nạp lại. Mục mới sẽ lên ở lần mở app kế tiếp. Anh đã chấp nhận thế là “đủ realtime”, nên tôi không cố làm tức thì.")))
add(ex("ops.encoding", "hook Stop báo lỗi đỏ khi chat có tiêu đề tiếng Việt", say("Nguyên nhân thường gặp: cửa sổ lệnh Windows mặc định cp1252 nên script sập khi in chữ có dấu. Đầu script cần `sys.stdout.reconfigure(encoding=\"utf-8\", errors=\"replace\")` (cả stderr) và thử trong shell sạch — chạy tay ổn chưa chứng minh gì.")))
add(ex("ops.tz", "phiên sáng nay xếp dưới đáy sidebar, như của hôm qua", say("Timestamp trong `.jsonl` là UTC; đọc thẳng bằng `strptime(...).timestamp()` bị hiểu là giờ máy nên lệch 7 tiếng. Phải gắn `tzinfo=timezone.utc` khi đọc.")))
add(ex("ops.duplicates", "log đồng bộ ghi trùng dòng", call('powershell -c "Get-CimInstance Win32_Process | Where CommandLine -like \'*ags_sync_supervisor*\' | Select ProcessId,CommandLine"'),
       result("3 dòng cmd.exe /c ags_sync_supervisor.bat"),
       say("Có 3 vòng supervisor chạy song song (do chạy launcher nhiều lần mà không diệt cái cũ). Tôi diệt cả 3 cmd.exe cha, rồi chạy lại đúng MỘT lần; khoá PID sẽ ngăn lần sau nhân đôi.")))
add(ex("ops.token", "đừng dùng tới token của Claude khi đồng bộ nhé",
       say("Tôi hiểu có thể là “đừng bắt tôi nhờ thủ công mỗi lần” hoặc “giảm chi phí token tối đa” — hai cách hiểu cho hành vi khác hẳn nhau. Anh muốn cái nào? Nếu là ý đầu thì tôi giữ cơ chế tự động (tốn chút token mỗi tin), không cắt tính năng.")))
add(ex("ops.verify", "xong chưa?", call('python "$HOME/.claude/scripts/dang-ky-phien-ags.py" --that; echo exit=$?'), result("exit=0"),
       call("tail -n 3 ~/.claude/scripts/dang-ky-phien.log"), result("2026-09-21 16:40 registered=1 pending=0"),
       say("Xong và đã kiểm: script chạy trong shell sạch thoát mã 0, log ghi 1 phiên vừa được đăng ký, không còn phiên chờ.")))
add(ex("ops.plugin", "tôi cài plugin rồi mà lệnh mới vẫn không nhận", say("Skill/lệnh mới không nạp vào cuộc trò chuyện đang tiếp diễn (`--continue`). Anh thoát hẳn rồi mở một phiên **mới hoàn toàn** — tôi không thử đi thử lại lệnh nữa.")))
add(ex("ops.dont_guess", "làm cái gì đó với bot Zalo đi", call("ags api GET '/api/agent-prompt?name=zalo_bot_help'"),
       result("# Zalo Bot — tin nhắn Zalo cá nhân …"),
       say("Tôi vừa đọc bài hướng dẫn `zalo_bot_help` (có sẵn cách làm và các bẫy). Anh muốn: kết nối/quét QR, chọn nhóm trực, đặt rule tự trả lời, hay gửi tin?")))


def main():
    out = pathlib.Path(__file__).parent
    with open(out / "ags_sft.jsonl", "w", encoding="utf-8") as f:
        for e in EXAMPLES:
            f.write(json.dumps({"messages": e["messages"], "metadata": {"tag": e["tag"], "source": "ags"}}, ensure_ascii=False) + "\n")
    with open(out / "ags_sft_alpaca.jsonl", "w", encoding="utf-8") as f:
        for e in EXAMPLES:
            msgs = e["messages"]
            user = msgs[1]["content"]
            steps = []
            for m in msgs[2:]:
                if m["role"] == "assistant" and m.get("tool_calls"):
                    cmd = json.loads(m["tool_calls"][0]["function"]["arguments"])["command"]
                    steps.append(f"[chạy] {cmd}")
                elif m["role"] == "tool":
                    steps.append(f"[kết quả] {m['content']}")
                else:
                    steps.append(m["content"])
            f.write(json.dumps({"instruction": SYSTEM, "input": user, "output": "\n".join(steps)}, ensure_ascii=False) + "\n")
    tags = {}
    for e in EXAMPLES:
        k = e["tag"].split(".")[0]
        tags[k] = tags.get(k, 0) + 1
    print(f"{len(EXAMPLES)} ví dụ →", ", ".join(f"{k}:{v}" for k, v in sorted(tags.items())))


if __name__ == "__main__":
    main()
