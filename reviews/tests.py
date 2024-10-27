
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from zoya.models import TempatKuliner, Variasi
from .models import Review
from django.utils import timezone
import json
from decimal import Decimal
from django.db.models import Avg
from django.contrib.messages import get_messages
from django.db import IntegrityError

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='userA', password='pass12345')
        self.user2 = User.objects.create_user(username='userB', password='pass12345')

        self.variasi1 = Variasi.objects.create(nama='Perunggasan')
        self.variasi2 = Variasi.objects.create(nama='Masakan Indonesia')

        self.tempat = TempatKuliner.objects.create(
            nama='Ayam Kremes Mas Harjo',
            description='A place with delicious Indonesian-styled fried kremes chicken.',
            alamat='123 Sample Street',
            longitude='106.8456',
            latitude='-6.2088',
            jamBuka='09:00:00',
            jamTutup='21:00:00',
            rating=None,
            foto_link='https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg'
        )
        self.tempat.variasi.set([self.variasi1, self.variasi2])

    def test_create_review(self):

        review = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=5,
            comment='Excellent!',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review.user, self.user1)
        self.assertEqual(review.tempat_kuliner, self.tempat)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Excellent!')

        expected_str = f'Review by {self.user1.username} for {self.tempat}'
        self.assertEqual(str(review), expected_str)

    def test_rating_choices_valid(self):

        for rating, _ in Review.RATING_CHOICES:
            review = Review(
                user=self.user1,
                tempat_kuliner=self.tempat,
                rating=rating,
                comment='Good',
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            try:
                review.full_clean()
                review.save()
            except Exception as e:
                self.fail(f'Valid rating {rating} raised an exception: {e}')

        self.assertEqual(Review.objects.count(), len(Review.RATING_CHOICES))

    def test_rating_choices_invalid(self):
        review = Review(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=6,  # Invalid rating
            comment='Invalid  review rating test .',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        with self.assertRaises(Exception) as context:
            review.full_clean()  # Expect a ValidationError
        self.assertTrue('rating' in context.exception.message_dict)

    def test_update_rating(self):
        self.assertIsNone(self.tempat.rating)
        review1 = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=4,
            comment='Good',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.tempat.update_rating()
        self.tempat.refresh_from_db()
        self.assertEqual(self.tempat.rating, Decimal('4.00'))

        review2 = Review.objects.create(
            user=self.user2,
            tempat_kuliner=self.tempat,
            rating=2,
            comment='Not great',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.tempat.update_rating()
        self.tempat.refresh_from_db()
        self.assertEqual(self.tempat.rating, Decimal('3.00'))

        review2.delete()
        self.tempat.update_rating()
        self.tempat.refresh_from_db()
        self.assertEqual(self.tempat.rating, Decimal('4.00'))
        review1.delete()
        self.tempat.update_rating()
        self.tempat.refresh_from_db()
        self.assertIsNone(self.tempat.rating)

    def test_comment_blank_allowed(self):
        review = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=3,
            comment='',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.assertEqual(review.comment, '')

    def test_comment_null_checking(self):
        review = Review(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=3,
            comment=None,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        review.full_clean()

    def test_related_name_reviews(self):
        review = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=5,
            comment='Awesome!',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.assertIn(review, self.tempat.reviews.all())

    def test_user_deletion_cascade(self):
        review = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=4,
            comment='Good',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.user1.delete()
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_tempat_kuliner_deletion_cascade(self):
        # Test that if we delete a TempatKuliner, the system cascades and deletes associated Reviews.
        review = Review.objects.create(
            user=self.user1,
            tempat_kuliner=self.tempat,
            rating=4,
            comment='Good',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.tempat.delete()
        self.assertFalse(Review.objects.filter(id=review.id).exists())

class ReviewViewTests(TestCase):
    def setUp(self):
        # Create users with consistent usernames
        self.userA = User.objects.create_user(username='userA', password='pass12345')
        self.userB = User.objects.create_user(username='userB', password='pass12345')
        
        # Create Variasi instances
        self.variasi1 = Variasi.objects.create(nama='Perunggasan')
        self.variasi2 = Variasi.objects.create(nama='Masakan Indonesia')
        
        # Create TempatKuliner with all required fields
        self.tempat = TempatKuliner.objects.create(
            nama='Ayam Kremes Mas Harjo',
            description='A place with delicious Indonesian-styled fried kremes chicken.',
            alamat='123 Sample Street',
            longitude='106.8456',
            latitude='-6.2088',
            jamBuka='09:00:00',
            jamTutup='21:00:00',
            rating=5.00,
            foto_link='https://cdn.britannica.com/36/123536-050-95CB0C6E/Variety-fruits-vegetables.jpg'
        )
        self.tempat.variasi.set([self.variasi1, self.variasi2])
        
        # Create a review by userA
        self.review1 = Review.objects.create(
            user=self.userA,
            tempat_kuliner=self.tempat,
            rating=5,
            comment='Great place!',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        
        self.client = Client()

    def test_user_owned_reviews_authenticated(self):
        # Log in as userA
        self.client.login(username='userA', password='pass12345')

        response = self.client.get(reverse('reviews:my_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great place!')
        self.assertQuerysetEqual(
            response.context['reviews'],
            [self.review1],
            transform=lambda x: x
        )

    def test_user_owned_reviews_unauthenticated(self):
        response = self.client.get(reverse('reviews:my_reviews'))

        login_url = reverse('main:login_user')
        expected_url = f'{login_url}?next={reverse("reviews:my_reviews")}'
        self.assertRedirects(response, expected_url)


    def test_create_review_success(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:create_review', args=[self.tempat.id])
        data = {
            'rating': '4',
            'comment': 'Good food.',
        }
        response = self.client.post(url, data, follow=True)
        
        # Ensure URL reversal uses 'tempatKulinerId'
        expected_redirect = reverse('marco:get_restaurant', kwargs={'tempatKulinerId': self.tempat.id})
        self.assertRedirects(response, expected_redirect)
        
        # Check messages in the response
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your review has been submitted successfully." in str(message) for message in messages))
        
        # Verify the review was created
        self.assertTrue(Review.objects.filter(user=self.userB, tempat_kuliner=self.tempat).exists())

    def test_create_review_duplicate(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:create_review', args=[self.tempat.id])
        data = {
            'rating': '4',
            'comment': 'Another review.',
        }
        response = self.client.post(url, data, follow=True)
        
        expected_redirect = reverse('marco:get_restaurant', kwargs={'tempatKulinerId': self.tempat.id})
        self.assertRedirects(response, expected_redirect)
        
        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You have already reviewed this place." in str(message) for message in messages))
        
        # Ensure only one review exists for userA
        self.assertEqual(Review.objects.filter(user=self.userA, tempat_kuliner=self.tempat).count(), 1)

    def test_create_review_invalid_rating(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:create_review', args=[self.tempat.id])
        data = {
            'rating': '6',  # This rating is not valid
            'comment': 'Invalid rating test.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Rating is not valid" in str(message) for message in messages))
        
        # Ensure the review was not created
        self.assertFalse(Review.objects.filter(user=self.userB, tempat_kuliner=self.tempat, rating=6).exists())

    def test_create_review_missing_rating(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:create_review', args=[self.tempat.id])
        data = {
            'comment': 'Missing rating.',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Rating is required." in str(message) for message in messages))
        
        # Ensure the review was not created
        self.assertFalse(Review.objects.filter(user=self.userB, tempat_kuliner=self.tempat).exists())

    def test_create_review_empty_comment(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:create_review', args=[self.tempat.id])
        data = {
            'rating': '3',
            'comment': '',
        }
        response = self.client.post(url, data, follow=True)
        
        expected_redirect = reverse('marco:get_restaurant', kwargs={'tempatKulinerId': self.tempat.id})
        self.assertRedirects(response, expected_redirect)
        
        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Your review has been submitted successfully." in str(message) for message in messages))
        
        # Verify the review was created with an empty comment
        self.assertTrue(Review.objects.filter(user=self.userB, tempat_kuliner=self.tempat, rating=3, comment='').exists())

    def test_get_reviews_authenticated(self):
        # Create another review by userB
        Review.objects.create(
            user=self.userB,
            tempat_kuliner=self.tempat,
            rating=4,
            comment='Good service.',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:get_reviews', args=[self.tempat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        reviews = json.loads(response.content)
        self.assertEqual(len(reviews), 2)
        
        # Check for correct usernames
        usernames = [review['user'] for review in reviews]
        self.assertIn('userA', usernames)
        self.assertIn('userB', usernames)

    def test_get_reviews_unauthenticated(self):
        url = reverse('reviews:get_reviews', args=[self.tempat.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        login_url = reverse('main:login_user')
        expected_redirect = f'{login_url}?next={url}'
        self.assertRedirects(response, expected_redirect, fetch_redirect_response=False)

    def test_get_review_by_id_success(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:get_review_by_id', args=[self.review1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        review_data = json.loads(response.content)
        expected_data = {
            "user": self.review1.user.username,
            "rating": self.review1.rating,
            "comment": self.review1.comment,
            "created_at": self.review1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "id": self.review1.id,
            "pk": self.review1.pk
        }
        self.assertEqual(review_data, expected_data)

    def test_get_review_by_id_not_found(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:get_review_by_id', args=[999])  # Assuming 999 doesn't exist
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_review_ajax(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:delete_review', args=[self.review1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Review deleted successfully.')
        self.assertFalse(Review.objects.filter(id=self.review1.id).exists())

    def test_delete_review_non_ajax(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:delete_review', args=[self.review1.id])
        response = self.client.post(url, follow=True)
        expected_redirect = reverse('marco:get_restaurant', kwargs={'tempatKulinerId': str(self.tempat.id)})
        self.assertRedirects(response, expected_redirect)
        self.assertFalse(Review.objects.filter(id=self.review1.id).exists())

    def test_delete_review_not_owner_ajax(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:delete_review', args=[self.review1.id])
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)  # Should not find the review for userB
        self.assertTrue(Review.objects.filter(id=self.review1.id).exists())

    def test_delete_review_not_owner_non_ajax(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:delete_review', args=[self.review1.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Review.objects.filter(id=self.review1.id).exists())

    def test_edit_review_success(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        data = {
            'rating': 4,
            'comment': 'Updated comment.',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Review updated successfully.')
        
        # Refresh from DB and verify changes
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.rating, 4)
        self.assertEqual(self.review1.comment, 'Updated comment.')

    def test_edit_review_invalid_rating(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        data = {
            'rating': 6,
            'comment': 'Invalid rating update.',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('Invalid rating value.', response_data['message'])
        
        # Ensure the review was not updated
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.rating, 5)  # Unchanged

    def test_edit_review_missing_data(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        data = {}  # No data provided
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Review updated successfully.')
        
        # Refresh from DB and verify no changes
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.rating, 5)  # Unchanged
        self.assertEqual(self.review1.comment, '')  # Unchanged

    def test_edit_review_not_owner(self):
        self.client.login(username='userB', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        data = {
            'rating': 3,
            'comment': 'WRONG edit.',
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
        # Ensure the review was not updated
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.rating, 5)
        self.assertEqual(self.review1.comment, 'Great place!')

    def test_edit_review_invalid_method(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_edit_review_invalid_json(self):
        self.client.login(username='userA', password='pass12345')
        url = reverse('reviews:edit_review', args=[self.review1.id])
        invalid_json = "This is not JSON"
        response = self.client.post(url, invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Invalid JSON data.')
        
        # Ensure the review was not updated
        self.review1.refresh_from_db()
        self.assertEqual(self.review1.comment, 'Great place!')