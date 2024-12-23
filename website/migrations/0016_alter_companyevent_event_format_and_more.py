# Generated by Django 5.1.4 on 2024-12-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_alter_companysurvey_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyevent',
            name='event_format',
            field=models.CharField(choices=[('online', 'Онлайн'), ('offline', 'Оффлайн')], default='offline', max_length=10, null=True, verbose_name='Формат проведения'),
        ),
        migrations.AlterField(
            model_name='companyevent',
            name='participation_type',
            field=models.CharField(choices=[('organizer', 'Организатор'), ('sooorganizer', 'Со-организатор')], default='organizer', max_length=15, null=True, verbose_name='Тип участия'),
        ),
    ]
