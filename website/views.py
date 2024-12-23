from cProfile import Profile

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, get_user_model

from django.db.models import OuterRef, Subquery, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.views.decorators.csrf import csrf_exempt

from .models import (GeneralInfo,CompanySurvey, CompanyProfile, CompanyPositioning, CompanyEvent,
                     CompanyRevenue, CompanyAwards,
                    CompanyEmployees, SurveyStatus)
from .forms import (UserRegistrationForm, CompanyProfileForm, GeneralInfoForm, CompanyEventForm,
                    CompanySurveyForm, CompanyAwardsForm, CompanyEmployeesForm, CompanyPositioningForm,
                    CompanyRevenueForm, UserUpdateForm, SinglePasswordChangeForm, UserMessageForm,
                    ModeratorCommentForm, SurveyFormUpdate
                    )
from django.forms import modelformset_factory
from datetime import datetime
import json

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('role_based_redirect')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    
    return render(request, 'login.html')

@login_required
def role_based_redirect(request):
    if request.user.is_staff:
        return redirect('moderator_dashboard')
    else:
        return redirect('user_dashboard')
    
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        company_form = CompanyProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            company_profile = company_form.save(commit=False)
            company_profile.user = user
            company_profile.save()

            login(request, user)

            if user.is_staff:
                return redirect('moderator_dashboard')
            else:
                return redirect('user_dashboard')

    else:
        user_form = UserRegistrationForm()
        company_form = CompanyProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'company_form': company_form
    })

@csrf_exempt
@login_required
def moderator_dashboard(request):
    general_info, created = GeneralInfo.objects.get_or_create(
        id=1,
        defaults={
            'methodology_file': '',
            'charter_file': '',
            'results_file': '',
        }
    )
    print(request.POST)
    # Обработка формы общей информации
    if request.method == 'POST' and 'general_info_form' in request.POST:

        form = GeneralInfoForm(request.POST, request.FILES, instance=general_info)
        if form.is_valid():
            form.save()
    else:
        form = GeneralInfoForm(instance=general_info)

    # Обработка изменения статуса анкеты
    if request.method == 'POST' and 'edit_status' in request.POST:
        survey_id = request.POST.get('survey_id')
        new_status = request.POST.get('edit_status')
        moderator_comment = request.POST.get('moderator_comment')
        try:
            survey = CompanySurvey.objects.get(id=survey_id)
            SurveyStatus.objects.create(
                survey=survey,
                status=new_status, user=request.user
            )

            if moderator_comment:
                survey.moderator_comment = moderator_comment
                survey.save()
        except CompanySurvey.DoesNotExist:
            print('Анкета не найдена')
    if request.method == 'POST' and 'edit_participant' in request.POST:
        try:
            profile = CompanyProfile.objects.get(id=request.POST.get('profile_id_rec'))
        except CompanyProfile.DoesNotExist:
            redirect('moderator_dashboard')
        company_profile_form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=profile.user)

        if company_profile_form.is_valid():
            company_profile_form.save()

        if user_form.is_valid():
            user_form.save()

    # Сбор данных об анкетах
    companies = CompanySurvey.objects.values('company_name').distinct()
    company_surveys = {}

    for company in companies:
        company_name = company['company_name']
        surveys = CompanySurvey.objects.filter(company_name=company_name)
        surveys_with_status = []

        for survey in surveys:
            latest_status = survey.statuses.latest('created_at') if survey.statuses.exists() else None
            comment_form = ModeratorCommentForm(instance=survey)
            positioning = list(survey.positionings.all())
            employees = list(survey.employees.all())
            awards = list(survey.awards.all())
            revenues = list(survey.revenues.all())
            events = list(survey.events.all())
            surveys_with_status.append({
                'survey': survey,
                'latest_status': latest_status.get_status_display() if latest_status else 'Нет статуса',
                'comment_form': comment_form,
                'positionings': positioning,
                'employees': employees,    
                'awards': awards,       
                'revenues': revenues, 
                'events': events, 
            })

        company_surveys[company_name] = surveys_with_status

    company_profiles = CompanyProfile.objects.all()
    profile_forms = [
        {'profile': profile, 'form': CompanyProfileForm(instance=profile), 'user_form': UserUpdateForm(instance=profile.user)}
        for profile in company_profiles
    ]
    active_users = User.objects.filter(company_profile__isnull=False)

    companies_with_surveys = CompanyProfile.objects.annotate(
        survey_count=Count('user__surveys')
    ).filter(survey_count__gt=0)
    #  {{ item.user_form.username }}
    context = {
        'general_info_form': form,
        'company_surveys': company_surveys,
        'companies': companies_with_surveys,
        'profile_forms': profile_forms,  # Профили с формами
    }

    return render(request, 'moderator_dashboard.html', context)


