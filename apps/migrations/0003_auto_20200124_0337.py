# Generated by Django 3.0.2 on 2020-01-23 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepicture',
            name='img',
            field=models.ImageField(default='profilepic/default.jpg', upload_to='profilepic/'),
        ),
    ]