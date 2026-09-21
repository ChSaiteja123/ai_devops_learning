from django.test import Client, TestCase, override_settings


@override_settings(DEBUG=True)
class AIAssistantAnonymousChatTests(TestCase):
    def test_chat_endpoint_allows_anonymous_demo_requests(self):
        client = Client()
        response = client.post(
            '/api/v1/ai/chat/',
            {'message': 'Explain Docker in simple terms'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('reply', response.json())
