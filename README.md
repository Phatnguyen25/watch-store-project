# ⌚ Hệ thống Thương mại Điện tử Đồng hồ Cao cấp (Watch Store)

> **Mô hình O2O (Online-to-Offline) tích hợp định vị không gian và quản lý dữ liệu động.**

Dự án được xây dựng nhằm giải quyết bài toán quản lý đa dạng thông số kỹ thuật của đồng hồ xa xỉ và tích hợp bản đồ số để định vị chuỗi cửa hàng vật lý. Hệ thống được đóng gói toàn diện bằng Docker, đảm bảo môi trường phát triển nhất quán cho toàn bộ đội ngũ kỹ thuật.

## 🌟 Tính năng Nổi bật

* **Quản lý Sản phẩm Động (Dynamic Specs):** Sử dụng `JSONField` để lưu trữ hàng chục thông số kỹ thuật khác nhau (Máy, Kính, Size...) mà không cần thay đổi cấu trúc Database.
* **Định vị Cửa hàng (Store Locator):** Tích hợp **PostGIS** và **Leaflet.js** để hiển thị bản đồ, tìm kiếm cửa hàng gần nhất dựa trên tọa độ GPS.
* **Quản trị Trực quan:** Giao diện Admin tích hợp sẵn bản đồ để ghim vị trí cửa hàng và trình soạn thảo JSON chuyên dụng.
* **Containerization:** Triển khai 100% trên Docker, chạy được trên mọi hệ điều hành (Windows/MacOS/Linux) mà không cần cài đặt môi trường phức tạp.

## 🛠️ Công nghệ Sử dụng

| Thành phần | Công nghệ |
| :--- | :--- |
| **Backend** | Python 3.10, Django 5.0 |
| **Database** | PostgreSQL 15 + **PostGIS Extension** (Xử lý dữ liệu không gian) |
| **Frontend** | Bootstrap 5, Leaflet.js (Bản đồ OpenStreetMap) |
| **DevOps** | Docker, Docker Compose |
| **Thư viện chính** | `djangorestframework-gis`, `django-leaflet`, `django-json-widget`, `Pillow` |

---

## 🚀 Hướng dẫn Cài đặt (Dành cho thành viên mới)

**Lưu ý quan trọng:** Bạn **KHÔNG CẦN** cài đặt Python hay PostgreSQL trên máy cá nhân. Mọi thứ đã có Docker lo.

### 1. Yêu cầu tiên quyết (Prerequisites)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Đã bật và đang chạy).
* [Git](https://git-scm.com/).
* [Visual Studio Code](https://code.visualstudio.com/).

### 2. Các bước triển khai

Bước 1: Clone dự án về máy
    Mở Terminal (hoặc PowerShell) và chạy lệnh:
  ```bash
  git clone [https://github.com/TEN-GITHUB-CUA-BAN/watch-store-project.git](https://github.com/TEN-GITHUB-CUA-BAN/watch-store-project.git)
  cd watch-store-project

**Bước 2:  Khởi động hệ thống (Build & Run) Lệnh này sẽ tải các thư viện cần thiết và khởi động Server + Database. Quá trình này có thể mất 3-5 phút trong lần đầu tiên.**
    docker-compose up --build

Bước 3: Khởi tạo Cơ sở dữ liệu (Chỉ chạy lần đầu) Mở một cửa sổ Terminal mới (giữ nguyên cửa sổ đang chạy server) và chạy lần lượt 2 lệnh sau:
1.Tạo bảng dữ liệu (Tables):

docker-compose exec web python manage.py migrate

2. Tạo tài khoản Quản trị viên (Superuser):

docker-compose exec web python manage.py createsuperuser

### 3.Cấu trúc thư mục
watch-store/
├── core/                # Cấu hình lõi của Django (settings, urls)
├── store/               # App chính xử lý nghiệp vụ
│   ├── migrations/      # Lịch sử thay đổi Database
│   ├── templates/       # Giao diện HTML (View)
│   ├── admin.py         # Cấu hình trang Admin (Map, JSON Widget)
│   ├── models.py        # Định nghĩa dữ liệu (Product, Store)
│   ├── views.py         # Logic xử lý (Controller)
│   └── urls.py          # Định tuyến cho app Store
├── media/               # Thư mục chứa ảnh sản phẩm upload
├── docker-compose.yml   # File cấu hình Docker (Quan trọng)
├── Dockerfile           # File cấu hình môi trường Python
├── requirements.txt     # Danh sách thư viện Python
└── manage.py            # Công cụ dòng lệnh của Django 

  **Các lỗi thường gặp: **
❓ Xử lý lỗi thường gặp (Troubleshooting)
Q1: Lỗi "ProgrammingError: relation 'store_category' does not exist"

Nguyên nhân : Bạn chưa chạy lệnh tạo bảng vào database.

Cách sửa: Chạy lệnh docker-compose exec web python manage.py migrate.

Q2: Lỗi "VS Code báo gạch chân màu vàng ở các dòng import"

Nguyên nhân: VS Code trên Windows không nhìn thấy thư viện cài trong Docker.

Cách sửa: Kệ nó. Miễn là server chạy không báo lỗi là được.

Q3: Lỗi "Port is already allocated"

Nguyên nhân: Cổng 8000 hoặc 5432 đang bị phần mềm khác chiếm dụng.

Cách sửa: Tắt các phần mềm đó hoặc đổi cổng trong file docker-compose.yml.

Q4: Code xong nhưng F5 không thấy thay đổi?

Nếu sửa code Python (.py): Server tự động reload, chỉ cần F5 trình duyệt.

Nếu thêm thư viện mới vào requirements.txt: Phải chạy lại docker-compose up --build.



#### Trước khi bắt đầu code (Mỗi sáng): Luôn chạy lệnh này để lấy code mới nhất mà người khác vừa đẩy lên:

Bash
git pull
Sau khi code xong: Thực hiện bộ 3 quyền lực:

Bash
git add .
git commit -m "Ghi rõ nội dung vừa sửa"
git push