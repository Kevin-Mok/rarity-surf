# Generated by Django 3.2.8 on 2021-10-13 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20211013_0706'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='token',
            name='unique_token',
        ),
        migrations.AddConstraint(
            model_name='token',
            constraint=models.UniqueConstraint(fields=('project', 'token_type', 'number'), name='unique_token'),
        ),
    ]
