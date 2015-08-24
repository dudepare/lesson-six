from django.test import TestCase
from django.utils import timezone
from datetime import timedelta


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
        self.assertContains(response, self.project_name)
        self.assertContains(response, self.client_name)

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

    def test_editClientDetail(self):
        response = self.client.get('/clients/')
        self.assertNotContains(response, self.client_name)
        
        Client.objects.create(name=self.client_name)
        response = self.client.get('/clients/')
        self.assertContains(response, self.client_name)
        
        detail_url = '/clients/{}/'.format(Client.objects.last().id)
        response = self.client.get(detail_url)
        data = response.context['form'].initial
        self.assertEqual(data['name'], self.client_name)
        
        new_client = "Fodra Co."
        data['name'] = new_client
        response = self.client.post(detail_url, data, follow=True)
        self.assertContains(response, new_client)

    def test_editProjectDetail(self):
        response = self.client.get('/projects/')
        self.assertNotContains(response, self.project_name)
        self.assertNotContains(response, self.client_name)
        
        Client.objects.create(name=self.client_name)
        client_id = Client.objects.last().id
        Project.objects.create(
            name=self.project_name, 
            client_id=str(client_id)
        )
        
        response = self.client.get('/projects/')
        self.assertContains(response, self.project_name)
        self.assertContains(response, self.client_name)

        detail_url = '/projects/{}/'.format(Project.objects.last().id)
        response = self.client.get(detail_url)
        self.assertEqual(response.context['form'].initial['name'], self.project_name)
        self.assertEqual(response.context['form'].initial['client'], client_id)

        new_project = "Disruptive android app"
        data = response.context['form'].initial
        data['name'] = new_project
        response = self.client.post(detail_url, data, follow=True)
        self.assertContains(response, new_project)
        self.assertNotContains(response, self.project_name)
        self.assertContains(response, self.client_name)

    def test_strClientModel(self):
        Client.objects.create(name=self.client_name)
        self.assertEqual(str(Client.objects.last()), self.client_name)

    def test_strProjectModel(self):
        Client.objects.create(name=self.client_name)
        client_id = Client.objects.last().id
        Project.objects.create(
            name=self.project_name,
            client_id=str(client_id)
        )
        self.assertEqual(
            str(Project.objects.last()),
            '<{}> {}'.format(self.client_name, self.project_name)
        )

    def test_strEntryModel(self):
        Client.objects.create(name=self.client_name)
        client_id = Client.objects.last().id
        Project.objects.create(
            name=self.project_name,
            client_id=str(client_id)
        )
        project_id = Project.objects.last().id
        start_time = timezone.now()
        stop_time = start_time + timedelta(hours=1)
        description_ = 'this is a big one.'
        Entry.objects.create(
            start=start_time,
            stop=stop_time,
            project_id=str(project_id),
            description=description_)
        self.assertEqual(
            str(Entry.objects.last()),
            '[{} - {}] ({}) {}'.format(start_time, stop_time, self.project_name, description_))
