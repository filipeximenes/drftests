from django.conf.urls import url
from bikes.endpoints import BikeListView


urlpatterns = [
    url(r'^bikes/', BikeListView.as_view(), name='bikes-list'),
]
