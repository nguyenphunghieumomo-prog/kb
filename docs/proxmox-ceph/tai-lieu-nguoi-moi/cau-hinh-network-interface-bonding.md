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

Trong bài viết này ta sẽ xem cách cấu hình network trên Proxmox

## 1. Cấu hình Interfaces

Mẫu cấu hình sẽ như sau:

```bash
auto lo
iface lo inet loopback

auto enp24s0f0np0
iface enp24s0f0np0 inet manual

auto enp24s0f1np1
iface enp24s0f1np1 inet manual
```

Giải thích:

`auto <tên_iface>`: interface sẽ tự khởi động cùng hệ thống.

`iface <tên_iface> inet manual`: khai báo interface tồn tại nhưng không gán IP trực tiếp — vì NIC này sẽ được đưa vào bond/bridge phía sau, không dùng độc lập.

Tên NIC (`enp24s0f0np0`, `ens3f0np0`, `eno1np0`...) là do udev đặt theo tên hãng/slot, mỗi máy có thể khác nhau — luôn kiểm tra bằng lệnh `ip a` trước khi cấu hình.

## 2. Cấu hình Bonding (gộp nhiều NIC)

Mục đích: gộp 2 (hoặc nhiều) card mạng vật lý thành 1 interface logic (`bond0`) để:

- Tăng khả năng chịu lỗi (1 dây đứt/switch die vẫn chạy).
- Tăng băng thông (tùy mode).

## 2.1. Linux Bonding (khi ta dùng cấu hình theo kiểu linux bridge)

Cấu hình sẽ như này:

```bash
auto bond0
iface bond0 inet manual
        bond_slaves enp24s0f1np1 enp24s0f0np0
        bond_miimon 100
        bond-mode active-backup
```

Giải thích:

`bond_slaves`: danh sách NIC vật lý tham gia bond.

`bond_miimon 100`: kiểm tra trạng thái link mỗi 100ms để phát hiện đứt cáp/failover.

`bond-mode active-backup`: 1 NIC active, 1 NIC dự phòng — switch vật lý không cần cấu hình port-channel/LACP phía switch.

| Mode                    | Cơ chế hoạt động                         | Yêu cầu phía Switch vật lý |
|---|---|---|
| balance-rr (Round-Robin) | Truyền các gói tin theo thứ tự tuần tự từ card đầu tiên đến card cuối cùng. Giúp gộp băng thông tối đa cho cả 1 kết nối đơn lẻ. | Bắt buộc cấu hình gộp cổng tĩnh (Static Link Aggregation / EtherChannel) trên Switch. |
| active-backup (Dự phòng) | Chỉ có 1 card active chạy,  các card khác standby. Khi card chính đứt kết nối, card phụ lập tức lên thay. | Không yêu cầu cấu hình gì trên Switch vật lý. |
| balance-xor | Cân bằng tải luồng ra dựa trên thuật toán hăm (Hash policy) của địa chỉ MAC hoặc IP nguồn/đích. Các gói tin đi đến cùng một đích sẽ luôn đi cố định trên một card. | Bắt buộc cấu hình gộp cổng tĩnh (Static Link Aggregation / EtherChannel) trên Switch. |
| broadcast | Truyền đồng thời tất cả gói tin ra toàn bộ các card mạng thành viên. | Bắt buộc cấu hình trên Switch hỗ trợ nhận gói tin trùng lặp. |
| LACP (802.3ad) | Chế độ gộp cổng động tiêu chuẩn quốc tế. Sử dụng giao thức LACP để tự động bắt tay, gom băng thông và kiểm tra lỗi link giữa Server và Switch. | Bắt buộc cấu hình LACP (Dynamic Link Aggregation / Dynamic Port-Channel) trên Switch. |
| balance-tlb (Transmit LB) | Chỉ cân bằng tải luồng dữ liệu đi ra (gửi đi) dựa trên tải của từng card mạng. Luồng dữ liệu đi vào (nhận về) vẫn chỉ đi qua 1 card mạng duy nhất. | Không yêu cầu cấu hình gì trên Switch vật lý. |
| balance-alb (Adaptive LB) | Cân bằng tải toàn diện cho cả luồng dữ liệu đi ra và đi vào. Sử dụng cơ chế bóc tách và thay đổi gói tin ARP (ARP negotiation) để điều phối luồng nhận. | Không yêu cầu cấu hình gì trên Switch vật lý. |

