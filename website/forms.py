from django import forms
from django.contrib.auth.models import User
from .models import (CompanyProfile, GeneralInfo, UserMessage, CompanySurvey,
                    CompanyEmployees, CompanyAwards, CompanyPositioning,
                    CompanyEvent, CompanyRevenue
                    )
from django.contrib.auth.password_validation import validate_password


only_digit= "return event.charCode >= 48 && event.charCode <= 57" 
only_procent="this.value = this.value.replace(/\D/g, ''); if (this.value > 100) this.value = 100; else if (this.value < 0) this.value = 0;"

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = [
            'email_for_newsletters',
            'company_name_full',
            'company_name_short',
            'company_logo',
            'postal_code',
            'postal_address',
            'responsible_email',
            'responsible_name',
            'responsible_phone',
            'consent_data_processing',
            'confirmation',
        ]
        widgets = {
            'consent_data_processing': forms.CheckboxInput(),
            'confirmation': forms.CheckboxInput(),
        }

class GeneralInfoForm(forms.ModelForm):
    class Meta:
        model = GeneralInfo
        fields = [
            'title',
            'period',
            'main_page_content',
            'methodology_file',
            'charter_file',
            'results_file',
        ]
        widgets = {
            'main_page_content': forms.Textarea(attrs={'rows': 5}),
        }

class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = [ 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 10}),
        }
        labels = {
            'message': 'Задать вопрос',
        }

class CompanySurveyForm(forms.ModelForm):
    class Meta:
        model = CompanySurvey
        fields = [
            'company_name', 'company_address', 'specialization', 'revenue', 
            'geography_activity', 'company_age', 'num_expert_employees', 
            'num_employees_over_3_years', 'num_employees_in_communications', 
            'num_government_awards', 'num_certificates','user_comment'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название компании'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите адрес компании'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите специализацию'}),
            'revenue': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите совокупную выручку','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'geography_activity': forms.Select(attrs={'class': 'form-control'}),
            'company_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите возраст компании','min' :0,  'step' : 1, 'onkeypress' : only_digit,}),
            'num_expert_employees': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество сотрудников-экспертов','min' :0,  'step' : 1, 'onkeypress' : only_digit,}),
            'num_employees_over_3_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сотрудники более 3 лет','min' :0,  'step' : 1, 'onkeypress' : only_digit,}),
            'num_employees_in_communications': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сотрудники в коммуникациях > 3 лет','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'num_government_awards': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Государственные награды','min' :0,  'step' : 1, 'onkeypress' : only_digit,}),
            'num_certificates': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество сертификатов','min' :0, 'step' : 1, 'onkeypress' : only_digit}),
            'company_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите возраст компании (лет)','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'user_comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Комментарий'}),

        }
    
class CompanyPositioningForm(forms.ModelForm):
    class Meta:
        model = CompanyPositioning
        fields = ['service', 'revenue_share']
        widgets = {
            'service': forms.Select(choices=[('students', 'Агентство полного цикла'),
                                             ('service', 'Маркетинговые коммуникации / Маркетинговые услуги'),
                                             ('explore', 'Коммуникационные исследования и аналитика / Исследования и аналитика'),
                                             ('commune', 'Корпоративные и общественные коммуникации, связи с общественностью и органами публичной власти / Связи с общественностью'),
                                             ('consult', 'Политические коммуникации / Политическое консультирование'),
                                             ('ads', 'Рекламные коммуникации / Реклама'),
                                             ('event', 'Событийные коммуникации / Мероприятия / Event'),
                                             ('digital', 'Цифровые коммуникации / Digital'),

                                             ]),
            'revenue_share': forms.NumberInput(attrs={'class': 'form-control',
                                                      'min' :0, 'max' : 100, 'step' : 1, 'onkeypress' : only_digit, 'oninput': only_procent }),
        }

class CompanyEmployeesForm(forms.ModelForm):
    class Meta:
        model = CompanyEmployees
        fields = ['department', 'employee_count']
        widgets = {
            'employee_count': forms.NumberInput(attrs={'min' :0,  'step' : 1, 'onkeypress' : only_digit,'class': 'input_to_copy_number'
            }),
            'department': forms.TextInput(attrs={
                'placeholder': 'Введите название компании или отдела', 'class': 'input_to_copy_text'
            })
        }

    def clean_employee_count(self):
        employee_count = self.cleaned_data.get('employee_count')
        if employee_count <= 0:
            raise forms.ValidationError("Количество сотрудников должно быть положительным числом.")
        return employee_count

class CompanyAwardsForm(forms.ModelForm):
    class Meta:
        model = CompanyAwards
        fields = ['award_name', 'award_category', 'award_type']
        widgets = {
            'award_category': forms.Select(choices=[
            ('A', 'А'),
            ('B', 'Б'),
            ('C', 'В'),
        ], attrs={'class': 'category-select',"onchange":"updateCategoryCounts()"}),
            'award_type': forms.Select(choices=[
                ('shortlist', 'Шорт лист'),
                ('award', 'Награда'),
                ('grandprix', 'Гранд При'),
            ], attrs={'class': 'type-select', "onchange": "updateCategoryCounts()"}),
        }

class CompanyEventForm(forms.ModelForm):
    class Meta:
        model = CompanyEvent
        fields = ['event_count', 'audience', 'participant_count', 'event_format', 'event_type', 'participation_type']
        widgets = {
            'event_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество мероприятий','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'audience': forms.Select(choices=[('students', 'Студенты'),('prof', 'Проф. Сообщества')],attrs={'class': 'form-control', 'placeholder': 'Аудитория'}),
            'participant_count': forms.NumberInput(attrs={'class': 'form-control','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'event_format': forms.Select(attrs={'class': 'form-control'}),
            'event_type': forms.Select(choices=[('solo', 'Единичное'),('complex', 'Комплекснная программа')],attrs={'class': 'form-control', 'placeholder': 'Формат мероприятия'}),
            'participation_type': forms.Select(attrs={'class': 'form-control'}),
        }

class CompanyRevenueForm(forms.ModelForm):
    class Meta:
        model = CompanyRevenue
        fields = ['company_name', 'inn', 'ownership_share', 'buying_share', 'revenue_amount']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании'}),
            'inn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ИНН','min' :0, 'step' : 1, 'onkeypress' : only_digit,}),
            'ownership_share': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Доля владения (%)','min' :0, 'max' : 100, 'step' : 1, 'onkeypress' : only_digit, 'oninput': only_procent,}),
            'buying_share': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Доля баинга в выручке (%)','min' :0, 'max' : 100, 'step' : 1, 'onkeypress' : only_digit, 'oninput': only_procent}),
            'revenue_amount': forms.NumberInput(attrs={'class': 'form-control revenue-input', 'placeholder': 'Доля выручки (тыс. рублей)','min' :0, 'step' : 1, 'onkeypress' : only_digit, 'oninput': 'calculateRevenue()'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Выбираем только те поля, которые будем редактировать
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Введите новый логин', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите новый email', 'class': 'form-control'}),
        }

class SinglePasswordChangeForm(forms.Form):
    new_password = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput,
        help_text="Введите новый пароль.",
        validators=[validate_password],
    )


class ModeratorCommentForm(forms.ModelForm):
    class Meta:
        model = CompanySurvey
        fields = ['moderator_comment']
        widgets = {
            'moderator_comment': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }
        labels = {
            'moderator_comment': 'Комментарий модератора',
        }