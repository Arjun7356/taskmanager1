from django.shortcuts import render, redirect
from django.views import View
from task.models import Task
from task.forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class TaskListView(View):
    template_name = "task_list.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(user=request.user)
        return render(request, self.template_name, {"tasks": tasks})

class TaskCreateView(View):
    template_name = "task_form.html"
    form_class = TaskForm

    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task-list")
        return render(request, self.template_name, {"form": form})

class TaskUpdateView(View):
    template_name = "task_form.html"
    form_class = TaskForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'), user=request.user)
        form = self.form_class(instance=task)
        return render(request, self.template_name, {"form": form, "task": task})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'), user=request.user)
        form = self.form_class(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task-list")
        return render(request, self.template_name, {"form": form, "task": task})

class TaskDeleteView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        task = Task.objects.get(id=kwargs.get('pk'), user=request.user)
        task.delete()
        return redirect("task-list")

class UserLoginView(View):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task-list')
        return render(request, self.template_name, {'error': 'Invalid credentials'})

class UserLogoutView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
