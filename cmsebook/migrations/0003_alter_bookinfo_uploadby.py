# Generated by Django 4.0.4 on 2023-12-22 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsebook', '0002_booksdownloadrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='uploadby',
            field=models.CharField(default='', max_length=50),
        ),
    ]
