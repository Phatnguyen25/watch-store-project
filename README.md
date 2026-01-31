# ⌚ Hệ thống Thương mại Điện tử Đồng hồ Cao cấp (Watch Store)

> **Mô hình O2O (Online-to-Offline) tích hợp định vị không gian và quản lý dữ liệu động.**

Dự án được xây dựng nhằm giải quyết bài toán quản lý đa dạng thông số kỹ thuật của đồng hồ xa xỉ và tích hợp bản đồ số để định vị chuỗi cửa hàng vật lý. Hệ thống được đóng gói toàn diện bằng Docker, đảm bảo môi trường phát triển nhất quán cho toàn bộ đội ngũ kỹ thuật.

## 🌟 Tính năng Nổi bật

- **Quản lý Sản phẩm Động (Dynamic Specs):** Sử dụng `JSONField` để lưu trữ hàng chục thông số kỹ thuật khác nhau (Máy, Kính, Size...) mà không cần thay đổi cấu trúc Database.
- **Định vị Cửa hàng (Store Locator):** Tích hợp **PostGIS** và **Leaflet.js** để hiển thị bản đồ, tìm kiếm cửa hàng gần nhất dựa trên tọa độ GPS.
- **Quản trị Trực quan:** Giao diện Admin tích hợp sẵn bản đồ để ghim vị trí cửa hàng và trình soạn thảo JSON chuyên dụng.
- **Containerization:** Triển khai 100% trên Docker, chạy được trên mọi hệ điều hành (Windows/MacOS/Linux) mà không cần cài đặt môi trường phức tạp.

## 🛠️ Công nghệ Sử dụng

| Thành phần         | Công nghệ                                                                   |
| :----------------- | :-------------------------------------------------------------------------- |
| **Backend**        | Python 3.10, Django 5.0                                                     |
| **Database**       | PostgreSQL 15 + **PostGIS Extension** (Xử lý dữ liệu không gian)            |
| **Frontend**       | Bootstrap 5, Leaflet.js (Bản đồ OpenStreetMap)                              |
| **DevOps**         | Docker, Docker Compose                                                      |
| **Thư viện chính** | `djangorestframework-gis`, `django-leaflet`, `django-json-widget`, `Pillow` |

---

## 🚀 Hướng dẫn Cài đặt (Dành cho thành viên mới)

**Lưu ý quan trọng:** Bạn **KHÔNG CẦN** cài đặt Python hay PostgreSQL trên máy cá nhân. Mọi thứ đã có Docker lo.

### 1. Yêu cầu tiên quyết (Prerequisites)

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Đã bật và đang chạy).
- [Git](https://git-scm.com/).
- [Visual Studio Code](https://code.visualstudio.com/).

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

PHẦN 1: DÀNH CHO DEVELOPER (Quy trình code hàng ngày)
Mọi thành viên (bao gồm cả bạn khi code tính năng) đều phải tuân thủ 4 bước này mỗi khi bắt đầu một công việc mới.

Bước 1: Lấy code mới nhất về (Sync)
Trước khi làm gì, phải chắc chắn máy mình đang có code mới nhất từ nhánh dev.

PowerShell
# Chuyển về nhánh dev
git checkout dev

# Kéo code mới nhất từ GitHub về
git pull origin dev
Bước 2: Tạo nhánh riêng (Feature Branch)
Tuyệt đối không code trên dev. Hãy tạo nhánh mới.

Quy tắc đặt tên: feature/ten-chuc-nang (Ví dụ: feature/login, feature/map-view).

PowerShell
# Tạo và chuyển sang nhánh mới
git checkout -b feature/ten-chuc-nang-cua-ban
Bước 3: Code và Lưu (Commit)
Làm việc bình thường trên VS Code. Khi xong một phần việc nhỏ:

PowerShell
# Thêm tất cả file đã sửa vào danh sách chờ
git add .

# Lưu lại với ghi chú (Ghi rõ ràng, tiếng Việt không dấu hoặc tiếng Anh)
git commit -m "Them giao dien dang nhap co ban"
Bước 4: Đẩy lên GitHub (Push)
Khi đã hoàn thành chức năng, đẩy nhánh này lên kho chứa.

PowerShell
git push -u origin feature/ten-chuc-nang-cua-ban
```
PHẦN 2: DÀNH CHO TECH LEAD (Quy trình Merge/Duyệt Code)
Sau khi thành viên làm xong Bước 4, họ sẽ báo bạn: "Ông ơi tôi push nhánh login rồi, merge giúp tôi với". Lúc này bạn làm như sau:

1. Tạo Pull Request (PR)
Thành viên (hoặc bạn) vào link GitHub dự án.

Bạn sẽ thấy một khung vàng hiện lên: "feature/... had recent pushes..." kèm nút xanh Compare & pull request. Bấm vào đó.

Quan trọng:

Base: chọn dev (Nhánh đích).

Compare: chọn feature/... (Nhánh vừa code).

Ghi tiêu đề và bấm Create pull request.

2. Review Code (Duyệt)
GitHub chuyển sang màn hình PR. Bạn bấm vào tab Files changed.

Xem code xem có gì vô lý không (Ví dụ: quên xóa file rác, code sai logic).

Nếu ổn: Chuyển sang bước 3.

Nếu chưa ổn: Comment thẳng vào dòng code đó bắt sửa lại.

3. Merge (Ghép code)
Bấm nút màu xanh lá Merge pull request -> Confirm merge.

Sau khi merge xong, bấm nút Delete branch (xóa nhánh feature cũ đi cho đỡ rác).

PHẦN 3: XỬ LÝ "XUNG ĐỘT" (CONFLICT) - CƠN ÁC MỘNG NHÓM
Tình huống: Bạn A sửa dòng 10 file models.py. Bạn B cũng sửa dòng 10 file models.py. Khi Merge, Git sẽ hét lên: "Conflict! Tôi không biết chọn dòng nào!".

Cách xử lý:

Trên GitHub: Nó sẽ chặn nút Merge và báo đỏ.

Cách sửa (Tech Lead sửa):

Bạn kéo nhánh của người bị conflict về máy: git pull origin feature/nhanh-bi-loi.

Mở VS Code lên. Bạn sẽ thấy các dòng code bị đánh dấu bằng các ký tự lạ như <<<<<<<, =======, >>>>>>>.

Current Change: Code hiện tại (trên máy bạn).

Incoming Change: Code mới (từ nhánh kia).

Việc của bạn: Xóa các ký tự lạ đi, giữ lại đoạn code đúng nhất (hoặc kết hợp cả hai).

Lưu lại:

Sau khi sửa xong file, chạy:

PowerShell
git add .
git commit -m "Fix conflict models.py"
git push
Lúc này trên GitHub sẽ xanh lại -> Bấm Merge được.