from datetime import datetime
from pdf_engine.models import (
    PersonalInfo,
    Summary,
    Resume,
    Experience,
    ResumeExperience,
    Skill,
    ResumeSkill,
    Education,
    ResumeEducation
)


class ResumeDataHandler:

    def extract_data_from_github(self, data):
        # Extract data from json
        pass

    def extract_data_from_linkedin(self, data):
        pass


    def populate_resume_from_json(self, data):
        # Create PersonalInfo
        personal_info = PersonalInfo.objects.create(
            name=data['name'],
            email=data['contact_info']['email'],
            phone=data['contact_info']['phone'],
            linkedin=data['contact_info']['linkedin'],
            website=data['contact_info']['website']
        )

        # Create Summary
        summary = Summary.objects.create(
            text=data['summary']
        )

        # Create Resume
        resume = Resume.objects.create(
            personal_info=personal_info,
            summary=summary
        )

        # Create Experiences and Map to Resume
        for position, exp in enumerate(data['experience'], start=1):
            experience = Experience.objects.create(
                title=exp['title'],
                company=exp['company'],
                start_date=datetime.strptime(exp['start_date'], '%b %Y').date(),
                end_date=datetime.strptime(exp['end_date'], '%b %Y').date() if exp['end_date'] != 'Present' else None,
                location=exp['location'],
                description=exp['description'],
                achievements=",".join(exp['achievements'])
            )
            ResumeExperience.objects.create(
                resume=resume,
                experience=experience,
                position=position
            )

        for position, edu in enumerate(data['education'], start=1):
            education = Education.objects.create(
                degree=edu['degree'],
                field=edu['field'],
                institution=edu['institution'],
                graduation_date=datetime.strptime(edu['graduation_date'], '%b %Y').date()
            )
            ResumeEducation.objects.create(
                resume=resume,
                education=education,
                position=position
            )
        # Create Skills and Map to Resume
        for position, skill_name in enumerate(data['skills'], start=1):
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            ResumeSkill.objects.create(
                resume=resume,
                skill=skill,
                position=position
            )

        # Add Additional Info (if required, store as part of resume or another table)
        if 'additional_info' in data:
            print(f"Additional Info: {data['additional_info']}")  # Handle as needed

        return resume
