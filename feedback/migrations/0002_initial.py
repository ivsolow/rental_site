# Generated by Django 4.2 on 2023-05-17 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feedback', '0001_initial'),
        ('rentals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rental',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rentals.rentals'),
        ),
    ]