from django.contrib import admin

from base.admin import BaseModelAdmin

# Register your models here.

from .models import (
    PersonalInfo,
    Summary,
    Experience,
    Education,
    Skill,
    Resume,
    ResumeExperience,
    ResumeEducation,
    ResumeSkill,
    ResumeTemplate
)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(BaseModelAdmin):
    search_fields = ('name', 'email', 'phone')
    list_display = ('name', 'email', 'phone', 'linkedin', 'website')


@admin.register(Summary)
class SummaryAdmin(BaseModelAdmin):
    search_fields = ('text',)
    list_display = ('text',)


@admin.register(Experience)
class ExperienceAdmin(BaseModelAdmin):
    search_fields = ('title', 'company', 'location')
    list_display = ('title', 'company', 'start_date', 'end_date', 'location', 'description', 'achievements')

@admin.register(Education)
class EducationAdmin(BaseModelAdmin):
    search_fields = ('degree', 'field', 'institution')
    list_display = ('degree', 'field', 'institution', 'graduation_date')


@admin.register(Skill)
class SkillAdmin(BaseModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(Resume)
class ResumeAdmin(BaseModelAdmin):
    search_fields = ('personal_info__name', 'summary__text')
    list_display = ('personal_info', 'summary')


@admin.register(ResumeExperience)
class ResumeExperienceAdmin(BaseModelAdmin):
    search_fields = ('resume__personal_info__name', 'experience__title', 'experience__company')
    list_display = ('resume', 'experience', 'position')


@admin.register(ResumeEducation)
class ResumeEducationAdmin(BaseModelAdmin):
    search_fields = ('resume__personal_info__name', 'education__degree', 'education__institution')
    list_display = ('resume', 'education', 'position')


@admin.register(ResumeSkill)
class ResumeSkillAdmin(BaseModelAdmin):
    search_fields = ('resume__personal_info__name', 'skill__name')
    list_display = ('resume', 'skill', 'position')


@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(BaseModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)
