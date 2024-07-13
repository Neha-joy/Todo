from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, ProjectForm, TaskForm
from .models import CustomUser, Project, Task

def dashboard(request):
    projects = []
    tasks = []

    if request.user.role == 'admin':
        projects = Project.objects.all()
    elif request.user.role == 'team_lead':
        projects = Project.objects.filter(assigned_to=request.user)
        tasks = Task.objects.filter(project__assigned_to=request.user)
    elif request.user.role == 'team_member':
        tasks = Task.objects.filter(assigned_to=request.user)

    context = {
        'projects': projects,
        'tasks': tasks
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'admin':
        projects = Project.objects.all()
    elif user.role == 'team_lead':
        projects = Project.objects.filter(assigned_to=user)
    else:
        projects = Project.objects.filter(tasks__assigned_to=user).distinct()
    return render(request, 'dashboard.html', {'projects': projects})

@login_required
def create_project(request):
    if not request.user.role == 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    team_leads = CustomUser.objects.filter(role='team_lead')
    return render(request, 'create_project.html', {'form': form, 'team_leads': team_leads})

@login_required
def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    if not request.user.role == 'admin':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    team_leads = CustomUser.objects.filter(role='team_lead')
    return render(request, 'edit_project.html', {'form': form, 'team_leads': team_leads})

@login_required
def delete_project(request, project_id):
    if not request.user.role == 'admin':
        return redirect('dashboard')

    project = Project.objects.get(pk=project_id)
    project.delete()
    return redirect('project_list')

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def is_admin(user):
    return user.role == 'admin'

@user_passes_test(is_admin)
def create_project(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to = CustomUser.objects.get(pk=request.POST['assigned_to'])
        Project.objects.create(title=title, description=description, created_by=request.user, assigned_to=assigned_to)
        return redirect('project_list')
    team_leads = CustomUser.objects.filter(role='team_lead')
    return render(request, 'create_project.html', {'team_leads': team_leads})

@user_passes_test(is_admin)
def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.assigned_to = CustomUser.objects.get(pk=request.POST['assigned_to'])
        project.save()
        return redirect('project_list')
    team_leads = CustomUser.objects.filter(role='team_lead')
    return render(request, 'edit_project.html', {'project': project, 'team_leads': team_leads})

@user_passes_test(is_admin)
def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    return redirect('project_list')

def is_team_lead(user):
    return user.role == 'team_lead'

@user_passes_test(is_team_lead)
def create_task(request, project_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to = CustomUser.objects.get(pk=request.POST['assigned_to'])
        project = Project.objects.get(pk=project_id)
        Task.objects.create(title=title, description=description, status='to_do', project=project, assigned_to=assigned_to, created_by=request.user)
        return redirect('project_detail', project_id=project_id)
    team_members = CustomUser.objects.filter(role='team_member')
    return render(request, 'create_task.html', {'team_members': team_members})

@user_passes_test(is_team_lead)
def edit_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.status = request.POST['status']
        task.assigned_to = CustomUser.objects.get(pk=request.POST['assigned_to'])
        task.save()
        return redirect('project_detail', project_id=task.project.id)
    team_members = CustomUser.objects.filter(role='team_member')
    return render(request, 'edit_task.html', {'task': task, 'team_members': team_members})

@user_passes_test(is_team_lead)
def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    project_id = task.project.id
    task.delete()
    return redirect('project_detail', project_id=project_id)

@user_passes_test(is_team_lead)
def project_detail(request, project_id):
    project = Project.objects.get(pk=project_id)
    tasks = project.tasks.all()
    return render(request, 'project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def view_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'view_tasks.html', {'tasks': tasks})

@login_required
def update_task_status(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        task.status = request.POST['status']
        task.save()
        return redirect('view_tasks')
    return render(request, 'update_task_status.html', {'task': task})