@login_required
def edit_general_info(request):
    general_info, created = GeneralInfo.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = GeneralInfoForm(request.POST, request.FILES, instance=general_info)
        if form.is_valid():
            form.save()
            return redirect('moderator_dashboard') 
    else:
        form = GeneralInfoForm(instance=general_info)

    return render(request, 'edit_general_info.html', {'form': form})


@login_required
def user_dashboardqqqq(request):
    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    general_info, created = GeneralInfo.objects.get_or_create(
        id=1,
        defaults={
            'methodology_file': '',
            'charter_file': '',
            'results_file': '',
        }
    )
    methodology_file = general_info.methodology_file.name.split('/')[-1] if general_info.methodology_file else 'No File'
    charter_file = general_info.charter_file.name.split('/')[-1] if general_info.charter_file else 'No File'
    results_file = general_info.results_file.name.split('/')[-1] if general_info.results_file else 'No File'
    profile_form = CompanyProfileForm(instance=profile)
    user_form = UserUpdateForm(instance=request.user)
    password_form = SinglePasswordChangeForm()
    user_message_form = UserMessageForm()
    survey_form = CompanySurveyForm()

    positioning_formset = modelformset_factory(
        CompanyPositioning, form=CompanyPositioningForm, extra=1, can_delete=True
    )(
        queryset=CompanyPositioning.objects.none(),
        prefix="positioning"
    )

    revenue_formset = modelformset_factory(
        CompanyRevenue, form=CompanyRevenueForm, extra=1, can_delete=True
    )(
        queryset=CompanyRevenue.objects.none(),
        prefix="revenue"
    )

    employees_formset = modelformset_factory(
        CompanyEmployees, form=CompanyEmployeesForm, extra=1, can_delete=True
    )(
        queryset=CompanyEmployees.objects.none(),
        prefix="employees"
    )

    awards_formset = modelformset_factory(
        CompanyAwards, form=CompanyAwardsForm, extra=1, can_delete=True
    )(
        queryset=CompanyAwards.objects.none(),
        prefix="awards"
    )

    events_formset = modelformset_factory(
        CompanyEvent, form=CompanyEventForm, extra=1, can_delete=True
    )(
        queryset=CompanyEvent.objects.none(),
        prefix="events"
    )

    if request.method == 'POST':
        # print("Данные POST:")
        # print(json.dumps(request.POST, indent=4, ensure_ascii=False))
        profile_form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = SinglePasswordChangeForm(request.POST)
        user_message_form = UserMessageForm(request.POST)

        if profile_form.is_valid():
            profile_form.save()

        if user_form.is_valid():
            user_form.save()

        if password_form.is_valid():
            new_password = password_form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user_dashboard')

        if user_message_form.is_valid():
            user_message_form.save()

        if 'create_survey' in request.POST or 'update_survey' in request.POST or 'submit_for_review' in request.POST:
            survey_form = SurveyFormUpdate(request.POST)








            if survey_form.is_valid():
                survey_id = survey_form.cleaned_data['survey_id']
                survey = CompanySurvey.objects.get(id=survey_id)
                print("редачим")
                survey_form = CompanySurveyForm(request.POST, instance=survey)
                positioning_formset = modelformset_factory(
                    CompanyPositioning, form=CompanyPositioningForm, extra=0, can_delete=True
                )(request.POST, prefix='positioning', queryset=survey.positionings.all())

                revenue_formset = modelformset_factory(
                    CompanyRevenue, form=CompanyRevenueForm, extra=0, can_delete=True
                )(request.POST, prefix='revenue', queryset=survey.revenues.all())

                employees_formset = modelformset_factory(
                    CompanyEmployees, form=CompanyEmployeesForm, extra=0, can_delete=True
                )(request.POST, prefix='employees', queryset=survey.employees.all())

                awards_formset = modelformset_factory(
                    CompanyAwards, form=CompanyAwardsForm, extra=0, can_delete=True
                )(request.POST, prefix='awards', queryset=survey.awards.all())

                events_formset = modelformset_factory(
                    CompanyEvent, form=CompanyEventForm, extra=0, can_delete=True
                )(request.POST, prefix='events', queryset=survey.events.all())

                # Если все формы прошли валидацию
                if (
                        positioning_formset.is_valid() and
                        revenue_formset.is_valid() and
                        employees_formset.is_valid() and
                        awards_formset.is_valid() and
                        events_formset.is_valid()
                ):
                    print('all valid gogogo')
                    # Сохраняем обновленную анкету
                    survey_form = CompanySurveyForm(request.POST, instance=survey)
                    if survey_form.is_valid():
                        print('survey valid googgogo')
                        survey_form.save()

                    # Сохраняем все связанные формы
                    for formset in [
                        positioning_formset,
                        revenue_formset,
                        employees_formset,
                        awards_formset,
                        events_formset,
                    ]:
                        instances = formset.save(commit=False)
                        for instance in instances:
                            instance.survey = survey

                            print('saving kekekekek')
                            instance.save()

                    messages.success(request, "Анкета успешно обновлена!")
                    return redirect('user_dashboard')











            survey_form = CompanySurveyForm(request.POST)
            positioning_formset = modelformset_factory(
                CompanyPositioning, form=CompanyPositioningForm, extra=1, can_delete=True
            )(request.POST, prefix='positioning')
            revenue_formset = modelformset_factory(
                CompanyRevenue, form=CompanyRevenueForm, extra=1, can_delete=True
            )(request.POST, prefix='revenue')
            employees_formset = modelformset_factory(
                CompanyEmployees, form=CompanyEmployeesForm, extra=1, can_delete=True
            )(request.POST, prefix='employees')
            awards_formset = modelformset_factory(
                CompanyAwards, form=CompanyAwardsForm, extra=1, can_delete=True
            )(request.POST, prefix='awards')
            events_formset = modelformset_factory(
                CompanyEvent, form=CompanyEventForm, extra=1, can_delete=True
            )(request.POST, prefix='events')
            if (
                survey_form.is_valid()
                and positioning_formset.is_valid()
                and revenue_formset.is_valid()
                and employees_formset.is_valid()
                and awards_formset.is_valid()
                and events_formset.is_valid()
            ):
                survey = survey_form.save(commit=False)
                survey.user = request.user
                survey.save()
                print(positioning_formset.data)
                for formset in [
                    positioning_formset,
                    revenue_formset,
                    employees_formset,
                    awards_formset,
                    events_formset,
                ]:
                    instances = formset.save(commit=False)
                    for instance in instances:
                        instance.survey = survey
                        instance.save()
                if 'create_survey' in request.POST:
                    SurveyStatus.objects.create(
                        survey=survey,
                        status='draft',
                        user=request.user
                    )
                if 'submit_for_review' in request.POST:
                    if ':' in request.POST:
                        try:
                            action = request.POST.get('action', '')
                            survey = CompanySurvey.objects.get(id=action.split(':')[1])
                            messages.success(request, f'Анкета "{survey.company_name}" отправлена на модерацию.')
                        except CompanySurvey.DoesNotExist:
                            messages.error(request, 'Анкета не найдена.')
                    SurveyStatus.objects.create(
                        survey=survey,
                        status='moderate',
                        user=request.user
                    )
                return render(request, 'user_dashboard.html', {
                'survey_form': survey_form,
                'positioning_formset': positioning_formset,
                'revenue_formset': revenue_formset,
                'employees_formset': employees_formset,
                'awards_formset': awards_formset,
                'events_formset': events_formset,
            })



            return render(request, 'user_dashboard.html', {
                'survey_form': survey_form,
                'positioning_formset': positioning_formset,
                'revenue_formset': revenue_formset,
                'employees_formset': employees_formset,
                'awards_formset': awards_formset,
                'events_formset': events_formset,
            })

    current_year = datetime.now().year

    STATUS_DISPLAY = dict(SurveyStatus.STATUS_CHOICES)
    latest_status = SurveyStatus.objects.filter(
        survey=OuterRef('pk')
    ).order_by('-created_at').values('status')[:1]

    user_surveys = [CompanySurvey.objects.filter(
        user=request.user,
        submission_date__year=current_year
    ).last()]
    if user_surveys[0] is None:
        context = {
            # 'surveys_with_forms': surveys_with_forms,
            'profile_form': profile_form,
            'user_form': user_form,
            'password_form': password_form,
            'profile': profile,
            'user_surveys': user_surveys,
            # 'old_surveys': old_surveys,
            "user_message_form": user_message_form,
            "survey_form": survey_form,
            "positioning_formset": positioning_formset,
            "revenue_formset": revenue_formset,
            "employees_formset": employees_formset,
            "awards_formset": awards_formset,
            "events_formset": events_formset,
            "general_info": general_info,
            "methodology_file": methodology_file,
            "charter_file": charter_file,
            "results_file": results_file,
            "current_year": current_year,
        }

        return render(request, 'user_dashboard.html', context)
    else:
        survey_id_context = None
        surveys_with_forms = []
        for survey in user_surveys:
            print(survey)
            survey_id_context = survey.id
            current_survey_form = CompanySurveyForm(instance=survey)
            # survey.latest_status_text = STATUS_DISPLAY.get(survey.latest_status, "Unknown")
            survey_positioning_formset = modelformset_factory(
                CompanyPositioning,
                form=CompanyPositioningForm,
                extra=0
            )(queryset=survey.positionings.all())


            survey_employees_formset = modelformset_factory(
                CompanyEmployees,
                form=CompanyEmployeesForm,
                extra=0
            )(queryset=survey.employees.all())

            survey_awards_formset = modelformset_factory(
                CompanyAwards,
                form=CompanyAwardsForm,
                extra=0
            )(queryset=survey.awards.all())

            survey_events_formset = modelformset_factory(
                CompanyEvent,
                form=CompanyEventForm,
                extra=0
            )(queryset=survey.events.all())

            survey_revenue_formset = modelformset_factory(
                CompanyRevenue,
                form=CompanyRevenueForm,
                extra=0
            )(queryset=survey.revenues.all())

            surveys_with_forms.append({
            'survey': survey,
            'current_survey_form': current_survey_form,
            'positioning_formset': survey_positioning_formset,
            'employees_formset': survey_employees_formset,
            'awards_formset': survey_awards_formset,
            'events_formset': survey_events_formset,
            'revenue_formset': survey_revenue_formset,
        })



    # old_surveys = CompanySurvey.objects.filter(
    #     user=request.user
    # ).exclude(submission_date__year=current_year).order_by('-submission_date')
    survey_form_update = SurveyFormUpdate(initial={'survey_id': survey_id_context})
    print(survey_positioning_formset, survey_revenue_formset )
    context = {
        # "survey_id": survey_id_context,
        "survey_form_update": survey_form_update,
        'survey_form': current_survey_form,
        'positioning_formset': survey_positioning_formset,
        'revenue_formset': survey_revenue_formset,
        'employees_formset': survey_employees_formset,
        'awards_formset': survey_awards_formset,
        'events_formset': survey_events_formset,
        'surveys_with_forms': surveys_with_forms,
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'profile': profile,
        'user_surveys': user_surveys,
        # 'old_surveys': old_surveys,
        "user_message_form": user_message_form,
        # "survey_form": survey_form,
        # "positioning_formset": positioning_formset,
        # "revenue_formset": revenue_formset,
        # "employees_formset": employees_formset,
        # "awards_formset": awards_formset,
        # "events_formset": events_formset,
        "general_info": general_info,
        "methodology_file": methodology_file,
        "charter_file": charter_file,
        "results_file": results_file,
        "current_year": current_year,
    }

    return render(request, 'user_dashboard.html', context)


