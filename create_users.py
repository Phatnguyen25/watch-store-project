import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

users = [
    ('khachhang1', 'khachhang1@example.com', '123456'),
    ('khachhang2', 'khachhang2@example.com', '123456')
]

for username, email, password in users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, email=email, password=password)
        print(f"Created user: {username} (Password: {password})")
    else:
        print(f"User {username} already exists")
