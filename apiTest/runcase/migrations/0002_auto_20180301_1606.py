# Generated by Django 2.0.2 on 2018-03-01 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runcase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='run_dir',
            field=models.CharField(default='null', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='upload',
            name='file_path',
            field=models.FileField(upload_to='./test_framework/upload/'),
        ),
    ]