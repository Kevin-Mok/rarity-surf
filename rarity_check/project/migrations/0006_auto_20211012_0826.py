# Generated by Django 3.2.8 on 2021-10-12 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_traitvalue_rarity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'ordering': ['-score']},
        ),
        migrations.RemoveField(
            model_name='token',
            name='rank',
        ),
    ]
