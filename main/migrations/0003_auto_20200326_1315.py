# Generated by Django 3.0.4 on 2020-03-26 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_group_is_full'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='main.Group'),
        ),
    ]
