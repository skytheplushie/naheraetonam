# Generated by Django 5.1.4 on 2024-12-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_one', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('content', models.TextField()),
                ('date', models.IntegerField()),
            ],
        ),
    ]