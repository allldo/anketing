from django.contrib import admin

from website.models import GeneralInfo, UserMessage, CompanySurvey, CompanyPositioning, CompanyEmployees, CompanyAwards, \
    CompanyRevenue, CompanyEvent, SurveyStatus, CompanyProfile

admin.site.register(GeneralInfo)
admin.site.register(UserMessage)
admin.site.register(CompanySurvey)
admin.site.register(CompanyPositioning)
admin.site.register(CompanyEmployees)
admin.site.register(CompanyAwards)
admin.site.register(CompanyRevenue)
admin.site.register(CompanyEvent)
admin.site.register(SurveyStatus)
admin.site.register(CompanyProfile)
