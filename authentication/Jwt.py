from functools import wraps

import jwt
from django.contrib.auth.models import User
from decouple import config
import datetime

from django.http import JsonResponse

SECRET_KEY = config('SECRET_KEY')

def generate_token(user: User, expiry_hours=24):
    payloads = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiry_hours),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payloads, SECRET_KEY, algorithm='HS256')
    return token

def jwt_required(f):
    @wraps(f)
    def verify_token(request, *args, **kwargs):
        print("jwt_required: Verifying token")
        token = request.META.get('HTTP_AUTHORIZATION')
        token = token[7:]
        print("jwt token : " + token)
        if not token:
            print("jwt_required: Token missing")
            return JsonResponse({'error': 'JWT token is missing'}, status=401)
        try:
            payloads = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            print("jwt_required: Token decoded successfully")
        except jwt.ExpiredSignatureError:
            print("jwt_required: Token expired")
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            print("jwt_required: Invalid token")
            return JsonResponse({'error': 'Invalid token'}, status=401)
        if payloads['id'] != request.user.id:
            print("token is not yours")
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return f(request, *args, **kwargs)
    return verify_token