# Prompt dán vào Copilot Chat (Visual Studio) — chạy một lần để khởi tạo

> Mở thư mục repo trong Visual Studio, bật Copilot Chat ở chế độ **Agent**, dán nguyên khối dưới đây.

```
Repo này là web sổ tay học tập tĩnh (HTML thuần + markdown), đăng bằng GitHub Pages. Hãy đọc kỹ
.github/copilot-instructions.md, DESIGN.md, data/categories.json và bài mẫu
docs/proxmox-ceph/cluster/tao-cluster-proxmox-3-node.md để hiểu cấu trúc và quy ước.

Việc cần làm lần này:
1. Chạy `python scripts/build_index.py` và `python -m http.server 8080`, kiểm tra web chạy đúng (trang chủ,
   mục, mục nhỏ, bài viết, tìm kiếm Ctrl+K, tab Chờ duyệt, tab Đẩy tài liệu). Báo lỗi nếu có, chưa sửa vội.
2. Kiểm tra `.github/workflows/pages.yml` và nói tôi cần bật gì trong Settings > Pages của repo
   (Source: GitHub Actions).
3. Nếu trong `inbox/` có file, thực hiện quy trình "Xử lý inbox" đúng như trong copilot-instructions.md:
   phân loại mục > mục nhỏ, hỏi tôi khi không khớp mục nào hoặc trùng chủ đề bài đã có, soạn bài ở trạng
   thái draft, chưa tự duyệt, chưa push.
4. Cuối cùng liệt kê: bài đã tạo, mục/mục nhỏ đã dùng, điều cần tôi xác nhận.

Ràng buộc: không sửa index.html và DESIGN.md nếu tôi chưa yêu cầu; không đưa mật khẩu/token vào bài;
hỏi tôi từng điểm chưa rõ thay vì tự đoán.
```

## Các câu lệnh dùng hằng ngày
- `Xử lý inbox`
- `Bài <tên> sửa như sau: ...`
- `Duyệt bài <tên>`
- `Thêm mục nhỏ <tên> vào mục <mục>` / `Tạo mục mới <tên>`
- `Đẩy bài <tên>`: Copilot phân tích path, cho bạn xem danh sách file, chờ bạn OK rồi mới commit + push
- `Đẩy tất cả bài đang chờ`: như trên nhưng cho mọi bài thay đổi
