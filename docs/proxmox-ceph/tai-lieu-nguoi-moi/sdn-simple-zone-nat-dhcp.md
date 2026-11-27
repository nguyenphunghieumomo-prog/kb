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

# TRIỂN KHAI PHÂN HỆ MẠNG SOFTWARE-DEFINED NETWORK (SDN SIMPLE ZONE)

## 1. Giới thiệu

Simple Zone là loại zone đơn giản nhất trong SDN của Proxmox, tạo ra 1 private network nội bộ cho các VM/CT trong cùng 1 node, sau đó NAT (SNAT) ra ngoài Internet qua IP Public duy nhất của node đó.

### 1.1. Mục tiêu kĩ thuật

- Thiết lập một phân vùng mạng nội bộ ảo cách ly (Private Network / NAT Network) giữa các máy ảo (VM) chạy chung trên một Node vật lý Proxmox duy nhất.
- Cho phép các máy ảo bên trong mạng nội bộ tự động nhận IP từ máy chủ DHCP.
- Cho phép các máy ảo đi internet ra ngoài thông qua cơ chế SNAT (Source Network Address Translation) chung một địa chỉ IP Public duy nhất của Host Proxmox.

Phù hợp với các trường hợp:

Chỉ có 1 IP Public duy nhất, dùng chung cho cả Proxmox Management và toàn bộ VM bên trong

VM chỉ cần ra Internet (SNAT), và thi thoảng cần mở port cụ thể vào VM (DNAT), không cần range IP Public riêng

Không có nhu cầu định tuyến phức tạp, ít thay đổi cấu hình về sau.

## 2. Cấu hình triển khai

### 2.1. Cài đặt packages cần thiết

Để phân hệ SDN Simple có thể tự cấp phát IP tự động (DHCP) cho các máy ảo, hệ thống yêu cầu cài đặt gói dịch vụ điều phối DHCP (dnsmasq) dưới nền của host proxmox. Bạn vào shell các host proxmox cần cấu hình và thực hiện lệnh cài sau:

```bash
apt update && apt install dnsmasq -y
```

### 2.2. Vô hiệu hóa dịch vụ mặc định của hệ thống

Do Proxmox SDN sẽ tự quản lý và gọi dịch vụ dnsmasq theo cơ chế riêng của nó, Admin bắt buộc phải tắt dịch vụ dnsmasq mặc định của hệ điều hành để tránh tranh chấp tiến trình:

```bash
systemctl disable --now dnsmasq
```

### 2.3. Cấu hình chi tiết trên WebGUI

Bước 1: Tạp phân vùng Simple Zone

Ta truy cập vào Datacenter → SDN → Zones → Add

Ta chọn loại Simple

Sau đó có 1 tab mới sẽ hiện ra

Thông số cần bạn điền như sau:

- ID (Định danh): Tên viết liền không dấu dùng để phân biệt vùng mạng này với các vùng mạng khác trong cụm Datacenter (Ví dụ: dhcpsnat hoặc LAN-Internal).
- MTU (Maximum Transmission Unit): Kích thước tối đa của một gói tin truyền trong mạng ảo này. Cấu hình để mặc định là auto thì hệ thống sẽ tự động tính toán dựa trên card mạng vật lý của Host để tối ưu luồng truyền tải dữ liệu, tránh hiện tượng phân mảnh gói tin.
- Nodes (Nút thành viên): Giới hạn vùng mạng ảo này chỉ hoạt động trên những Node vật lý nào trong Cluster. Cấu hình mặc định là All (No restrictions) nghĩa là tất cả các Node trong cụm đều có thể sử dụng vùng mạng này. Nếu ta muốn cô lập vùng mạng này chỉ chạy duy nhất trên một Node lab cụ thể, ta bấm dropdown chọn riêng Node đó.
- IPAM (IP Address Management - Quản lý địa chỉ IP): Cơ chế quản lý việc cấp phát và ghi nhận trạng thái của các địa chỉ IP trong mạng ảo. Cấu hình mặc định chọn pve thì proxmox sẽ tự động sử dụng cơ sở dữ liệu nội bộ của nó để ghi nhớ xem IP nào đã được cấp cho máy ảo nào, tránh bị trùng lặp cấu hình.
- DNS Server / Reverse DNS Server / DNS Zone: Ý nghĩa: Các trường thông tin dùng để tích hợp vùng mạng này với các hệ thống quản lý tên miền tự động (như PowerDNS hoặc CoreDNS). Tôi chỉ cấu hình kịch bản lab mạng Simple cơ bản nên để trống các ô này.
- automatic DHCP (Tự động cấp phát cấu hình mạng): Đây chính là tính năng cốt lõi để bật máy chủ DHCP Helper cho vùng mạng. Cấu hình: Bắt buộc tích chọn ô này. Khi tích vào đây, dịch vụ ngầm của Proxmox phối hợp với gói dnsmasq mới có thể tự cấp IP, Subnet Mask và Gateway xuống cho các máy ảo một cách tự động khi chúng vừa khởi động lên.

