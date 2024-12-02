import io
import json
from reportlab.lib.colors import HexColor
from typing import List, Dict
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
from reportlab.graphics.shapes import Drawing, Line
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


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

        # job_title_style = ParagraphStyle(
        #     'JobTitleStyle',
        #     parent=self.styles['Normal'],
        #     fontSize=12,
        #     textColor=colors.darkgreen,
        #     spaceAfter=3
        # )
        # self.custom_styles['job_title'] = job_title_style

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
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.darkgreen,
            spaceAfter=3
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

        link_style = ParagraphStyle(
            'LinkStyle',
            parent=self.styles['Normal'],
            textColor=colors.blue,
            underline=True
        )
        self.custom_styles['link'] = link_style

    def load_styles_from_config(self, json_style):
        """
        Load styles from a JSON configuration file.
        """
        config = json_style

        # Parse colors
        title_color = HexColor(config.get("title_color", "#000000"))
        section_color = HexColor(config.get("section_color", "#000000"))

        # Parse font sizes and styles
        font_sizes = config.get("font_sizes", {})
        font_styles = config.get("font_styles", {})

        self.custom_styles['name'].textColor = title_color

        self.custom_styles['section_header'].textColor = section_color
        self.custom_styles['section_header'].borderBottomColor = section_color

        # Update other properties in custom styles
        self.custom_styles['name'].fontName = font_styles.get("title", "Helvetica-Bold")
        self.custom_styles['name'].fontSize = font_sizes.get("title", 18)

        self.custom_styles['section_header'].fontName = font_styles.get("section_header", "Helvetica-Bold")
        self.custom_styles['section_header'].fontSize = font_sizes.get("section_header", 14)

        # Update default Normal style
        self.styles['Normal'].fontName = font_styles.get("normal", "Helvetica")
        self.styles['Normal'].fontSize = font_sizes.get("normal", 12)

        self.custom_styles['subtitle'].fontName = font_styles.get("subtitle", "Helvetica")
        self.custom_styles['subtitle'].fontSize = font_sizes.get("subtitle", 12)

    def add_text(self,
                 text: str,
                 style: str = 'Normal',
                 space_after: float = 0.1 *inch):
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
            spacer = Spacer(0, space_after)
            self.elements.append(spacer)

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

    def create_hyperlink(self, url: str, text: str = None):
        text = text or url
        return f'<link href="{url}">{text}</link>'

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

    def add_horizontal_line(self,
                            line_color="#000000",
                            line_thickness=1,
                            line_width=None,
                            space_after: float = 0.2 * inch):
        """
        Add a horizontal line to the document.

        :param line_color: Color of the horizontal line (hex or named color).
        :param line_thickness: Thickness of the horizontal line.
        :param line_width: Width of the line; defaults to document width.
        :param space_after: Space after the horizontal line.
        """
        line_width = line_width or self.doc.width  # Default to full document width
        drawing = Drawing(line_width, line_thickness)
        line = Line(0, 0, line_width, 0)  # Start at (0,0), end at (line_width,0)
        line.strokeColor = HexColor(line_color)
        line.strokeWidth = line_thickness
        drawing.add(line)
        self.elements.append(drawing)
        # Add spacing after the line

    def generate(self):
        """
        Generate the final PDF document

        :return: Path to the generated PDF
        """
        # Build PDF
        self.doc.build(self.elements)

        return self.filename


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class TwoColumnResume:
    def __init__(self, filename='resume.pdf'):
        self.filename = filename
        self.page_width, self.page_height = letter
        self.margin = 0.5 * inch
        self.column_gap = 0.2 * inch
        self.column_width = (self.page_width - 2 * self.margin - self.column_gap) / 2
        self.current_y_left = self.page_height - self.margin  # Y-position for the left column
        self.current_y_right = self.page_height - self.margin  # Y-position for the right column
        self.column = 0  # Start with the left column
        self.canvas = canvas.Canvas(self.filename, pagesize=letter)

    def _get_column_x(self):
        """Calculate the starting X coordinate for the current column."""
        return self.margin + self.column * (self.column_width + self.column_gap)

    def _next_position(self, height):
        """Determine the next position, switching column or page if needed."""
        if self.column == 0:  # Left column
            if self.current_y_left - height < self.margin:
                self.column = 1  # Switch to the second column
                self.current_y_left = self.page_height - self.margin  # Reset left column Y-position
                if self.column > 1:  # Move to the next page if both columns are full
                    self.canvas.showPage()
                    self.column = 0  # Start over with the first column
                    self.current_y_left = self.page_height - self.margin
                    self.current_y_right = self.page_height - self.margin
        else:  # Right column
            if self.current_y_right - height < self.margin:
                self.column = 0  # Switch back to the first column
                self.current_y_right = self.page_height - self.margin  # Reset right column Y-position
                if self.column == 0:  # If switching back to left, move to the next page
                    self.canvas.showPage()

    def add_text(self, text, font='Helvetica', size=10, line_height=12, space_after=2):
        """Add text to the current column, handling word wrapping and column flow, with optional space after."""
        self.canvas.setFont(font, size)
        words = text.split(' ')
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            if self.canvas.stringWidth(test_line, font, size) > self.column_width:
                # Render the current line and reset it
                self._render_line(line, line_height)
                line = word
            else:
                line = test_line

        # Render the last line
        if line:
            self._render_line(line, line_height)

        # Add optional space after text
        self.current_y_left -= space_after if self.column == 0 else 0
        self.current_y_right -= space_after if self.column == 1 else 0

    def _render_line(self, line, line_height):
        """Render a single line of text, flowing between columns/pages as needed."""
        self._next_position(line_height)
        x = self._get_column_x()
        y = self.current_y_left if self.column == 0 else self.current_y_right  # Set Y for left or right column
        self.canvas.drawString(x, y - line_height, line)
        if self.column == 0:
            self.current_y_left -= line_height
        else:
            self.current_y_right -= line_height

    def draw_line(self, thickness=1):
        """Draw a horizontal line across the current column width."""
        x1 = self._get_column_x()
        x2 = x1 + self.column_width
        y = self.current_y_left if self.column == 0 else self.current_y_right
        self.canvas.setLineWidth(thickness)
        self.canvas.line(x1, y, x2, y)
        if self.column == 0:
            self.current_y_left -= thickness + 5  # Adjust spacing for the left column
        else:
            self.current_y_right -= thickness + 5  # Adjust spacing for the right column

    def add_section(self, title, content, space_after=2):
        """Add a section with a title and flowing content in the current column."""
        self.add_text(title, font='Helvetica-Bold', size=12, line_height=14)
        self.draw_line(thickness=0.5)
        self.add_text(content, font='Helvetica', size=10, line_height=12, space_after=space_after)

    def add_section_in_column(self, title, content, column=1, space_after=2):
        """Add a section with a title and flowing content to the specified column."""
        if column not in [1, 2]:
            raise ValueError("Column must be 1 or 2.")

        # Switch to the correct column
        self.column = column - 1  # Column is 1 or 2, but column index is 0 or 1
        self.add_section(title, content, space_after=space_after)

    def add_paragraph(self, text, style='Normal', space_after=10):
        """Add styled paragraph text."""
        styles = getSampleStyleSheet()
        style_obj = styles[style]
        p = Paragraph(text, style_obj)
        p_width, p_height = p.wrap(self.column_width, self.page_height)

        # Adjust Y position before adding paragraph
        self._next_position(p_height)
        if self.column == 0:
            y_pos = self.current_y_left
            self.current_y_left -= p_height + space_after
        else:
            y_pos = self.current_y_right
            self.current_y_right -= p_height + space_after

        # Draw the paragraph
        self.canvas.saveState()
        p.drawOn(self.canvas, self._get_column_x(), y_pos)
        self.canvas.restoreState()

    def generate(self):
        """Save the final PDF."""
        self.canvas.save()


