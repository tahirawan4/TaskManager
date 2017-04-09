from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from tasks.forms import ContactForm
from tasks.models import Task


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')

        return render(request, self.template_name, {})


class HomeView(View):
    template_name = 'index.html'

    def mark_done(self, mark_done_id, remove=False):
        task = Task.objects.filter(id=mark_done_id)
        if task and remove:
            task.update(deleted=True)
        elif task:
            task.update(done=True)

    def get(self, request):
        user = request.user
        mark_done_id = request.GET.get('mark_done_id', None)
        remove_task_id = request.GET.get('remove_task_id', None)
        if mark_done_id:
            self.mark_done(mark_done_id)
        if remove_task_id:
            self.mark_done(remove_task_id, remove=True)

        tasks = Task.objects.filter(deleted=False)
        for task in tasks:
            if task.user == user:
                setattr(task, 'self', True)

        return render(request, self.template_name, {'page': 'home', 'tasks': tasks})


class AddTaskView(View):
    template_name = 'add_task.html'

    def get(self, request):
        id = request.GET.get('task_id', None)
        instance = Task.objects.filter(id=id)
        form = ContactForm()
        if instance:
            instance = instance[0]
            form = ContactForm(instance=instance)

        return render(request, self.template_name, {'page': 'home', 'form': form})

    def post(self, request):
        user = request.user
        id = request.POST.get('id', '')
        form = ContactForm(request.POST)
        if id and Task.objects.filter(id=id):
            form = ContactForm(request.POST, instance=Task.objects.get(id=id))
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            messages.success(request, 'Your response has been recorded')
        else:
            messages.error(request, 'Please Correct The error below')
        if 'add' in request.POST:
            return redirect('index')
        return render(request, self.template_name, {'page': 'home', 'form': form})


class LogOutView(View):
    template_name = 'login.html'

    def get(self, request):
        logout(request)
        return redirect('login')
