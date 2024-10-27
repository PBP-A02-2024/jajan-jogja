from django.test import TestCase
from reksa.models import FoodPlan
# Create your tests here.
def test_food_plan_view(self):
    response = self.client.get('/food_plan/')
    self.assertEqual(response.status_code, 200)

def test_food_plan_view_context(self):
    response = self.client.get('/food_plan/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'food_plan.html')
    self.assertIsInstance(response.context['food_plan'], FoodPlan)

def test_food_plan_view_context_restaurants(self):
    response = self.client.get('/food_plan/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'food_plan.html')
    self.assertIsInstance(response.context['restaurants'], list)

def test_food_plan_view_context_restaurant_ids(self):
    response = self.client.get('/food_plan/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'food_plan.html')
    self.assertIsInstance(response.context['restaurant_ids'], list)

