# Generated by Django 3.2.9 on 2022-02-19 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_productdetail_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetail',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]