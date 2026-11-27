---
title: Tạo Cluster Proxmox VE với 3 node
cat: proxmox-ceph
sub: cluster
type: Quy trình
tags: proxmox, cluster, quorum, join, vlan
status: approved
updated: 2026-11-27
summary: Các bước tạo cluster 3 node PVE1/PVE2/PVE4, lấy Join Information và join node.
source: 1_2_TẠO_CLUSTER.docx
---
# Tạo Cluster Proxmox VE với 3 node

Cluster Proxmox cần **tối thiểu 3 node** để đảm bảo quorum.

## 1. Sơ đồ triển khai

Ví dụ dùng 3 node PVE1, PVE2, PVE4 cùng đấu vào switch NK5 (trunk all VLAN).

![Sơ đồ triển khai 3 node](assets/img/proxmox-ceph/tao-cluster-proxmox-3-node/pve-cluster-so-do.png)

| Node | MGT (vlan70) | CLS (vlan301) | CEPH (vlan302) | Migrate (vlan303) |
|---|---|---|---|---|
| PVE1 | 192.168.70.147/24 | 10.80.101.147/24 | 10.80.102.147/24 | 10.80.103.147/24 |
| PVE2 | 192.168.70.146/24 | 10.80.101.146/24 | 10.80.102.146/24 | 10.80.103.146/24 |
| PVE4 | 192.168.70.148/24 | 10.80.101.148/24 | 10.80.102.148/24 | 10.80.103.148/24 |

## 2. Điều kiện trước khi tạo

- Ping thông giữa cả 3 node trên các dải mạng đã cấu hình.
- IP của mạng Cluster (CLS) đã được đặt trên từng node.

## 3. Tạo cluster trên node đầu tiên

Ở ví dụ này PVE2 được chọn làm master node.

1. Vào **Datacenter** → **Cluster** → **Create Cluster**.
2. Đặt tên cluster, chọn IP của dải CLS (vlan301) của PVE2.
3. Nhấn **Create**.

## 4. Lấy thông tin để join

Trên node vừa tạo cluster: **Datacenter** → **Cluster** → **Join Information** → copy đoạn mã.

![Mã thông tin join cluster](assets/img/proxmox-ceph/tao-cluster-proxmox-3-node/pve-join-information.png)

## 5. Join các node còn lại

Trên từng node còn lại (PVE1, PVE4):

1. **Datacenter** → **Cluster** → **Join Cluster**.
2. Dán đoạn mã Join Information, thông tin cluster sẽ tự hiện ra.
3. Nhập mật khẩu của master node và chọn dải IP CLS phù hợp theo sơ đồ.

## 6. Kết quả

Sau khi join xong, cluster hiển thị đủ 3 node, mỗi node 1 vote.

![Cluster 3 node PVE1, PVE2, PVE4](assets/img/proxmox-ceph/tao-cluster-proxmox-3-node/pve-cluster-3-node.png)

> Nguồn: tài liệu "1.2 Tạo Cluster".