@csrf_exempt
@login_required
def user_dashboard(request):
    print(request.POST)
    profile, created = CompanyProfile.objects.get_or_create(user=request.user)
    survey = CompanySurvey.objects.filter(user=request.user).last()
    general_info, created = GeneralInfo.objects.get_or_create(
        id=1,
        defaults={
            'methodology_file': '',
            'charter_file': '',
            'results_file': '',
        }
    )
    methodology_file = general_info.methodology_file.name.split('/')[-1] if general_info.methodology_file else 'No File'
    charter_file = general_info.charter_file.name.split('/')[-1] if general_info.charter_file else 'No File'
    results_file = general_info.results_file.name.split('/')[-1] if general_info.results_file else 'No File'
    latest_status = SurveyStatus.objects.filter(
        survey=survey
    ).order_by('-created_at')[:1].first()
    if request.method == 'POST':
        print("POST request received.")

        if 'create_survey' in request.POST or 'update_survey' in request.POST or 'submit_for_review' in request.POST:
            # Попытка получить или создать анкету
            # print(request.POST)

            survey_form = CompanySurveyForm(request.POST, request.FILES,instance=survey)

            # Формсеты
            positioning_formset = modelformset_factory(
                CompanyPositioning, form=CompanyPositioningForm, extra=1, can_delete=True
            )(request.POST, prefix='positioning')
            revenue_formset = modelformset_factory(
                CompanyRevenue, form=CompanyRevenueForm, extra=1, can_delete=True
            )(request.POST, prefix='revenue')
            employees_formset = modelformset_factory(
                CompanyEmployees, form=CompanyEmployeesForm, extra=1, can_delete=True
            )(request.POST, prefix='employees')
            awards_formset = modelformset_factory(
                CompanyAwards, form=CompanyAwardsForm, extra=1, can_delete=True
            )(request.POST, prefix='awards')
            events_formset = modelformset_factory(
                CompanyEvent, form=CompanyEventForm, extra=1, can_delete=True
            )(request.POST, prefix='events')

            # Вывод валидности формсетов
            print("Formset validity:")
            print("Positioning:", positioning_formset.is_valid())
            print("Revenue:", revenue_formset.is_valid())
            print("Employees:", employees_formset.is_valid())
            print("Awards:", awards_formset.is_valid())
            print("Events:", events_formset.is_valid())
            # Сохранение анкеты
            if survey_form.is_valid():
                survey = survey_form.save(commit=False)
                survey.user = request.user
                survey.save()

                for formset in [positioning_formset, revenue_formset, employees_formset, awards_formset, events_formset]:
                    if formset.is_valid():
                        instances = formset.save(commit=False)
                        print('alot', instances)
                        for instance in instances:
                            instance.survey = survey
                            instance.save()
                        for form in formset:
                            if form.cleaned_data.get('mask_for_deletion') == "DELETE":
                                form.instance.delete()
                    else:
                        print(f"Errors in {formset.prefix} formset: {formset.errors}")
                        print(f"Non-form errors in {formset.prefix}: {formset.non_form_errors()}")

                try:
                    CompanyPositioning.objects.filter(survey=survey)[0]
                except IndexError:
                    CompanyPositioning.objects.create(survey=survey)
                try:
                    CompanyRevenue.objects.filter(survey=survey)[0]
                except IndexError:
                    CompanyRevenue.objects.create(survey=survey)
                try:
                    CompanyEmployees.objects.filter(survey=survey)[0]
                except IndexError:
                    CompanyEmployees.objects.create(survey=survey)
                try:
                    CompanyAwards.objects.filter(survey=survey)[0]
                except IndexError:
                    CompanyAwards.objects.create(survey=survey)
                try:
                    CompanyEvent.objects.filter(survey=survey)[0]
                except IndexError:
                    CompanyEvent.objects.create(survey=survey)

                # Создание статуса анкеты
                if 'create_survey' in request.POST:
                    SurveyStatus.objects.create(
                        survey=survey,
                        status='draft',
                        user=request.user
                    )

                print('submit_for_review')
                if 'submit_for_review' in request.POST:
                    if ':' in request.POST:
                        try:
                            action = request.POST.get('action', '')
                            survey = CompanySurvey.objects.get(id=action.split(':')[1])
                            messages.success(request, f'Анкета "{survey.company_name}" отправлена на модерацию.')
                        except CompanySurvey.DoesNotExist:
                            messages.error(request, 'Анкета не найдена.')
                    SurveyStatus.objects.create(
                        survey=survey,
                        status='moderate',
                        user=request.user
                    )

                return redirect('user_dashboard')

        profile_form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = SinglePasswordChangeForm(request.POST)
        user_message_form = UserMessageForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()

        if user_form.is_valid():
            user_form.save()
        if password_form.is_valid():
            new_password = password_form.cleaned_data['new_password']
            if len(new_password) < 2:
                return redirect('user_dashboard')
            user = request.user
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('user_dashboard')
        # Профиль, пользователь, пароль и сообщения


        if user_message_form.is_valid():
            user_message_form.save()

    else:
        # Инициализация форм
        profile_form = CompanyProfileForm(instance=profile)
        user_form = UserUpdateForm(instance=request.user)
        password_form = SinglePasswordChangeForm()
        user_message_form = UserMessageForm()
        survey_form = CompanySurveyForm(instance=survey) if survey else CompanySurveyForm(initial={'specialization': 'full cycle'})

        # Формсеты для анкеты
        if survey:
            PositioningFormSet = modelformset_factory(CompanyPositioning, form=CompanyPositioningForm, extra=0,
                                                      can_delete=True)
            RevenueFormSet = modelformset_factory(CompanyRevenue, form=CompanyRevenueForm, extra=0, can_delete=True)
            EmployeesFormSet = modelformset_factory(CompanyEmployees, form=CompanyEmployeesForm, extra=0,
                                                    can_delete=True)
            AwardsFormSet = modelformset_factory(CompanyAwards, form=CompanyAwardsForm, extra=0, can_delete=True)
            EventsFormSet = modelformset_factory(CompanyEvent, form=CompanyEventForm, extra=0, can_delete=True)
        else:
            PositioningFormSet = modelformset_factory(CompanyPositioning, form=CompanyPositioningForm, extra=1,
                                                      can_delete=True)
            RevenueFormSet = modelformset_factory(CompanyRevenue, form=CompanyRevenueForm, extra=1, can_delete=True)
            EmployeesFormSet = modelformset_factory(CompanyEmployees, form=CompanyEmployeesForm, extra=1,
                                                    can_delete=True)
            AwardsFormSet = modelformset_factory(CompanyAwards, form=CompanyAwardsForm, extra=1, can_delete=True)
            EventsFormSet = modelformset_factory(CompanyEvent, form=CompanyEventForm, extra=1, can_delete=True)

        PositioningFormSet = PositioningFormSet(
            queryset=CompanyPositioning.objects.filter(survey=survey) if survey else CompanyPositioning.objects.none(),
            prefix='positioning')
        RevenueFormSet = RevenueFormSet(
            queryset=CompanyRevenue.objects.filter(survey=survey) if survey else CompanyRevenue.objects.none(),
            prefix='revenue')
        EmployeesFormSet = EmployeesFormSet(
            queryset=CompanyEmployees.objects.filter(survey=survey) if survey else CompanyEmployees.objects.none(),
            prefix='employees')
        AwardsFormSet = AwardsFormSet(
            queryset=CompanyAwards.objects.filter(survey=survey) if survey else CompanyAwards.objects.none(),
            prefix='awards')
        EventsFormSet = EventsFormSet(
            queryset=CompanyEvent.objects.filter(survey=survey) if survey else CompanyEvent.objects.none(),
            prefix='events')

    return render(request, 'user_dashboard.html', {
        'survey': survey,
        'profile_form': profile_form,
        'profile': profile,
        'user_form': user_form,
        'password_form': password_form,
        'user_message_form': user_message_form,
        'survey_form': survey_form,
        'latest_status': latest_status,
        'positioning_formset': PositioningFormSet,
        'revenue_formset': RevenueFormSet,
        'employees_formset': EmployeesFormSet,
        'awards_formset': AwardsFormSet,
        'events_formset': EventsFormSet,
        "general_info": general_info,
        "methodology_file": methodology_file,
        "charter_file": charter_file,
        "results_file": results_file
    })

