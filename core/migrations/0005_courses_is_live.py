# Generated by Django 3.2 on 2021-04-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_agoranews_links'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='is_live',
            field=models.BooleanField(default=False),
        ),
    ]