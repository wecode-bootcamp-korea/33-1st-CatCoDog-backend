# Generated by Django 4.0.4 on 2022-05-25 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='pet_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.pettype'),
        ),
    ]