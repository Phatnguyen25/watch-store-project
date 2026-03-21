from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from store.models import Store
import requests  

def store_locator(request):
    return render(request, 'store/stores/locator.html')


def api_find_nearest_store(request):
    """API: Tìm cửa hàng gần nhất dựa trên TỔNG QUÃNG ĐƯỜNG LÁI XE (Đường bộ)"""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not lat or not lng:
        return JsonResponse({'found': False, 'error': 'Thiếu tọa độ'})

    try:
        user_location = Point(float(lng), float(lat), srid=4326)

        # 🌟 BƯỚC 1: PostGIS lấy Top 3 cửa hàng gần nhất theo đường chim bay (Để tối ưu tốc độ)
        top_stores = Store.objects.annotate(
            straight_distance=Distance('location', user_location)
        ).order_by('straight_distance')[:3]

        if not top_stores:
            return JsonResponse({'found': False})

        nearest_store = None
        min_driving_distance = float('inf') # Đặt số km ban đầu là vô cực

        # 🌟 BƯỚC 2: Gọi OSRM đo đường đi bộ/lái xe thực tế cho 3 cửa hàng này
        for store in top_stores:
            # Format của OSRM: kinh_độ_1,vĩ_độ_1;kinh_độ_2,vĩ_độ_2
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lng},{lat};{store.location.x},{store.location.y}?overview=false"
            
            try:
                # Gửi Request lấy dữ liệu đường đi (timeout 2s để tránh web bị đơ)
                response = requests.get(osrm_url, timeout=2)
                data = response.json()
                
                if data.get('code') == 'Ok':
                    # Lấy tổng quãng đường đi thực tế (đơn vị: mét)
                    driving_distance = data['routes'][0]['distance']
                    
                    # Nếu quãng đường này ngắn hơn kỷ lục hiện tại -> Cập nhật lại Quán Gần Nhất
                    if driving_distance < min_driving_distance:
                        min_driving_distance = driving_distance
                        nearest_store = store
            except Exception:
                pass # Bỏ qua nếu lỗi mạng

        # 🌟 BƯỚC 3: Nếu API OSRM bị lỗi mạng hết, rớt lại dùng tạm thằng số 1 của đường chim bay
        if not nearest_store:
            nearest_store = top_stores[0]
            # Quy đổi từ độ (degree) của PostGIS ra mét (mức độ tương đối)
            min_driving_distance = top_stores[0].straight_distance.m if hasattr(top_stores[0].straight_distance, 'm') else 0

        # Trả về cửa hàng có QUÃNG ĐƯỜNG ĐI thực tế ngắn nhất
        return JsonResponse({
            'found': True,
            'name': nearest_store.name,
            'address': nearest_store.address,
            'lat': nearest_store.location.y,
            'lng': nearest_store.location.x,
            'distance_km': round(min_driving_distance / 1000, 1) # Chuyển mét sang Km (làm tròn 1 số)
        })

    except Exception as e:
        return JsonResponse({'found': False, 'error': str(e)})