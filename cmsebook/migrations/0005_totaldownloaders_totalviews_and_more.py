# Generated by Django 4.0.6 on 2023-12-27 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsebook', '0004_bookinfo_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='totaldownloaders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('downloade_by', models.CharField(default='', max_length=50)),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsebook.bookinfo')),
            ],
        ),
        migrations.CreateModel(
            name='totalviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewd_by', models.CharField(default='', max_length=50)),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsebook.bookinfo')),
            ],
        ),
        migrations.DeleteModel(
            name='booksdownloadrecord',
        ),
    ]