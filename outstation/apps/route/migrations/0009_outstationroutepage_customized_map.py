# Generated by Django 2.1.8 on 2019-08-28 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outstationroute', '0008_auto_20190712_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='outstationroutepage',
            name='customized_map',
            field=models.ImageField(null=True, upload_to='customized_map'),
        ),
    ]