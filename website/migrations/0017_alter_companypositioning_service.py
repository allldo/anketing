# Generated by Django 5.1.4 on 2024-12-20 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_companyevent_event_format_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companypositioning',
            name='service',
            field=models.CharField(blank=True, choices=[('full cycle', 'Агентство полного цикла'), ('service', 'Маркетинговые коммуникации / Маркетинговые услуги'), ('explore', 'Коммуникационные исследования и аналитика / Исследования и аналитика'), ('commune', 'Корпоративные и общественные коммуникации, связи с общественностью и органами публичной власти / Связи с общественностью'), ('consult', 'Политические коммуникации / Политическое консультирование'), ('ads', 'Рекламные коммуникации / Реклама'), ('event', 'Событийные коммуникации / Мероприятия / Event'), ('digital', 'Цифровые коммуникации / Digital')], default='full cycle', max_length=255, null=True, verbose_name='Позиционирование'),
        ),
    ]
