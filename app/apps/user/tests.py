from rest_framework.response import Response
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from .models.user import User
from .views.user import RegisterUserAPIView, LogInAPIView, LogOutAPIView


# Create your tests here.
class UserTests(APITestCase):
    factory = APIRequestFactory()

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        userdata = {
           "first_name": "firstname",
           "last_name": "lastname",
           'email': 'test@te.st',
           'username': 'testname',
           # 'password': 'p@55w0rDp@55w0rD',
           # 're_password': 'p@55w0rDp@55w0rD',
        }
        User.objects.create(**userdata)

    def test_register_user_happy_path(self):
        """
        Successful registration of the user:
        {
           "first_name": "firstname",
           "last_name": "lastname",
           'email': 'username@te.st',
           'username': 'username',
           'password': 'p@55w0rDp@55w0rD',
           're_password': 'p@55w0rDp@55w0rD'
        }
        """
        request = self.factory.post('/api/v1/auth-register/',
                               {
                                   "first_name": "firstname",
                                   "last_name": "lastname",
                                   'email': 'username@te.st',
                                   'username': 'username',
                                   'password': 'p@55w0rDp@55w0rD',
                                   're_password': 'p@55w0rDp@55w0rD',
                               },
                               content_type='application/json')
        view = RegisterUserAPIView().as_view()

        response: Response = view(request)
        self.assertFalse(response.data['is_staff'])
        self.assertFalse(response.data['is_superuser'])
        self.assertTrue(response.data['is_active'])
        self.assertTrue(response.cookies.get('access_token'), msg='access_token should be in cookies')
        self.assertTrue(response.cookies.get('refresh_token'), msg='refresh_token should be in cookies')
        self.assertFalse(response.exception, msg='Registration must be successful')

    def test_login_user_happy_path(self):
        """
        Successful login of the user:
        {
          'email': 'username@te.st',
          'password': 'p@55w0rDp@55w0rD'
        }
        """
        request = self.factory.post('/api/v1/auth-login/',
                               {
                                   'email': 'username@te.st',
                                   # 'username': 'username',
                                   'password': 'p@55w0rDp@55w0rD',
                               },
                               content_type='application/json')
        view = LogInAPIView().as_view()
        response: Response = view(request)

    def test_logout_user_happy_path(self):
        user = User.objects.get(id=1)
        self.assertGreater(User.objects.count(), 0,'one user must exist')
        self.assertEqual(user.first_name, 'firstname')
        request = self.factory.post('/api/v1/auth-logout')

        user: User = User.objects.all()[0]
        # user = User.objects.get(username='username')
        force_authenticate(request, user=user)

        view = LogOutAPIView().as_view()
        response: Response = view(request)
        self.assertFalse(response.exception, msg=response.data)
        print(response.cookies.items())
        # self.assertFalse(response.cookies.get('access_token')) # TODO: fully clear cookies

