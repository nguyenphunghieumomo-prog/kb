---
title: Triển khai SDN Simple Zone với DHCP và NAT
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, sdn, simple zone, dhcp, dnsmasq, nat, snat
status: draft
updated: 2026-11-27
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

## 8. Hình minh họa từ tài liệu

![SDN Simple Zone - trang 1](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-01.png)

*Hình 1: Giới thiệu SDN Simple Zone và mục tiêu NAT/DHCP.*

![Cấu hình cài đặt và Simple Zone - trang 2](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-02.png)

*Hình 2: Cài dnsmasq, tắt dịch vụ mặc định và tạo Zone.*

![Thông tin Simple Zone - trang 3](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-03.png)

*Hình 3: Các thông số ID, MTU, Nodes, IPAM và automatic DHCP.*

![Ví dụ cấu hình Zone - trang 4](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-04.png)

*Hình 4: Ví dụ giới hạn Simple Zone trên node PROX5 và PROX6.*

![Tạo VNet - trang 5](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-05.png)

*Hình 5: Cấu hình VNet và liên kết với Simple Zone.*

![Tham số VNet - trang 6](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-06.png)

*Hình 6: Name, Alias, Zone, Isolate Ports và VLAN Aware.*

![Cấu hình VNet đơn giản - trang 7](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-07.png)

*Hình 7: Ví dụ cấu hình VNet vnet0.*

![Tạo Subnet - trang 8](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-08.png)

*Hình 8: Tạo Subnet cho VNet và cấu hình dải mạng private.*

![Cấu hình Subnet và SNAT - trang 9](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-09.png)

*Hình 9: Subnet 10.0.0.0/24, Gateway 10.0.0.1 và SNAT.*

![Cấu hình DHCP range - trang 10](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-10.png)

*Hình 10: Phạm vi cấp phát DHCP từ 10.0.0.50 đến 10.0.0.200.*

![Kích hoạt SDN và Firewall DHCP - trang 11](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-11.png)

*Hình 11: Nhấn Apply và tạo rule cho phép DHCP.*

![Cấu hình Firewall DHCP/DNS - trang 12](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-12.png)

*Hình 12: Rule DHCPfwd, DNS và destination gateway.*

![Kiểm tra DHCP trên VM - trang 13](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-13.png)

*Hình 13: VM117 và VM118 nhận địa chỉ từ DHCP range.*

![Kết quả DHCP VM117/VM118 - trang 14](assets/img/proxmox-ceph/sdn-simple-zone-nat-dhcp/page-14.png)

*Hình 14: Địa chỉ VM117 là 10.0.0.52 và VM118 là 10.0.0.51.*

> Nguồn: Simple SDN.pdf
