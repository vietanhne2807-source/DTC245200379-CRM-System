CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    company VARCHAR(120),
    status VARCHAR(30) DEFAULT 'Tiềm năng',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) ON DELETE CASCADE,
    contact_name VARCHAR(100) NOT NULL,
    position VARCHAR(80),
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS interactions (
    id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(id) ON DELETE CASCADE,
    channel VARCHAR(50) NOT NULL,
    summary TEXT NOT NULL,
    staff_name VARCHAR(100) DEFAULT 'Nguyễn Trần Việt Anh (DTC245200379)',
    interaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (full_name, email, phone, company, status) VALUES
('Trần Minh Tuấn', 'tuan.tran@viettel.com.vn', '0988123456', 'Viettel Thái Nguyên', 'Đang hợp tác'),
('Lê Thị Hương', 'huong.le@fpt.com', '0912345678', 'FPT Software', 'Tiềm năng'),
('Phạm Quốc Bảo', 'bao.pham@vnpt.vn', '0977654321', 'VNPT Thái Nguyên', 'Mới đăng ký');

INSERT INTO contacts (customer_id, contact_name, position, phone, email) VALUES
(1, 'Nguyễn Hoàng Nam', 'Trưởng phòng Kỹ thuật', '0988111222', 'nam.nh@viettel.com.vn'),
(2, 'Đỗ Thu Trang', 'Chuyên viên Mua sắm', '0912333444', 'trang.dt@fpt.com'),
(3, 'Hoàng Văn Kiên', 'Giám đốc Chi nhánh', '0977555666', 'kien.hv@vnpt.vn');

INSERT INTO interactions (customer_id, channel, summary, staff_name) VALUES
(1, 'Gọi điện', 'Tư vấn gia hạn gói dịch vụ Cloud Server năm 2026', 'Nguyễn Trần Việt Anh (DTC245200379)'),
(2, 'Email', 'Gửi báo giá giải pháp CRM doanh nghiệp và hẹn lịch demo', 'Nguyễn Trần Việt Anh (DTC245200379)'),
(3, 'Gặp trực tiếp', 'Hỗ trợ kỹ thuật tích hợp hệ thống cơ sở dữ liệu PostgreSQL', 'Nguyễn Trần Việt Anh (DTC245200379)');

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'crm_user') THEN
        CREATE USER crm_user WITH PASSWORD 'CrmApp@2026!Secure379';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE crm_db TO crm_user;
GRANT USAGE ON SCHEMA public TO crm_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO crm_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO crm_user;
