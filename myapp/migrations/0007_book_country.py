# Generated by Django 3.2.9 on 2021-12-03 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='country',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='myapp.country'),
        ),
    ]
