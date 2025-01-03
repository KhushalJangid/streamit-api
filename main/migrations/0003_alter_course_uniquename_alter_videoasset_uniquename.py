# Generated by Django 5.0.6 on 2024-05-10 14:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_course_uniquename_alter_videoasset_uniquename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='uniqueName',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='uniqueName',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
