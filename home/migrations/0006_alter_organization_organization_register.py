# Generated by Django 5.1.5 on 2025-03-10 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_organizationregister_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_register',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='home.organizationregister'),
        ),
    ]
