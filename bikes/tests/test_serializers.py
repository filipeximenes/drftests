from decimal import Decimal
from rest_framework.test import APITestCase
from bikes.models import Bike
from bikes.serializers import BikeSerializer


class BikeSerializerTests(APITestCase):

    def setUp(self):
        self.bike_attributes = {
            'color': 'yellow',
            'size': 52.0}

        self.bike = Bike.objects.create(**self.bike_attributes)
        self.serializer = BikeSerializer(instance=self.bike)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['color', 'size']))

    def test_color_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['color'], self.bike_attributes['color'])

    def test_size_field_content(self):
        data = self.serializer.data

        self.assertEqual(data['size'], self.bike_attributes['size'])

    def test_size_should_be_float(self):
        data = self.serializer.data

        self.assertIsInstance(data['size'], float)

    def test_size_lower_bound(self):
        self.bike_attributes['size'] = 29.9

        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))

    def test_size_upper_bound(self):
        self.bike_attributes['size'] = 60.1

        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors), set(['size']))

    def test_float_to_decimal(self):
        self.bike_attributes['size'] = 31.789

        serializer = BikeSerializer(data=self.bike_attributes)
        serializer.is_valid()

        new_bike = serializer.save()
        new_bike.refresh_from_db()

        self.assertEqual(new_bike.size, Decimal('31.79'))

    def test_color_must_be_in_choices(self):
        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)
        self.assertTrue(serializer.is_valid())

        self.bike_attributes['color'] = 'red'

        serializer = BikeSerializer(instance=self.bike, data=self.bike_attributes)

        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['color']))
