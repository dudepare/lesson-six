from django.shortcuts import render, get_object_or_404, redirect

from .forms import EntryForm, ProjectForm, ClientForm
from .models import Client, Entry, Project


def clients(request):
    if request.method == 'POST':
        # Create our form object with our POST data
        form = ClientForm(request.POST)
        if form.is_valid():
            # If the form is valid, create a client with submitted data
            # Below is the shortcut equivalent of:
            # client = Client()
            # client.name = form.cleaned_data['name']
            # client.save()
            # Sometimes you don't want to save the object until the end,
            # sometimes you don't care!
            client = Client.objects.create(name=form.cleaned_data['name'])
            return redirect('client-list')
    else:
        form = ClientForm()

    client_list = Client.objects.all()
    return render(request, 'clients.html', {
        'client_list': client_list,
        'form': form,
    })


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            # Update client details
            client.name = form.cleaned_data['name']
            client.save()
            return redirect('client-list')
    else:
        # Initialise form with client data
        form = ClientForm(initial={'name': client.name})

    return render(request, 'client_detail.html', {
        'client': client,
        'form': form,
    })


def entries(request):
    if request.method == 'POST':
        # Create our form object with our POST data
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            # If the form is valid, let's create and Entry with the submitted data
            entry = Entry()
            entry.start = entry_form.cleaned_data['start']
            entry.stop = entry_form.cleaned_data['stop']
            entry.project = entry_form.cleaned_data['project']
            entry.description = entry_form.cleaned_data['description']
            entry.save()
            return redirect('entry-list')
    else:
        entry_form = EntryForm()

    entry_list = Entry.objects.all()
    return render(request, 'entries.html', {
        'entry_list': entry_list,
        'entry_form': entry_form,
    })


def projects(request):
    if request.method == 'POST':
        # Create our form object with our POST data
        form = ProjectForm(request.POST)
        if form.is_valid():
            Project.objects.create(
                name=form.cleaned_data['name'],
                client=form.cleaned_data['client']
            )
            return redirect('project-list')
    else:
        form = ProjectForm()

    project_list = Project.objects.all()
    return render(request, 'projects.html', {
        'project_list': project_list,
        'form': form
    })


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Update project details
            project.name = form.cleaned_data['name']
            project.client=form.cleaned_data['client']
            project.save()
            return redirect('project-list')
    else:
        # Initialise form with project data
        form = ProjectForm(initial={'name': project.name, 'client': project.client})

    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {
        'project': project,
        'form': form,
    })
