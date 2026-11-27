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

VLAN trên Linux Bridge thường được chia tách bằng sub-interface; OVS có thể quản lý nhiều VLAN trên một bridge nhờ OVS Internal Port và VLAN tag.

## 1. VLAN trên Linux Bridge

Linux Bridge truyền thống tạo sub-interface theo định dạng:

```text
<tên-giao-diện>.<VLAN_ID>
```

Ví dụ cấu hình Bond VLAN 70:

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

- `vlan-raw-device bond0`: xác định Bond làm giao diện vật lý của VLAN.
- `bridge-ports bond0.70`: gắn sub-interface đã lọc VLAN vào bridge.
- Switch vật lý kết nối đến Bond phải cấu hình Trunk/Tagged VLAN 70.

## 2. Trunk nhiều VLAN trên Linux Bridge

```bash
auto bond0
iface bond0 inet manual
        bond-slaves enpxxxs0fxnpx enpxxxs0fxnpx
        bond_miimon 100
        bond-mode 802.3ad
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

Khi dùng `802.3ad`, switch vật lý phải cấu hình LACP đối ứng.

> Giới hạn của mô hình này: mỗi bridge thường chỉ phục vụ một VLAN. Khi cần nhiều VLAN cho VM, phải tạo thêm các cặp `bond0.<VLAN_ID>` và `vmbrX` tương ứng.

## 3. VLAN trên OVS Bridge

Trong mô hình OVS, một bridge chính có thể phục vụ nhiều phân đoạn mạng thông qua `OVSIntPort`:

```bash
auto vlan_MGT
iface vlan_MGT inet static
        address 192.168.xx.xx/24
        gateway 192.168.xx.x
        ovs_type OVSIntPort
        ovs_bridge vmbr0
        ovs_options tag=VLAN_MGT_ID

auto vlan_web
iface vlan_web inet static
        address 10.xx.xx.xx/24
        ovs_type OVSIntPort
        ovs_bridge vmbr0
        ovs_options tag=VLAN_WEB_ID
```

- Chỉ đặt gateway trên mạng quản trị MGT.
- `ovs_type OVSIntPort`: port nội bộ của OVS Bridge.
- `ovs_bridge`: bridge sở hữu port.
- `ovs_options tag=<VLAN_ID>`: gắn VLAN tag cho port.

## 4. Cấu hình OVS Bridge tổng

```bash
auto vmbr0
iface vmbr0 inet manual
        ovs_type OVSBridge
        ovs_ports bond0 vlan_MGT vlan_CLS vlan_WEB

auto bond0
iface bond0 inet manual
        ovs_bonds ens1xx ens2xx
        ovs_type OVSBond
        ovs_bridge vmbr0
        ovs_options bond_mode=active-backup
```

Trên switch vật lý, port nối với Bond phải được cấu hình Trunk để cho phép các VLAN cần sử dụng.

## 5. Khi nào dùng OVS cho VLAN

- Một host đơn lẻ thường chỉ cần hai VLAN: quản trị và dịch vụ.
- Cluster lớn có nhiều VLAN MGT, CLS, CEPH và migration thì OVS giúp quy hoạch tập trung trên một bridge.
- Linux Bridge dễ hiểu và phù hợp vài VLAN nhưng cấu hình sẽ dài và rối khi số VLAN tăng nhiều.

## 6. Hình minh họa từ tài liệu

![VLAN Linux Bridge - trang 1](assets/img/proxmox-ceph/cau-hinh-vlan-tren-linux-bridge-va-ovs/page-1.png)

*Hình 1: Sub-interface VLAN trên Linux Bridge và cấu hình Bond VLAN.*

![Trunk nhiều VLAN - trang 2](assets/img/proxmox-ceph/cau-hinh-vlan-tren-linux-bridge-va-ovs/page-2.png)

*Hình 2: Cấu hình Trunk nhiều VLAN bằng Bond và nhiều bridge.*

![VLAN trên OVS - trang 3](assets/img/proxmox-ceph/cau-hinh-vlan-tren-linux-bridge-va-ovs/page-3.png)

*Hình 3: OVSIntPort, VLAN tag và mô hình mạng quản trị/dịch vụ.*

![Cấu hình OVS Bridge tổng - trang 4](assets/img/proxmox-ceph/cau-hinh-vlan-tren-linux-bridge-va-ovs/page-4.png)

*Hình 4: Cấu hình tổng bond0 và vmbr0 cho nhiều VLAN.*

> Nguồn: Cấu hình VLAN.pdf
