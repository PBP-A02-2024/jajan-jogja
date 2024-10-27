from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from zoya.models import Makanan, TempatKuliner
from reksa.models import FoodPlan
import json
from django.utils import timezone
from decimal import Decimal
class MarcoViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.tempat_kuliner = TempatKuliner.objects.create(
            nama='Test Restaurant',
            description='Test Description',
            alamat='Test Address',
            longitude='123.456',
            latitude='78.910',
            jamBuka=timezone.now().time(),
            jamTutup=timezone.now().time(),
            rating=Decimal('4.1')
        )
        
        self.food_plan = FoodPlan.objects.create(
            nama='Test Plan',
            user=self.user
        )
        
        self.food_plan.tempat_kuliner.add(self.tempat_kuliner)
        
        self.makanan = Makanan.objects.create(
            tempat_kuliner=self.tempat_kuliner,
            nama='Test Food',
            description='Test Food Description',
            harga=50000
        )
        
        self.client = Client()
        self.client.login(username='testuser', password='testpass')

    def test_get_restaurant_view(self):
        url = reverse('marco:get_restaurant', args=[self.tempat_kuliner.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/index.html')
        self.assertIn('restoran', response.context)
        
    def test_get_makanan_json_view(self):
        url = reverse('marco:get_makanan_json', args=[self.tempat_kuliner.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        
    def test_get_food_plans_json_view(self):
        url = reverse('marco:get_food_plans_json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertIn(self.food_plan.nama, response.content.decode())

    def test_save_food_plan_view_post(self):
        post_data = {
          'currentResto': str(self.tempat_kuliner.id),
          'makanan_id': str(self.makanan.id),
          'foodPlansData': json.dumps([{'id': str(self.food_plan.id), 'checked': True}])
        }
        url = reverse('marco:save_food_plan')
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)
        
        self.food_plan.refresh_from_db()
        self.assertTrue(self.food_plan.makanan.filter(id=self.makanan.id).exists())

    def test_save_food_plan_view_get(self):
        url = reverse('marco:save_food_plan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')