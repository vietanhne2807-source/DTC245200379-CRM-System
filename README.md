# ĐỀ 4: HỆ THỐNG CRM CHĂM SÓC KHÁCH HÀNG (DOCKER COMPOSE)

## 1. Thông tin Sinh viên thực hiện
- **Họ và tên:** Nguyễn Trần Việt Anh
- **Mã số sinh viên:** DTC245200379
- **Chủ đề:** Đề 4 – Hệ thống CRM Chăm sóc Khách hàng (Quản lý khách hàng, liên hệ, lịch sử tương tác)

## 2. Kiến trúc Hệ thống & Công nghệ sử dụng
Hệ thống được đóng gói và triển khai hoàn toàn bằng **Docker Compose** với 11 containers chia thành 3 phân vùng mạng cô lập (`frontend_net`, `backend_net`, `monitor_net`):
1. **Ứng dụng Web CRM (`crm_web`):** Python Flask + Gunicorn (quản lý khách hàng, người liên hệ, lịch sử tương tác).
2. **Cơ sở dữ liệu (`crm_postgres`):** PostgreSQL 15 Alpine (khởi tạo tự động qua `db/init.sql`).
3. **Công cụ quản trị DB (`crm_pgadmin`):** pgAdmin 4.
4. **Reverse Proxy (`crm_nginx`):** Nginx 1.25 Alpine cấu hình HTTPS tự ký (TLSv1.2/1.3) và Security Headers.
5. **Hệ thống Giám sát (`crm_prometheus`, `crm_grafana`, `crm_cadvisor`, `crm_nginx_exporter`, `crm_postgres_exporter`):** Thu thập metrics và hiển thị Dashboard tự động.
6. **Hệ thống Log tập trung (`crm_loki`, `crm_promtail`):** Thu thập log từ toàn bộ container và truy vấn qua LogQL.

## 3. Hướng dẫn Triển khai
Chạy các lệnh sau trên Terminal để khởi động toàn bộ hệ thống:

    git clone https://github.com/DTC245200379/DTC245200379-CRM-System.git
    cd DTC245200379_CRM
    docker compose up -d --build
    docker compose ps

## 4. Cổng dịch vụ & Thông tin truy cập
| Dịch vụ | Đường dẫn truy cập | Tài khoản / Ghi chú |
| :--- | :--- | :--- |
| **Web CRM (HTTPS)** | `https://localhost` | Giao diện chính (qua Nginx Reverse Proxy) |
| **pgAdmin 4** | `http://localhost:5050` | `vietanh.dtc245200379@ictu.edu.vn` / `PgAdminWeb@2026!379` |
| **Grafana** | `http://localhost:3000` | `admin_vietanh` / `Grafana@2026!Secure379` |
| **Prometheus** | `http://localhost:9090` | Kiểm tra `/targets` |
| **Loki API** | `http://localhost:3100/ready` | Hệ thống lưu trữ Log tập trung |

## 5. Các câu truy vấn LogQL mẫu (trên Grafana Explore -> Loki)
- **Query 1 (Lọc log nghiệp vụ ứng dụng CRM):**
  `{job="container_logs"} |= "CRM-APP"`
- **Query 2 (Lọc các truy cập HTTP GET thành công - Status 200):**
  `{job="container_logs"} |= "GET /" |= "200"`
- **Query 3 (Thống kê lưu lượng log theo luồng trong 5 phút):**
  `sum by (stream) (count_over_time({job="container_logs"}[5m]))`

## 6. Các biện pháp Bảo mật (Hardening) đã áp dụng
1. **Non-root Container:** Ứng dụng `crm_web` chạy dưới quyền user `crmappuser` (UID `10001`), không dùng quyền `root`.
2. **Network Isolation:** Tách biệt mạng `frontend_net`, `backend_net` và `monitor_net`. Database PostgreSQL không mở cổng ra ngoài máy chủ host.
3. **Database Least Privilege:** Ứng dụng web kết nối vào DB bằng tài khoản `crm_user` chỉ có quyền `SELECT, INSERT, UPDATE, DELETE`, không dùng tài khoản `postgres`.
4. **Mật khẩu mạnh & Biến môi trường:** Toàn bộ mật khẩu phức tạp được quản lý tập trung qua file `.env`.
5. **Nginx HTTPS & Security Headers:** Chuyển hướng HTTP sang HTTPS (TLSv1.2/1.3), ẩn phiên bản (`server_tokens off`) và bật `X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Strict-Transport-Security`, `Referrer-Policy`.
