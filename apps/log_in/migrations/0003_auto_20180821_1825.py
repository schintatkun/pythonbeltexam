# Generated by Django 2.1 on 2018-08-21 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_in', '0002_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='item',
            name='wishedby_users',
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
