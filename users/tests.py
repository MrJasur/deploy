from django.test import TestCase
from .models import CustomUserModel
from django.urls import reverse
from django.contrib.auth import get_user

# Create your tests here.
class RegistrTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(reverse('users:register'), 
        data={
            "username":"coder",
            "first_name":"Jasurbek",
            "last_name":"Odilov",
            "email":"abc@gmail.com",
            "password":"1202abc",
        }
        )

        user = CustomUserModel.objects.get(username='coder')

        self.assertEqual(user.first_name, "Jasurbek")
        self.assertEqual(user.last_name, "Odilov")
        self.assertEqual(user.email, "abc@gmail.com")
        self.assertNotEqual(user.password, "1202abc")
        self.assertTrue(user.check_password('1202abc'))

    def test_register_page_status_code(self):
        response = self.client.get(reverse('users:register'))
        self.assertEquals(response.status_code, 200)

    def test_required_fields(self):
        response = self.client.post(reverse('users:register'),
        data = {
            'first_name':'Jasurbek',
            'email': 'abc@gmail.com',
        })
        user_count = CustomUserModel.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')


    def test_invalid_email(self):
        response = self.client.post(reverse('users:register'),
        data = {
            "username":"coder",
            "first_name":"Jasurbek",
            "last_name":"Odilov",
            "email":"invalid",
            "password":"1202abc",
        })
        user_count = CustomUserModel.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUserModel.objects.create(username = 'coder', first_name = 'Jasurbek')
        user.set_password('1202abc')
        user.save()

        response = self.client.post(reverse('users:register'),
        data = {
            "username":"coder",
            "first_name":"Jasurbek",
            "last_name":"Odilov",
            "email":"abcd@gmail.com",
            "password":"1202abc",
        })
        user_count = CustomUserModel.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')

class LoginTestCase(TestCase):
    def test_successful_login(self):
        user=CustomUserModel.objects.create(username='coder', first_name='Jasurbek')
        user.set_password('abc123')
        user.save()

        self.client.post(
            reverse('users:login'),
            data = {
                'username':'coder',
                'password':'abc123'
            }
        )

        user=get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        user = CustomUserModel.objects.create(username='coder')
        user.set_password('abc123')
        user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username':'coder2',
                'password':'1bc123'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        user = CustomUserModel.objects.create(username='coder3')
        user.set_password('abc123')
        user.save()

        self.client.post(
            reverse('users:login'),
            data={
                'username':'coder3',
                'password':'abc1234'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class LogoutTestCase(TestCase):

    #bazada user yaratyapmiz
    def test_logout(self):
        user = CustomUserModel.objects.create(
            username = 'coder',
            first_name = 'Jasurbek',
            last_name = 'Odilov',
            email = 'abc@gmail.com'
             )
        user.set_password('123')
        user.save()
    
        #user di login qildiryapmiz
        self.client.login(username='coder', password='123')

        #logout qildiryapmiz
        self.client.get(reverse('users:logout'))

        #login qilgan userni olvoldik
        user = get_user(self.client)
        #login qilgan user logout boldimi yodmi tekshirdik 
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        # print(response.status_code)
        self.assertEqual(response.url, reverse("users:login"))

    def test_profile_details(self):
        user = CustomUserModel.objects.create(
            username = 'coder1202',
            first_name = 'Jasurbek',
            last_name = 'Odilov',
            email = 'abc@gmail.com'
        )
        user.set_password('1202')
        user.save()

        # print(f'User soni: {User.objects.get(id=1).username}')

        self.client.login(username='coder1202', password='1202')
        
        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)


    def test_update_profile(self):
        user = CustomUserModel.objects.create(
            username = 'coder1202',
            first_name = 'Jasurbek',
            last_name = 'Odilov',
            email = 'abc@gmail.com'
        )
        user.set_password('1202')
        user.save()

        self.client.login(username='coder1202', password='1202')

        response = self.client.post(
            reverse("users:profile_edit"),
            
            data = {
                "username" : 'coder',
                "first_name" : 'Jasurbek',
                "last_name" : 'Odilov',
                "email" : 'abc123@gmail.com'
            }
        )

        # user = CustomUserModel.objects.get(pk=user.pk) #bu yerda eski userni olvoldik
        user.refresh_from_db()

        self.assertEqual(user.username, 'coder')
        self.assertEqual(user.email, 'abc123@gmail.com')
        self.assertEqual(response.url, reverse('users:profile'))

    
