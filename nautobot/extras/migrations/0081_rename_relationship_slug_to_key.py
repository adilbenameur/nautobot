# Generated by Django 3.2.18 on 2023-05-09 16:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("extras", "0080_tagsfield"),
    ]

    operations = [
        migrations.RenameField(
            model_name="relationship",
            old_name="slug",
            new_name="key",
        ),
    ]