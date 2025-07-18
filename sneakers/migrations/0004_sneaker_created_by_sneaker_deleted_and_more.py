# Generated by Django 5.2.4 on 2025-07-16 10:59

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0003_brand_country_brand_year_founded'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='sneaker',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sneakers_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sneaker',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sneaker',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sneaker',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sneakers_deleted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sneaker',
            name='last_updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sneakers_last_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='brand',
            name='year_founded',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)]),
        ),
        migrations.AlterField(
            model_name='sneaker',
            name='year_released',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2025)]),
        ),
    ]
