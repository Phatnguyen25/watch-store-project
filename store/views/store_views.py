from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from store.models import Store

def store_locator(request):
    return render(request, 'store/stores/locator.html')

def api_find_nearest_store(request):
    """API tìm cửa hàng gần nhất dựa trên tọa độ gửi lên"""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if lat and lng:
        # 1. Tạo điểm mốc từ vị trí người dùng
        user_location = Point(float(lng), float(lat), srid=4326)

        # 2. Truy vấn Database:
        # - annotate: Tính khoảng cách cho từng cửa hàng
        # - order_by: Sắp xếp từ gần đến xa
        # - first: Lấy cái đầu tiên
        nearest_store = Store.objects.annotate(
            distance=Distance('location', user_location)
        ).order_by('distance').first()

        if nearest_store:
            return JsonResponse({
                'found': True,
                'name': nearest_store.name,
                'address': nearest_store.address,
                'lat': nearest_store.location.y, # Vĩ độ
                'lng': nearest_store.location.x, # Kinh độ
                'distance_km': round(nearest_store.distance.km, 2)
            })
    
    return JsonResponse({'found': False})