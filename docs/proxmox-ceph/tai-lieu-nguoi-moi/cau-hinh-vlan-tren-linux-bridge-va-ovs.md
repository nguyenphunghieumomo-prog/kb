---
title: Cấu hình VLAN trên Linux Bridge và OVS
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, vlan, linux bridge, ovs, trunk, bond
status: draft
updated: 2026-11-27
summary: Cách cấu hình VLAN bằng sub-interface trên Linux Bridge và OVSIntPort trên Open vSwitch.
source: Cấu hình VLAN.pdf
review_note:
---

# Cấu hình VLAN trên Linux Bridge và OVS

Trong bài viết này ta sẽ làm rõ về cách cấu hình vlan trên Proxmox.

## 4. Cấu hình VLAN

## 4.1 VLAN trên Linux Bridge — dùng sub-interface

Cơ chế xử lý VLAN của Linux Bridge truyền thống là bóc tách luồng dữ liệu bằng cách tạo ra các giao diện con (Sub-interface) dựa trên card vật lý hoặc cổng gộp Bond. Tên của sub-interface bắt buộc phải tuân theo định dạng: <tên_giao_diện>.<VLAN_ID>. Sau đó, ta gắn chính sub-interface đã lọc VLAN này vào Linux Bridge.

```bash
auto bond0.70
iface bond0.70 inet manual
        vlan-raw-device bond0

auto vmbr0
iface vmbr0 inet static
        address 192.168.70.147/24
        gateway 192.168.70.1
        bridge-ports bond0.70
        bridge-stp off
        bridge-fd 0
```

Trunk nhiều VLAN kiểu tổng quát (đặt tên NIC/VLAN theo thực tế):

```bash
auto enpxxxs0fxnpx
iface enpxxxs0fxnpx inet manual

auto enpxxxs0fxnpx
iface enpxxxs0fxnpx inet manual

auto bond0
iface bond0 inet manual
        bond-slaves enpxxxs0fxnpx enpxxxs0fxnpx
        bond_miimon 100
        bond-mode 802.3ad
        bond-primary enpxxxs0fxnpx
        mtu 9000

auto bond0.<Vlan_tag>
iface bond0.<Vlan_tag> inet manual

auto vmbr0
iface vmbr0 inet static
        address 10.2.xxx.xxx/24
        gateway 10.2.xxx.x
        bridge-ports bond0.<Vlan_tag>
        bridge-stp off
        bridge-fd 0
        mtu 9000
```

Chú ý: cấu hình này bond đang dùng mode 802.3ad tức LACP tức switch vật lý phải cấu hình thêm phần LACP

Ở mô hình truyền thống này, mỗi một Switch ảo (vmbrX) chỉ phục vụ cho duy nhất 1 VLAN (với các gói tin đi ra/vào đã bóc sẵn tag). Nếu hệ thống yêu cầu cấp nhiều VLAN khác nhau cho các máy ảo (VM), ta bắt buộc phải tạo thêm nhiều cặp tương ứng: bond0.<VLAN_ID_mới> kết hợp với một Bridge mới (vmbr1, vmbr2,...).

## 4.2. VLAN trên OVS Bridge — Dùng OVSIntPort với tag

Mô hình Open vSwitch (OVS) xử lý VLAN gọn gàng và tối ưu hơn nhiều so với Linux Bridge: Toàn bộ hệ thống chỉ cần duy nhất 1 giao diện Bridge chính (vmbr0). Mỗi phân đoạn mạng (VLAN) sẽ được quản lý độc lập bằng một cổng nội bộ ảo (OVSIntPort) định danh bằng tùy chọn tag=<VLAN_ID> ghim trực tiếp vào Bridge đó.

- Thường nếu chúng ta sử dụng 1 host Proxmox để chạy dịch vụ thì hầu như chỉ cần 2 vlan là đủ chạy 1 Vlan cho MGT và 1 vlan cho dịch vụ mình chạy
- Nếu cụm chúng ta là 1 cluster > 3 thì lúc đó OVS sẽ phát huy điểm mạnh của nó, giúp ta quy hoạch các vlan rất hữu ích chỉ trên 1 card vmbrx

VD: vêd cấu hình Vlan trên OVS:

```bash
# 1. Cấu hình Mạng quản trị (Management Network)

auto vlan_MGT
iface vlan_MGT inet static
        address 192.168.xx.xx/24
        gateway 192.168.xx.x               # Lưu ý: Chỉ đặt DUY NHẤT 1 gateway tại mạng MGT
        ovs_type OVSIntPort
        ovs_bridge vmbr0
        ovs_options tag=VLAN_MGT_ID
#MGT — Mạng quản lý/quản trị host

# 2. Cấu hình vlan cho dịch vụ chạy web, mail, …

auto vlan_web
iface vlan_web inet static
        address 10.xx.xx.xx/24
        ovs_type OVSIntPort
        ovs_bridge vmbr0
        ovs_options tag=VLAN_WEB_ID
```
…. Add thêm Vlan theo nhu cầu sử dụng

```bash
# 3. Giao diện OVS Bridge tổng quản lý tập trung

auto vmbr0
iface vmbr0 inet manual
        ovs_type OVSBridge
        ovs_ports bond0 vlan_MGT vlan_CLS vlan_WEB
```

Tổng quát ta có

```bash
auto lo
iface lo inet loopback

auto ens1xx
iface ens1xx inet manual

auto ens2xx
iface enp2xx inet manual

auto ten_vlan
iface ten_vlan inet static
        address 192.168.x.x/24
        gateway 192.168.x.x
        ovs_type OVSIntPort
        ovs_bridge vmbr0
        ovs_options tag=vlan_id

auto bond0
iface bond0 inet manual
        ovs_bonds ens1xx ens2xx
        ovs_type OVSBond
        ovs_bridge vmbr0
        ovs_options bond_mode -> chọn mode theo nhu cầu

auto vmbr0
iface vmbr0 inet manual
        ovs_type OVSBridge
        ovs_ports bond0 vlan70
```

> Nguồn: Cấu hình VLAN.pdf
