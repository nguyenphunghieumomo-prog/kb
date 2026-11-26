---
title: Triển khai SDN Simple Zone với DHCP và NAT
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, sdn, simple zone, dhcp, dnsmasq, nat, snat
status: draft
updated: 2026-11-26
summary: Hướng dẫn tạo Simple Zone, VNet, subnet DHCP, SNAT và firewall rule cho VM/CT.
source: Simple SDN.pdf
review_note:
---

# Triển khai SDN Simple Zone với DHCP và NAT

Simple Zone là zone đơn giản trong Proxmox SDN. Zone tạo mạng private nội bộ cho VM/Container trên một node, sau đó dùng SNAT để các máy ra Internet qua IP public của host.

## 1. Khi nào dùng Simple Zone

Simple Zone phù hợp khi:

- Chỉ có một IP public dùng chung cho host và VM.
- VM cần ra Internet bằng SNAT.
- Có nhu cầu DNAT hoặc mở port cụ thể vào VM.
- Không cần định tuyến phức tạp hoặc thay đổi mạng thường xuyên.

VM trong mạng private nhận IP từ DHCP và không cần IP public riêng.

## 2. Cài đặt dnsmasq

Chạy trên host Proxmox:

```bash
apt update && apt install dnsmasq -y
```

Tắt dịch vụ dnsmasq mặc định để SDN tự quản lý tiến trình:

```bash
systemctl disable --now dnsmasq
```

Thứ tự chạy dịch vụ là bắt buộc: không nên để cả dịch vụ mặc định và dịch vụ do Proxmox SDN quản lý tranh cổng DHCP.

## 3. Tạo Simple Zone

1. Vào **Datacenter → SDN → Zones**.
2. Chọn **Add**.
3. Chọn loại **Simple**.
4. Nhập thông tin:

- **ID:** Tên viết liền, không dấu để phân biệt zone trong Datacenter.
- **MTU:** Có thể để `auto` để hệ thống tính theo mạng vật lý.
- **Nodes:** Chọn tất cả node hoặc giới hạn một vài node cụ thể.
- **IPAM:** Chọn `pve` để Proxmox lưu trữ và theo dõi IP cấp phát.
- **DNS Server**, **Reverse DNS Server**, **DNS Zone:** Có thể để trống cho lab NAT cơ bản.
- **automatic DHCP:** Bật để tự cấp IP, subnet mask và gateway cho VM/CT.

## 4. Tạo VNet

1. Vào **Datacenter → SDN → VNets**.
2. Chọn **Add**.
3. Cấu hình:

- **Name:** Ví dụ `vnet0` hoặc `vnet-internal`.
- **Alias:** Mô tả mục đích mạng, có thể để trống.
- **Zone:** Chọn zone Simple vừa tạo.
- **Isolate Ports:** Bật nếu VM không được phép giao tiếp trực tiếp với nhau.
- **VLAN Aware:** Bật nếu VNet cần xử lý nhiều VLAN; với mô hình đơn giản nên để mặc định.

## 5. Tạo Subnet và DHCP Range

Tại VNet vừa tạo, chọn **Create Subnet** và cấu hình ví dụ:

- **Subnet:** `10.0.0.0/24`
- **Gateway:** `10.0.0.1`
- **SNAT:** Bật để VM private đi ra Internet qua IP public của host
- **DHCP Range:** `10.0.0.50` đến `10.0.0.200`

Sau khi tạo, nhấn **Apply** để kích hoạt cấu hình SDN.

## 6. Cấu hình Firewall DHCP và DNS

Vào **Datacenter → Firewall** và tạo hai rule.

### Rule cho DHCP

- **Direction:** `in`
- **Action:** `ACCEPT`
- **Interface:** `vnet0`
- **Macro:** `DHCPfwd`
- **Enable:** Bật rule

Macro DHCPfwd hỗ trợ các cổng UDP 67 và 68.

### Rule cho DNS

- **Macro:** `DNS`
- **Destination:** `10.0.0.1`
- **Protocol:** DNS macro cho phép TCP/UDP port 53

Đích DNS chỉ nên giới hạn tại gateway `10.0.0.1` để VM không truy vấn DNS tùy ý ra bên ngoài.

## 7. Kiểm tra VM nhận DHCP

Sau khi Apply và cấu hình VM/CT gắn vào `vnet0`, kiểm tra:

- VM nhận IP trong DHCP range `10.0.0.50-10.0.0.200`.
- VM nhận gateway `10.0.0.1`.
- VM ping được gateway.
- VM ra Internet qua SNAT.
- Hai VM trong mạng private có kết nối lẫn nhau nếu không bật `Isolate Ports`.

Ví dụ trong tài liệu kiểm thử:

- VM 117 nhận IP `10.0.0.52`.
- VM 118 nhận IP `10.0.0.51`.
- Cả hai đều nhận DHCP thành công.

> Nguồn: Simple SDN.pdf