Tôi sẽ cấu hình test như sau:

Tôi đã giới hạn phân vùng mạng ảo này chỉ chạy trên hai Node cụ thể là PROX5 và PROX6 thay vì để tất cả các node trong cụm.

Bước 2: Tạo VNet

Ta truy cập vào Datacenter → SDN → VNets → VNets → Add

Sẽ có 1 tab con hiện ra

- Name (Tên VNet): Ta đặt tên viết liền, không dấu và nên có số thứ tự (Ví dụ: vnet0 hoặc vnet-internal). Tên này sẽ xuất hiện trong danh sách Bridge khi ta cấu hình phần cứng mạng cho VM.
- Alias (Tên gợi nhớ/Biệt danh): Dùng để viết chú thích bằng tiếng Việt có dấu hoặc mô tả nhanh mục đích của card mạng này (Ví dụ: Mạng Private NAT cho khách hàng). Ô này có thể để trống nếu không có nhu cầu.
- Zone (Phân vùng mạng): Ta bấm vào dropdown và chọn chính xác cái Zone dhcpsnat mà tôi vừa tạo thành công ở bước trước. Việc này giúp gán card mạng ảo này chạy dưới cơ chế Simple và DHCP tự động của Zone đó.
- Isolate Ports (Cô lập cổng mạng): Đây là một tính năng bảo mật rất hay (tương tự như Private VLAN). Khi tích chọn ô này, các máy ảo chạy chung trên card mạng vnet0 sẽ bị cấm giao tiếp trực tiếp với nhau (máy ảo này không ping hay hack sang máy ảo kia được), nhưng cả hai máy vẫn có thể đi ra internet và giao tiếp với Gateway bình thường.

VLAN Aware là tính năng biến card mạng ảo (vnet0 hoặc vmbr0) thành một cổng Trunk (Trunk Port) của Switch.

- Khi KHÔNG tích chọn VLAN Aware (Mặc định): Card mạng ảo chỉ hiểu và truyền tải các gói tin thông thường (không có tag VLAN - Untagged). Nó giống như một cái Access Port trên Switch vật lý, chỉ gán cứng cho một VLAN duy nhất.
- Khi CÓ tích chọn VLAN Aware: Card mạng ảo cho phép nhiều tag VLAN khác nhau (VLAN 10, VLAN 20, VLAN 100...) cùng đi qua chung một sợi cáp ảo này. Lúc này, ta có thể cấu hình chia nhỏ VLAN trực tiếp ngay trong phần cài đặt mạng của từng máy ảo (VM) kết nối vào card vnet0.

Tôi sẽ để cấu hình đơn giản như sau:

Bước 3: Định nghĩa dải Subnet và dải IP DHCP

Chọn vào mạng ảo vnet0 vừa tạo → Tại bảng Subnets bên phải, chọn Create.

Ta cấu hình tiếp tab con này:

- Subnet (Dải mạng nội bộ): Lớp mạng Private được cấp phát riêng cho các máy ảo chạy bên trong Node. Cấu hình nhập: 10.0.0.0/24 (Lớp mạng này sẽ cung cấp tối đa 254 địa chỉ IP khả dụng từ 10.0.0.1 đến 10.0.0.254).
- Gateway (Cổng ra mặc định): Địa chỉ IP đại diện cho Host Proxmox đóng vai trò làm Router ảo điều phối lưu lượng mạng cho các VM. Cấu hình nhập: 10.0.0.1 (Địa chỉ IP đầu tiên của dải mạng).
- SNAT (Source Network Address Translation): Cho phép các máy ảo mang dải IP Private (10.0.0.x) "mượn" địa chỉ IP Public vật lý của Host Proxmox để đi ra ngoài Internet. Cấu hình: BẮT BUỘC TÍCH CHỌN. Nếu không tích ô này, máy ảo nhận được IP nhưng sẽ hoàn toàn bị cô lập và không thể truy cập Internet.
- DNS Zone Prefix: Cấu hình: Để trống (Không cần thiết cho mô hình NAT cơ bản)

