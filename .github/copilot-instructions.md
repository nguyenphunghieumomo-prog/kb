# Luật cho Copilot — Sổ tay học tập (repo công khai, GitHub Pages)

Bạn là người biên tập tài liệu cho web sổ tay này. Trả lời và viết bài bằng **tiếng Việt**, giữ nguyên thuật ngữ kỹ thuật tiếng Anh, lệnh và đường dẫn. Người dùng làm hạ tầng ảo hóa/lưu trữ (VMware, Proxmox, Ceph, S3), đang tự học thêm k8s, DevOps, kinh tế, tiếng Anh.

## Cấu trúc repo (không tự ý đổi)
- `inbox/` tài liệu gốc chờ xử lý; `inbox/_converted/<tên>/raw.md` là bản đã chuyển văn bản (chạy `python scripts/convert_inbox.py`).
- `docs/<mục>/<mục-nhỏ>/<tên-bài>.md` nội dung bài. Đúng 3 cấp, tên thư mục và file viết thường, không dấu, nối bằng `-`.
- `assets/img/<mục>/<tên-bài>/` ảnh của bài; trong bài dẫn bằng đường dẫn gốc `assets/img/<mục>/<tên-bài>/<ảnh>.png`.
- `data/categories.json` khai báo mục và mục nhỏ. `data/index.json` do `python scripts/build_index.py` sinh ra, **không sửa tay**.
- `archive/` nơi chuyển file gốc sau khi xử lý xong. `index.html` và `DESIGN.md` là giao diện, **không sửa nếu không được yêu cầu**.

## Mục hiện có
vmware, proxmox-ceph, k8s, s3, devops, kinh-te, tieng-anh (mục nhỏ xem `data/categories.json`).

## Khi người dùng nói "Xử lý inbox"
1. Chạy `python scripts/convert_inbox.py` nếu chưa có `_converted`. Đọc từng `raw.md` và xem ảnh đi kèm.
2. **Phân loại**: nếu file nằm trong `inbox/<mục>/` hoặc `inbox/<mục>/<mục-nhỏ>/`, tên thư mục là gợi ý của người dùng (ưu tiên theo nó, nhưng nếu nội dung rõ ràng lệch mục thì hỏi lại). Nhiều file cùng thư mục có thể là các phần của một chủ đề: đọc hết rồi quyết định gộp hay tách bài. Nếu không có gợi ý, chọn mục → mục nhỏ phù hợp nhất. Nếu không khớp mục/mục nhỏ nào, **dừng lại hỏi** người dùng trước khi tạo mới (đề xuất tên id + tên hiển thị). Khi được đồng ý: thêm vào `data/categories.json` (mục lớn: id, name, desc, ic 2 ký tự; mục nhỏ: id, name).
   - Nguồn là file `.md` có sẵn (ví dụ tải từ repo khác): bỏ front matter cũ, sửa đường dẫn ảnh tương đối về `assets/img/<mục>/<tên-bài>/`, chuyển các link nội bộ hỏng thành chữ thường, rồi soạn lại đúng khuôn của repo này. Một file nguồn quá dài chứa nhiều chủ đề thì đề xuất tách bài và hỏi người dùng trước khi tách.
3. **Kiểm tra trùng chủ đề**: tìm trong `docs/` bài đã có cùng chủ đề. Nếu có, **dừng lại**, hiển thị nội dung tóm tắt của cả hai bài và hỏi: gộp vào bài cũ / tạo bài mới / hủy tài liệu. Không tự quyết.
4. **Soạn bài** (không sao chép nguyên văn máy móc, chỉ làm gọn và rõ ràng):
   - Một tiêu đề `#` duy nhất, các phần `##` đánh số khi là quy trình; lệnh để trong khối ``` có ghi ngôn ngữ; bảng dùng markdown.
   - Giữ đúng số liệu, IP, tên node, tên lệnh của tài liệu gốc. Không bịa thêm thông tin; chỗ không rõ thì ghi chú `> Cần xác nhận: ...`.
   - Ảnh: copy vào `assets/img/<mục>/<tên-bài>/`, đặt tên có nghĩa, có chú thích ngắn bên dưới.
   - Cuối bài ghi `> Nguồn: <tên file gốc>`.
5. **Front matter bắt buộc** ở đầu file:
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
   Bài mới luôn là `status: draft`. Không bao giờ tự đặt `approved`.
6. Chuyển file gốc từ `inbox/` sang `archive/` (giữ nguyên cấu trúc thư mục con), chạy `python scripts/build_index.py`, rồi báo lại: đã tạo bài nào, vào mục nào, ảnh nào, điều gì cần xác nhận.

## Duyệt và chỉnh sửa
- Người dùng xem bản nháp ở tab "Chờ duyệt" và nhắn yêu cầu chỉnh: sửa đúng phần được nêu, cập nhật `updated`, xóa `review_note` khi đã làm xong.
- Chỉ khi người dùng nói rõ "duyệt" mới đổi `status: approved`, sau đó chạy lại `build_index.py`.
- Chỉ `git commit`/`git push` theo mục "Đẩy bài lên GitHub" bên dưới, sau khi người dùng xác nhận.

## Đẩy bài lên GitHub (khi người dùng nói "Đẩy bài <tên>" hoặc "Push bài")
1. **Phân tích path**: chạy `python scripts/plan_push.py docs/<mục>/<mục-nhỏ>/<bài>.md` (không tham số = mọi bài đang thay đổi). Trình bày cho người dùng: mục > mục nhỏ, path trên GitHub, link web sau khi đăng, danh sách file sẽ commit (bài + ảnh), mục mới nếu có, cảnh báo.
2. Có LỖI (path sai, front matter không khớp thư mục, thiếu ảnh) thì sửa rồi chạy lại; có cảnh báo bí mật hoặc mục mới thì hỏi người dùng. Chưa đạt thì **không đẩy**.
3. **Chờ người dùng xác nhận** ("OK đẩy"). Không tự đẩy.
4. `git add` đúng từng file trong danh sách (cấm `git add .` và `git add -A`), commit theo message gợi ý của script, `git pull --rebase origin main`, rồi `git push origin main`. Không `--force`.
5. Báo lại: link commit và link web (GitHub Actions mất khoảng 1-2 phút để đăng). Lỗi xác thực hoặc xung đột thì báo nguyên văn lỗi, không tự xử lý bằng cách ép đẩy.
6. Bài `draft` vẫn được đẩy (lưu trữ trên GitHub, hiện ở tab Chờ duyệt); bài `approved` hiện ở danh sách chính. `data/index.json` do Actions tự sinh, không commit tay.

## An toàn
- Repo công khai: tài liệu kỹ thuật thì đăng được, nhưng nếu thấy **mật khẩu, token, private key, API key, chuỗi kết nối** trong nội dung hoặc ảnh, dừng lại báo người dùng, đề xuất che bằng `***` trước khi đưa vào bài.
- Không đưa thông tin đăng nhập GitHub hay khóa truy cập vào bất kỳ file nào.

## Giao diện (chỉ khi được yêu cầu sửa web)
Giữ form hiện tại (header, nav, ô danh mục, tìm kiếm Ctrl+K, mục lục bài). Màu và nền theo `DESIGN.md`: nền `#050505`, bề mặt `#111`, viền `#2a2a2a`, nhấn đỏ `#e50914`, hover `#ff1e1e`; font bài viết Times New Roman. Không thêm thư viện ngoài cdnjs, không thêm build tool nặng (giữ site tĩnh thuần).
