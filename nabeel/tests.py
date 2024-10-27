from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from zoya.models import Makanan, TempatKuliner, Variasi
from nabeel.models import Search
import uuid

class ViewsTestCase(TestCase):
    def setUp(self):
        # Setup user and login
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')
        
        # Setup data for TempatKuliner and Variasi
        self.variasi = Variasi.objects.create(nama="Spicy")
        self.tempat_kuliner = TempatKuliner.objects.create(
            nama="Resto A", description="Description", alamat="Alamat",
            longitude="123", latitude="456", jamBuka="10:00", jamTutup="22:00"
        )
        self.tempat_kuliner.variasi.add(self.variasi)
        
        # Setup data for Search
        self.search_content = "Soto"
        self.search = Search.objects.create(
            content=self.search_content, user=self.user
        )

    def test_search_page_get(self):
        response = self.client.get(reverse('nabeel:search_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search-page.html')
        self.assertIn('list_resto', response.context)
        
    def test_search_page_post(self):
        response = self.client.post(reverse('nabeel:search_page'), {'content': 'Test Search'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Search.objects.filter(content='Test Search').exists())

    def test_search_by_keyword_get(self):
        response = self.client.get(reverse('nabeel:search_by_keyword', kwargs={'keyword': self.search_content}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search-page.html')
        self.assertIn('list_resto', response.context)
        self.assertIn('list_variasi', response.context)
        self.assertIn('search_history', response.context)

    def test_delete_search_history(self):
        response = self.client.get(reverse('nabeel:delete_search_history', kwargs={'id': self.search.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Search.objects.filter(id=self.search.id).exists())
        
    def test_show_search_history(self):
        response = self.client.get(reverse('nabeel:show_search_history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_search_history_by_id(self):
        response = self.client.get(reverse('nabeel:show_search_history_by_id', kwargs={'id': self.search.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
    def test_edit_search_history_post(self):
        response = self.client.post(reverse('nabeel:edit_search_history', kwargs={'id': self.search.id}), {'content': 'Updated Content'})
        self.assertEqual(response.status_code, 200)
        self.search.refresh_from_db()
        self.assertEqual(self.search.content, 'Updated Content')

    def test_show_tempat_kuliner_by_category(self):
        response = self.client.get(reverse('nabeel:show_tempat_kuliner_by_category', kwargs={'keyword': 'Resto', 'id': self.variasi.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
