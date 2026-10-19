FROM python:3.11-slim

WORKDIR /app

# Cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn ứng dụng
COPY . .

# HARDENING: Tạo non-root user (UID 10001) và chuyển quyền sở hữu thư mục
RUN groupadd -g 10001 crmgroup && \
    useradd -u 10001 -g crmgroup -m -s /sbin/nologin crmappuser && \
    chown -R crmappuser:crmgroup /app

USER crmappuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
