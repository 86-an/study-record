from django.db import models

# Create your models here.
class Studyrecord(models.Model):
    date = models.DateField(verbose_name='日付')
    study_time = models.FloatField(verbose_name='勉強時間') 