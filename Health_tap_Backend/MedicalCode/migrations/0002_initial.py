# Generated by Django 4.2.2 on 2023-06-30 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MedicalCode', '0001_initial'),
        ('Patient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicaleditcode',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_edit_codes', to='Patient.patient'),
        ),
    ]