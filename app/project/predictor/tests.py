from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from project.predictor.models import Team


# Create your tests here.

class TeamTest(APITestCase):

    def setUp(self):
                # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.team_create = reverse('team-list')
        self.client.force_authenticate(user=self.test_user)

    def test_create_team(self):
        """
        Ensure we can create a Team object
        """
        data = {
            'name': 'Guatemala',
            'flag': 'gt'
        }
        
        response = self.client.post(self.team_create, data, format='json')

        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(Team.objects.count(),1)


    def test_create_team_without_flag(self):
        """
        Ensure we get error bad request 
        """
        data = {
            'name': 'Guatemala'
        }

        response = self.client.post(self.team_create, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(),0)