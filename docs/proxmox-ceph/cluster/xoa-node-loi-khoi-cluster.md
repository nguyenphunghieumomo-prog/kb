---
title: Xóa node lỗi khỏi cluster Proxmox
cat: proxmox-ceph
sub: cluster
type: Sự cố
tags: proxmox, cluster, quorum, corosync, pvecm
status: draft
updated: 2026-11-25
summary: Cách kiểm tra quorum và xóa node đang lỗi khỏi cluster bằng pvecm delnode.
source: 1.3 REMOVE  NODE LỖI.docx
review_note:
---

# Xóa node lỗi khỏi cluster Proxmox

Đây là quy trình loại bỏ một node lỗi khỏi cluster Proxmox. Trước khi thực hiện, cần bảo đảm cluster còn quorum.

## 1. Kiểm tra điều kiện quorum

Quorum yêu cầu hơn 50% node trong cluster vẫn hoạt động bình thường.

| Số node trong cluster | Số node tối thiểu cần hoạt động | Bắt buộc quorum |
|---|---|---|
| 3 node | 2 node | Còn quorum |

> Mục tiêu là tránh trường hợp cluster mất quorum. Trong ví dụ 3 node, hãy tắt node lỗi chỉ sau khi ít nhất 2 node còn hoạt động và tham gia cluster.

Khi không còn quorum, bạn không được phép thay đổi cấu hình cluster, chẳng hạn tạo hoặc xóa VM, migrate VM, hay sửa HA.

## 2. Tắt node đang lỗi

Tắt node cần loại bỏ khỏi cluster bằng giao diện hoặc nguồn cấp khi chưa thể đưa node về trạng thái an toàn.

Đảm bảo node còn lại trong cluster vẫn có kết nối và dịch vụ corosync hoạt động.

## 3. Xóa node khỏi cấu hình cluster

Đăng nhập vào terminal của một node còn hoạt động bình thường, sau đó chạy:

```bash
pvecm delnode <tên-node>
```

Thay `<tên-node>` bằng tên chính xác của node đang lỗi.

## 4. Nguyên tắc cần nhớ

- Quorum là điều kiện bắt buộc để thay đổi cấu hình cluster.
- Cluster đạt quorum khi số node hoạt động lớn hơn 50% tổng số node.
- Chỉ chạy `pvecm delnode` sau khi xác nhận node đã dừng và không còn là thành viên hoạt động cần giữ lại.
- Nếu số node hoạt động không đạt quorum, khôi phục hoặc kiểm tra các node còn lại trước khi thay đổi cấu hình.

> Nguồn: 1.3 REMOVE  NODE LỖI.docx
