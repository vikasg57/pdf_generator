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
        self.resume.elements.append(Paragraph(name, self.resume.custom_styles['name']))

        contact_lines = []
        for key, value in contact_info.items():
            if key == 'email':
                contact_lines.append(self.resume.create_hyperlink(f"mailto:{value}", value))
            elif key in ['website', 'linkedin']:
                contact_lines.append(self.resume.create_hyperlink(value))
            else:
                contact_lines.append(Paragraph(value, self.resume.custom_styles['contact']))

        for contact_line in contact_lines:
            self.resume.elements.append(contact_line)

        self.resume.elements.append(Spacer(1, 0.2 * inch))

    def add_experience(self,
                       experiences: List[Dict],
                       show_bullet_points: bool = True):
        """
        Add work experience section

        :param experiences: List of work experiences
        :param show_bullet_points: Whether to show detailed bullet points
        """
        from reportlab.platypus import Spacer

        self.resume.elements.append(
            Paragraph("Professional Experience", self.resume.custom_styles['section_header']))

        for exp in experiences:
            # Job Title and Company
            job_title_text = f"{exp['title']} at {exp['company']}"
            self.resume.elements.append(Paragraph(job_title_text, self.resume.custom_styles['subtitle']))

            # Duration and Location
            duration_text = f"{exp['start_date']} - {exp.get('end_date', 'Present')} | {exp.get('location', 'Remote')}"
            self.resume.elements.append(Paragraph(duration_text, self.resume.styles['Normal']))

            # Bullet Points or Description
            if show_bullet_points and 'achievements' in exp:
                for achievement in exp['achievements']:
                    self.resume.elements.append(Paragraph(f"• {achievement}", self.resume.styles['Normal']))
            elif 'description' in exp:
                self.resume.elements.append(Paragraph(exp['description'], self.resume.styles['Normal']))

            # Add spacing between experiences
            self.resume.elements.append(Spacer(1, 0.2 * inch))

    def add_education(self, education_details: List[Dict]):

        self.resume.elements.append(
            Paragraph("Education", self.resume.custom_styles['section_header']))

        # self.resume.add_text("Education", style='section_header', space_after=0.2 * inch)

        for edu in education_details:
            # Degree and Institution
            degree_text = f"{edu['degree']} in {edu['field']}"
            self.resume.elements.append(Paragraph(degree_text, self.resume.custom_styles['subtitle']))

            # Institution and Graduation
            inst_text = f"{edu['institution']} | Graduated: {edu.get('graduation_date', 'Present')}"
            self.resume.elements.append(Paragraph(inst_text, self.resume.styles['Normal']))

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

    def add_skills_bullet(self, skills: List[str]):
        self.resume.elements.append(
            Paragraph("Skills", self.resume.custom_styles['section_header']))
        for skill in skills:
            self.resume.elements.append(Paragraph(f"• {skill}", self.resume.styles['Bullet']))

        # Add spacing after the section
        self.resume.elements.append(Spacer(1, 0.2 * inch))

    def add_summary(self, summary_text: str):
        self.resume.elements.append(
            Paragraph("Professional Summary", self.resume.custom_styles['section_header']))
        self.resume.elements.append(
            Paragraph(summary_text, self.resume.styles['Normal']))

    def add_additional_info(self, additional_info: str):
        self.resume.elements.append(
            Paragraph("Additional Information", self.resume.custom_styles['section_header']))
        self.resume.add_text(
            additional_info,
            style='justified_text'
        )
