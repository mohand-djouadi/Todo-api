from taskManagement.models import Task
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import json

@login_required
@csrf_protect
def get_tasks(request):
    if request.method == 'GET':
        try:
            tasks = Task.objects.filter(user=request.user)
            tasks_data = [{'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done}
                          for task in tasks]
            return JsonResponse({'tasks':tasks_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error':'format JSON inccorect'}, status=400)
    else:
        return JsonResponse({'error':'methode HTTP non autoriser'}, status=405)

@login_required
@csrf_protect
def add_task(request):
    if request.method == 'POST':
        try:
            taskData = json.loads(request.body)
            task = Task.objects.create(
                title= taskData.get('title', ''),
                taskDate= taskData.get('taskDate', ''),
                location= taskData.get('location', ''),
                description= taskData.get('description', ''),
                user= request.user
            )
            task.save()
            return JsonResponse({'message':'task add succesfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Format de données JSON incorrect'},status=400)
    else:
        return JsonResponse({'error':'methode HTTP non autorise'},status=405)