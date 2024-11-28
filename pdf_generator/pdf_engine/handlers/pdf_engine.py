import io
from typing import List, Dict, Union
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image,
    PageBreak
)
from reportlab.graphics.shapes import Drawing
from PIL import Image as PILImage


class PDFTemplateEngine:
    def __init__(self,
                 filename: str = 'output.pdf',
                 pagesize=letter,
                 margins: tuple = (0.5 *inch, 0.5 *inch, 0.5 *inch, 0.5 *inch)):
        """
        Initialize PDF template engine with advanced configuration

        :param filename: Output PDF filename
        :param pagesize: PDF page size (default: letter)
        :param margins: Page margins (left, top, right, bottom)
        """
        self.filename = filename
        self.pagesize = pagesize
        self.margins = margins

        # Prepare document template
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=pagesize,
            leftMargin=margins[0],
            topMargin=margins[1],
            rightMargin=margins[2],
            bottomMargin=margins[3]
        )

        # Styles
        self.styles = getSampleStyleSheet()
        self.custom_styles = {}

        # Content elements to be added to PDF
        self.elements = []

        self._create_custom_styles()

    def _create_custom_styles(self):
        """
        Create and register custom paragraph styles

        :param name: Name of the style
        :param base_style: Base style to modify
        :param kwargs: Style parameters to override
        :return: Created style
        """
        # base = self.styles[base_style]
        # custom_style = ParagraphStyle(
        #     name,
        #     parent=base,
        #     **kwargs
        # )
        # self.custom_styles[name] = custom_style

        name_style = ParagraphStyle(
            'NameStyle',
            parent=self.styles['Title'],
            fontSize=18,
            textColor=colors.darkblue,
            spaceAfter=6,
            alignment=1  # Center alignment
        )
        self.custom_styles['name'] = name_style

        # Contact Style
        contact_style = ParagraphStyle(
            'ContactStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.darkgray,
            alignment=0  # Center alignment
        )
        self.custom_styles['contact'] = contact_style

        # Section Header Style
        section_style = ParagraphStyle(
            'SectionStyle',
            parent=self.styles['Heading3'],
            textColor=colors.darkblue,
            borderBottomWidth=1,
            borderBottomColor=colors.darkblue,
            spaceAfter=6
        )
        self.custom_styles['section'] = section_style

        # Job Title Style
        job_title_style = ParagraphStyle(
            'JobTitleStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.darkgreen,
            spaceAfter=3
        )
        self.custom_styles['job_title'] = job_title_style

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=24,
            leading=28,  # Line height
            textColor=colors.darkblue,
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        self.custom_styles['title'] = title_style

        # Subtitle Style
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=self.styles['Heading2'],
            fontSize=18,
            textColor=colors.darkgreen,
            spaceAfter=10,
            alignment=0  # Left alignment
        )
        self.custom_styles['subtitle'] = subtitle_style

        # Section Header Style
        section_header_style = ParagraphStyle(
            'SectionHeaderStyle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.navy,
            underline=True,
            spaceAfter=6
        )
        self.custom_styles['section_header'] = section_header_style

        # Subtext Style (Generic Gray Text)
        sub_text_gray_style = ParagraphStyle(
            'SubTextGray',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.gray,
            leading=12,
            spaceAfter=4
        )
        self.custom_styles['sub_text_gray'] = sub_text_gray_style

        # Highlighted Text Style
        highlighted_text_style = ParagraphStyle(
            'HighlightedText',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.red,
            backColor=colors.yellow,
            spaceAfter=6
        )
        self.custom_styles['highlighted_text'] = highlighted_text_style

        # Bullet List Item Style
        bullet_list_style = ParagraphStyle(
            'BulletList',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            leftIndent=20,  # Indent for bullets
            spaceBefore=2,
            spaceAfter=2
        )
        self.custom_styles['bullet_list'] = bullet_list_style

        # Centered Text Style
        centered_text_style = ParagraphStyle(
            'CenteredText',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            alignment=1  # Center alignment
        )
        self.custom_styles['centered_text'] = centered_text_style

        # Justified Text Style
        justified_text_style = ParagraphStyle(
            'JustifiedText',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.black,
            alignment=4  # Justified alignment
        )
        self.custom_styles['justified_text'] = justified_text_style

        # Small Caps Style
        small_caps_style = ParagraphStyle(
            'SmallCaps',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            spaceAfter=4,
            textTransform='uppercase'
        )
        self.custom_styles['small_caps'] = small_caps_style

    def update_styles(self, title_color=None, section_color=None):
        if title_color:
            self.custom_styles['name'].textColor = title_color

        if section_color:
            self.custom_styles['section_header'].textColor = section_color
            self.custom_styles['section_header'].borderBottomColor = section_color

    def add_text(self,
                 text: str,
                 style: str = 'Normal',
                 space_after: float = 0.2 *inch):
        """
        Add formatted text paragraph

        :param text: Text content
        :param style: Text style (built-in or custom)
        :param space_after: Space after text
        """
        # Use custom style if exists, otherwise use built-in
        text_style = (
                self.custom_styles.get(style) or
                self.styles.get(style, self.styles['Normal'])
        )
        para = Paragraph(text, text_style)
        self.elements.append(para)

        # Add optional spacing
        if space_after:
            self.elements.append(Spacer(1, space_after))

    def add_image(self,
                  image_path: str,
                  width: float = None,
                  height: float = None,
                  maintain_ratio: bool = True,
                  horizontal_alignment: str = 'CENTER'):
        """
        Add image with advanced sizing and alignment options

        :param image_path: Path to image file
        :param width: Desired width
        :param height: Desired height
        :param maintain_ratio: Maintain aspect ratio
        :param horizontal_alignment: Image alignment
        """
        # Open image to get original dimensions
        img = PILImage.open(image_path)
        original_width, original_height = img.size

        # Calculate dimensions
        if width and height:
            final_width, final_height = width, height
        elif width:
            final_width = width
            final_height = original_height * (width / original_width) if maintain_ratio else width
        elif height:
            final_height = height
            final_width = original_width * (height / original_height) if maintain_ratio else height
        else:
            final_width, final_height = original_width, original_height

        # Create ReportLab image with alignment
        img = Image(image_path, width=final_width, height=final_height)
        img.hAlign = horizontal_alignment

        self.elements.append(img)

    def _create_hyperlink(self, url: str, text: str = None):
        """
        Create a hyperlink paragraph

        :param url: URL to link
        :param text: Optional display text
        :return: Paragraph with hyperlink
        """
        from reportlab.platypus import Paragraph

        text = text or url
        link_style = ParagraphStyle(
            'LinkStyle',
            parent=self.styles['Normal'],
            textColor=colors.blue,
            underline=True
        )
        return Paragraph(f'<link href="{url}">{text}</link>', link_style)

    def add_personal_info(self, name: str, contact_info: Dict[str, str]):
        """
        Add personal information section

        :param name: Full name
        :param contact_info: Dict with contact details
        """
        # Add Name
        self.elements.append(Paragraph(name, self.custom_styles['name']))

        # Add Contact Information
        contact_lines = []
        for key, value in contact_info.items():
            if key == 'email':
                contact_lines.append(self._create_hyperlink(f"mailto:{value}", value))
            elif key in ['website', 'linkedin']:
                contact_lines.append(self._create_hyperlink(value))
            else:
                contact_lines.append(Paragraph(value, self.custom_styles['contact']))

        # Append each contact line as a separate element
        for contact_line in contact_lines:
            self.elements.append(contact_line)

        # Optionally, add some spacing after contact info
        self.elements.append(Spacer(1, 0.2 * inch))

    def add_summary(self, summary_text: str):
        """
        Add professional summary

        :param summary_text: Professional summary paragraph
        """
        self.elements.append(Paragraph("Professional Summary", self.custom_styles['section']))
        self.elements.append(Paragraph(summary_text, self.styles['Normal']))

    def add_experience(self,
                       experiences: List[Dict],
                       show_bullet_points: bool = True):
        """
        Add work experience section

        :param experiences: List of work experiences
        :param show_bullet_points: Whether to show detailed bullet points
        """
        from reportlab.platypus import Spacer

        # self.elements.append(Paragraph("Professional Experience", self.custom_styles['section']))

        for exp in experiences:
            # Job Title and Company
            job_title_text = f"{exp['title']} at {exp['company']}"
            self.elements.append(Paragraph(job_title_text, self.custom_styles['job_title']))

            # Duration and Location
            duration_text = f"{exp['start_date']} - {exp.get('end_date', 'Present')} | {exp.get('location', 'Remote')}"
            self.elements.append(Paragraph(duration_text, self.styles['Normal']))

            # Bullet Points or Description
            if show_bullet_points and 'achievements' in exp:
                for achievement in exp['achievements']:
                    self.elements.append(Paragraph(f"• {achievement}", self.styles['Normal']))
            elif 'description' in exp:
                self.elements.append(Paragraph(exp['description'], self.styles['Normal']))

            # Add spacing between experiences
            self.elements.append(Spacer(1, 0.2 * inch))

    def add_education(self, education_details: List[Dict]):

        for edu in education_details:
            # Degree and Institution
            degree_text = f"{edu['degree']} in {edu['field']}"
            self.elements.append(Paragraph(degree_text, self.custom_styles['job_title']))

            # Institution and Graduation
            inst_text = f"{edu['institution']} | Graduated: {edu.get('graduation_date', 'Present')}"
            self.elements.append(Paragraph(inst_text, self.styles['Normal']))

    def add_skills(self, skills: List[str], columns: int = 3):
        """
        Add skills section with multi-column layout

        :param skills: List of skills
        :param columns: Number of columns to display skills
        """
        from math import ceil

        self.elements.append(Paragraph("Skills", self.custom_styles['section']))

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

        self.elements.append(skill_table)

    def add_skills_bullet(self, skills: List[str]):
        """
        Add skills section with a bullet list layout.

        :param skills: List of skills
        """
        # Add the section title

        # Add each skill as a bullet point
        for skill in skills:
            self.elements.append(Paragraph(f"• {skill}", self.styles['Bullet']))

        # Add spacing after the section
        self.elements.append(Spacer(1, 0.2 * inch))

    def add_table(self,
                  data: List[List[str]],
                  col_widths: List[float] = None,
                  style_config: Dict = None):
        """
        Create and add table with advanced styling

        :param data: 2D list of table data
        :param col_widths: Optional column widths
        :param style_config: Custom table styling
        """
        # Create table
        table = Table(data, colWidths=col_widths)

        # Default style if not provided
        default_style = [
            ('BACKGROUND', (0 ,0), (-1 ,0), colors.grey),
            ('TEXTCOLOR', (0 ,0), (-1 ,0), colors.whitesmoke),
            ('ALIGN', (0 ,0), (-1 ,-1), 'CENTER'),
            ('FONTNAME', (0 ,0), (-1 ,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0 ,0), (-1 ,0), 12),
            ('BOTTOMPADDING', (0 ,0), (-1 ,0), 12),
            ('BACKGROUND', (0 ,1), (-1 ,-1), colors.beige),
            ('GRID', (0 ,0), (-1 ,-1), 1, colors.black)
        ]

        # Apply custom or default style
        table_style = TableStyle(style_config or default_style)
        table.setStyle(table_style)

        self.elements.append(table)

    def add_page_break(self):
        """
        Add a page break to the document
        """
        self.elements.append(PageBreak())

    def generate(self):
        """
        Generate the final PDF document

        :return: Path to the generated PDF
        """
        # Build PDF
        self.doc.build(self.elements)

        return self.filename

