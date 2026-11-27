# Prompt cho Copilot (Visual Studio Code, chế độ Agent)

Luật đầy đủ nằm trong `.github/copilot-instructions.md`: Copilot tự đọc file này ở mọi cuộc chat mới, nên **tắt VS Code hay xóa lịch sử chat không làm mất luật**. Chỉ cần file này đã được commit trong repo.

## Dùng hằng ngày (chỉ cần gõ ngắn)
- `Xử lý inbox`
- `Bài <tên> sửa như sau: ...`
- `Duyệt <tên bài>` hoặc `Duyệt tất cả`
- `Thêm mục nhỏ <tên> vào mục <mục>` / `Tạo mục mới <tên>`
- `Xử lý lại bài <tên> theo luật mới` (làm lại bài cũ từ file gốc trong archive/)

## Nếu Copilot có vẻ không theo luật (chat mới, luật bị bỏ qua)
```
Đọc kỹ .github/copilot-instructions.md rồi làm đúng từng mục, đặc biệt:
- Mục 3: văn bản gốc giữ nguyên, không sửa, không cắt, không lược bỏ; chạy scripts/check_fidelity.py.
- Mục 4: ảnh lệnh/cấu hình chuyển thành code; ảnh minh họa cắt phần liên quan bằng scripts/crop_image.py và đặt đúng chỗ.
- Mục 6: tự sắp xếp bố cục theo form chuẩn.
- Mục 7: nội dung mơ hồ thì tra tài liệu chính thức trên mạng, chỉnh cho chính xác và ghi khối "Đối chiếu".
Bây giờ thực hiện: Xử lý inbox.
```
