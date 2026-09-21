from django.test import Client, TestCase, override_settings


@override_settings(DEBUG=True)
class ArchitectureGeneratorAnonymousTests(TestCase):
    def test_generate_endpoint_allows_anonymous_demo_requests(self):
        client = Client()
        response = client.post(
            '/api/v1/architecture/generate/',
            {'prompt': 'A simple AWS web app with ALB, EC2, and RDS', 'cloud_provider': 'aws'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('diagram_data', response.json())
