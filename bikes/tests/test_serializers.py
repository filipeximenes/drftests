from decimal import Decimal
from rest_framework.test import APITestCase
from bikes.models import Bike
from bikes.serializers import BikeSerializer


class BikeSerializerTests(APITestCase):

    def setUp(self):
        self.bike_attributes = {
            'color': 'yellow',
            'size': Decimal('52.12')}

        self.serializer_data = {
            'color': 'black',
            'size': 51.23
        }

        self.bike = Bike.objects.create(**self.bike_attributes)
        self.serializer = BikeSerializer(instance=self.bike)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['color', 'size']))

    def test_color_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['color'], self.bike_attributes['color'])

    def test_size_field_content(self):
        # Caution:
        # data['size'] == float(self.bike_attributes['size']
        # Decimal(data['size']) != self.bike_attributes['size']
        data = self.serializer.data

        self.assertEqual(data['size'], float(self.bike_attributes['size']))

    def test_size_lower_bound(self):
        self.serializer_data['size'] = 29.9

        serializer = BikeSerializer(instance=self.bike, data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))

    def test_size_upper_bound(self):
        self.serializer_data['size'] = 60.1

        serializer = BikeSerializer(instance=self.bike, data=self.serializer_data)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))

    def test_float_data_correctly_saves_as_decimal(self):
        self.serializer_data['size'] = 31.789

        serializer = BikeSerializer(data=self.serializer_data)
        serializer.is_valid()

        new_bike = serializer.save()
        # Not refreshing from db will cause the bike size to remain
        # a float
        new_bike.refresh_from_db()

        self.assertEqual(new_bike.size, Decimal('31.79'))

    def test_color_must_be_in_choices(self):
        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)
        self.assertTrue(serializer.is_valid())

        self.bike_attributes['color'] = 'red'

        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['color']))
