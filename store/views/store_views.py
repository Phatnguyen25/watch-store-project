from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from store.models import Store
import requests  

def store_locator(request):
    stores = Store.objects.all()
    return render(request, 'store/stores/locator.html', {'stores': stores})


def api_find_nearest_store(request):
    """API: Tìm cửa hàng gần nhất dựa trên TỔNG QUÃNG ĐƯỜNG LÁI XE (Đường bộ)"""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not lat or not lng:
        return JsonResponse({'found': False, 'error': 'Thiếu tọa độ'})

    try:
        user_location = Point(float(lng), float(lat), srid=4326)

        # 🌟 BƯỚC 1: PostGIS lấy Top 5 cửa hàng gần nhất theo đường chim bay
        top_stores = Store.objects.annotate(
            straight_distance=Distance('location', user_location)
        ).order_by('straight_distance')[:5]

        if not top_stores:
            return JsonResponse({'found': False, 'results': []})

        results = []

        # 🌟 BƯỚC 2: Gọi OSRM đo đường đua thực tế cho 5 cửa hàng này
        for store in top_stores:
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lng},{lat};{store.location.x},{store.location.y}?overview=false"
            
            driving_distance = float('inf')
            driving_time = 0
            
            try:
                response = requests.get(osrm_url, timeout=2)
                data = response.json()
                
                if data.get('code') == 'Ok':
                    driving_distance = data['routes'][0]['distance']  # meters
                    driving_time = data['routes'][0]['duration']      # seconds
                else:
                    driving_distance = store.straight_distance.m if hasattr(store.straight_distance, 'm') else 0
            except Exception:
                driving_distance = store.straight_distance.m if hasattr(store.straight_distance, 'm') else 0

            results.append({
                'id': store.id,
                'name': store.name,
                'address': store.address,
                'lat': store.location.y,
                'lng': store.location.x,
                'distance_m': driving_distance,
                'distance_km': round(driving_distance / 1000, 1),
                'time_minutes': round(driving_time / 60)
            })

        # Sắp xếp mảng lại theo khoảng cách đường lái xe
        results.sort(key=lambda x: x['distance_m'])

        return JsonResponse({
            'found': True,
            'results': results
        })

    except Exception as e:
        return JsonResponse({'found': False, 'error': str(e)})