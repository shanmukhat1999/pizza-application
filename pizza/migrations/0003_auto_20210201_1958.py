# Generated by Django 3.1.3 on 2021-02-01 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0002_auto_20210201_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_size',
            field=models.CharField(choices=[('Small', 'S'), ('Large', 'L'), ('None', 'N')], default=None, max_length=10, null=True),
        ),
    ]
