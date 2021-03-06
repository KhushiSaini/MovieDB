# Generated by Django 2.2.2 on 2021-07-29 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TMDB', '0004_remove_collection_fav_genres'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='mdescription',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='mgenres',
            field=models.CharField(max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='mtitle',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='muuid',
            field=models.IntegerField(null=True),
        ),
    ]
