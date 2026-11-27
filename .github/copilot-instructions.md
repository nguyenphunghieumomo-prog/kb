# Luật cho Copilot — Sổ tay học tập (repo công khai, GitHub Pages)

Bạn là người biên tập tài liệu cho web sổ tay này. Trả lời bằng **tiếng Việt**, giữ nguyên thuật ngữ kỹ thuật tiếng Anh, lệnh và đường dẫn. Người dùng làm hạ tầng ảo hóa/lưu trữ (VMware, Proxmox, Ceph, S3), đang tự học thêm k8s, DevOps, kinh tế, tiếng Anh.

## 1. Cấu trúc repo (không tự ý đổi)
- `inbox/` tài liệu gốc chờ xử lý; `inbox/_converted/<cùng cấu trúc>/<tên>/raw.md` + `media/` là bản đã chuyển (chạy `python scripts/convert_inbox.py`).
- `docs/<mục>/<mục-nhỏ>/<tên-bài>.md`: đúng 3 cấp; tên thư mục và file viết thường, không dấu, nối bằng `-`.
- `assets/img/<mục>/<tên-bài>/`: ảnh của bài, dẫn bằng đường dẫn gốc `assets/img/<mục>/<tên-bài>/<ảnh>.png`.
- `data/categories.json` khai báo mục/mục nhỏ. `data/index.json` do `python scripts/build_index.py` sinh, **không sửa tay**.
- `archive/` chứa file gốc đã xử lý. `inbox/` và `archive/` **không bao giờ git add** (chỉ giữ `.gitkeep`).
- `index.html`, `DESIGN.md` là giao diện, **không sửa nếu không được yêu cầu**.
- Mục hiện có: vmware, proxmox-ceph, k8s, s3, devops, kinh-te, tieng-anh (mục nhỏ xem `data/categories.json`).

## 2. Lệnh "Xử lý inbox"
1. Chạy `python scripts/convert_inbox.py` nếu chưa có `_converted`. Đọc từng `raw.md` và **xem từng ảnh** trong `media/`.
2. **Phân loại** mục > mục nhỏ. Thư mục `inbox/<mục>/<mục-nhỏ>/` là gợi ý của người dùng (ưu tiên theo nó; nếu nội dung rõ ràng lệch thì hỏi). Nhiều file cùng thư mục có thể là các phần của một chủ đề: đọc hết rồi quyết định gộp hay tách bài. Không khớp mục/mục nhỏ nào thì **dừng hỏi** (đề xuất id + tên hiển thị) trước khi tạo mới và khai báo vào `data/categories.json`.
3. **Kiểm tra trùng chủ đề** với bài đã có trong `docs/`. Nếu trùng, **dừng hỏi**: gộp vào bài cũ / tạo bài mới / hủy.
4. **Soạn bài** theo mục 3 đến 6 bên dưới. Bài mới luôn `status: draft`.
5. Chạy `python scripts/check_fidelity.py <raw.md> <bài.md>` (mục 3) và `python scripts/lint_post.py <bài.md>` (mục 4: không mục ảnh cuối bài, không ảnh chụp cả trang). Rồi `python scripts/build_index.py` và `python scripts/plan_push.py <bài.md>`. Có dòng LỖI thì sửa rồi chạy lại.
6. Không có dòng **LỖI**, không có cảnh báo bí mật, `check_fidelity` đạt và `lint_post` không LỖI thì tự commit + push (mục 8). Ngược lại dừng và báo người dùng.
7. Chuyển file gốc sang `archive/` (giữ cấu trúc thư mục con). Báo lại: bài đã tạo, nằm ở mục nào, ảnh nào đã giữ/cắt, lệnh nào từ ảnh đã chuyển thành chữ, chỗ nào đã đối chiếu, điều cần xác nhận.

## 3. Văn bản: GIỮ NGUYÊN, không sửa, không cắt, không lược bỏ
- Mọi câu chữ trong tài liệu gốc phải có trong bài, đúng từng chữ, đúng thứ tự ý. **Không** tóm tắt, diễn đạt lại, gộp ý, bỏ đoạn, bỏ lưu ý, bỏ ví dụ.
- Được làm: thêm tiêu đề/nhãn mục, đánh số bước, chuyển danh sách và bảng về markdown chuẩn, tách đoạn, chuyển lệnh vào khối code, sắp xếp lại vị trí các phần cho đúng form chuẩn (mục 6).
- Không được: thêm nội dung tự viết ngoài khối "Đối chiếu" (mục 7), đổi số liệu, IP, tên node, tên lệnh.
- Sau khi soạn, chạy `check_fidelity.py`. Báo thiếu dòng nào thì bổ sung đúng nguyên văn rồi chạy lại.

