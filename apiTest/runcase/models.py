from django.db import models


# Create your models here.
class Upload(models.Model):
    run_dir = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='./test_framework/upload/')
