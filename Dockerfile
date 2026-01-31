# Sử dụng Python 3.10 slim để nhẹ và ổn định
FROM python:3.10-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# CÀI ĐẶT QUAN TRỌNG: Các thư viện C++ hỗ trợ xử lý bản đồ (GDAL, GEOS, PROJ)
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /code

# Cài đặt thư viện Python
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy toàn bộ code vào container
COPY . /code/