@login_required
def fill_survey(request):
    if request.method == 'POST':
        print("Данные POST:")
        print(json.dumps(request.POST, indent=4, ensure_ascii=False))

        survey_form = CompanySurveyForm(request.POST)
        
        positioning_formset = modelformset_factory(
            CompanyPositioning,
            form=CompanyPositioningForm,
            extra=0,
            can_delete=True
        )(request.POST)
        

        employees_formset = modelformset_factory(
            CompanyEmployees,
            form=CompanyEmployeesForm,
            extra=0,
            can_delete=True
        )(request.POST)

        awards_formset = modelformset_factory(
            CompanyAwards,
            form=CompanyAwardsForm,
            extra=0,
            can_delete=True
        )(request.POST)

        events_formset = modelformset_factory(
            CompanyEvent,
            form=CompanyEventForm,
            extra=0,
            can_delete=True
        )(request.POST)

        revenue_formset = modelformset_factory(
            CompanyRevenue,
            form=CompanyRevenueForm,
            extra=0,
            can_delete=True
        )(request.POST)


        print("Данные основной формы:", survey_form.data)
        print("Данные формсета (positioning_formset):", positioning_formset.management_form)
        print("Данные формсета (employees_formset):", employees_formset.management_form)
        print("Данные формсета (awards_formset):", awards_formset.management_form)
        print("Данные формсета (events_formset):", events_formset.management_form)
        print("Данные формсета (revenue_formset):", revenue_formset.management_form)
        if all([
            survey_form.is_valid(),
            positioning_formset.is_valid(),
            employees_formset.is_valid(),
            awards_formset.is_valid(),
            events_formset.is_valid(),
            revenue_formset.is_valid()
        ]):
            survey = survey_form.save(commit=False)
            survey.user = request.user
            survey.save()

            SurveyStatus.objects.create(
                survey=survey,
                status='moderate',
                user=request.user
            )
            for formset in [
                positioning_formset,
                employees_formset,
                awards_formset,
                events_formset,
                revenue_formset
            ]:
                for form in formset:
                    if form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.survey = survey
                        instance.save()

            return redirect('user_dashboard') 
        else:
            print(survey_form.errors)
            for formset in [positioning_formset, employees_formset, awards_formset, events_formset, revenue_formset]:
                print(formset.errors)

    else:
        survey_form = CompanySurveyForm()

        positioning_formset = modelformset_factory(
            CompanyPositioning,
            form=CompanyPositioningForm,
            extra=1
        )(queryset=CompanyPositioning.objects.none())

        employees_formset = modelformset_factory(
            CompanyEmployees,
            form=CompanyEmployeesForm,
            extra=1
        )(queryset=CompanyEmployees.objects.none())

        awards_formset = modelformset_factory(
            CompanyAwards,
            form=CompanyAwardsForm,
            extra=1
        )(queryset=CompanyAwards.objects.none())

        events_formset = modelformset_factory(
            CompanyEvent,
            form=CompanyEventForm,
            extra=1
        )(queryset=CompanyEvent.objects.none())

        revenue_formset = modelformset_factory(
            CompanyRevenue,
            form=CompanyRevenueForm,
            extra=1
        )(queryset=CompanyRevenue.objects.none())

    return render(request, 'fill_survey.html', {
        'survey_form': survey_form,
        'positioning_formset': positioning_formset,
        'employees_formset': employees_formset,
        'awards_formset': awards_formset,
        'events_formset': events_formset,
        'revenue_formset': revenue_formset,
    })

