import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from api.views import HealthStatusView


class TestHealthStatusView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = HealthStatusView.as_view()

    def test_health_status(self):
        request = self.factory.get('api/health/status')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = json.loads(response.content)
        self.assertEqual(response_json, {'status': 'healthy'})
