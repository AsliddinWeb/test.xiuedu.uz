from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Dashboard
    path('dashboard/', include('dashboard_app.urls')),

    # Student
    path('', include('studentui_app.urls')),
]