# Example Usage Demonstrations


def quote_generator_example():
    # Create PDF engine
    pdf = PDFTemplateEngine('quote.pdf')

    # Add quote details
    pdf.add_text("Business Quote", style='Title')

    # Quote details table
    quote_data = [
        ['Item', 'Description', 'Quantity', 'Unit Price', 'Total'],
        ['Web Design', 'Professional Website', 1, '$1000', '$1000'],
        ['SEO', 'Search Optimization', 1, '$500', '$500']
    ]
    pdf.add_table(quote_data)

    # Total section
    pdf.add_text("Total: $1500", style='Heading3')

    # Generate PDF
    pdf.generate()


# Demonstration of how to use the engine
if __name__ == "__main__":
    # Create a sample PDF with custom margins and A4 size
    pdf = PDFTemplateEngine(
        'sample.pdf',
        pagesize=A4,
        margins=( 1 *inch, 1* inch, 1 * inch, 1 * inch)
    )

    # Demonstrate capabilities
    pdf.add_text("PDF Generation Demo", style='Title')

    # Add a table
    sample_data = [
        ['Name', 'Age', 'City'],
        ['John Doe', '30', 'New York'],
        ['Jane Smith', '25', 'San Francisco']
    ]
    pdf.add_table(sample_data)

    # Add page break
    pdf.add_page_break()

    # Add another section
    pdf.add_text("Additional Content", style='Heading2')

    # Generate the PDF
    pdf.generate()