## 2.2. OVS Bonding (khi ta dùng cấu hình theo kiểu OVS Bridge)

Cấu hinh:

```bash
auto bond0
iface bond0 inet manual
        ovs_bonds ens3f1np1 ens3f0np0
        ovs_type OVSBond
        ovs_bridge vmbr0
        ovs_options bond_mode=active-backup
```

Giải thích:

‘ovs_bonds ens3f1np1 ens3f0np0’: Danh sách các card mạng (NIC) vật lý tham gia vào nhóm gộp cổng (Bonding) thuộc kiến trúc Open vSwitch (OVS).

‘ovs_type OVSBond’: Định nghĩa loại giao diện ảo này là một Bond của Open vSwitch, giúp hệ thống phân biệt với cấu hình Linux Bond truyền thống.

‘ovs_bridge vmbr0’: Chỉ định rõ ràng cổng Bond này sẽ được ghim (gắn) trực tiếp vào Switch ảo nào (ở đây là OVS Bridge vmbr0). Trong cấu hình OVS, việc gán trực tiếp như thế này giúp luồng dữ liệu được quản lý tập trung và chuẩn xác hơn.

‘ovs_options bond_mode=active-backup’: Cấu hình chế độ chạy cho Bond. Ở chế độ active-backup, tại một thời điểm chỉ có 1 card mạng thực hiện truyền nhận dữ liệu (Active), card còn lại sẽ ở trạng thái chờ (Backup). Nếu card active gặp sự cố (đứt cáp, sập nguồn), card backup sẽ ngay lập tức chuyển sang active để duy trì kết nối. Giống như Linux Bond, chế độ này không yêu cầu thiết bị switch vật lý phía trên phải cấu hình Port-Channel hay LACP.

Ngoài options trên OVS có khá nhiều tùy chọn để ta setup như:

Cấu hình Cổng Access: `ovs_options tag=10` → Mọi gói tin đi vào cổng này nếu chưa có tag sẽ được OVS tự động gắn thẻ (tag) 10, và khi đi ra ngoài sẽ được bóc tag (untagged) để trả về dữ liệu thô cho thiết bị/máy ảo.

Hoặc còn có thể cấu hình trunk, native Vlan …

Một số mode cấu hình bond trên OVS

| Mode | Cơ chế hoạt động | Yêu cầu phía Switch vật lý |
|---|---|---|
| active-backup | Chỉ có 1 card chạy thực tế, các card còn lại ở trạng thái chờ. Tự động chuyển đổi (Failover) ngay lập tức khi card chính đứt cáp. | Không yêu cầu cấu hình gì trên Switch vật lý. |
| balance-slb | Cân bằng tải luồng dữ liệu đi ra dựa trên địa chỉ MAC nguồn của máy ảo (VM). Switch chỉ cần chung mạng và bật tính năng tự học địa chỉ MAC (MAC learning). | Không yêu cầu cấu hình LACP. Mỗi VM được phân bổ đi theo một card riêng để tối ưu tổng băng thông. |
| LACP (balance-slb) | Giống cơ chế cân bằng tải theo MAC nguồn của balance-slb. Có thêm giao thức LACP chủ động giám sát trạng thái bắt tay giữa Host và Switch. | Bắt buộc bật LACP (Link Aggregation / Dynamic Port-Channel) trên các cổng tương ứng của Switch. |
| LACP (balance-tcp) | Chế độ cân bằng tải mạnh nhất. Bóc tách luồng dữ liệu chi tiết theo từng kết nối TCP/UDP (IP/Port nguồn-đích). Một VM chạy nhiều kết nối có thể tận dụng băng thông của cả 2 card cùng lúc. | Bắt buộc bật LACP (Link Aggregation / Dynamic Port-Channel) trên Switch vật lý. |

Đánh giá:

Linux Bridge: Khi bạn muốn chia VLAN, bạn phải tạo từng giao diện ảo riêng lẻ hoặc bật tính năng vlan-aware rồi gõ số VLAN vào phần cứng của VM. Cấu hình file text sẽ bị dài và rối nếu hệ thống có hàng trăm VLAN.

