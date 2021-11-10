from django.urls.conf import include, path

from . import views


urlpatterns = [
        path('', views.api_root),

        path('city/', views.CityList.as_view(), name='city-list'),
        path('shop/', lambda request: None, name='shop-list'),
]