def create_sample_resume():
    # Create Resume Generator
    resume = PDFTemplateEngine('john_doe_resume.pdf')

    # Personal Information
    resume.add_personal_info(
        name="John Doe",
        contact_info={
            'email': 'john.doe@example.com',
            'phone': '+1 (123) 456-7890',
            'linkedin': 'https://linkedin.com/in/johndoe',
            'website': 'https://johndoe.com'
        }
    )

    # Professional Summary
    resume.add_summary(
        "Innovative software engineer with 5+ years of experience "
        "in developing scalable web applications and microservices."
    )

    # Professional Experience
    resume.add_experience([
        {
            'title': 'Senior Software Engineer',
            'company': 'TechCorp Inc.',
            'start_date': 'Jan 2020',
            'end_date': 'Present',
            'location': 'San Francisco, CA',
            'achievements': [
                'Led development of microservices architecture',
                'Reduced system latency by 40% through optimization',
                'Mentored junior developers in agile methodologies'
            ]
        },
        {
            'title': 'Software Engineer',
            'company': 'StartUp Solutions',
            'start_date': 'Jun 2017',
            'end_date': 'Dec 2019',
            'location': 'New York, NY',
            'description': 'Developed and maintained full-stack web applications'
        }
    ])

    # Education
    resume.add_education([
        {
            'degree': 'Master of Science',
            'field': 'Computer Science',
            'institution': 'Stanford University',
            'graduation_date': '2017'
        }
    ])

    # Skills
    resume.add_skills([
        'Python', 'Django', 'React', 'Docker', 'Kubernetes',
        'AWS', 'Machine Learning', 'CI/CD', 'Microservices'
    ])

    # Generate Resume
    resume.generate()

