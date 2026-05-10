# ⌚ Hệ thống Watch Store O2O (Online-to-Offline)

> **Dự án thương mại điện tử tích hợp định vị không gian (GIS) và quản lý dữ liệu động.**

![Project Status](https://img.shields.io/badge/Status-Phase%202:%20Frontend%20&%20Map-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-green) ![Gitflow](https://img.shields.io/badge/Workflow-Gitflow-orange)

## 🌟 Tổng quan

Hệ thống được xây dựng trên kiến trúc **Micro-modular** (chia nhỏ module) để tối ưu hóa khả năng mở rộng và làm việc nhóm.

- **Backend:** Django 5.0.1
- **Database:** PostgreSQL + PostGIS (Quản lý dữ liệu không gian)
- **Frontend:** HTML, Tailwind CSS (qua CDN), Leaflet.js (Bản đồ)
- **Infrastructure:** Docker hóa toàn diện bằng `docker-compose`.

---

## 🛠️ Công nghệ & Thư viện Chính

Dưới đây là các thư viện lõi (chi tiết xem trong `requirements.txt`):
- **Django (5.0.1)**: Framework chính.
- **psycopg2-binary**: Driver kết nối PostgreSQL.
- **djangorestframework & djangorestframework-gis**: Xây dựng API và xử lý dữ liệu địa lý.
- **django-leaflet**: Tích hợp bản đồ Leaflet.js cho phép hiển thị và tương tác tọa độ.
- **django-json-widget**: Trình soạn thảo JSON trực quan trong Admin.
- **xhtml2pdf**: Thư viện cho phép xuất báo cáo doanh thu ra file PDF (yêu cầu các thư viện C++ ở mức hệ thống như `libcairo2`, `libpango`).
- **django-excel & pyexcel-xlsx**: Hỗ trợ nhập/xuất dữ liệu hàng loạt bằng file Excel.
- **Pillow**: Xử lý ảnh sản phẩm.

---

## 🚀 Hướng dẫn Cài đặt & Chạy dự án từ Nguyên sơ đến Hoàn chỉnh

### Yêu cầu hệ thống:
- Đã cài đặt **Docker Desktop** và **Git**.

### Bước 1: Lấy code về
```bash
git clone https://github.com/Phatnguyen25/watch-store-project.git
cd watch-store-project
```

### Bước 2: Build & Khởi động Docker (Lần đầu tiên)
Chạy lệnh sau để Docker tự động tải Image, cài đặt các thư viện hệ thống (`libcairo2`, `gdal`, v.v.) và các thư viện Python:
```bash
docker compose up --build -d
```
*(Quá trình này có thể mất ~5-10 phút tùy mạng).*
Website sẽ chạy tại: **http://localhost:8001**

### Bước 3: Cài đặt Database
Có **2 CÁCH** để khởi tạo dữ liệu cho database: **(A) Restore từ file Backup** hoặc **(B) Chạy Migrate & Seed Script từ đầu**.

#### CÁCH A: Phục hồi (Restore) từ file SQL Backup (KHUYÊN DÙNG)
Dự án đã đính kèm sẵn file `watchstore_backup.sql` bao gồm đầy đủ cấu trúc bảng và dữ liệu mẫu (sản phẩm, đơn hàng từ đầu năm, cửa hàng, đánh giá...). Để phục hồi:

```bash
docker compose exec -T db psql -U admin -d watchstore_db < watchstore_backup.sql
```
Sau đó, bạn có thể đăng nhập ngay với:
- Tên đăng nhập Admin: `admin` / Mật khẩu: `adminpass123`
- Tài khoản KH 1: `user1` / Mật khẩu: `userpass123`

#### CÁCH B: Tạo Database nguyên sơ & Seed dữ liệu thủ công
Nếu bạn muốn tạo lại từ đầu mà không dùng file backup:
```bash
# 1. Chạy migrate để tạo cấu trúc bảng:
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# 2. Tạo tài khoản Admin (tùy ý nhập username/password):
docker compose exec web python manage.py createsuperuser

# 3. Chạy lần lượt các script để tạo dữ liệu mẫu (Seed Data):
docker compose exec web python seed_data.py            # Tạo danh mục và sản phẩm
docker compose exec web python seed_stores.py          # Tạo danh sách cửa hàng
docker compose exec web python seed_coupons.py         # Tạo mã giảm giá
docker compose exec web python seed_users_orders.py    # Tạo người dùng & đơn hàng cũ
docker compose exec web python seed_reviews.py         # Tạo đánh giá sản phẩm
docker compose exec web python seed_orders.py          # Tạo dữ liệu đơn hàng thống kê từ đầu năm đến nay
docker compose exec web python manage.py seed_stock    # Khởi tạo lịch sử nhập xuất kho
```

---

## 📂 Cấu trúc Dự án
Dự án đã được Refactor (tái cấu trúc) để tách biệt logic:
```text
watch-store/
├── core/                   # Cấu hình lõi (Settings, URLs tổng)
├── store/                  # App chính
│   ├── models/             # 🟢 DATABASE MODELS (Đã tách nhỏ: product, store, order...)
│   ├── views/              # 🟢 LOGIC VIEW (Đã tách nhỏ)
│   └── management/         # Các custom commands (VD: seed_stock)
├── templates/              # 🟢 GIAO DIỆN (HTML)
├── docker-compose.yml      # Cấu hình Docker
├── Dockerfile              # Script build Docker image (cài C++ dependencies)
├── requirements.txt        # Danh sách thư viện Python
└── watchstore_backup.sql   # File backup CSDL đầy đủ
```

---

## 🚦 Quy trình làm việc nhóm (Gitflow)

1. **Đồng bộ code trước khi làm việc:**
```bash
git checkout dev
git pull origin dev
```

2. **Tạo nhánh chức năng mới:**
```bash
git checkout -b feature/ten-chuc-nang
```

3. **Lưu thay đổi & Đẩy code lên nhánh của mình:**
```bash
git add .
git commit -m "Mô tả công việc"
git push origin feature/ten-chuc-nang
```

4. **Tạo Pull Request (PR):** Truy cập GitHub, tạo PR từ nhánh `feature/...` vào nhánh `dev` để review. Mọi thay đổi vào nhánh `main` do Tech Lead phụ trách.

---

### 🐛 Khắc phục lỗi thường gặp

1. **Lỗi `ModuleNotFoundError: No module named 'xhtml2pdf'`**
- Nguyên nhân: Chưa build lại Docker image sau khi thêm thư viện.
- Xử lý: Chạy lại lệnh `docker compose up --build -d`.

2. **Lỗi khi xuất PDF hoặc lỗi giao diện bản đồ bị trắng**
- Nguyên nhân: Thiếu các thư viện C++ ở hệ điều hành.
- Xử lý: Các thư viện như `build-essential`, `libcairo2`, `gdal-bin` đã được khai báo trong `Dockerfile`. Đảm bảo container được build thành công từ file này.