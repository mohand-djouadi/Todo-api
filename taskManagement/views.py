from django.forms import model_to_dict

from taskManagement.models import Task
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from taskManagement.models import Comment
from authentication.Jwt import jwt_required
import json
from datetime import date

@login_required
@csrf_exempt
@jwt_required
def get_tasks(request):
    if request.method == 'GET':
        try:
            tasks = Task.objects.filter(user=request.user)
            tasks_data = [{'id': task.id, 'title': task.title, 'location':task.location, 'description': task.description, 'status': task.status}
                          for task in tasks]
            return JsonResponse({'tasks':tasks_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error':'format JSON inccorect'}, status=400)
    else:
        return JsonResponse({'error':'methode HTTP non autoriser'}, status=405)

@login_required
@csrf_exempt
@jwt_required
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
            task_dict = model_to_dict(task)
            return JsonResponse(task_dict, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Format de données JSON incorrect'},status=400)
    else:
        return JsonResponse({'error':'methode HTTP non autorise'},status=405)

@login_required
@csrf_exempt
@jwt_required
def edit_task(request,id):
    if request.method == 'PUT':
        try:
            taskToEdit = json.loads(request.body)
            currentTask = Task.objects.get(id=id)
            currentTask.update_fields(**taskToEdit)
            currentTask.save()
            updatedTask = model_to_dict(currentTask)
            return JsonResponse(updatedTask, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error':'donne JSON invalide'}, status=400)
    else:
        return JsonResponse({'error':'methode HTTP non authorise'}, status=405)

@login_required
@csrf_exempt
@jwt_required
def delete_task(request,id):
    if request.method == 'DELETE':
        try:
            taskToDelete = get_object_or_404(Task, id=id)
            taskToDelete.delete()
            return JsonResponse({'message':'task deleted succesfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error':'donner JSON non valide'}, status=400)
    else:
        return JsonResponse({'error':'methodle HTTP non autorizer'}, status=405)

@login_required
@csrf_exempt
@jwt_required
def get_comments(request, id):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(task=id)
            comment_data = [ { 'id':comment.id, 'content':comment.content, 'createdAt':comment.createdAt } for comment in comments ]
            return JsonResponse({'comments':comment_data}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error':'donner JSON non valide'}, status=400)
    else:
        return JsonResponse({'error':'methodle HTTP non autorizer'}, status=405)


@login_required
@csrf_exempt
@jwt_required
def addCommentToTask(request, id):
    createdAt = date.today()
    if request.method == 'POST':
        try:
            commentData = json.loads(request.body)
            task = get_object_or_404(Task, id=id)
            comment = Comment.objects.create(
                content=commentData.get("content", ""),
                createdAt=createdAt,
                task=task
            )
            comment.save()
            comment_dict = model_to_dict(comment)
            return JsonResponse(comment_dict, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'message':'error donnee json no valide'}, status=400)
    else:
        return JsonResponse({'message':'error method not allowed'}, status=405)

