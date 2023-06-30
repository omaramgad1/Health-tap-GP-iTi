# Generated by Django 4.2.2 on 2023-06-30 21:03

import MedicalEntry.models
import cloudinary.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Patient', '0001_initial'),
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('prescription_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[MedicalEntry.models.validateImage])),
                ('analysis_image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, validators=[MedicalEntry.models.validateImage])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_history', to='Patient.patient')),
            ],
        ),
    ]
