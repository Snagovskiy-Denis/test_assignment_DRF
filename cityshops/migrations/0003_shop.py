# Generated by Django 3.2.9 on 2021-11-10 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cityshops', '0002_street'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('house_numbers', models.CharField(max_length=16)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cityshops.city')),
                ('street', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cityshops.street')),
            ],
        ),
    ]
