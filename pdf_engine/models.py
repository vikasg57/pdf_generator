from django.db import models
from base.models import AbstractBaseModel


class PersonalInfo(AbstractBaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    linkedin = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)


class Summary(AbstractBaseModel):
    text = models.TextField()


class Experience(AbstractBaseModel):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # Null for current jobs
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)  # Store as a comma-separated list

    def get_achievements_list(self):
        return self.achievements.split(',') if self.achievements else []


class Education(AbstractBaseModel):
    degree = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_date = models.DateField(blank=True, null=True)


class Skill(AbstractBaseModel):
    name = models.CharField(max_length=255)


class Resume(AbstractBaseModel):
    personal_info = models.OneToOneField(PersonalInfo, on_delete=models.CASCADE)
    summary = models.OneToOneField(Summary, on_delete=models.CASCADE)


class ResumeExperience(AbstractBaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  # For ordering


class ResumeEducation(AbstractBaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  # For ordering


class ResumeSkill(AbstractBaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()  # For ordering


class ResumeTemplate(AbstractBaseModel):
    name = models.CharField(max_length=255)
    default = models.BooleanField(default=False)
    style_json = models.JSONField()

    def __str__(self):
        return self.name
