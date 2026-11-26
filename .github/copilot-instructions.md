````instructions
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

## Khi người dùng nói `Xử lý inbox`
1. Chạy `python scripts/convert_inbox.py` nếu chưa có `_converted`. Sau đó đọc từng `raw.md` và xem ảnh đi kèm.
2. **Phân loại**: tên thư mục trong `inbox/<mục>/` hoặc `inbox/<mục>/<mục-nhỏ>/` là gợi ý. Chọn mục và mục nhỏ phù hợp nhất trong cấu trúc hiện có; không hỏi nếu có thể phân loại hợp lý.
3. **Chỉ hỏi người dùng** khi:
   - Không tìm thấy mục/mục nhỏ phù hợp an toàn để tạo bài.
   - Phát hiện trùng chủ đề quan trọng với bài đã có trong `docs/`.
   - Phát hiện mật khẩu, token, private key, API key hoặc chuỗi kết nối trong nội dung hoặc ảnh cần che.
   - File dài chứa nhiều chủ đề rõ rệt cần quyết định tách bài.
4. **Kiểm tra trùng chủ đề**: nếu trùng bài cũ, chỉ dừng để tóm tắt cả hai và hỏi gộp vào bài cũ, tạo bài mới hay hủy tài liệu. Không tự chọn cho trường hợp này.
5. **Soạn lại bài** (không sao chép nguyên văn máy móc):
   - Một tiêu đề `#` duy nhất. Các phần quy trình dùng `##` đánh số.
   - Lệnh đặt trong khối ``` có ghi ngôn ngữ; bảng dùng Markdown.
   - Giữ đúng số liệu, IP, tên node, tên lệnh và thông tin kỹ thuật của nguồn.
   - Không bịa thông tin. Chỗ chưa rõ ghi `> Cần xác nhận: ...`.
   - Copy ảnh vào `assets/img/<mục>/<tên-bài>/`, đặt tên có nghĩa và thêm chú thích ngắn.
   - Cuối bài ghi `> Nguồn: <tên file gốc>`.
   - Bỏ front matter cũ nếu tài liệu `.md` đã tải từ repo khác; sửa link ảnh và link nội bộ về cấu trúc của repo.
6. **Front matter bắt buộc** ở đầu bài:
```yaml
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
7. Chuyển file gốc từ `inbox/` sang `archive/`, giữ nguyên cấu trúc thư mục con.
8. Chạy `python scripts/build_index.py` để cập nhật index.
9. Chạy `python scripts/plan_push.py` cho toàn bộ bài mới hoặc bài vừa thay đổi.
10. Nếu plan không có dòng `LỖI` và không có cảnh báo bí mật/mật khẩu/token, tự commit và push bài `draft` lên `main`. Không chờ xác nhận.
11. Nếu plan có dòng `LỖI` hoặc cảnh báo bí mật/mật khẩu/token, dừng push và báo người dùng nguyên văn cảnh báo để họ xử lý.

## Khi tôi gõ `Duyệt <tên bài>` hoặc `Duyệt tất cả`
- Chỉ thực hiện duyệt khi nhận đúng một trong hai lệnh này.
- `Duyệt <tên bài>`: đổi đúng bài được chỉ định thành `status: approved`, cập nhật `updated` và chạy `python scripts/build_index.py`.
- `Duyệt tất cả`: đổi mọi bài `draft` thành `approved`, cập nhật `updated` và chạy `python scripts/build_index.py`.
- Sau khi duyệt, chạy `python scripts/plan_push.py` cho các bài đã duyệt.
- Nếu plan không có dòng `LỖI` và không có cảnh báo bí mật/mật khẩu/token, commit và push lên `main` để bài hiện trong danh sách chính.
- Không tự duyệt bài khi chỉ chạy `Xử lý inbox`.

## Git và push
- Không quét hoặc xử lý tự động theo lịch. Chỉ xử lý khi tôi gõ `Xử lý inbox`.
- Không bao giờ chạy `git add` với file hoặc thư mục dưới `inbox/` hoặc `archive/`; cả hai thư mục được giữ trên máy local.
- Chỉ `git add` bài trong `docs/`, ảnh trong `assets/`, `data/categories.json`, `data/index.json` và các file cấu hình/giao diện thực sự thay đổi.
- `git add .` và `git add -A` là không được phép.
- Không dùng `git push --force`, `--force-with-lease` hoặc biến thể ép push nào.
- Khi push gặp lỗi xác thực hoặc xung đột, báo nguyên văn lỗi và dừng lại. Không tự rebase, merge hoặc chỉnh lịch sử để ép push.

## An toàn
- Repo công khai có thể chứa tài liệu kỹ thuật, nhưng mật khẩu, token, private key, API key và chuỗi kết nối phải dừng lại để đề xuất che bằng `***` trước khi đăng.
- Không đưa thông tin đăng nhập GitHub hoặc khóa truy cập vào bất kỳ file nào.

## Giao diện (chỉ khi được yêu cầu sửa web)
Giữ form hiện tại (header, nav, ô danh mục, tìm kiếm Ctrl+K, mục lục bài). Màu và nền theo `DESIGN.md`: nền `#050505`, bề mặt `#111`, viền `#2a2a2a`, nhấn đỏ `#e50914`, hover `#ff1e1e`; font bài viết Times New Roman. Không thêm thư viện ngoài cdnjs, không thêm build tool nặng (giữ site tĩnh thuần).
````
