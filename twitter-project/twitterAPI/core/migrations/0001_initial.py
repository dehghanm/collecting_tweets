# Generated by Django 3.2.12 on 2022-06-21 13:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('orientation', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
    ]
