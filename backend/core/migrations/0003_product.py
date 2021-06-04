# Generated by Django 3.2.4 on 2021-06-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=254)),
                ('image', models.CharField(max_length=254)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]