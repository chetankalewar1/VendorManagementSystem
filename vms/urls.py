from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorCRUDView, PurchaseOrderCRUDView, VendorPerformanceView

router = DefaultRouter()
router.register(r'vendors', VendorCRUDView, basename='vendor')
router.register(r'purchase_orders', PurchaseOrderCRUDView, basename='purchase_order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
]