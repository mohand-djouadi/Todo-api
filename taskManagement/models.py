from django.db import models
from django.conf import settings

class Task(models.Model):
    class Meta:
        db_table = 'tasks'
    NOT_STARTED = 'NOT_STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    ON_HOLD = 'ON_HOLD'
    CANCELED = 'CANCELED'

    CHOICES_STATUS = (
        (NOT_STARTED, 'Not started'),
        (IN_PROGRESS, 'In progress'),
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (ON_HOLD, 'On hold'),
        (CANCELED, 'Canceled')
    )

    title = models.CharField(max_length=80, blank=False, null=False)
    location = models.CharField(max_length=80, blank=True, null=True)
    taskDate = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=80, choices=CHOICES_STATUS, default=NOT_STARTED, null=False)
    description = models.CharField(max_length=5000, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    @classmethod
    def get_status_value(cls, label):
        """
        Cette méthode de classe permet de récupérer la valeur du statut correspondant à un label donné.
        Elle recherche dans le dictionnaire des statuts (`CHOICES_STATUS`) et renvoie la clé associée au label.

        :param label: Le label du statut (ex. "Not started", "In progress").
        :return: La valeur associée au label du statut (ex. 'NOT_STARTED', 'IN_PROGRESS').
        """
        status_dict = dict(cls.CHOICES_STATUS)
        for key, value in status_dict.items():
            if value == label:
                return key

    def update_fields(self, **kwargs):
        """
        Cette méthode permet de mettre à jour les champs de la tâche avec les données fournies dans `kwargs`.
        Elle vérifie que les champs modifiés sont valides et met à jour les attributs correspondants de l'instance de tâche.
        Si le champ `status` est modifié, la méthode convertit le label en valeur.

        :param kwargs: Un ensemble de paires clé-valeur représentant les champs à mettre à jour. Les clés doivent être parmi
        'title', 'location', 'taskDate', 'status', 'description'.
        """
        for field, value in kwargs.items():
            if field in ['title', 'location', 'taskDate', 'status', 'description']:
                setattr(self, field, value)
        if 'status' in kwargs:
            self.status = self.get_status_value(self.status)
        self.save()

class Comment(models.Model):
    class Meta:
        db_table = 'comments'
    content = models.CharField(max_length=1200, blank=False, null=False)
    createdAt = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)