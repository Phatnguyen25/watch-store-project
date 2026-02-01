# ⌚ Hệ thống Watch Store O2O (Online-to-Offline)

> **Dự án thương mại điện tử tích hợp định vị không gian (GIS) và quản lý dữ liệu động.**

![Project Status](https://img.shields.io/badge/Status-Phase%202:%20Frontend%20&%20Map-blue) ![Docker](https://img.shields.io/badge/Docker-Ready-green) ![Gitflow](https://img.shields.io/badge/Workflow-Gitflow-orange)

## 🌟 Tổng quan
Hệ thống được xây dựng trên kiến trúc **Micro-modular** (chia nhỏ module) để tối ưu hóa khả năng mở rộng và làm việc nhóm.
* **Backend:** Django 5, PostGIS (Quản lý dữ liệu không gian).
* **Frontend:** Tailwind CSS (Giao diện), Leaflet.js (Bản đồ).
* **Infrastructure:** Docker hóa toàn diện.

---

## 📂 Cấu trúc Dự án (New Architecture)

Dự án đã được Refactor (tái cấu trúc) để tách biệt logic. Các thành viên vui lòng tuân thủ cấu trúc này:

```text
watch-store/
├── core/                   # Cấu hình lõi (Settings, URLs tổng)
├── store/                  # App chính
│   ├── models/             # 🟢 DATABASE MODELS (Đã tách nhỏ)
│   │   ├── __init__.py     # Khai báo models
│   │   ├── product.py      # Chứa Product, Category
│   │   └── store.py        # Chứa Store (PostGIS)
│   ├── views/              # 🟢 LOGIC VIEW (Đã tách nhỏ)
│   │   ├── __init__.py     
│   │   ├── product_views.py 
│   │   └── store_views.py
│   ├── urls.py             # Định tuyến API/View
│   └── admin.py            # Cấu hình trang quản trị
├── templates/              # 🟢 GIAO DIỆN (HTML)
│   ├── base.html           # Layout khung sườn (Chứa TailwindCDN)
│   └── store/              # Giao diện của app Store
│       ├── products/       # Trang danh sách/chi tiết sản phẩm
│       └── stores/         # Trang bản đồ cửa hàng
├── docker-compose.yml      # Cấu hình Docker
└── requirements.txt        # Danh sách thư viện
```

### 🚦 Quy trình Git (Gitflow) - BẮT BUỘC
Để tránh xung đột code (Conflict), toàn bộ team phải tuân thủ luật sau:

1. Các nhánh chính

🔴 main: Nhánh sản phẩm. CẤM push trực tiếp. Chỉ Tech Lead mới được Merge.

🟡 dev: Nhánh phát triển chung. Code phải chạy ổn định mới được merge vào đây.

🟢 feature/...: Nhánh làm việc cá nhân.

2. Quy trình làm việc hàng ngày

Đồng bộ code:
```bash
git checkout dev
git pull origin dev
```
Tạo nhánh chức năng mới:
```bash
git checkout -b feature/ten-chuc-nang (VD: feature/product-detail)
```
Code&Push
```bash
git add .
git commit -m "Mô tả rõ ràng công việc"
git push origin feature/ten-chuc-nang
```
Ghép code: Vào GitHub tạo Pull Request (PR) từ nhánh feature vào nhánh dev.

### 🚀 Cài đặt & Chạy dự án
*** Yêu cầu: Máy tính đã cài Docker Desktop.**
Bước 1: Lấy code về
```bash
git clone [https://github.com/Phatnguyen25/watch-store-project.git](https://github.com/Phatnguyen25/watch-store-project.git)
cd watch-store-project
```
Bước 2: Khởi động (Lần đầu sẽ mất ~5 phút)
```bash
docker-compose up --build
```
Bước 3: Tạo Database & Admin (Chỉ chạy lần đầu)
Mở terminal mới và chạy:
```bash
# Tạo bảng
docker-compose exec web python manage.py migrate

# Tạo tài khoản admin
docker-compose exec web python manage.py createsuperuser
```
### 🛠️ Công nghệ & Thư viện Chính
***Tailwind CSS: Tích hợp qua CDN (trong base.html). Không cần cài Node.js.**

***Django JSON Widget: Trình soạn thảo JSON trực quan trong Admin.**

***Django Leaflet: Tích hợp bản đồ OpenStreetMap.**

***PostGIS: Extension của PostgreSQL xử lý tọa độ, khoảng cách.**
### 🐛 Khắc phục lỗi thường gặp
***1. Lỗi "TemplateDoesNotExist: base.html"**

Nguyên nhân: Sai cấu trúc thư mục templates.

Xử lý: Đảm bảo file base.html nằm ở thư mục templates/ ngoài cùng (ngang hàng manage.py).

***2. Lỗi "ModuleNotFoundError: No module named 'store.models'"**

Nguyên nhân: Quên file __init__.py khi tách thư mục.

Xử lý: Kiểm tra thư mục store/models/ đã có file __init__.py chưa.