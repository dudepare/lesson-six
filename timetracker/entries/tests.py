from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from .factories import (ClientFactory, ProjectFactory, EntryFactory)
from .forms import (ClientForm, ProjectForm, EntryForm)
from .models import (Client, Project, Entry)


class TestModels(TestCase):

    client_name = "Mister Mann"
    project_name = "devops"

    def test_strClientModel(self):
        client = ClientFactory()
        self.assertEqual(str(client), client.name)

    def test_strProjectModel(self):
        project = ProjectFactory()
        self.assertEqual(
            str(project),
            '<{}> {}'.format(project.client.name, project.name)
        )

    def test_strEntryModel(self):
        entry = EntryFactory()
        self.assertEqual(
            str(entry),
            '[{} - {}] ({}) {}'.format(entry.start, entry.stop, entry.project.name, entry.description))


class TestViews(TestCase):

    client_name = 'Blah Client'
    project_name = 'Blah Project'

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
        client = ClientFactory()
        data = {
            'name': self.project_name,
            'client': str(client.id)
        }
        response = self.client.post(
            '/projects/', data, follow=True
        )
        self.assertRedirects(response, '/projects/', 302, 200)
        self.assertContains(response, self.project_name)
        self.assertContains(response, client.name)

    def test_createValidEntryWithoutEndTime(self):
        start = timezone.now()
        project = ProjectFactory()
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

        client = ClientFactory(name=self.client_name)
        response = self.client.get('/clients/')
        self.assertContains(response, client.name)

        detail_url = '/clients/{}/'.format(client.id)
        response = self.client.get(detail_url)
        data = response.context['form'].initial
        self.assertEqual(data['name'], client.name)

        new_client = "Fodra Co."
        data['name'] = new_client
        response = self.client.post(detail_url, data, follow=True)
        self.assertContains(response, new_client)

    def test_editProjectDetail(self):
        response = self.client.get('/projects/')
        self.assertNotContains(response, self.project_name)
        self.assertNotContains(response, self.client_name)

        project = ProjectFactory(name=self.project_name, client__name=self.client_name)

        response = self.client.get('/projects/')
        self.assertContains(response, self.project_name)
        self.assertContains(response, self.client_name)

        detail_url = '/projects/{}/'.format(project.id)
        response = self.client.get(detail_url)
        self.assertEqual(response.context['form'].initial['name'], self.project_name)
        self.assertEqual(response.context['form'].initial['client'], project.client.id)

        new_project = "Disruptive android app"
        data = response.context['form'].initial
        data['name'] = new_project
        response = self.client.post(detail_url, data, follow=True)
        self.assertContains(response, new_project)
        self.assertNotContains(response, self.project_name)
        self.assertContains(response, self.client_name)


class TestForms(TestCase):

    client_name = "Dingo"
    project_name = "Disruptive App"
    start = timezone.now()
    description = "fixed line endings"

    def test_clientFormValidName(self):
        form = ClientForm({'name': self.client_name})
        self.assertTrue(form.is_valid())
        client = form.save(commit=False)
        self.assertEqual(client.name, self.client_name)

    def test_clientFormBlankName(self):
        form = ClientForm({'name': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'name': ['This field is required.']})

    def test_projectFormValidStuff(self):
        client = ClientFactory()
        form = ProjectForm({
            'name': self.project_name,
            'client': str(client.id)
        })
        self.assertTrue(form.is_valid())
        project = form.save()
        self.assertEqual(project.name, self.project_name)
        self.assertEqual(project.client.name, client.name)

    def test_entryFormValidData(self):
        project = ProjectFactory()
        stop = self.start + timedelta(hours=1)
        form = EntryForm({
            'start': self.start.strftime("%Y-%m-%d %H:%M"),
            'stop': stop.strftime("%Y-%m-%d %H:%M"),
            'project': str(project.id),
            'description': self.description
        })
        self.assertTrue(form.is_valid())
        entry = form.save(commit=False)
        self.assertEqual(
            entry.start.strftime("%Y-%m-%d %H:%M"),
            self.start.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(
            entry.stop.strftime("%Y-%m-%d %H:%M"),
            stop.strftime("%Y-%m-%d %H:%M")
        )
        self.assertEqual(entry.project.name, project.name)
        self.assertEqual(entry.description, self.description)

    def test_entryFormStartComesAfterNow(self):
        project = ProjectFactory()
        one_hour = timedelta(hours=1)
        self.start += one_hour
        stop = self.start + one_hour
        form = EntryForm({
            'start': self.start.strftime("%Y-%m-%d %H:%M"),
            'stop': stop.strftime("%Y-%m-%d %H:%M"),
            'project': str(project.id),
            'description': self.description
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'start': ['Start time must be in the past']})

    def test_entryFormStopComesBeforeStart(self):
        project = ProjectFactory()
        one_hour = timedelta(hours=1)
        stop = self.start - one_hour
        form = EntryForm({
            'start': self.start.strftime("%Y-%m-%d %H:%M"),
            'stop': stop.strftime("%Y-%m-%d %H:%M"),
            'project': str(project.id),
            'description': self.description
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['End time must come after start time']})

    def test_entryFormCreateWithEndNow(self):
        project = ProjectFactory()
        form = EntryForm({
            'start': self.start.strftime("%Y-%m-%d %H:%M"),
            'stop': "",
            'project': str(project.id),
            'description': self.description,
            'submit_end_now': "Create Entry with End Now"
        })
        self.assertTrue(form.is_valid())
        entry = form.save(commit=False)
        self.assertEqual(
            entry.start.strftime("%Y-%m-%d %H:%M"),
            self.start.strftime("%Y-%m-%d %H:%M")
        )
        self.assertIsNotNone(entry.stop)
        self.assertEqual(entry.project.name, project.name)
        self.assertEqual(entry.description, self.description)

