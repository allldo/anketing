from django.db import models
from django.contrib.auth.models import User

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    email_for_newsletters = models.EmailField(verbose_name="Email для рассылки новостей HR2K")
    company_name_full = models.CharField(max_length=255, verbose_name="Название компании (полное)")
    company_name_short = models.CharField(max_length=20, verbose_name="Название компании (краткое)")
    company_logo = models.ImageField(upload_to='company_logos/', verbose_name="Логотип компании")
    postal_code = models.CharField(max_length=10, verbose_name="Почтовый индекс")
    postal_address = models.CharField(max_length=255,verbose_name="Почтовый адрес")
    responsible_email = models.EmailField(verbose_name="Email ответственного")
    responsible_name = models.CharField(max_length=255, verbose_name="Имя и фамилия ответственного")
    responsible_phone = models.CharField(max_length=15, verbose_name="Телефон ответственного")
    consent_data_processing = models.BooleanField(default=False, verbose_name="Согласие на обработку данных")
    confirmation = models.BooleanField(default=False, verbose_name="Подтверждение условий")

    def __str__(self):
        return self.company_name_full
    
class GeneralInfo(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    period = models.CharField(max_length=255, verbose_name="Период")
    main_page_content = models.TextField(verbose_name="Главная страница")
    
    methodology_file = models.FileField(upload_to='general_info/', verbose_name="Методология", blank=True, null=True)
    charter_file = models.FileField(upload_to='general_info/', verbose_name="Уставные документы", blank=True, null=True)
    results_file = models.FileField(upload_to='general_info/', verbose_name="Результаты старых рейтингов", blank=True, null=True)

    def __str__(self):
        return self.title
    

class UserMessage(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя пользователя")
    email = models.EmailField(verbose_name="Email пользователя")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
    

class CompanySurvey(models.Model):
    GEOGRAPHY_CHOICES = [
        ('federal', 'Федеральный уровень'),
        ('regional', 'Региональный уровень'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys',blank=True, null=True)
    company_name = models.CharField(max_length=255, verbose_name="Фирменное наименование",blank=True,null=True)
    company_address = models.CharField(max_length=255,verbose_name="Адрес головного офиса",blank=True,null=True)
    specialization = models.CharField(max_length=255, verbose_name="Основная специализация",blank=True,null=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Совокупная выручка", null=True, blank=True)
    geography_activity = models.CharField(
        max_length=20,
        choices=GEOGRAPHY_CHOICES,
        default='federal',
        verbose_name="География активности",
        null=True,blank=True
    )
    company_age = models.PositiveIntegerField(
        verbose_name="Возраст компании (лет)",
        null=True,
        blank=True
    )
    num_expert_employees = models.PositiveIntegerField(
        verbose_name="Количество сотрудников-экспертов",
        null=True,
        blank=True
    )
    num_employees_over_3_years = models.PositiveIntegerField(
        verbose_name="Количество сотрудников, работающих более 3 лет",
        null=True,
        blank=True
    )
    num_employees_in_communications = models.PositiveIntegerField(
        verbose_name="Количество сотрудников, работающих в коммуникациях более 3 лет",
        null=True,
        blank=True
    )
    num_government_awards = models.PositiveIntegerField(
        verbose_name="Количество государственных наград",
        null=True,
        blank=True
    )
    num_certificates = models.PositiveIntegerField(
        verbose_name="Количество сертификатов",
        null=True,
        blank=True
    )
    submission_date = models.DateField(auto_now_add=True, verbose_name="Дата заполнения")
    user_comment = models.TextField(
        verbose_name="Комментарий пользователя",
        null=True,
        blank=True
    )
    moderator_comment = models.TextField(
        verbose_name="Комментарий модератора",
        null=True,
        blank=True
    )
    def __str__(self):
        return f"Анкета {self.company_name} - {self.submission_date}"
    
    
class CompanyPositioning(models.Model):
    survey = models.ForeignKey(CompanySurvey, on_delete=models.CASCADE, related_name='positionings')
    service = models.CharField(max_length=255, verbose_name="Позиционирование",null=True,blank=True)
    revenue_share = models.PositiveIntegerField(verbose_name="Распределение выручки (%)",null=True,blank=True)

class CompanyEmployees(models.Model):
    survey = models.ForeignKey(CompanySurvey, on_delete=models.CASCADE, related_name='employees')
    department = models.CharField(max_length=255, verbose_name="Название компании/отдела",null=True,blank=True)
    employee_count = models.PositiveIntegerField(verbose_name="Количество сотрудников",null=True,blank=True)

class CompanyAwards(models.Model):
    survey = models.ForeignKey(CompanySurvey, on_delete=models.CASCADE, related_name='awards')
    award_name = models.CharField(max_length=255, verbose_name="Название премии",null=True,blank=True)
    award_category = models.CharField(max_length=50, verbose_name="Категория премии",null=True,blank=True)
    award_type = models.CharField(max_length=50, verbose_name="Тип награды",null=True,blank=True)


class CompanyRevenue(models.Model):
    survey = models.ForeignKey(
        'CompanySurvey', 
        on_delete=models.CASCADE,
        related_name='revenues',
        verbose_name="Анкета"
        ,null=True,blank=True
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name="Название компании",null=True,blank=True
    )
    inn = models.CharField(
        max_length=12,
        verbose_name="ИНН компании",null=True,blank=True
    )
    ownership_share = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Доля владения (%)",null=True,blank=True
    )
    buying_share = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Доля баинга в выручке (%)",null=True,blank=True
    )
    revenue_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Доля выручки (тыс. рублей)",null=True,blank=True
    )

    def __str__(self):
        return f"{self.company_name} (ИНН: {self.inn}) - Выручка: {self.revenue_amount} тыс. руб."
    
class CompanyEvent(models.Model):
    EVENT_FORMAT_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Оффлайн'),
        # ('hybrid', 'Гибридный'),
    ]

    PARTICIPATION_TYPE_CHOICES = [
        # ('speaker', 'Спикер'),
        # ('participant', 'Участник'),
        ('organizer', 'Организатор'),
        ('sooorganizer', 'Со-организатор'),
    ]

    survey = models.ForeignKey(
        'CompanySurvey',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name="Анкета"
    )
    event_count = models.PositiveIntegerField(verbose_name="Количество мероприятий",null=True,blank=True)
    audience = models.CharField(max_length=255, verbose_name="Аудитория",null=True,blank=True)
    participant_count = models.PositiveIntegerField(verbose_name="Количество участников",null=True,blank=True)
    event_format = models.CharField(
        max_length=10,
        choices=EVENT_FORMAT_CHOICES,
        verbose_name="Формат проведения",null=True
    )
    event_type = models.CharField(max_length=255, verbose_name="Формат мероприятия",null=True,blank=True)
    participation_type = models.CharField(
        max_length=15,
        choices=PARTICIPATION_TYPE_CHOICES,
        verbose_name="Тип участия",null=True
    )

    def __str__(self):
        return f"{self.event_type} ({self.event_format}) - Участники: {self.participant_count}"
    
class SurveyStatus(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderate', 'На модерации'),
        ('return', 'На доработку'),
        ('approved', 'Принят'),
        ('rejected', 'Отклонено'),
    ]

    survey = models.ForeignKey(
        CompanySurvey,
        on_delete=models.CASCADE,
        related_name='statuses',
        verbose_name="Анкета"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Статус",
        default='draft'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата установки статуса"
    )

    def __str__(self):
        return f"{self.survey.company_name}: {self.get_status_display()} ({self.created_at}) - {self.user.username if self.user else 'Системный'}"