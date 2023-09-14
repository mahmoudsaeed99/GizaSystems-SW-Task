from rest_framework.test import  APITestCase , APIRequestFactory
from .views.SimulateController import SimulateController
from django.urls import reverse
from django.shortcuts import redirect , render
from rest_framework import status


class TestSimulator(APITestCase) :
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SimulateController.as_view()
        self.urls = reverse("simulate")

    def test_get_simulator(self):
        request = self.factory.get(self.urls)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        #simulator_1
        self.assertEqual(response.data['name'], "simulator_1")

    def test_post_simulator(self):
        data = {
            "startDate":"2018-11-02",
            "name":"simulator_1",
            "timeSeries_type":"multiplicative",
            "producer_type":"type1",
            "endDate":"2018-11-02",
            "dataset":[{
                "frequency":"H1",
                "trend_coefficients":[0,2,1,3],
                "missing_percentage":0.06,
                "outlier_percentage":10,
                "noise_level":10,
                "cycle_amplitude":0,
                "cycle_frequency":1,
                "seasonality_components":[{
                    "frequency":"Weekly",
                    "multiplier":1,
                    "phase_shift":0,
                    "amplitude":3
                }]
                }]

            }

        request = self.factory.post(self.urls,data)
        response = self.view(request)
        self.assertEqual(response.status_code , status.HTTP_200_OK)

