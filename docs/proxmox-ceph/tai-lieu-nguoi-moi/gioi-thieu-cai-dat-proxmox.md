---
title: Giới thiệu và cài đặt Proxmox VE cho người mới
cat: proxmox-ceph
sub: tai-lieu-nguoi-moi
type: Quy trình
tags: proxmox, beginner, system requirements, iso, installation, gui
status: draft
updated: 2026-11-25
summary: Yêu cầu phần cứng, quy trình cài đặt Proxmox VE bằng ISO và các khu vực chính của giao diện quản trị.
source: 1.1. Yêu cầu về hệ thống.pdf; Cài đặt OS.pdf; Truy cập giới thiệu giao diện cơ bản.pdf
review_note:
---

# Giới thiệu và cài đặt Proxmox VE cho người mới

Bài viết hướng dẫn ba bước đầu khi bắt đầu với Proxmox VE: kiểm tra yêu cầu hệ thống, cài đặt hệ điều hành bằng ISO và truy cập giao diện quản trị.

## 1. Yêu cầu hệ thống

Theo khuyến cáo chính thức từ Proxmox Server Solutions GmbH, cấu hình phần cứng được chia thành hai mức: tối thiểu và khuyến nghị cho Production.

### Cấu hình tối thiểu

| Thành phần | Yêu cầu |
|---|---|
| RAM | Tối thiểu 4 GB để chạy hệ điều hành và các dịch vụ Proxmox VE |
| CPU | 64-bit; Intel EMT64 hoặc AMD-V |
| Ổ cứng | Có dung lượng trống để cài đặt hệ điều hành |
| Mạng | Ít nhất một NIC 1 Gbps |

### Cấu hình khuyến nghị cho Production

- **CPU:** Intel Xeon hoặc AMD EPYC, hỗ trợ tính năng ảo hóa phần cứng Intel VT/AMD-V.
- **RAM:** Tối thiểu 8 GB. Bổ sung RAM theo nhu cầu máy ảo và Container. Với hệ thống lưu trữ Ceph hoặc ZFS, tài liệu khuyến nghị thêm ít nhất 1 GB RAM cho mỗi 1 TB dung lượng lưu trữ.
- **Ổ cứng:** Ưu tiên SSD/NVMe cấp doanh nghiệp. Có thể dùng RAID phần cứng hoặc ZFS để tăng tốc độ và bảo đảm an toàn dữ liệu.
- **Mạng:** Nên dùng card mạng 10 Gbps trở lên cho đồng bộ Cluster, lưu trữ Ceph và Live Migration.

## 2. Chuẩn bị và tạo USB cài đặt

1. Tải file ISO Proxmox VE chính thức từ trang tải của Proxmox.
2. Chọn phiên bản phù hợp; tài liệu ví dụ khuyến nghị bản 8.4 trở lên.
3. Tạo USB Boot bằng Rufus, Ventoy hoặc BalenaEtcher.

Ngoài USB, bạn có thể mount ISO qua iDRAC, iLO hoặc giao diện quản lý server tương tự để cài đặt trên máy chủ vật lý.

## 3. Cài đặt Proxmox VE

1. Cắm USB Boot vào thiết bị cần cài đặt.
2. Cấu hình BIOS/UEFI ưu tiên khởi động từ USB.
3. Chọn **Install Proxmox VE (Graphical)** và nhấn `Enter`.
4. Chọn **I agree** để đồng ý với thỏa thuận sử dụng.
5. Chọn ổ đĩa boot OS tại mục **Target Disk**.

### Cấu hình ổ đĩa

- Với một ổ đĩa, chọn trực tiếp ổ cài đặt tại mục **Target Disk**.
- Với hai ổ đĩa cài ZFS mirror tương đương RAID 1, giữ một ổ làm thành viên mirror và đặt ổ không sử dụng thành `do not use`.
- Màn hình cài đặt có thể hỗ trợ thêm các kiểu ZFS như RAID 5 hoặc RAID 10 tùy phiên bản và số lượng ổ.

Sau khi chọn dung lượng và kiểu Storage, nhấn **Next**.

## 4. Cấu hình vị trí và tài khoản

1. Chọn quốc gia tương ứng, ví dụ **Việt Nam**.
2. Nhấn **Next**.
3. Đặt mật khẩu cho tài khoản `root`.
4. Điền email quản lý.

> Cần bảo mật mật khẩu `root` và không ghi mật khẩu thực tế vào tài liệu công khai.

## 5. Cấu hình mạng

Các thông tin cần nhập:

- **Management Interface:** Card mạng vật lý dùng để quản lý server.
- **Hostname (FQDN):** Tên máy chủ đầy đủ theo dạng `Tên_Server.Tên_Miền`.
- **IP Address (CIDR):** Địa chỉ IP quản lý kèm subnet mask.
- **Gateway:** IP gateway của dải mạng.
- **DNS Server:** Máy chủ phân giải tên miền.
- **Pin network interface names:** Có thể bật trên phiên bản mới để cố định tên card mạng theo phần cứng.

Sau khi nhập đầy đủ, nhấn **Next**, kiểm tra lại toàn bộ thông tin và chọn **Install**.

Ví dụ mạng quản lý trong tài liệu: `https://192.168.69.137:8006`.

## 6. Truy cập giao diện quản trị

Sau khi cài đặt hoàn tất, truy cập:

```text
https://<IP-quản-lý>:8006
```

Đăng nhập với:

- **Username:** `root`
- **Password:** Mật khẩu đã thiết lập khi cài đặt hệ điều hành
- **Realm:** `Linux PAM standard authentication`

## 7. Các khu vực chính của giao diện

Giao diện Proxmox VE gồm 4 khu vực:

1. **Thanh công cụ phía trên:** Tạo VM hoặc Container, tìm kiếm và quản lý tài khoản.
2. **Server View bên trái:** Cây quản trị từ Datacenter, Node vật lý, VM/Container đến Storage.
3. **Main Panel ở giữa:** Hiển thị thông tin chi tiết của đối tượng đang được chọn.
4. **Tab Summary:** Theo dõi CPU, RAM, dung lượng ổ, thông tin phần cứng và uptime.
5. **Log/Tasks phía dưới:** Hiển thị nhật ký tác vụ theo thời gian thực như bật/tắt VM, backup hoặc lỗi phát sinh.

> Nguồn: 1.1. Yêu cầu về hệ thống.pdf; Cài đặt OS.pdf; Truy cập giới thiệu giao diện cơ bản.pdf
