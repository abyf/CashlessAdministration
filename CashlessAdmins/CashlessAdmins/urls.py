from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('AdminsCashless.urls')),
]
admin.site.index_title = "TapNyamoo"
admin.site.site_header = "Cashless Administration"
admin.site.site_title = "Cashless"  
