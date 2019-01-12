import unittest
import os
import json
from pyphercises.app import app


class WeatherTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client

    def test_root_endpoint_redirection(self):
        """Test root API / for get"""
        res = self.client().get('/')
        self.assertEqual(res.status_code, 302)

    def test_base_endpoint_get(self):
        """Test base API /api/v1/ for get"""
        res = self.client().get('/api/v1/')
        app_name = "Basic weather app"
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["name"], app_name)

    def test_version_endpoint_get(self):
        """Test version API /api/v1/version for get"""
        res = self.client().get('/api/v1/version')
        from pyphercises.version import _app_version_
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["version"], _app_version_)

    def test_invalid_endpoint_get(self):
        """Test an endpoint that does not exist"""
        res = self.client().get('/api/v1/random')
        self.assertEqual(res.status_code, 404)

    def test_weather_api_default(self):
        """Test weather endpoint with default values"""
        res = self.client().get('/api/v1/weather')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.data)["error"], "Too few parameters")

    def test_invalid_metric_parameter(self):
        """Test invalid parameter for units"""
        res = self.client().get('/api/v1/weather?units=random')
        self.assertEqual(res.status_code, 400)
     

if __name__ == "__main__":
    unittest.main()
