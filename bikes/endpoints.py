from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from bikes.serializers import BikeSerializer
from bikes.models import Bike


class BikeListView(ListCreateAPIView):
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bike.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
