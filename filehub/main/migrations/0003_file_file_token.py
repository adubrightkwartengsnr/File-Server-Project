# Generated by Django 4.2.1 on 2023-06-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_token',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]