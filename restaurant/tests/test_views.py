from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Menu
from ..serializers import MenuSerializer

class MenuViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.list_url = '/restaurant/menu/'

        Menu.objects.create(title="IceCream", price=30, inventory=100)
        Menu.objects.create(title="Pasta", price=50, inventory=80)
        Menu.objects.create(title="Falafel", price=40, inventory=40)

    def test_get_all(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the data
        items = Menu.objects.all()
        serializer = MenuSerializer(items, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_menu_item(self):
        # Test creating a new menu item
        item = {
            'title': 'Hummus',
            'price': 250,
            'inventory': 25
        }
        response = self.client.post(self.list_url, item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the item was created
        self.assertEqual(Menu.objects.count(), 4)  # Initially 3 item, now 4
        self.assertEqual(Menu.objects.last().title, 'Hummus')
