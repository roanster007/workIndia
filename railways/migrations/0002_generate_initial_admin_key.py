# Generated by Django 5.0.10 on 2025-02-17 17:02

from django.db import migrations
from railways.lib.admin import generate_new_key

def generate_initial_api_key(apps, schema_editor):
    generate_new_key(initial=True)


class Migration(migrations.Migration):

    dependencies = [
        ("railways", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(generate_initial_api_key),
    ]