OVS: Nó quản lý VLAN theo kiến trúc của một Switch vật lý thực thụ (Cisco/HP...). Bạn có thể cấu hình một Port của OVS đóng vai trò là Trunk, Access, hoặc Native VLAN rất dễ dàng và tường minh thông qua các tùy chọn (ovs_options).

> Nguồn: Cấu hình Network Interface, Bonding.pdf

balance-rr   card đầu tiên đến card cuối cùng.                Bắt buộc cấu hình gộp cổng tĩnh
(Round-                                                       (Static Link Aggregation /
Robin)       • Giúp gộp băng thông tối đa cho cả 1 kết        EtherChannel) trên Switch.
             nối đơn lẻ.

             • Chỉ có 1 card active chạy, các card khác
active-
             standby.
backup                                                        Không yêu cầu cấu hình gì trên
(Dự                                                           Switch vật lý.
             • Khi card chính đứt kết nối, card phụ lập tức
phòng)
             lên thay.

             • Cân bằng tải luồng ra dựa trên thuật toán
balance-     hăm (Hash policy) của địa chỉ MAC hoặc IP        Bắt buộc cấu hình gộp cổng tĩnh
xor                                                           nguồn/đích.  (Static Link Aggregation /
                                                              EtherChannel) trên Switch.
             • Các gói tin đi đến cùng một đích sẽ luôn đi
             cố định trên một card.

             • Truyền đồng thời tất cả gói tin ra toàn bộ     Bắt buộc cấu hình trên Switch hỗ trợ
broadcast
             các card mạng thành viên.                        nhận gói tin trùng lặp.

              • Chế độ gộp cổng động tiêu chuẩn quốc tế.
 LACP                                                       Bắt buộc cấu hình LACP (Dynamic
              • Sử dụng giao thức LACP để tự động bắt       Link Aggregation / Dynamic Port-
 (802.3ad)
              tay, gom băng thông và kiểm tra lỗi link      Channel) trên Switch.
              giữa Server và Switch.

              • Chỉ cân bằng tải luồng dữ liệu đi ra (gửi
 balance-
              đi) dựa trên tải của từng card mạng.
 tlb                                                        Không yêu cầu cấu hình gì trên
 (Transmit                                                  Switch vật lý.
 LB)          • Luồng dữ liệu đi vào (nhận về) vẫn chỉ đi
              qua 1 card mạng duy nhất.

              • Cân bằng tải toàn diện cho cả luồng dữ
 balance-     liệu đi ra và đi vào.
 alb                                                        Không yêu cầu cấu hình gì trên
 (Adaptive    • Sử dụng cơ chế bóc tách và thay đổi gói     Switch vật lý.
 LB)          tin ARP (ARP negotiation) để điều phối
              luồng nhận.

  Mode                Cơ chế hoạt động                          Yêu cầu phía Switch vật lý

            • Chỉ có 1 card chạy thực tế, các card
            còn lại ở trạng thái chờ
 active-
 backup                                              Không yêu cầu cấu hình gì trên Switch vật lý.
            • Tự động chuyển đổi (Failover) ngay
            lập tức khi card chính đứt cáp

             • Cân bằng tải luồng dữ liệu đi ra dựa
             trên địa chỉ MAC nguồn của máy ảo        Không yêu cầu cấu hình LACP.
 balance-    (VM).
 slb                                                  • Switch chỉ cần chung mạng và bật tính năng
             • Mỗi VM được phân bổ đi theo một        tự học địa chỉ MAC (MAC learning).
             card riêng để tối ưu tổng băng thông.

             • Giống cơ chế cân bằng tải theo MAC
             nguồn của balance-slb.                   Bắt buộc bật LACP (Link Aggregation /
 LACP
 (balance-                                            Dynamic Port-Channel) trên các cổng tương
             • Có thêm giao thức LACP chủ động
 slb)                                                 ứng của Switch.
             giám sát trạng thái bắt tay giữa Host
             và Switch.

             • Chế độ cân bằng tải mạnh nhất.

             • Bóc tách luồng dữ liệu chi tiết theo
 LACP        từng kết nối TCP/UDP (IP/Port nguồn-
                                                      Bắt buộc bật LACP (Link Aggregation /
 (balance-   đích).
 tcp)                                                 Dynamic Port-Channel) trên Switch vật lý.

> Nguồn: Cấu hình Network Interface, Bonding.pdf
