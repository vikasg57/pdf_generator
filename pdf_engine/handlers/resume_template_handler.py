from pdf_engine.handlers.resume_generator import ResumeGenerator
from pdf_engine.models import Resume, ResumeTemplate


class ResumeTemplateHandler:

    def register_template(self, name: str):
        default_template, _ = ResumeTemplate.objects.get_or_create(
            name=name,
            defaults={
                'style_json': {
                    "Elegant Gold Theme": {
                        "title_color": "#FFD700",
                        "section_color": "#DAA520",
                        "font_sizes": {
                            "title": 24,
                            "section_header": 18,
                            "normal": 12,
                            "subtitle": 14
                        },
                        "font_styles": {
                            "title": "Times-Bold",
                            "section_header": "Times-BoldItalic",
                            "normal": "Times-Roman",
                            "subtitle": "Times-Italic"
                        }
                    }
                }

            }
        )
        return default_template

    def apply_template(self, template: str, filename: str, json_style: str, **kwargs):
        """
        Applies a registered template to generate a resume.
        """
        if not template:
            raise ValueError(f"Template is not registered.")
        resume = ResumeGenerator(filename)
        self.modern_template(resume, json_style, **kwargs)
        resume.generate()
        print(f"Resume generated successfully as '{filename}'")

    def modern_template(self, resume: ResumeGenerator, json_style: str, **kwargs):
        resume.load_styles_from_config(json_style)
        self._add_common_sections(resume, **kwargs)

    def _add_common_sections(self, resume: ResumeGenerator, **kwargs):
        """
        Adds common sections to the resume (shared across templates).
        """
        resume.add_personal_info(
            name=kwargs.get('name', 'John Doe'),
            contact_info=kwargs.get('contact_info', {})
        )

        if 'summary' in kwargs:
            resume.add_summary(kwargs['summary'])

        if 'experience' in kwargs:
            resume.add_experience(kwargs['experience'])

        if 'education' in kwargs:
            resume.add_education(kwargs['education'])

        if 'skills' in kwargs:
            resume.add_skills_bullet(kwargs['skills'])

        if 'additional_info' in kwargs:
            resume.add_additional_info(kwargs['additional_info'])

    def resume_to_dict(self, resume):
        experiences = resume.resumeexperience_set.select_related('experience').order_by('position')
        education = resume.resumeeducation_set.select_related('education').order_by('position')
        skills = resume.resumeskill_set.select_related('skill').order_by('position')

        # Build the dictionary
        resume_data = {
            'name': resume.personal_info.name,
            'contact_info': {
                'email': resume.personal_info.email,
                'phone': resume.personal_info.phone,
                'linkedin': resume.personal_info.linkedin,
                'website': resume.personal_info.website,
            },
            'summary': resume.summary.text,
            'experience': [
                {
                    'title': exp.experience.title,
                    'company': exp.experience.company,
                    'start_date': exp.experience.start_date.strftime('%b %Y'),
                    'end_date': exp.experience.end_date.strftime('%b %Y') if exp.experience.end_date else 'Present',
                    'location': exp.experience.location,
                    'description': exp.experience.description,
                    'achievements': exp.experience.get_achievements_list(),
                }
                for exp in experiences
            ],
            'education': [
                {
                    'degree': edu.education.degree,
                    'field': edu.education.field,
                    'institution': edu.education.institution,
                    'graduation_date': edu.education.graduation_date.strftime(
                        '%Y') if edu.education.graduation_date else 'Present',
                }
                for edu in education
            ],
            'skills': [skill.skill.name for skill in skills],
            'additional_info': "Available for remote opportunities and willing to relocate. "
                               "Passionate about mentoring and open-source contributions.",

        }

        return resume_data

    def create_resume(self, resume_id, template_name):
        resume = Resume.objects.get(uuid=resume_id)
        resume_data = self.resume_to_dict(resume)
        pdf_generator = ResumeTemplateHandler()
        resume_template = pdf_generator.register_template(template_name)
        pdf_generator.apply_template(
            resume_template,
            f"{resume.personal_info.name}_resume.pdf",
            resume_template.style_json,
            **resume_data
        )
        return {
            "message": "Resume generated successfully."
        }
