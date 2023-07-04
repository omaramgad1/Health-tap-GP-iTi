# Generated by Django 4.2.2 on 2023-07-04 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0002_initial'),
        ('Reservation', '0003_alter_reservation_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='appointment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_data', to='Appointment.appointment'),
        ),
    ]
