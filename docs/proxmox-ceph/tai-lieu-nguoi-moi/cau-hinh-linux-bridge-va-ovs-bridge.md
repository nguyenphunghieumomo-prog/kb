---
title: Cấu hình Linux Bridge và OVS Bridge trên Proxmox
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, linux bridge, ovs, vmbr0, networking
status: draft
updated: 2026-11-27
summary: Cấu hình Linux Bridge và Open vSwitch Bridge, kèm ưu nhược điểm và mô hình VLAN/Trunk.
source: Cấu hình Bridge.pdf
review_note:
---

# Cấu hình Linux Bridge và OVS Bridge trên Proxmox

Trong bài viết này ta sẽ xem cấu hình của Linux bridge và OVS bridge như nào

## 3.1. Linux bridge

Thứ nhất, cấu hình linux-bridge mode access, đây là cấu hình default khi ta cài đặt OS (switch vật lý cấu hình mode access)

```bash
auto vmbr0
iface vmbr0 inet static
        address 192.168.70.109/24
        gateway 192.168.70.1
        bridge-ports ens18
        bridge-stp off
        bridge-fd 0
```

‘auto vmbr0 (Virtual Bridge 0)’: đây là Switch ảo chính được tạo ra.

‘bridge-ports ens18’: Dòng này cực kỳ quan trọng, nó thực hiện "gắn" (bridge) card vật lý ens18 vào Switch ảo vmbr0. Tất cả lưu lượng dữ liệu đi qua vmbr0 sẽ đi ra ngoài môi trường vật lý thông qua card ens18.

‘address 192.168.70.109/24’: IP quản trị của chính host Proxmox được gán trực tiếp vào Switch ảo này.

`bridge-stp off`: tắt Spanning Tree Protocol (thường tắt vì đã có bonding lo việc failover, STP có thể gây delay convergence không cần thiết).

`bridge-fd 0`: forwarding delay = 0 (bridge lên nhanh, không delay 15s theo mặc định STP).

Ví dụ: Nếu cổng Switch vật lý nối với ens18 được cấu hình là Access VLAN 10, thì toàn bộ các máy ảo kết nối vào vmbr0 trên host Proxmox mặc nhiên sẽ nhận IP và hoạt động trong VLAN 10.

Đánh giá linux bridge:

Ưu điểm: Cấu hình cực kỳ đơn giản, trực quan, dễ cô lập lỗi, hiệu năng cao và máy ảo không cần phải biết gì về cấu hình VLAN.

Nhược điểm: Thiếu linh hoạt khi cần mở rộng. Nếu bạn muốn máy ảo VM_A thuộc VLAN 10, máy ảo VM_B thuộc VLAN 20, bạn bắt buộc phải có nhiều card mạng vật lý riêng biệt nối vào các cổng Access tương ứng trên Switch

Thứ hai cấu hình linux-bridge bonding vlan 70 (switch vật lý cấu hình trunk allow vlan70/all)

```bash
auto vmbr0
iface vmbr0 inet static
        address 192.168.70.147/24
        gateway 192.168.70.1
        bridge-ports bond0.70
        bridge-stp off
        bridge-fd 0
```

`bridge-ports`: interface nào được gắn vào bridge (ở đây là `bond0.70` — sub-interface VLAN 70 của bond0, xem phần VLAN bên dưới).

## 3.2. OVS Bridge

Cấu hình OVS Bridge bonding (trên SW vật lí cần cấu hình trunk allow vlanx/all theo nhu cầu)

```bash
auto vmbr0
iface vmbr0 inet manual
        ovs_type OVSBridge
        ovs_ports bond0 vlan70 vlan71 vlan72 ….
```

`vmbr0` ở đây không có IP trực tiếp (`inet manual`) — vì địa chỉ quản lý IP sẽ nằm ở một `OVSIntPort` riêng (`vlan70`), bridge chỉ đóng vai trò switch ảo.

`ovs_ports`: liệt kê tất cả port thuộc bridge này, gồm bond uplink và các VLAN internal port.

Đánh giá về OVS

Ưu điểm OVS:

- Rất linh hoạt: 1 bridge duy nhất phục vụ được nhiều VLAN, không cần nhiều NIC vật lý cho mỗi VLAN như Linux Bridge.
- VM có thể tự chọn VLAN qua tag ngay trên port ảo (OVSIntPort/OVSPort), dễ mở rộng thêm VLAN mới mà không cần đụng phần cứng.
- Bonding tích hợp sẵn trong OVS, hỗ trợ nhiều thuật toán cân bằng tải (LACP, balance-slb...) linh hoạt hơn.
- Phù hợp mô hình cluster nhiều host, nhiều mạng logic (MGT/CLS/CEPH...) chạy chung hạ tầng vật lý.

Nhược điểm OVS:

- Cấu hình phức tạp hơn, người mới cần tìm hiểu kĩ
- Cấu hình sai (đặc biệt VLAN tag, trunk) ảnh hưởng cả cụm vì nhiều VLAN dùng chung 1 bridge — rủi ro "một lỗi, ảnh hưởng nhiều mạng" cao hơn.

> Nguồn: Cấu hình Bridge.pdf