@login_required
def view_survey(request, survey_id):
    survey = get_object_or_404(CompanySurvey, id=survey_id, user=request.user)
    positionings = survey.positionings.all()
    revenues = survey.revenues.all()
    employees = survey.employees.all()
    awards = survey.awards.all()
    events = survey.events.all()

    context = {
        'survey': survey,
        'positionings': positionings,
        'revenues': revenues,
        'employees': employees,
        'awards': awards,
        'events': events,
    }
    return render(request, 'view_survey.html', context)


def change_survey_status(request, survey_id):
    survey = get_object_or_404(CompanySurvey, id=survey_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(SurveyStatus.STATUS_CHOICES):
            SurveyStatus.objects.create(
                survey=survey,
                status=new_status,
                user=request.user 
            )
            survey.moderator_comment = request.POST.get('moderator_comment', '')
            survey.save()

            return redirect('moderator_dashboard')
    else:
        return render(request, 'change_status.html', {'survey': survey})
    
@login_required
def edit_survey(request, survey_id):
    try:
        survey = CompanySurvey.objects.get(id=survey_id, user=request.user)
    except CompanySurvey.DoesNotExist:
        return redirect('user_dashboard') 

    if request.method == 'POST':
        survey_form = CompanySurveyForm(request.POST, instance=survey)

        positioning_formset = modelformset_factory(
            CompanyPositioning,
            form=CompanyPositioningForm,
            extra=0,
            can_delete=True
        )(request.POST, queryset=survey.positionings.all())

        employees_formset = modelformset_factory(
            CompanyEmployees,
            form=CompanyEmployeesForm,
            extra=0,
            can_delete=True
        )(request.POST, queryset=survey.employees.all())

        awards_formset = modelformset_factory(
            CompanyAwards,
            form=CompanyAwardsForm,
            extra=0,
            can_delete=True
        )(request.POST, queryset=survey.awards.all())

        events_formset = modelformset_factory(
            CompanyEvent,
            form=CompanyEventForm,
            extra=0,
            can_delete=True
        )(request.POST, queryset=survey.events.all())

        revenue_formset = modelformset_factory(
            CompanyRevenue,
            form=CompanyRevenueForm,
            extra=0,
            can_delete=True
        )(request.POST, queryset=survey.revenues.all())

        if all([
            survey_form.is_valid(),
            positioning_formset.is_valid(),
            employees_formset.is_valid(),
            awards_formset.is_valid(),
            events_formset.is_valid(),
            revenue_formset.is_valid()
        ]):
            survey = survey_form.save()

            # Save the associated formsets
            for formset in [
                positioning_formset,
                employees_formset,
                awards_formset,
                events_formset,
                revenue_formset
            ]:
                for form in formset:
                    if form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.survey = survey
                        instance.save()
            SurveyStatus.objects.create(
                survey=survey,
                status='draft',
                user=request.user 
            )
            return redirect('user_dashboard')  # Redirect to user dashboard after successful edit
        else:
            print(survey_form.errors)
            for formset in [positioning_formset, employees_formset, awards_formset, events_formset, revenue_formset]:
                print(formset.errors)
    else:
        survey_form = CompanySurveyForm(instance=survey)

        positioning_formset = modelformset_factory(
            CompanyPositioning,
            form=CompanyPositioningForm,
            extra=0
        )(queryset=survey.positionings.all())

        employees_formset = modelformset_factory(
            CompanyEmployees,
            form=CompanyEmployeesForm,
            extra=0
        )(queryset=survey.employees.all())

        awards_formset = modelformset_factory(
            CompanyAwards,
            form=CompanyAwardsForm,
            extra=0
        )(queryset=survey.awards.all())

        events_formset = modelformset_factory(
            CompanyEvent,
            form=CompanyEventForm,
            extra=0
        )(queryset=survey.events.all())

        revenue_formset = modelformset_factory(
            CompanyRevenue,
            form=CompanyRevenueForm,
            extra=0
        )(queryset=survey.revenues.all())
    moderator_comment = survey.moderator_comment
    return render(request, 'edit_survey.html', {
        'survey_form': survey_form,
        'moderator_comment': moderator_comment,
        'positioning_formset': positioning_formset,
        'employees_formset': employees_formset,
        'awards_formset': awards_formset,
        'events_formset': events_formset,
        'revenue_formset': revenue_formset,
    })