# Generated by Django 5.1.4 on 2024-12-20 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_alter_companypositioning_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyevent',
            name='audience',
            field=models.CharField(blank=True, choices=[('students', 'Студенты'), ('prof', 'Проф. Сообщества')], default='students', max_length=255, null=True, verbose_name='Аудитория'),
        ),
        migrations.AlterField(
            model_name='companyevent',
            name='event_type',
            field=models.CharField(blank=True, choices=[('solo', 'Единичное'), ('complex', 'Комплексная программа')], default='solo', max_length=255, null=True, verbose_name='Формат мероприятия'),
        ),
    ]
