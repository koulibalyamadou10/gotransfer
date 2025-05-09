# Generated by Django 5.2 on 2025-04-19 18:40

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('debit', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('details', models.CharField(max_length=191)),
                ('currency', models.CharField(max_length=191)),
                ('statement_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
