# Generated by Django 5.1.4 on 2024-12-20 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0018_alter_companyevent_audience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='responsible_phone',
            field=models.CharField(max_length=30, verbose_name='Телефон ответственного'),
        ),
    ]
