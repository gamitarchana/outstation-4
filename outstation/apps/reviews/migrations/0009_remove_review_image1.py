# Generated by Django 2.1.8 on 2019-09-30 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outstationreview', '0008_review_image1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='image1',
        ),
    ]
