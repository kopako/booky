# from django.test.utils import setup_test_environment
# setup_test_environment()
# from rest_framework.test import APITestCase, APIRequestFactory
# from django.urls import include, path, reverse
#
# from ..views import LocationView
# from apps.user.models.user import User
# from proj import settings
#
#
# class LocationTestCase(APITestCase):
#
#     def setUp(self):
#         User.objects.create_superuser(username='admin', email='admin@te.st', password='admin')
#         User.objects.create_user(username='user', email='user@te.st', password='user')
#
#     def test_list_location(self):
#         # url = reverse()
#         api_request = APIRequestFactory().get("/api/v1/a/location")
#         detail_view = LocationView.as_view({'get': 'retrieve'})
#         response = detail_view(api_request)
#         self.assertEqual(response.status_code, 401)
#
#
