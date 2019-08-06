# Generated by Django 2.0.2 on 2018-04-03 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summoner_name', models.CharField(max_length=16)),
                ('region', models.CharField(choices=[('eun1', 'EUNE'), ('euw1', 'EUW'), ('na1', 'NA')], max_length=4)),
                ('accountID', models.IntegerField(default=0)),
                ('summonerID', models.IntegerField(default=0)),
                ('gamesPlayed', models.TextField()),
                ('championsPlayed', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'Posts',
            },
        ),
    ]
