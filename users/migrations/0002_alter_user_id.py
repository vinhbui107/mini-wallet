# Generated by Django 3.2.5 on 2021-07-28 07:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c6f959ef-c156-45f5-881b-1841063ee9b4'), editable=False, primary_key=True, serialize=False),
        ),
    ]