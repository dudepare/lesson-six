from django.test import TestCase
from django.utils import timezone


from .models import (Client, Project, Entry)


class TestViews(TestCase):

    client_name = 'Monolith Co.'
    project_name = 'Disruptive App'

    def test_rootRedirectsToClientView(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/clients/', 302, 200)

    def test_createValidClient(self):
        data = {'name': self.client_name}
        response = self.client.post(
            '/clients/', data, follow=True
        )
        self.assertRedirects(response, '/clients/', 302, 200)
        self.assertContains(response, self.client_name)

    def test_createValidProject(self):
        client_obj = Client.objects.create(name=self.client_name)
        data = {
            'name': self.project_name,
            'client': str(client_obj.id)
        }
        response = self.client.post(
            '/projects/', data, follow=True
        )
        self.assertRedirects(response, '/projects/', 302, 200)
        expected = '<a href="/projects/1/">{}</a> (<a href="/clients/1/">{}</a>)'.format(self.project_name, self.client_name)
        self.assertContains(response, expected)

    def test_createValidEntryWithoutEndTime(self):
        start = timezone.now()
        client = Client.objects.create(name=self.client_name)
        project = Project.objects.create(name=self.project_name, client_id=str(client.id))
        description = 'Tralalala'
        data = {
            'start': start.strftime("%Y-%m-%d %H:%M"),
            'stop': "",
            'project': str(project.id),
            'description': description
        }
        response = self.client.post(
            '/entries/', data, follow=True
        )
        self.assertRedirects(response, '/entries/', 302, 200)
        self.assertContains(response, description)
