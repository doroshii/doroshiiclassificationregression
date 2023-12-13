# Generated by Django 3.2.16 on 2023-12-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_regressiondata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('radio', models.FloatField()),
                ('in_store_spending', models.FloatField()),
                ('discount', models.FloatField()),
                ('tv_spending', models.FloatField()),
                ('stock_rate', models.FloatField()),
                ('online_ads_spending', models.FloatField()),
                ('predicted_sale', models.FloatField(blank=True, null=True)),
                ('week_number', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='RegressionData',
        ),
    ]