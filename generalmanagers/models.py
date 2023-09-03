from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class GeneralManager(models.Model):
    name=models.OneToOneField(User,on_delete=models.CASCADE)


    def __str__(self):

        return self.name.username