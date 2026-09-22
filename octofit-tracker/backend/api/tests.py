from django.test import SimpleTestCase
from django.urls import reverse


class OctofitTrackerApiTests(SimpleTestCase):
    def test_api_root_exists(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, 200)

    def test_api_root_includes_expected_endpoints(self):
        response = self.client.get(reverse('api-root'))
        payload = response.json()
        self.assertIn('users', payload)
        self.assertIn('teams', payload)
        self.assertIn('activities', payload)
        self.assertIn('leaderboard', payload)
        self.assertIn('workouts', payload)
