from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class CustomUserManager(BaseUserManager):


    def create_user(self, username, first_name, last_name, email, password, quest_label, sec_answ):
        if username == '' or first_name == '' or last_name == '' or email == '' or password == '':
            raise ValueError('required fields are missing')
        if self.model.objects.filter(username=username).exists():
            raise ValueError('username already userd')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            security_answ=sec_answ,
            security_quest = User.get_security_quest_value(quest_label)
        )
        user.set_password(password)  # Hachage automatique du mot de passe
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    FIRST_QUEST = 'QUESTION_1'
    SECOND_QUEST = 'QUESTION_2'
    THIRD_QUEST = 'QUESTION_3'
    FOURTH_QUEST = 'QUESTION_4'
    FIFTH_QUEST = 'QUESTION_5'

    CHOICES_QUEST = (
        (FIRST_QUEST, 'what is your favorite movie'),
        (SECOND_QUEST, 'what is your first animal companion'),
        (THIRD_QUEST, 'what is your mother\'s name'),
        (FOURTH_QUEST, 'what is your childhood nickname'),
        (FIFTH_QUEST, 'what is the name of your best teacher')
    )

    username = models.CharField(max_length=50, blank=False, unique=True, null=False)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    security_quest = models.CharField(max_length=50, choices=CHOICES_QUEST, blank=False, null=False)
    security_answ = models.CharField(max_length=50, blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    objects = CustomUserManager()

    @classmethod
    def get_security_quest_value(cls, label):
        quest_dict = dict(cls.CHOICES_QUEST)
        for key, value in quest_dict.items():
            if value == label:
                return key

    @classmethod
    def get_Security_quest_label(cls, quest):
        quest_dict = dict(cls.CHOICES_QUEST)
        for key, value in quest_dict.items():
            if key == quest:
                return value