def create_sample_resume_2():
    """
    Generates a sample resume for John Doe using the PDFTemplateEngine.
    """
    # Initialize the PDF generator with a filename
    resume = PDFTemplateEngine('john_doe_resume.pdf')

    resume.update_styles(
        title_color=colors.green,  # Custom title color
        section_color=colors.red   # Custom section color
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

    # Add a Professional Summary
    resume.add_text(
        "Professional Summary",
        style='section_header',
        space_after=0.2 * inch
    )
    resume.add_text(
        "Innovative software engineer with 5+ years of experience "
        "in developing scalable web applications and microservices. "
        "Proven track record of leading projects and optimizing system performance.",
        style='justified_text'
    )

    # Add Professional Experience
    resume.add_text("Professional Experience", style='section_header', space_after=0.2 * inch)
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
    resume.add_text("Education", style='section_header', space_after=0.2 * inch)
    resume.add_education([
        {
            'degree': 'Master of Science',
            'field': 'Computer Science',
            'institution': 'Stanford University',
            'graduation_date': '2017'
        }
    ])

    # Add Skills
    resume.add_text("Skills", style='section_header', space_after=0.2 * inch)

    resume.add_skills_bullet(
        [
            'Python', 'Django', 'React', 'Docker', 'Kubernetes',
            'AWS', 'Machine Learning', 'CI/CD', 'Microservices'
        ]
    )
    # resume.add_skills([
    #     'Python', 'Django', 'React', 'Docker', 'Kubernetes',
    #     'AWS', 'Machine Learning', 'CI/CD', 'Microservices'
    # ])

    # Add a Page Break and Additional Section
    resume.add_page_break()
    resume.add_text("Additional Information", style='section_header', space_after=0.2 * inch)
    resume.add_text(
        "Available for remote opportunities and willing to relocate. "
        "Passionate about mentoring and open-source contributions.",
        style='justified_text'
    )

    # Generate the final PDF
    resume.generate()
    print("Resume generated successfully as 'john_doe_resume.pdf'")
