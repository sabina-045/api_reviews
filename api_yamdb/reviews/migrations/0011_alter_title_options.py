# Generated by Django 3.2 on 2023-03-30 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20230330_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
    ]
