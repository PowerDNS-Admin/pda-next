from django.test import TestCase


class TestApiSchema(TestCase):
    def test_schema_returns_success(self):
        response = self.client.get("/api/schema/")
        self.assertEqual(200, response.status_code)
