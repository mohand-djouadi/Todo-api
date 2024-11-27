from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class CustomUserManager(BaseUserManager):


    def create_user(self, username, first_name, last_name, email, password):
        if username == '' or first_name == '' or last_name == '' or email == '' or password == '':
            raise ValueError('required fields are missing')
        if self.model.objects.filter(username=username).exists():
            raise ValueError('username already userd')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)  # Hachage automatique du mot de passe
        user.save(using=self._db)
        return user





class User(AbstractBaseUser):
    class Meta:
        db_table = 'users'
    username = models.CharField(max_length=50, blank=False, unique=True, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    objects = CustomUserManager()


