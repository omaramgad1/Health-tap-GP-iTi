# Generated by Django 4.2.2 on 2023-07-03 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0002_initial'),
        ('Reservation', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_data', to='Appointment.appointment'),
        ),
    ]
