# Generated by Django 4.2.2 on 2023-07-01 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MedicalEntry', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalentry',
            name='prescription_image',
        ),
        migrations.AddField(
            model_name='medicalentry',
            name='prescription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
