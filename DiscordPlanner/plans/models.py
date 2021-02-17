from django.db import models
from baseApp.models import User


class Plan(models.Model):
    guild = models.IntegerField(verbose_name='길드ID')
    name = models.CharField(max_length=64, verbose_name='이름')
    dttm = models.DateTimeField(verbose_name='시각')
    max_attendee = models.IntegerField(verbose_name='최대인원', null=True)
    attendee = models.ManyToManyField(User, related_name='참가자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'PlanTable'
        verbose_name = 'plan'
        verbose_name_plural = 'plans'
