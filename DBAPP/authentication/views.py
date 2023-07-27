
# authentication/views.py
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import CityForm
from .models import City
from django.core.paginator import Paginator
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse

def index_view(request):
    tasks_list = Task.objects.exclude(deleted=True).order_by("id")
    user_filter = None

    if request.method == "POST":
        filter_type = request.POST.get("filter")
        user_filter = request.POST.get("user", None)

        if filter_type == "completed":
            tasks_list = tasks_list.filter(completed=True)
        elif filter_type == "not_completed":
            tasks_list = tasks_list.filter(completed=False)
        elif filter_type == "deleted":
            tasks_list = Task.objects.filter(deleted=True).order_by("id")
        if user_filter:
            tasks_list = tasks_list.filter(user_id=user_filter)

    return render(
        request,
        "authentication/index.html",
        {
            "tasks": tasks_list,
            "users": User.objects.all(),
            "user_filter": int(user_filter) if user_filter else None,
        },
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Проверяем введенные логин и пароль на соответствие существующему пользователю
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Если пользователь найден, выполняем вход
            login(request, user)
            return redirect('/')  # Замените 'profile' на URL вашей страницы профиля пользователя
        else:
            # Если пользователь не найден, выводим сообщение об ошибке
            error_message = "Неправильный логин или пароль."
            return render(request, 'authentication/login.html', {'error_message': error_message})

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')  # Replace 'login' with the URL name of your login page


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Создаем нового пользователя
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Вместо простого перенаправления на страницу профиля,
        # можно добавить дополнительные действия, например, отправку
        # email с подтверждением регистрации или автоматический вход
        # пользователя после успешной регистрации.

        return redirect('/')  # Замените 'profile' на URL вашей страницы профиля пользователя

    return render(request, 'authentication/register.html')


def add_city(request):
    if not request.user.is_authenticated:
        # Если пользователь не авторизован, перенаправляем на страницу входа
        return redirect('login')

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            # Проверяем уникальность города в базе данных
            name = form.cleaned_data['name']
            if City.objects.filter(name=name).exists():
                # Если город уже существует, выводим ошибку
                error_message = "Город с таким названием уже существует."
                return render(request, 'authentication/add_city.html', {'form': form, 'error_message': error_message})
            
            # Сохраняем новый город в базе данных
            form.save()
            success_message = "Город успешно добавлен!"  # Сообщение об успешном добавлении города
            return render(request, 'authentication/add_city.html', {'form': form, 'success_message': success_message})
    else:
        form = CityForm()

    return render(request, 'authentication/add_city.html', {'form': form})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'authentication/task_added.html')
    else:
        form = TaskForm()

    return render(request, 'authentication/add_task.html', {'form': form})


def complete_selected_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        # Обновляем выполнение задач
        for task_id in task_ids:
            try:
                task = Task.objects.get(pk=task_id)
                task.completed = True
                task.save()
            except Task.DoesNotExist:
                pass  # Обработка ошибки, если задача не найдена

        return JsonResponse({'message': 'Задачи успешно выполнены'}, status=200)

    return JsonResponse({'message': 'Неверный запрос'}, status=400)


def delete_selected_tasks(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_ids = data.get('task_ids', [])

        # Обновляем выполнение задач
        for task_id in task_ids:
            try:
                task = Task.objects.get(pk=task_id)
                task.deleted = True
                task.save()
            except Task.DoesNotExist:
                pass  # Обработка ошибки, если задача не найдена

        return JsonResponse({'message': 'Задачи успешно выполнены'}, status=200)

    return JsonResponse({'message': 'Неверный запрос'}, status=400)