# Generated by Django 3.1.3 on 2021-01-31 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(max_length=64)),
                ('item_name', models.CharField(max_length=64)),
                ('item_size', models.CharField(choices=[('S', 'small'), ('L', 'large')], default=None, max_length=10, null=True)),
                ('price', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User_order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_ordered', models.CharField(max_length=64)),
                ('status', models.BooleanField(default=False)),
                ('price', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item_cost', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza.user_order')),
            ],
        ),
    ]