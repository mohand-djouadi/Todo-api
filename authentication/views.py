from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.middleware.csrf import get_token
from authentication.models import User
import json


@csrf_exempt
def logIn(request):
    if request.method == 'POST':
        try:
            userInputs = json.loads(request.body)
            username = userInputs.get('username', '')
            password = userInputs.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                token = get_token(request)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'token': token
                }
                return JsonResponse(user_data, status=200)
            else:
                return JsonResponse({'error': 'Nom d\'utilisateur ou mot de passe incorrect'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format de données JSON incorrect'}, status=400)
    else:
        return JsonResponse({'error': 'Méthode HTTP non autorisée'}, status=405)

@csrf_exempt
def signUp(request):
    if request.method == 'POST':
        try:
            userInputs = json.loads(request.body)
            username = userInputs.get('username','')
            first_name = userInputs.get('first_name', '')
            last_name = userInputs.get('last_name', '')
            email = userInputs.get('email', '')
            password = userInputs.get('password', '')
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.full_clean()
            user.save()

            userData = model_to_dict(User.objects.get(username=user.username))
            return JsonResponse(userData, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'format de donnee invalid'}, status=400)
        except ValidationError as e:
            error = dict(e)
            return JsonResponse({'error': error}, status=400)
    else:
        return JsonResponse({'error': 'methode HTTP non autoriser'}, status=405)