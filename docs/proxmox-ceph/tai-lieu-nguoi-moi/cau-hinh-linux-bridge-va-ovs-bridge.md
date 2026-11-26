---
title: Cấu hình Linux Bridge và OVS Bridge trên Proxmox
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, linux bridge, ovs, vmbr0, networking
status: draft
updated: 2026-11-26
summary: Cấu hình Linux Bridge và Open vSwitch Bridge, kèm ưu nhược điểm và mô hình VLAN/Trunk.
source: Cấu hình Bridge.pdf
review_note:
---

# Cấu hình Linux Bridge và OVS Bridge trên Proxmox

Linux Bridge và Open vSwitch (OVS) đều tạo Switch ảo để kết nối máy chủ, VM và Container với mạng vật lý. Linux Bridge phù hợp mô hình đơn giản; OVS phù hợp hơn khi cần quản lý nhiều VLAN hoặc quy hoạch mạng phức tạp.

## 1. Linux Bridge

### 1.1. Access VLAN

Ví dụ cấu hình Linux Bridge `vmbr0` với cổng vật lý `ens18`:

```bash
auto vmbr0
iface vmbr0 inet static
        address 192.168.70.109/24
        gateway 192.168.70.1
        bridge-ports ens18
        bridge-stp off
        bridge-fd 0
```

- `auto vmbr0`: khởi động bridge cùng hệ thống.
- `bridge-ports ens18`: gắn NIC vật lý vào bridge.
- `address`: đặt IP quản trị trực tiếp trên bridge.
- `bridge-stp off`: tắt STP khi không cần; có thể cần kích hoạt lại theo thiết kế mạng.
- `bridge-fd 0`: bridge không chờ forwarding delay của STP.

Nếu cổng Switch vật lý nối với `ens18` được đặt Access VLAN 10, các VM và VM port gắn vào `vmbr0` sẽ hoạt động trong VLAN 10.

### 1.2. Linux Bridge qua Bond và VLAN

Khi Switch vật lý dùng Trunk cho VLAN 70:

```bash
auto vmbr0
iface vmbr0 inet static
        address 192.168.70.147/24
        gateway 192.168.70.1
        bridge-ports bond0.70
        bridge-stp off
        bridge-fd 0
```

Trong ví dụ này, `bond0.70` là sub-interface VLAN 70 của Bond `bond0`. Bridge nhận lưu lượng đã được gắn thẻ VLAN và gán IP quản trị của host.

### 1.3. Ưu và nhược điểm

**Ưu điểm Linux Bridge:**

- Cấu hình đơn giản, trực quan.
- Dễ cô lập và xử lý lỗi.
- Hiệu năng cao.
- VM không cần tự cấu hình VLAN trong mô hình Access.

**Nhược điểm Linux Bridge:**

- Tốn nhiều NIC hoặc bridge khi mở rộng nhiều VLAN.
- VM thuộc VLAN khác nhau thường phải có cặp NIC/bridge tương ứng.

## 2. OVS Bridge

Ví dụ một OVS Bridge dùng Bond và nhiều VLAN:

```bash
auto vmbr0
iface vmbr0 inet manual
        ovs_type OVSBridge
        ovs_ports bond0 vlan70 vlan71 vlan72
```

`vmbr0` không gán IP trực tiếp ở ví dụ này. Địa chỉ quản trị đặt trên `OVSIntPort` riêng, ví dụ port VLAN 70.

- `ovs_type OVSBridge`: khai báo đây là OVS Bridge.
- `ovs_ports`: liệt kê Bond và các OVS VLAN Internal Port thuộc bridge.
- `OVSIntPort`: port nội bộ mang IP của một mạng VLAN.

### 2.1. Ưu điểm OVS

- Một bridge có thể phục vụ nhiều VLAN.
- Hỗ trợ cấu hình VLAN tag trực tiếp trên port VM hoặc Container.
- Dễ mở rộng VLAN mà không cần thêm NIC vật lý cho từng VLAN.
- Hỗ trợ Bonding và nhiều chế độ cân bằng tải.
- Phù hợp cluster nhiều host, nhiều mạng logic như MGT, CLS và CEPH.

### 2.2. Nhược điểm OVS

- Cấu hình phức tạp hơn Linux Bridge.
- VLAN tag và Bond mode sai có thể ảnh hưởng nhiều mạng cùng lúc.
- Cần kiểm tra kỹ switch vật lý và cấu hình Trunk.

> Nguồn: Cấu hình Bridge.pdf
