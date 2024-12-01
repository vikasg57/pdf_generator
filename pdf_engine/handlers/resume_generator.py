from typing import List, Dict

from reportlab.lib import colors
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.units import inch
from pdf_engine.handlers.pdf_engine import PDFTemplateEngine


class ResumeGenerator:
    def __init__(self, name):
        self.resume = PDFTemplateEngine(name)

    def __getattr__(self, item):
        """
        Delegate attribute or method access to PDFTemplateEngine if not found in ResumeGenerator.
        """
        return getattr(self.resume, item)

    def add_personal_info(self, name: str, contact_info: Dict[str, str]):
        self.resume.add_text(name, style='name', space_after=5.0)
        self.resume.add_horizontal_line()
        for key, value in contact_info.items():
            if key == 'email':
                email = self.resume.create_hyperlink(f"mailto: {value}", value)
                self.resume.add_text(email, style='link', space_after=5.0)
            elif key in ['website', 'linkedin']:
                url = self.resume.create_hyperlink(value, value)
                self.resume.add_text(url, style='link', space_after=5.0)
            else:
                self.add_text(value, space_after=5.0)
        self.resume.add_horizontal_line()

    def add_experience(self,
                       experiences: List[Dict],
                       show_bullet_points: bool = True,
                       add_line_after: bool = True):
        """
        Add work experience section

        :param add_line_after:
        :param experiences: List of work experiences
        :param show_bullet_points: Whether to show detailed bullet points
        """
        from reportlab.platypus import Spacer

        self.resume.elements.append(
            Paragraph("Professional Experience", self.resume.custom_styles['section_header']))

        for exp in experiences:
            # Job Title and Company
            job_title_text = f"{exp['title']} at {exp['company']}"
            self.resume.elements.append(self.resume.add_text(job_title_text, style='subtitle'))

            # Duration and Location
            duration_text = f"{exp['start_date']} - {exp.get('end_date', 'Present')} | {exp.get('location', 'Remote')}"
            self.resume.elements.append(self.resume.add_text(duration_text))

            # Bullet Points or Description
            if show_bullet_points and 'achievements' in exp:
                for achievement in exp['achievements']:
                    self.resume.elements.append(self.resume.add_text(f"• {achievement}"))
            elif 'description' in exp:
                self.resume.elements.append(self.resume.add_text(exp['description']))
        if add_line_after:
            self.resume.add_horizontal_line()

    def add_education(self, education_details: List[Dict], add_line_after: bool = True):

        self.resume.elements.append(
            Paragraph("Education", self.resume.custom_styles['section_header']))

        # self.resume.add_text("Education", style='section_header', space_after=0.2 * inch)

        for edu in education_details:
            # Degree and Institution
            degree_text = f"{edu['degree']} in {edu['field']}"
            self.resume.elements.append(self.resume.add_text(degree_text, style='subtitle'))

            # Institution and Graduation
            inst_text = f"{edu['institution']} | Graduated: {edu.get('graduation_date', 'Present')}"
            self.resume.elements.append(self.resume.add_text(inst_text))

        if add_line_after:
            self.resume.add_horizontal_line()

    def add_skills(self, skills: List[str], columns: int = 3):
        from math import ceil

        self.resume.elements.append(Paragraph("Skills", self.resume.custom_styles['section']))

        # Calculate rows needed
        rows = ceil(len(skills) / columns)

        # Create skill table
        skill_data = []
        for i in range(rows):
            row = skills[i * columns: (i + 1) * columns]
            # Pad row with empty strings if needed
            row += [''] * (columns - len(row))
            skill_data.append(row)

        skill_table = Table(skill_data, colWidths=[2 * inch] * columns)
        skill_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))

        self.resume.elements.append(skill_table)

    def add_skills_bullet(self, skills: List[str], add_line_after: bool = True):
        self.resume.elements.append(
            Paragraph("Skills", self.resume.custom_styles['section_header']))
        for skill in skills:
            self.resume.elements.append(self.add_text(f"• {skill}", space_after=0.1 * inch))

        if add_line_after:
            self.resume.add_horizontal_line()

    def add_summary(self, summary_text: str, add_line_after: bool = True):
        self.resume.elements.append(
            Paragraph("Professional Summary", self.resume.custom_styles['section_header']))
        self.resume.add_text(summary_text)
        if add_line_after:
            self.resume.add_horizontal_line()

    def add_additional_info(self, additional_info: str, add_line_after: bool = True):
        self.resume.elements.append(
            Paragraph("Additional Information", self.resume.custom_styles['section_header']))
        self.resume.add_text(additional_info)

        if add_line_after:
            self.resume.add_horizontal_line()