Tab này để cấu hình dải IP tự động cấp phát cho máy ảo

Tôi sẽ cấu hình dải cấp phát từ 10.0.0.50 → 10.0.0.200

Sau khi xong ta ấn create là xong

Sau khi đã cấu hình xong xuôi hết phần SDN này thì ấn Apply

Chờ 1 lát sẽ dịch vụ sẽ được kích hoạt

Bước 4: Cấu hình Firewall cho phép cấp DHCP và DNS (Nếu có bật Firewall)

Vào Datacenter → Firewall → Add

Cấu hình Rule 1 - cho phép DHCP:

Thông số:

- Direction: in: Cho phép gói tin từ máy ảo đi vào hệ thống lọc.
- Action: ACCEPT: Chấp nhận cho đi qua.
- Interface: vnet0: Áp dụng luật này riêng cho card mạng ảo vnet0.
- Macro: DHCPfwd: Proxmox tự động mở các cổng UDP cần thiết (67 và 68) dành cho dịch vụ DHCP.
- Enable: Đã tích chọn để luật có hiệu lực.

Cấu hình Rule 2 - cho phép DNS:

Thông số cần lưu ý:

- Macro: DNS (Bộ lọc định nghĩa sẵn): Thay vì ta phải gõ thủ công từng thông số như Protocol: udp, Dest. port: 53 (cổng dịch vụ DNS truyền thống), Proxmox cung cấp sẵn một cái khuôn tên là DNS. Chọn cái này, hệ thống tự động hiểu là cho phép luồng lưu lượng chạy qua Port 53 (cả TCP và UDP).
- Destination: 10.0.0.1 (Đích đến): Đây chính là phần "ăn tiền" về mặt bảo mật. Ô này chỉ định rõ: Máy ảo kết nối vào mạng vnet0 chỉ được phép gửi yêu cầu truy vấn DNS về duy nhất địa chỉ 10.0.0.1 (chính là IP Gateway của Host Proxmox đang chạy dịch vụ dnsmasq). Nếu để trống ô này, máy ảo của khách hàng có thể thoải mái cấu hình trỏ DNS đi bất cứ đâu ngoài internet (Ví dụ các DNS lậu, DNS độc hại).

Tôi đã tọa xong 2 Rules

Tiếp đến tôi sẽ thử test dùng 2 VM 117 và 118 trên cùng 1 host xem nhận DHCP được không và ping với nhau xem và ra net không.

Kiểm tra kết quả tôi đã thấy 2 đều nhận DHCP

VM117 → Nhận IP là 10.0.0.52

VM118 → Nhận IP là 10.0.0.51

Cả IP đều trong dãy DHCP đã cấu hình ở trên

ping test cả 2 VM đều ổn

VM117

VM118

Như vậy là bài testing SDN Simple của tôi đã xong.

Lưu ý: Nếu bài này tôi test 2 VM, mỗi VM trên 1 host rồi ping thử xem có thông không → Thì câu trả lời là không.

Vì: Simple Zone sẽ tạo ra 1 VNet bridge riêng biệt trên mỗi node — bridge này không gắn với interface vật lý nào, nên traffic chỉ tồn tại cục bộ trong phạm vi node đó.

Điều này có nghĩa: dù bạn tạo cùng 1 VNet name (vd vnet0) trên cả 2 node, thực chất Proxmox tạo ra 2 bridge độc lập hoàn toàn, mỗi node có 1 gateway/NAT riêng, không hề có tunnel hay kết nối nào giữa 2 node để traffic đi qua.

Vậy có cách nào cấu hình thõa yêu cầu trên?

Câu trả lời là có: ta không dùng vùng mạng loại Simple nữa, mà bắt buộc phải chuyển sang cấu hình vùng mạng loại VXLAN hoặc EVPN. Các loại Zone nâng cao này sẽ tự động tạo một đường ống ngầm (Tunnel) qua cổng vật lý để thông mạng nội bộ giữa các Host với nhau.

> Nguồn: Simple SDN.pdf
