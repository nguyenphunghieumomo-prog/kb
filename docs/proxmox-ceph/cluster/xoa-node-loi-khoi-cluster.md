---
title: 1.3. Remove node lỗi khỏi cluster
cat: proxmox-ceph
sub: cluster
type: Sự cố
tags: node lỗi, cluster, quorum, pvecm
status: draft
updated: 2026-11-27
summary: Cách loại bỏ node lỗi khỏi cluster Proxmox khi quorum vẫn được duy trì.
source: 1.3 REMOVE  NODE LỖI.docx
review_note:
---

# 1.3. Remove node lỗi khỏi cluster

## 1. Điều kiện quorum

Nếu số node đang hoạt động bình thường > 50%

Giả sử bạn đang có 3 node nhưng 1 node bị vấn đề gì đó bạn cần loại bỏ nó ra khỏi cluster thì bạn cần làm như sau:

Đầu tiên, bạn cần đảm bảo các node đang hoạt động >50%, nếu ta có 3 node thì tối thiểu 2 node phải hoạt động bình thường. Quorum

## 2. Tắt node đang lỗi

Tiếp theo bạn tắt node đang lỗi.

## 3. Xóa node khỏi cluster

Sau đó bạn vào terminal của 1 trong các node còn lại trong cluster gõ lệnh sau:

```bash
pvecm delnode <tên-node>
```

## 4. Nguyên tắc cần nhớ

Quorum = hơn 50% số node trong cluster.

Nếu không đạt quorum: Không được phép thay đổi cấu hình cluster, như tạo/xóa VM, migrate, sửa HA...

> Nguồn: 1.3 REMOVE  NODE LỖI.docx
