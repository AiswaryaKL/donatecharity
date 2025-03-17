# Generated by Django 5.1 on 2025-03-16 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_delete_charityreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharityReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_donations', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('num_donors', models.IntegerField(default=0)),
                ('num_campaigns', models.IntegerField(default=0)),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charity_reports', to='home.organization')),
            ],
            options={
                'unique_together': {('organization', 'month', 'year')},
            },
        ),
    ]
