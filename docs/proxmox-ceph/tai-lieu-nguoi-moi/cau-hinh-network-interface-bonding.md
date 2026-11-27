---
title: Cấu hình Network Interface và Bonding trên Proxmox
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, network, nic, bonding, lacp, ovs
status: draft
updated: 2026-11-27
summary: Cấu hình NIC, Linux Bonding và OVS Bonding cùng các mode và yêu cầu switch vật lý.
source: Cấu hình Network Interface, Bonding.pdf
review_note:
---

# Cấu hình Network Interface và Bonding trên Proxmox

Bonding gộp nhiều card mạng vật lý thành một interface logic để tăng khả năng chịu lỗi và, tùy mode, tăng băng thông.

## 1. Cấu hình Network Interface

Ví dụ khai báo hai NIC vật lý:

```bash
auto lo
iface lo inet loopback

auto enp24s0f0np0
iface enp24s0f0np0 inet manual

auto enp24s0f1np1
iface enp24s0f1np1 inet manual
```

- `auto <interface>`: khởi động interface cùng hệ thống.
- `inet manual`: interface chỉ tồn tại và không gán IP trực tiếp.
- Tên NIC do udev đặt theo tên hãng, loại card và slot.

Luôn kiểm tra tên NIC bằng:

```bash
ip a
```

## 2. Linux Bonding

Ví dụ Linux Bond dùng chế độ `active-backup`:

```bash
auto bond0
iface bond0 inet manual
        bond_slaves enp24s0f1np1 enp24s0f0np0
        bond_miimon 100
        bond-mode active-backup
```

- `bond_slaves`: danh sách NIC tham gia bond.
- `bond_miimon 100`: kiểm tra link mỗi 100 ms.
- `bond-mode active-backup`: một NIC hoạt động, NIC còn lại dự phòng.

Khi không dùng chế độ động, thường không cần cấu hình Port-Channel hay LACP trên switch.

## 3. Các mode Bond thường dùng

| Mode | Cơ chế | Yêu cầu Switch |
|---|---|---|
| `balance-rr` | Luân phiên gửi gói theo từng NIC | Static Link Aggregation / EtherChannel |
| `active-backup` | Chỉ một NIC active, NIC khác standby | Không yêu cầu thêm cấu hình |
| `balance-xor` | Cân bằng theo hash MAC hoặc IP | Static Link Aggregation |
| `broadcast` | Gửi song song trên mọi NIC thành viên | Switch hỗ trợ nhận gói trùng lặp |
| `802.3ad` | Gộp động theo giao thức LACP | Bật LACP trên switch |
| `balance-tlb` | Cân bằng luồng gửi đi | Không yêu cầu cấu hình switch |
| `balance-alb` | Cân bằng cả gửi và nhận qua ARP negotiation | Không yêu cầu LACP |

## 4. OVS Bonding

Ví dụ Bond trong kiến trúc OVS:

```bash
auto bond0
iface bond0 inet manual
        ovs_bonds ens3f1np1 ens3f0np0
        ovs_type OVSBond
        ovs_bridge vmbr0
        ovs_options bond_mode=active-backup
```

- `ovs_bonds`: danh sách NIC vật lý.
- `ovs_type OVSBond`: khai báo Bond của Open vSwitch.
- `ovs_bridge vmbr0`: gắn Bond trực tiếp vào OVS Bridge.
- `bond_mode=active-backup`: chỉ một NIC truyền nhận tại một thời điểm.

Có thể cấu hình thêm VLAN cho port OVS bằng `ovs_options tag=<VLAN_ID>`.

## 5. Các mode Bond trên OVS

| Mode | Cơ chế | Yêu cầu Switch |
|---|---|---|
| `active-backup` | Một NIC active, tự failover sang NIC dự phòng | Không yêu cầu cấu hình thêm |
| `balance-slb` | Cân bằng luồng gửi theo địa chỉ MAC của VM | Không yêu cầu LACP |
| `LACP (balance-slb)` | Balance-SLB kết hợp giám sát LACP | Bật LACP trên switch |
| `LACP (balance-tcp)` | Cân bằng theo kết nối TCP/UDP chi tiết | Bật LACP trên switch |

## 6. Lựa chọn Bridge và Bond

- Linux Bridge: thích hợp mô hình đơn giản, ít VLAN và cấu hình ngắn gọn.
- OVS: linh hoạt khi quản lý VLAN, Trunk, Access và nhiều mạng logic.
- Với `active-backup`, không bắt buộc Port-Channel/LACP trên switch.
- Với `802.3ad`, `balance-xor` hoặc `balance-rr`, kiểm tra cấu hình Link Aggregation trên cả switch và host.

## 7. Hình minh họa từ tài liệu

![Network Interface và Linux Bonding - trang 1](assets/img/proxmox-ceph/cau-hinh-network-interface-bonding/page-1.png)

*Hình 1: Cấu hình Interface và Bonding Linux.*

![Các mode Linux Bonding - trang 2](assets/img/proxmox-ceph/cau-hinh-network-interface-bonding/page-2.png)

*Hình 2: Các mode balance-rr, active-backup, balance-xor và broadcast.*

![Các mode LACP và balance mode - trang 3](assets/img/proxmox-ceph/cau-hinh-network-interface-bonding/page-3.png)

*Hình 3: Cấu hình 802.3ad, balance-tlb và balance-alb.*

![OVS Bonding - trang 4](assets/img/proxmox-ceph/cau-hinh-network-interface-bonding/page-4.png)

*Hình 4: Cấu hình OVSBond, ovs_bonds và bond_mode.*

![OVS Bond mode - trang 5](assets/img/proxmox-ceph/cau-hinh-network-interface-bonding/page-5.png)

*Hình 5: Các mode OVS và so sánh Linux Bridge/OVS.*

> Nguồn: Cấu hình Network Interface, Bonding.pdf
