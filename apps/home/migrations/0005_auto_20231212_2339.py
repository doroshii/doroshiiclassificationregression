# Generated by Django 3.2.16 on 2023-12-12 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20231212_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productdata',
            old_name='predicted_sale',
            new_name='predicted_price',
        ),
        migrations.RemoveField(
            model_name='productdata',
            name='week_number',
        ),
        migrations.AddField(
            model_name='productdata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
