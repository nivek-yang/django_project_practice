# Generated by Django 5.2 on 2025-04-14 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=50)),
                ('interview_date', models.DateField(null=True)),
                ('review', models.TextField()),
                ('rating', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
