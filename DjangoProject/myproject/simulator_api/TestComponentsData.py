from rest_framework.test import  APITestCase , APIRequestFactory
from .views.ComponentController import ComponentController
from django.urls import reverse
from django.shortcuts import redirect , render
from rest_framework import status


class TestSimulator(APITestCase) :
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ComponentController.as_view()
        self.urls = reverse("Components")

    def test_get_simulator(self):
        request = self.factory.get(self.urls)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

