# Generated by Django 4.2 on 2024-03-06 14:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('WSSGTemplate', '0015_servercommand'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerMessage',
            fields=[
                ('genericID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(default='test', max_length=1000)),
                ('message', models.JSONField(default=list)),
                ('identifier', models.CharField(default='test', max_length=1000)),
            ],
        ),
        migrations.DeleteModel(
            name='ServerCommand',
        ),
    ]