# Generated by Django 2.1.1 on 2018-09-10 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmaster_api', '0005_auto_20180910_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='searchable_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='sitemap_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
