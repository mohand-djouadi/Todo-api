from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from authentication.models import User
from authentication.Jwt import generate_token, jwt_required
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
                token = generate_token(user)
                print(f"Token CSRF généré: {token}")
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'token': token,
                    'security_quest': User.get_Security_quest_label(user.security_quest)
                }
                response = JsonResponse(user_data, status=200)
                return response
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
            security_quest = userInputs.get('security_quest', '')
            security_answ = userInputs.get('security_answ', '')
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                quest_label=security_quest,
                sec_answ=security_answ
            )
            user.full_clean()
            user.save()
            token = generate_token(user)
            print(f"Token CSRF généré: {token}")
            login(request, user)
            userData = model_to_dict(User.objects.get(username=user.username))
            userData['security_quest'] = security_quest
            userData['token'] = token
            response = JsonResponse(userData, status=200)
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'format de donnee invalid'}, status=400)
        except ValidationError as e:
            error = dict(e)
            return JsonResponse({'error': error}, status=400)
    else:
        return JsonResponse({'error': 'methode HTTP non autoriser'}, status=405)


@login_required
@csrf_exempt
@jwt_required
def change_password(request):
    if request.method == 'PUT':
        try:
            userInuputs = json.loads(request.body)
            currentPassword = userInuputs.get('current_password', '')
            newPassword = userInuputs.get('new_password', '')
            confirmPasssword = userInuputs.get('confirmation', '')
            if not request.user.check_password(currentPassword):
                return JsonResponse({'error': 'le mot de pass actuelle est incorrect'}, status=400)
            if newPassword == confirmPasssword:
                request.user.set_password(newPassword)
                return JsonResponse({'message':'mot de pass changer avec succes'}, status=201)
            else:
                return JsonResponse({'error': 'mot de pass ne pas confirmer'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error':'donnee JSON invalide'}, status=400)
    else:
        return JsonResponse({'eror':'methode HTTP non autoriser'}, status=405)

@login_required
@csrf_exempt
@jwt_required
def logOut(request):
    print("Starting logout process")
    try:
        logout(request)
        print("User logged out successfully")
        return JsonResponse({'message': 'user logged out'}, status=200)
    except Exception as e:
        print(f"Error during logout: {e}")
    return JsonResponse({'error': 'Logout failed'}, status=500)