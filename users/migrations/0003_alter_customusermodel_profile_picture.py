# Generated by Django 4.0 on 2022-04-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customusermodel_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='profile_picture',
            field=models.ImageField(default='default_user.jpg', upload_to=''),
        ),
    ]
