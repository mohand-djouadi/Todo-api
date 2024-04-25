from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from authentication.models import User
import json

def logIn(request):
    userInputs = json.loads(request.body)
    username = userInputs.get('username', '')
    password = userInputs.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request,user)
        userData = User.objects.get(username=user.username)
        return JsonResponse(userData, status=200)

def signUp(request):
    userInputs = json.loads(request.body)
    userData = userInputs.save()
    return JsonResponse(userData)
