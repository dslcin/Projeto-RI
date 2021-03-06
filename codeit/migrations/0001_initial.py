# Generated by Django 2.0.6 on 2018-06-28 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_text', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('mem_limit', models.CharField(max_length=15)),
                ('description', models.TextField()),
                ('problem_input', models.TextField()),
                ('problem_output', models.TextField()),
                ('time_limit', models.CharField(max_length=15)),
            ],
        ),
    ]
