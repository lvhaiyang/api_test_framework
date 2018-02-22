from django.db import models


# Create your models here.
class Upload(models.Model):
    file_path = models.FileField(upload_to='./test_framework/upload/')
