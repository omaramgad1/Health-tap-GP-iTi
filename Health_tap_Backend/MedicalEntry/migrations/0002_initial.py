# Generated by Django 4.2.2 on 2023-07-01 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Patient', '0001_initial'),
        ('MedicalEntry', '0001_initial'),
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalentry',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor'),
        ),
        migrations.AddField(
            model_name='medicalentry',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_history', to='Patient.patient'),
        ),
    ]
