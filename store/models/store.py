from django.db import models
from django.contrib.gis.db import models as gis_models # Chú ý import GIS
class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    
    # PointField: Lưu Kinh độ (Longitude) và Vĩ độ (Latitude)
    location = gis_models.PointField(srid=4326) 
    
    def __str__(self):
        return self.name