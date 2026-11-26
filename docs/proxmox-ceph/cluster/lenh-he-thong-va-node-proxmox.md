---
title: Lệnh quản trị hệ thống và node Proxmox
cat: proxmox-ceph
sub: cluster
type: Lệnh
tags: proxmox, system, node, kernel, upgrade, certificate
status: draft
updated: 2026-11-25
summary: Nhóm lệnh kiểm tra hệ thống, node, dịch vụ, chứng chỉ, thời gian, boot và nâng cấp Proxmox VE.
source: A01-system-and-node.md
review_note:
---

# Lệnh quản trị hệ thống và node Proxmox

Ký hiệu `[chỉ đọc]` là lệnh chỉ xem trạng thái. Các lệnh còn lại có thể thay đổi cấu hình hoặc trạng thái hệ thống; hãy đọc kỹ trước khi chạy.

## Phiên bản

```bash
# [chỉ đọc] Xem phiên bản PVE và các gói liên quan
pveversion -v

# [chỉ đọc] Xem hostname và hệ điều hành
hostnamectl

# [chỉ đọc] Xem kernel đang chạy
uname -r
```

## Tải hệ thống

```bash
# [chỉ đọc] Xem thời gian máy chạy và mức tải
uptime
```

## Thời gian

```bash
# [chỉ đọc] Xem múi giờ và trạng thái đồng bộ giờ
timedatectl

# [chỉ đọc] Xem độ lệch NTP trên máy hiện tại
chronyc tracking

# [chỉ đọc] Liệt kê các nguồn NTP đang dùng
chronyc sources -v
```

## Dịch vụ

```bash
# [chỉ đọc] Liệt kê service đang bị lỗi
systemctl --failed

# [chỉ đọc] Xem trạng thái các service lõi của PVE
systemctl status pve-cluster pvedaemon pveproxy pvestatd pve-firewall pvescheduler
```

## Node

```bash
# [chỉ đọc] Xem cấu hình của node
pvenode config get

# Bật toàn bộ VM/CT trên node
pvenode startall

# Tắt toàn bộ VM/CT trên node
pvenode stopall

# Di chuyển toàn bộ VM/CT sang node khác
pvenode migrateall <target-node>
```

## Chứng chỉ

```bash
# [chỉ đọc] Xem thông tin chứng chỉ của node
pvenode cert info

# Tạo lại chứng chỉ cho cluster
pvecm updatecerts --force
```

## Nâng cấp

```bash
# Cập nhật danh sách gói từ repository
apt update

# Nâng cấp toàn bộ gói
apt full-upgrade

# [chỉ đọc] Kiểm tra trước khi nâng cấp PVE 8 lên 9
pve8to9 --full
```

## Kernel

```bash
# [chỉ đọc] Xem cấu hình boot
proxmox-boot-tool status

# [chỉ đọc] Liệt kê các kernel đã cài
proxmox-boot-tool kernel list

# Ghim một kernel làm mặc định
proxmox-boot-tool kernel pin <version>
```

## Trường hợp liên quan

- Nâng cấp Proxmox VE 8 lên 9 trong cluster có Ceph.
- PVE host hỏng đĩa boot, không có backup cấu hình.
- Proxmox boot ZFS mirror và thay disk rpool.
- Clock skew trên MON (lệch giờ).
- GUI Proxmox bị đăng xuất liên tục.
- RGW/S3 trả 403.
- Bảo trì hoặc reboot một node Proxmox và Ceph.
- Di chuyển VM giữa hai cluster bằng remote migration.
- Xóa node hỏng và join lại cùng tên.
- Nâng cấp Ceph trên Proxmox.
- Nâng cấp một node Proxmox VE 5.4 lên 8.x qua ZFS.
- NAS NFS làm storage dùng chung cho cluster.
- Cấu hình Nginx proxy console cho VM Proxmox.

> Nguồn: A01-system-and-node.md
