
import datetime
from random import randint

from django.shortcuts import render

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from django.utils.timezone import localtime

from django.conf import settings
from django.contrib.auth import authenticate,login,logout

from django.utils.timezone import localtime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from authentication.models import User
from authentication.Jwt import generate_token, jwt_required
import json
from random import randint
import datetime
from django.utils import timezone

#swagger render view
@csrf_exempt
def swagger_ui(request):
    return render(request, "swagger.html")

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
            existUser = User.objects.filter(Q(email=email) | Q(username=username))
            if len(existUser) == 0:
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
            else:
                return JsonResponse({'error': 'username or email already used'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid data format'}, status=400)
        except ValidationError as e:
            error = dict(e)
            return JsonResponse({'error': error}, status=400)
    else:
        return JsonResponse({'error': 'HTTP method not allowed'}, status=405)


def get_OTP(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            return JsonResponse({'error':'email parameter is required'}, status=400)
        else:
            try:
                otp = ''.join([str(randint(0, 9)) for i in range(6)])
                user = User.objects.get(email=email)
                user.otp = otp
                user.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
                user.save()
                subject = 'Votre code de vérification OTP'
                plain_message = 'Votre code de vérification est : ' + otp
                html_message = render_to_string('email.html', {'user': user, 'otp': otp})
                send_mail(
                    subject, # Message en texte brut
                    plain_message,
                    settings.EMAIL_HOST_USER,  # L'adresse email de l'expéditeur
                    [email],  # L'adresse email du destinataire
                    html_message=html_message,  # Message HTML
                )
                return JsonResponse({'message': 'OTP sent successfully'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error':'email not exist'}, error=404)
    else:
        return JsonResponse({'error':'HTTP method not allowed'}, status=405)


def validate_otp(request):
    if request.method == 'POST':
        try:
            email = request.GET.get('email')
            otp = json.loads(request.body).get('otp', '')
            if otp != '' or email:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'User not found'}, status=404)
                print('user', user.username)
                print("now", localtime(timezone.now()))
                print("otp expiry",  localtime(user.otp_expiry))
                print("is otp not expired ",localtime(timezone.now()) < localtime(user.otp_expiry))
                if localtime(timezone.now()) < localtime(user.otp_expiry):
                    if user.otp == otp:
                        user.otp = None
                        user.otp_expiry = None
                        print('before save')
                        user.save()
                        print('after save')
                        return JsonResponse({'message':'otp verified succesfully'}, status=200)
                    else:
                        return JsonResponse({'error':'otp is not valide'}, status=400)
                else:
                    return JsonResponse({'error':'otp is expired'}, status=400)
            else:
                return JsonResponse({'error':'otp and email is required'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid data format'}, status=400)
        except ValidationError as e:
            error = dict(e)
            return JsonResponse({'error': error}, status=400)
    else:
        return JsonResponse({'error','HTTP method not allowed'}, status=405)

def validate_answer(request):
    if request.method == 'POST':
        try:
            email = request.GET.get('email')
            answer = json.loads(request.body).get('answer', '')
            if answer != '' and email:
                try:
                    user = User.objects.get(email=email)
                    if answer == user.security_answ:
                        return JsonResponse({'message':'answer validated successfully'}, status=200)
                    else:
                        return JsonResponse({'error': 'wrong answer'}, status=400)
                except User.DoesNotExist:
                    return JsonResponse({'error':'email not exist'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid data format'}, status=400)
        except ValidationError as e:
            error = dict(e)
            return JsonResponse({'error': error}, status=400)

    else:
        return JsonResponse({'error','HTTP method not allowed'}, status=405)

@login_required
@csrf_exempt
@jwt_required
def reset_password(request):
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
                request.user.save()
                return JsonResponse({'message': 'mot de pass changer avec succes'}, status=201)
            else:
                return JsonResponse({'error': 'mot de pass ne pas confirmer'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'donnee JSON invalide'}, status=400)
    else:
        return JsonResponse({'error': 'methode HTTP non autoriser'}, status=405)

@csrf_exempt
def forgot_password(request):
    if request.method == 'PUT':
        try:
            email = request.GET.get('email')
            user = User.objects.get(email=email)
            userInputs = json.loads(request.body)
            newPassword = userInputs.get('new_password', '')
            confirm = userInputs.get('confirmation', '')
            if email:
                if newPassword == confirm:
                    user.set_password(newPassword)
                    user.save()
                    return JsonResponse({'message': 'password changed successfully'}, status=201)
                else:
                    return JsonResponse({'error': 'password not confirmed'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error':'email not exist'}, status=404)
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


