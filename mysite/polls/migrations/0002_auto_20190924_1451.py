# Generated by Django 2.2.5 on 2019-09-24 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AddField(
            model_name='question',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
