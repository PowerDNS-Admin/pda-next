from django.test import Client, TestCase


class ApiSchemaTestCase(TestCase):
    def test_schema_filters(self):
        c = Client()
        response = c.get("/api/schema/")
        response_yaml = response.content.decode("utf-8")
        self.assertFalse("/cms/" in response_yaml)
