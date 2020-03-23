from django.contrib.auth.models import User
from django.test import TestCase, Client

# Create your tests here.
from .models import Image
import json

# Create your tests here.
class GalleryTestCase(TestCase):

    def test_list_images_status(self):
        url = '/gallery/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_count_images_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model, isPublic=True)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model, isPublic=True)
        Image.objects.create(name='nuevo3', url='No', description='testImage', type='jpg', user=user_model, isPublic=True)

        response = self.client.get('/gallery/')
        current_data = json.loads(response.content)
        print(current_data)
        self.assertEqual(len(current_data), 3)

    def test_verify_first_from_images_list(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model,  isPublic=True)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model,  isPublic=True)
        Image.objects.create(name='nuevo3', url='No', description='testImage', type='jpg', user=user_model,  isPublic=True)

        response = self.client.get('/gallery/')
        current_data = json.loads(response.content)

        self.assertEqual(current_data[0]['fields']['name'], "nuevo")

    def test_add_user(self):
        response = self.client.post('/gallery/addUser/', json.dumps(
            {"username": "testUser", "first_name": "Test", "last_name": "User", "password": "AnyPas#5",
             "email": "test@test.com"}), content_type='application/json')
        current_data = json.loads(response.content)
        self.assertEqual(current_data[0]['fields']['username'], 'testUser')

    def test_portafolio_public(self):

        user_model = User.objects.create_user(username='testUser', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        Image.objects.create(name='nuevo', url='No', description='testImage', type='jpg', user=user_model, isPublic=True)
        Image.objects.create(name='nuevo2', url='No', description='testImage', type='jpg', user=user_model,isPublic=False)

        response = self.client.get('/gallery/portafolioFiltroPublico/?username=testUser')
        current_data = json.loads(response.content)
        print(current_data)
        self.assertEqual(current_data[0]['fields']['isPublic'], True)

    def test_login(self):
        user_model = User.objects.create_user(username='test', password='kd8wke-DE34', first_name='test',
                                              last_name='test', email='test@test.com')
        response = self.client.post('/gallery/login/', json.dumps(
            {"username": "test", "password": "kd8wke-DE34"}), content_type='application/json')
        current_data = json.loads(response.content)
        print(current_data)
        self.assertEqual(current_data['user'], "test")