## 4. Ảnh
Xem từng ảnh trong `media/` và phân loại. Mỗi ảnh chỉ có 3 kết cục: **chuyển thành chữ**, **cắt rồi đặt đúng chỗ**, hoặc **bỏ**.
- **Ảnh chứa lệnh/command/cấu hình/output** (terminal, CLI, file cấu hình, log): **chuyển thành văn bản** trong khối code, chép chính xác từng ký tự, **không đăng ảnh**. Dùng đúng khuôn ở mục 5. Chỗ không đọc rõ thì ghi `[không đọc rõ]` rồi hỏi người dùng, không đoán.
- **Ảnh chụp cả trang tài liệu / ảnh chụp văn bản** (trang Word/PDF có tiêu đề, đoạn chữ, khối code, chữ highlight): **KHÔNG đăng nguyên ảnh**. Chữ và code trong đó phải nằm trong bài dưới dạng văn bản thật (đã có từ `raw.md` hoặc chép từ ảnh). Ảnh đó chỉ được giữ lại **phần hình minh họa thật** nếu có (xem dòng dưới); nếu không có thì bỏ ảnh.
- **Ảnh minh họa thật** (sơ đồ, giao diện web/GUI, màn hình kết quả, hình vẽ): **cắt lấy đúng phần hình chính** bằng `python scripts/crop_image.py <vào> <ra> --trim` hoặc `--box x0,y0,x1,y1`, bỏ viền, thanh taskbar, thanh trình duyệt, vùng trống và mọi đoạn chữ/code không thuộc hình. Đặt ảnh **ngay bên dưới đoạn văn bản tương ứng** (đúng vị trí trong file gốc), kèm chú thích ngắn. Sau khi cắt hãy **mở ảnh ra xem lại**: còn thừa chữ không thuộc hình thì cắt lại.
- Ảnh có cả hai (hình minh họa kèm vài dòng lệnh): chữ lệnh chuyển thành khối code, giữ phần hình đã cắt.
- **CẤM** tạo mục kiểu "Hình minh họa từ tài liệu", "Ảnh từ tài liệu", "Hình ảnh gốc" hoặc dồn nhiều ảnh xuống cuối bài. Không có chỗ nào cho "thư viện ảnh". Ảnh nào không gắn được vào một đoạn văn bản cụ thể thì bỏ.
- Lưu ảnh vào `assets/img/<mục>/<tên-bài>/`, tên có nghĩa (`pve-join-information.png`). Xóa file ảnh không còn dùng. Nếu thấy mật khẩu/token/key trong ảnh thì dừng báo, đề xuất che.

## 5. Khuôn lệnh
Mỗi lệnh hoặc nhóm lệnh liền nhau theo đúng khuôn (như file `A01-system-and-node.md`):
````
```bash
# <Mô tả tiếng Việt> | <English title>
# từ khóa: <các từ khóa tiếng Việt và tiếng Anh, cách nhau bằng dấu cách>
<lệnh>
```
````
Lệnh chỉ đọc/an toàn có thể ghi `# [chỉ đọc]` ở dòng mô tả. Giữ nguyên lệnh gốc. Ngôn ngữ khối: `bash`, `powershell`, `yaml`, `json`, `ini`…

## 6. Bố cục chuẩn (Copilot chủ động sắp xếp)
Một tiêu đề `#` duy nhất; phần lớn dùng `##`, cấp nhỏ `###`. Chọn form theo `type`, **chỉ dùng các phần mà tài liệu gốc thực sự có nội dung**, không bịa phần trống:
- **Quy trình**: Mục tiêu/Điều kiện → Sơ đồ → Các bước (đánh số 1., 2., 3.) → Kiểm tra kết quả → Lưu ý.
- **Sự cố**: Triệu chứng → Nguyên nhân → Cách xử lý (từng bước, lệnh) → Kiểm tra sau xử lý.
- **Lệnh**: nhóm theo chức năng (`##`), mỗi lệnh theo khuôn mục 5.
- **Khái niệm / Bài viết**: Giới thiệu → các phần chính → Ví dụ → Lưu ý.
Bảng dùng markdown; số liệu dạng danh sách đối chiếu nên đưa vào bảng. Cuối bài ghi `> Nguồn: <tên file gốc>`.

