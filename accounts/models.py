from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Topic(models.Model):
    topic_name=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.topic_name

class CustomUser(AbstractUser):
    job_title=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=20)
    age=models.IntegerField()
    SEX_FEMALE = 'F'
    SEX_MALE = 'M'

    SEX_OPTIONS = (
        (SEX_FEMALE, 'Female'),
        (SEX_MALE, 'Male'),
        
    )
    gender = models.CharField(max_length=1, choices=SEX_OPTIONS)

    topics=models.ManyToManyField(Topic)
  

