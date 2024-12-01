from pdf_engine.handlers.resume_generator import ResumeGenerator
from pdf_engine.models import Resume, ResumeTemplate


class ResumeTemplateHandler:

    def register_template(self, name: str):
        default_template, _ = ResumeTemplate.objects.get_or_create(
            name=name,
            default=False,
            style_json={
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
        )
        return default_template

    def apply_template(self, template: str, filename: str, style_name: str, **kwargs):
        """
        Applies a registered template to generate a resume.
        """
        if not template:
            raise ValueError(f"Template is not registered.")
        resume = ResumeGenerator(filename)
        self.modern_template(resume, 'styles.json', style_name, **kwargs)
        resume.generate()
        print(f"Resume generated successfully as '{filename}'")

    def modern_template(self, resume: ResumeGenerator, file_name: str, style_name: str, **kwargs):
        resume.load_styles_from_config(file_name, style_name)
        self._add_common_sections(resume, **kwargs)

    # def classic_template(self, resume: ResumeGenerator, **kwargs):
    #     resume.load_styles_from_config('styles.json')
    #     self._add_common_sections(resume, **kwargs)

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

        print(experiences)
        print(education)
        print(skills)

        # Build the dictionary
        resume_data = {
            'contact_info': {
                'name': resume.personal_info.name,
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

    def create_resume(self, resume_id):
        resume = Resume.objects.get(uuid=resume_id)
        resume_data = self.resume_to_dict(resume)
        print(resume_data)
        pdf_generator = ResumeTemplateHandler()
        resume_template = pdf_generator.register_template("modern")
        pdf_generator.apply_template(
            resume_template,
            f"{resume.personal_info.name}_resume.pdf",
            "Elegant Gold Theme",
            **resume_data
        )


handler = ResumeTemplateHandler()

# Register templates
resume_template_d = handler.register_template("modern")
#
# Apply a template
handler.apply_template(
    resume_template_d,
    "john_doe_modern_resume.pdf",
    "Elegant Gold Theme",
    name="John Doe",
    contact_info={
        'email': 'john.doe@example.com',
        'phone': '+1 (123) 456-7890',
        'linkedin': 'https://linkedin.com/in/johndoe',
        'website': 'https://johndoe.com'
    },
    summary="Experienced software engineer with a passion for developing scalable web applications. "
            "Proficient in Python, Django, React, Docker, Kubernetes, and AWS.",

    experience=[
        {
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'start_date': 'Jan 2020',
            'end_date': 'Present',
            'location': 'San Francisco, CA',
            'achievements': [
                'Led development of microservices architecture.',
                'Reduced system latency by 40% through optimization.',
                'Mentored junior developers in agile methodologies.',
                'Collaborated with cross-functional teams to deliver high-quality software products.',
                'Implemented CI/CD pipelines for automated testing and deployment.',
                'Designed and developed RESTful APIs for internal and external services.',
                'Participated in code reviews and provided constructive feedback to team members.',
                'Utilized Docker and Kubernetes for containerization and orchestration of services.',
            ]
        },
        {
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'start_date': 'Jan 2020',
            'end_date': 'Present',
            'location': 'San Francisco, CA',
            'achievements': [
                'Led development of microservices architecture.',
                'Participated in code reviews and provided constructive feedback to team members.',
                'django and React for building web applications.',
                'AWS for cloud infrastructure and services.',
                'python and Django for backend development.',
                'quickly learn new technologies and adapt to new environments.',
                'Mentored junior developers in agile methodologies.',
                'Collaborated with cross-functional teams to deliver high-quality software products.',
                'Implemented CI/CD pipelines for automated testing and deployment.',
                'Designed and developed RESTful APIs for internal and external services.',
                'Utilized Docker and Kubernetes for containerization and orchestration of services.',
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'StartUp Solutions',
            'start_date': 'Jun 2017',
            'end_date': 'Dec 2019',
            'location': 'New York, NY',
            'achievements': [
                'Led development of microservices architecture.',
                'Reduced system latency by 40% through optimization.',
                'Mentored junior developers in agile methodologies.',
                'python and Django for backend development.',
                'quickly learn new technologies and adapt to new environments.',
                'Mentored junior developers in agile methodologies.',
                'Collaborated with cross-functional teams to deliver high-quality software products.',
                'Reduced system latency by 40% through optimization.',
                'Implemented CI/CD pipelines for automated testing and deployment.',
                'Designed and developed RESTful APIs for internal and external services.',
                'Implemented CI/CD pipelines for automated testing and deployment.',
                'Designed and developed RESTful APIs for internal and external services.',
                'Utilized Docker and Kubernetes for containerization and orchestration of services.',
            ],
        }
    ],
    education=[
                {
                    'degree': 'Master of Science',
                     'field': 'Computer Science',
                     'institution': 'Stanford University',
                     'graduation_date': '2017'
                },
                {
                    'degree': 'Bachelor of Science',
                    'field': 'Computer Science',
                    'institution': 'Stanford University',
                    'graduation_date': '2015'
                }
    ],
    skills=['Python', 'Django', 'React', 'Docker', 'Kubernetes', 'AWS'],
    additional_info=
    "Available for remote opportunities and willing to relocate. "
    "Passionate about mentoring and open-source contributions.",
)
