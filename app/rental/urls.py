from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import (
    RegisterView,
    BikeListView,
    bike_return,
    bike_rent,
    RentalHistoryView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bikes/', BikeListView.as_view(), name='bike-list'),
    path('rent/<int:bike_id>/', bike_rent, name='bike-rent'),
    path('return/<int:bike_id>/', bike_return, name='bike-return'),
    path('history/', RentalHistoryView.as_view(), name='rental-history'),
]