# Example usage
# resume = TwoColumnResume()
#
# # Add sections explicitly to columns
# resume.add_section_in_column("Personal Info", "John Doe\nEmail: john.doe@example.com", column=1)
# resume.add_section_in_column("Education", "MSc in Computer Science, Stanford University", column=2)
# resume.add_section_in_column("Skills", "Python, Django, React, Flask", column=1)
# resume.add_section_in_column("Experience", "Senior Software Engineer at TechCorp", column=2)
# resume.add_section_in_column("Personal Info", "John Doe\nEmail: john.doe@example.com", column=1)
# resume.add_section_in_column("Education", "MSc in Computer Science, Stanford University", column=2)
# resume.add_section_in_column("Skills", "Python, Django, React, Flask", column=1)
# resume.add_section_in_column("Experience", "Senior Software Engineer at TechCorp", column=2)
# resume.add_section_in_column("Personal Info", "John Doe\nEmail: john.doe@example.com", column=1)
# resume.add_section_in_column("Education", "MSc in Computer Science, Stanford University", column=2)
# resume.add_section_in_column("Skills", "Python, Django, React, Flask", column=1)
# resume.add_section_in_column("Experience", "Senior Software Engineer at TechCorp", column=2)
# resume.add_section_in_column("Personal Info", "John Doe\nEmail: john.doe@example.com", column=1)
# resume.add_section_in_column("Education", "MSc in Computer Science, Stanford University", column=2)
# resume.add_section_in_column("Skills", "Python, Django, React, Flask", column=1)
# resume.add_section_in_column("Experience", "Senior Software Engineer at TechCorp", column=2)
# resume.add_section_in_column("Personal Info", "John Doe\nEmail: john.doe@example.com", column=1)
# resume.add_section_in_column("Education", "MSc in Computer Science, Stanford University", column=2)
# resume.add_section_in_column("Skills", "Python, Django, React, Flask", column=1)
# resume.add_section_in_column("Experience", "Senior Software Engineer at TechCorp", column=2)
#
#
# resume.generate()
# print("Resume saved as 'resume.pdf'")
