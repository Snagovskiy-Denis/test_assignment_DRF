from django.urls.conf import include, path

from . import views


urlpatterns = [
        path('', views.api_root),

        path('city/', views.CityList.as_view(), name='city-list'),
        path('shop/', views.ShopList.as_view(), name='shop-list'),

        path('city/<int:city_pk>/street/', views.CityStreetsList.as_view()),
]
