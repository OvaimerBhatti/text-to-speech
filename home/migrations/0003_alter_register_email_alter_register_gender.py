# Generated by Django 4.0.4 on 2022-04-23 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_register_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='gender',
            field=models.BinaryField(max_length=1),
        ),
    ]
