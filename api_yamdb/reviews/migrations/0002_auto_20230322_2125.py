# Generated by Django 3.2 on 2023-03-22 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Описание произведения'),
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.genre')),
                ('title_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.title')),
            ],
        ),
    ]
