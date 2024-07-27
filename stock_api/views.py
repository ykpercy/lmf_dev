from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import StockInfo, StockSpot, StockData
from .serializers import StockInfoSerializer, StockSpotSerializer, StockDataSerializer

# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 300

class StockSpotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StockSpot.objects.all().order_by('-timestamp')
    serializer_class = StockSpotSerializer
    pagination_class = CustomPagination

class StockDataView(APIView):
    def get(self, request):
        try:
            stocks = StockData.objects.all()
            serializer = StockDataSerializer(stocks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

