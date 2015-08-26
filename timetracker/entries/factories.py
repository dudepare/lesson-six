from django.utils import timezone
from datetime import timedelta
import factory

from .models import (Client, Project, Entry)


class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    name = "Monolith Co."


class ProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Project

    name = "Disruptive App"
    client = factory.SubFactory(ClientFactory)


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entry
        exclude = ('start_time', 'stop_time')

    start_time = timezone.now()
    stop_time = start_time + timedelta(hours=1)
    start = timezone.now()
    stop = start + timedelta(hours=1)
    project = factory.SubFactory(ProjectFactory)
    description = "changed line endings"
