from reportlab.lib import colors
from reportlab.lib.units import inch

from pdf_engine.handlers.resume_generator import ResumeGenerator


class ResumeTemplateHandler:

    def create_resume_from_various_templates(self, name):

        resume = ResumeGenerator(name)

        # Initialize the PDF generator with a filename
        resume.update_styles(
            title_color=colors.black,  # Custom title color
            section_color=colors.black  # Custom section color
        )

        # Add Personal Information
        resume.add_personal_info(
            name="John Doe",
            contact_info={
                'email': 'john.doe@example.com',
                'phone': '+1 (123) 456-7890',
                'linkedin': 'https://linkedin.com/in/johndoe',
                'website': 'https://johndoe.com'
            }
        )

        resume.add_summary(
            "Innovative software engineer with 5+ years of experience "
            "in developing scalable web applications and microservices. "
            "Proven track record of leading projects and optimizing system performance.",
        )

        # Add Professional Experience
        resume.add_experience([
            {
                'title': 'Senior Software Engineer',
                'company': 'TechCorp Inc.',
                'start_date': 'Jan 2020',
                'end_date': 'Present',
                'location': 'San Francisco, CA',
                'achievements': [
                    'Led development of microservices architecture.',
                    'Reduced system latency by 40% through optimization.',
                    'Mentored junior developers in agile methodologies.'
                ]
            },
            {
                'title': 'Software Engineer',
                'company': 'StartUp Solutions',
                'start_date': 'Jun 2017',
                'end_date': 'Dec 2019',
                'location': 'New York, NY',
                'description': 'Developed and maintained full-stack web applications.'
            }
        ])

        # Add Education
        resume.add_education([
            {
                'degree': 'Master of Science',
                'field': 'Computer Science',
                'institution': 'Stanford University',
                'graduation_date': '2017'
            }
        ])

        # Add Skills
        resume.add_skills_bullet(
            [
                'Python', 'Django', 'React', 'Docker', 'Kubernetes',
                'AWS', 'Machine Learning', 'CI/CD', 'Microservices'
            ]
        )

        # Add a Page Break and Additional Section
        resume.add_page_break()

        resume.add_additional_info(
            "Available for remote opportunities and willing to relocate. "
            "Passionate about mentoring and open-source contributions.",
        )

        # Generate the final PDF
        resume.generate()
        print("Resume generated successfully as 'john_doe_resume.pdf'")
