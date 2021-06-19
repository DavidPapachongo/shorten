# Generated by Django 3.2.2 on 2021-05-27 02:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shortURL', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortURL.urlmodel')),
            ],
        ),
    ]
