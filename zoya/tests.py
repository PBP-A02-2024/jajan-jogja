from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
import json
import uuid

from zoya.models import CommunityForum, TempatKuliner, Makanan, Variasi
from zoya.forms import CommunityForumForm

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test data for TempatKuliner
        self.tempat = TempatKuliner.objects.create(
            nama='Test Restaurant',
            description='Test Description',
            alamat='Test Address',
            longitude='123.456',
            latitude='78.910',
            jamBuka=timezone.now().time(),
            jamTutup=timezone.now().time(),
            rating=Decimal('4.5')
        )
        
        # Create test data for Makanan
        self.makanan = Makanan.objects.create(
            tempat_kuliner=self.tempat,
            nama='Test Food',
            description='Test Food Description',
            harga=50000
        )
        
        # Create test data for Variasi
        self.variasi = Variasi.objects.create(
            nama='Test Variation'
        )
        
        # Create test data for CommunityForum
        self.forum_entry = CommunityForum.objects.create(
            user=self.user,
            comment='Test Comment'
        )

    def test_tempat_kuliner_str(self):
        self.assertEqual(str(self.tempat), 'Test Restaurant')

    def test_makanan_str(self):
        self.assertEqual(str(self.makanan), 'Test Food')

    def test_variasi_str(self):
        self.assertEqual(str(self.variasi), 'Test Variation')

    def test_community_forum_str(self):
        self.assertEqual(str(self.forum_entry), 'Test Comment')

    def test_tempat_kuliner_rating_update(self):
        self.tempat.rating = Decimal('4.0')
        self.tempat.save()
        self.assertEqual(self.tempat.rating, Decimal('4.0'))

class FormTests(TestCase):
    def test_community_forum_form_valid(self):
        form_data = {
            'comment': 'Test comment'
        }
        form = CommunityForumForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_community_forum_form_html_stripping(self):
        form_data = {
            'comment': '<p>Test comment with <b>HTML</b></p>'
        }
        form = CommunityForumForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['comment'], 'Test comment with HTML')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.forum_entry = CommunityForum.objects.create(
            user=self.user,
            comment='Test Comment'
        )

    def test_show_main_view(self):
        response = self.client.get(reverse('zoya:show_main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')

    def test_show_json_tempat(self):
        response = self.client.get(reverse('zoya:show_json_tempat'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_show_json_forum(self):
        response = self.client.get(reverse('zoya:show_json_forum'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_add_forum_entry_ajax_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('zoya:add_forum_entry_ajax'),
            {'comment': 'New Test Comment'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(CommunityForum.objects.filter(comment='New Test Comment').exists())

    def test_add_forum_entry_ajax_unauthenticated(self):
        response = self.client.post(
            reverse('zoya:add_forum_entry_ajax'),
            {'comment': 'New Test Comment'}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_forum_entry_authenticated_owner(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.delete(
            reverse('zoya:delete_forum_entry', args=[self.forum_entry.id])
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CommunityForum.objects.filter(id=self.forum_entry.id).exists())

    def test_delete_forum_entry_unauthenticated(self):
        response = self.client.delete(
            reverse('zoya:delete_forum_entry', args=[self.forum_entry.id])
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(CommunityForum.objects.filter(id=self.forum_entry.id).exists())

    def test_edit_forum_entry(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('zoya:edit_forum_entry', args=[self.forum_entry.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_forum.html')

    def test_get_user_by_id(self):
        response = self.client.get(
            reverse('zoya:get_user_by_id', args=[self.user.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['username'], 'testuser')

    def test_get_current_user_id_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('zoya:get_current_user_id'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['user_id'], self.user.id)

    def test_get_current_user_id_unauthenticated(self):
        response = self.client.get(reverse('zoya:get_current_user_id'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIsNone(data['user_id'])
