from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.


class VendorCRUDView(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderCRUDView(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        performance_data = {
            'on_time_delivery_rate': instance.on_time_delivery_rate,
            'quality_rating': instance.quality_rating_avg,
            'response_time': instance.average_response_time,
            'fulfillment_rate': instance.fulfillment_rate,
        }

        return Response(performance_data)