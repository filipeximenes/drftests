# from django.core.urlresolvers import resolve, reverse
# from django.contrib.auth.models import User
# from rest_framework.test import (
#     APITestCase, APIRequestFactory,
#     force_authenticate, APIClient)
# from rest_framework import status
# from bikes.models import Bike
# from bikes.endpoints import BikeListView
# from bikes.serializers import BikeSerializer


# factory = APIRequestFactory()


# class BikeListTest(APITestCase):
#     view_class = BikeListView
#     view_name = 'bikes-list'

#     def setUp(self):
#         self.view = self.view_class.as_view()
#         self.user = User.objects.create(username='theuser')
#         self.bike_data = {
#             'color': 'yellow',
#             'size': '52.00',
#         }
#         self.auth_client = APIClient()
#         self.auth_client.force_authenticate(user=self.user)

#     def test_list_url(self):
#         resolver = resolve('/api/bikes/')
#         self.assertEqual(resolver.func.__name__, self.view_class.__name__)

#     def test_list_url_name(self):
#         resolver = resolve('/api/bikes/')
#         self.assertEqual(resolver.url_name, self.view_name)

#     def test_list_uses_bike_serializer(self):
#         self.assertEqual(self.view_class().get_serializer_class(), BikeSerializer)

#     def test_create_bike_returns_201(self):
#         response = self.auth_client.post(reverse(self.view_name), self.bike_data)

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_create_correctly_saves_to_db(self):
#         request = factory.post('', self.bike_data)
#         force_authenticate(request, user=self.user)
#         self.view(request)

#         bikes = Bike.objects.all()

#         self.assertEqual(len(bikes), 1)

#         bike = bikes[0]

#         self.assertEqual(bike.color, self.bike_data['color'])
#         self.assertEqual(str(bike.size), self.bike_data['size'])

#     def test_create_returns_400_on_errors(self):
#         self.bike_data['color'] = 'wrong color value'
#         self.bike_data['size'] = 1

#         request = factory.post('', self.bike_data)
#         force_authenticate(request, user=self.user)
#         response = self.view(request)

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # we know we have to fix the test when adding new field
#         self.assertEqual(len(response.data.keys()), len(self.bike_data.keys()))
#         # we know that the fields we expected where in the error list
#         self.assertEqual(set(response.data.keys()), set(['color', 'size']))

#     def test_list_returns_403_if_not_authorized(self):
#         response = self.client.get(reverse(self.view_name))

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_create_returns_403_if_not_authorized(self):
#         response = self.client.post(reverse(self.view_name), self.bike_data)

#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
