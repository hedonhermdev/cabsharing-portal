# Generated by Django 3.0.4 on 2020-03-26 12:10

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
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_location', models.CharField(choices=[('PIL', 'PILANI'), ('LOH', 'LOHARU'), ('DEL', 'DELHI'), ('JAI', 'JAIPUR')], max_length=3)),
                ('from_location', models.CharField(choices=[('PIL', 'PILANI'), ('LOH', 'LOHARU'), ('DEL', 'DELHI'), ('JAI', 'JAIPUR')], max_length=3)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_location', models.CharField(choices=[('PIL', 'PILANI'), ('LOH', 'LOHARU'), ('DEL', 'DELHI'), ('JAI', 'JAIPUR')], max_length=3)),
                ('from_location', models.CharField(choices=[('PIL', 'PILANI'), ('LOH', 'LOHARU'), ('DEL', 'DELHI'), ('JAI', 'JAIPUR')], max_length=3)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='main.Group')),
                ('lister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]