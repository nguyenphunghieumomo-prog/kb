---
title: Lệnh quản trị hệ thống và node Proxmox
cat: proxmox-ceph
sub: cluster
type: Lệnh
tags: proxmox, system, node, kernel, upgrade, certificate
status: draft
updated: 2026-11-27
summary: Nhóm lệnh kiểm tra hệ thống, node, dịch vụ, chứng chỉ, thời gian, boot và nâng cấp Proxmox VE.
source: A01-system-and-node.md
review_note:
---

# Lệnh quản trị hệ thống và node Proxmox

Ký hiệu `[chỉ đọc]` là lệnh chỉ xem trạng thái, không thay đổi hệ thống; ký hiệu `⚠ NGUY HIỂM` chỉ các lệnh phá hủy hoặc ảnh hưởng dịch vụ. Các lệnh không ghi chú là lệnh có thể thay đổi cấu hình hoặc trạng thái hệ thống, nên đọc kỹ trước khi chạy.

## Phiên bản (Version)

```bash
# [chỉ đọc] Xem phiên bản PVE và các gói liên quan | PVE and package versions
# từ khóa: version phiên bản kernel gói nâng cấp kiểm tra
pveversion -v

# [chỉ đọc] Xem hostname và hệ điều hành | Hostname, OS
# từ khóa: hostname tên máy os debian đổi đổi node set-hostname
hostnamectl

# [chỉ đọc] Xem kernel đang chạy | Running kernel
# từ khóa: kernel phiên bản nhân boot
uname -r
```

## Tải hệ thống (Load)

```bash
# [chỉ đọc] Thời gian máy chạy và mức tải | Uptime and load
# từ khóa: uptime load tải reboot lần cuối boot lúc nào thời gian chạy
uptime
```

## Thời gian (Time)

```bash
# [chỉ đọc] Múi giờ và trạng thái đồng bộ giờ | Time zone and sync state
# từ khóa: giờ ntp lệch giờ timezone clock
timedatectl

# [chỉ đọc] Độ lệch NTP trên máy hiện tại | NTP offset
# từ khóa: ntp chrony lệch giờ clock skew
chronyc tracking

# [chỉ đọc] Xem các nguồn NTP đang dùng | NTP sources
# từ khóa: ntp chrony nguồn giờ lệch giờ
chronyc sources -v
```

## Dịch vụ (Services)

```bash
# [chỉ đọc] Liệt kê service đang bị lỗi | Failed units
# từ khóa: service lỗi failed sau reboot không chạy
systemctl --failed

# [chỉ đọc] Trạng thái các service lõi của PVE | Core PVE services
# từ khóa: service pve gui treo pveproxy pvedaemon pvestatd
systemctl status pve-cluster pvedaemon pveproxy pvestatd pve-firewall pvescheduler
```

## Node

```bash
# [chỉ đọc] Xem cấu hình của node | Node config
# từ khóa: node config cấu hình
pvenode config get

# Bật toàn bộ VM/CT trên node | Start all guests on node
# từ khóa: khởi động tất cả sau bảo trì start all
pvenode startall

# Tắt toàn bộ VM/CT trên node | Stop all guests on node
# từ khóa: tắt tất cả trước bảo trì stop all
pvenode stopall

# Di chuyển toàn bộ VM/CT sang node khác | Migrate all guests away
# từ khóa: bảo trì node migrate hết reboot
pvenode migrateall <target-node>
```

## Chứng chỉ (Certificates)

```bash
# [chỉ đọc] Xem thông tin chứng chỉ của node | Certificate details
# từ khóa: chứng chỉ ssl cert hết hạn
pvenode cert info

# Tạo lại chứng chỉ cho cluster | Regenerate cluster certificates
# từ khóa: chứng chỉ lỗi ssh known_hosts node mới join cert
pvecm updatecerts --force
```

## Nâng cấp (Upgrade)

```bash
# Cập nhật danh sách gói từ repo | Refresh package lists
# từ khóa: apt repo cập nhật nâng cấp no-subscription enterprise repository subscription 401 unauthorized sources.list
apt update

# Nâng cấp toàn bộ gói (kể cả thêm/xóa gói phụ thuộc) | Upgrade packages
# từ khóa: nâng cấp upgrade cập nhật hệ thống dist-upgrade
apt full-upgrade

# [chỉ đọc] Công cụ kiểm tra trước khi nâng cấp PVE 8 lên 9 | Pre-upgrade checker (PVE 8 to 9)
# từ khóa: nâng cấp upgrade 8 9 kiểm tra trước
pve8to9 --full
```

## Kernel

```bash
# [chỉ đọc] Xem cấu hình boot (ESP, kernel) | Boot setup status
# từ khóa: boot uefi esp lỗi boot grub systemd-boot
proxmox-boot-tool status

# [chỉ đọc] Liệt kê các kernel đã cài | Installed kernels
# từ khóa: kernel danh sách phiên bản
proxmox-boot-tool kernel list

# Ghim kernel mặc định khi boot | Pin default kernel
# từ khóa: kernel pin ghim lỗi sau nâng cấp quay về kernel cũ
proxmox-boot-tool kernel pin <version>
```

## Trường hợp liên quan

- Nâng cấp Proxmox VE 8 lên 9 trong cluster có Ceph.
- PVE host hỏng đĩa boot, không có backup cấu hình: kiểm kê và dựng lại node.
- Proxmox boot ZFS mirror: kiểm tra trước khi thay disk rpool.
- Clock skew trên MON (lệch giờ).
- GUI Proxmox bị đăng xuất liên tục hoặc không đăng nhập được.
- RGW/S3 trả 403 (AccessDenied, SignatureDoesNotMatch, QuotaExceeded).
- Bảo trì hoặc reboot một node Proxmox và Ceph.
- Di chuyển VM giữa hai cluster Proxmox bằng remote migration.
- Xóa node hỏng và join lại cùng tên (node ma xám trong GUI).
- Nâng cấp Ceph trên Proxmox (ví dụ Reef lên Squid).
- Nâng cấp Ceph Quincy 17.2.8 → Reef 18.2.8 → Squid 19.2.4 trên PVE 8.4 (3 node, có CephFS).
- Nâng cấp một node Proxmox VE từ 5.4 lên 8.x (qua 6, 7, 8) kèm ZFS.
- NAS NFS làm storage dùng chung cho cluster Proxmox.
- Cấu hình Nginx proxy console cho VM Proxmox (noVNC qua portal).

> Nguồn: A01-system-and-node.md