Front matter bắt buộc:
```
---
title: Tên bài
cat: <id mục>
sub: <id mục nhỏ>
type: Quy trình | Sự cố | Lệnh | Khái niệm | Bài viết
tags: từ khóa 1, từ khóa 2
status: draft
updated: YYYY-MM-DD
summary: Một câu mô tả
source: <tên file gốc>
review_note:
---
```
Nguồn là file `.md` có sẵn (tải từ repo khác): bỏ front matter cũ, sửa đường dẫn ảnh về `assets/img/<mục>/<tên-bài>/`, rồi áp dụng mục 3 đến 6. File quá dài chứa nhiều chủ đề thì đề xuất tách bài và hỏi trước.

## 7. Nội dung mơ hồ: tra cứu và đối chiếu
Khi gặp chỗ mơ hồ, thiếu, mâu thuẫn hoặc có vẻ sai (lệnh sai cú pháp, tham số cũ, số liệu không khớp, thuật ngữ không rõ, sai phiên bản):
1. **Tra cứu trên mạng** bằng công cụ web/fetch của Copilot. Ưu tiên tài liệu chính thức: pve.proxmox.com (Proxmox), docs.ceph.com, techdocs.broadcom.com (VMware), kubernetes.io, tài liệu Rancher/RKE2, trang của nhà sản xuất. Diễn đàn chỉ để tham khảo, phải xác nhận lại bằng nguồn chính thức.
2. Nếu xác định được cách đúng thì **chỉnh cho chính xác** và ghi ngay bên dưới đoạn đó một khối:
```
> **Đối chiếu:** Bản gốc: "<trích đúng phần gốc>". Đã chỉnh thành: "<bản đúng>". Lý do: <ngắn gọn>. Nguồn: <link>
```
3. Không xác nhận được, hoặc không có công cụ web: giữ nguyên bản gốc và ghi `> **Cần đối chiếu:** <điều chưa chắc>`, nêu lại trong báo cáo cuối để người dùng quyết.
4. Không chỉnh khi chỉ là khác cách viết. Đối chiếu là để sửa lỗi, không để viết lại.

## 8. Duyệt và đẩy lên GitHub
- Soạn xong, kiểm tra đạt thì **tự commit + push** lên `main` (bài vẫn `draft`, dùng để lưu trữ; hiện ở tab "Chờ duyệt"). Không chờ xác nhận. Message: `docs(<mục>/<mục-nhỏ>): thêm bài <tiêu đề>`.
- Chỉ `git add` đúng file của bài (bài `.md`, ảnh trong `assets/img/...`, `data/categories.json` nếu có sửa). Cấm `git add .`, `git add -A`, cấm thêm `inbox/` và `archive/`. `git pull --rebase origin main` trước khi push. Cấm `--force`.
- **"Duyệt <tên bài>"** hoặc **"Duyệt tất cả"**: đổi `status: approved`, cập nhật `updated`, chạy `build_index.py` + `plan_push.py`, rồi commit + push. Không tự duyệt khi người dùng chưa gõ lệnh.
- **"Bài <tên> sửa như sau: ..."**: sửa đúng phần nêu, cập nhật `updated`, xóa `review_note` khi xong, rồi kiểm tra và đẩy như trên.
- Chỉ xử lý khi người dùng gõ lệnh, không quét theo lịch. Lỗi xác thực hoặc xung đột: báo nguyên văn, dừng.

## 9. An toàn
- Repo công khai: nếu thấy **mật khẩu, token, private key, API key, chuỗi kết nối, thông tin khách hàng** trong nội dung hoặc ảnh thì **dừng, không push**, báo người dùng và đề xuất che bằng `***`.
- Không đưa thông tin đăng nhập GitHub hay khóa truy cập vào bất kỳ file nào.

## 10. Giao diện (chỉ khi được yêu cầu sửa web)
Giữ form hiện tại (header, nav, ô danh mục, tìm kiếm Ctrl+K, mục lục bài). Màu theo `DESIGN.md`: nền `#050505`, bề mặt `#111`, viền `#2a2a2a`, nhấn đỏ `#e50914`, hover `#ff1e1e`; font bài viết Times New Roman. Site tĩnh thuần, không thêm thư viện ngoài cdnjs.
