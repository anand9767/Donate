# Generated by Django 3.2.9 on 2022-01-20 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_productdetail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
