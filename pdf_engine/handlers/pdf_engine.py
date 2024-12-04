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
    PageBreak,
    Frame,
    FrameBreak,
    PageTemplate
)
from reportlab.graphics.shapes import Drawing, Line
from PIL import Image as PILImage
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


class PDFTemplateEngine:
    def __init__(self,
                 filename: str = 'output.pdf',
                 pagesize=letter,
                 margins: tuple = (0.5 *inch, 0.5 *inch, 0.5 *inch, 0.5 *inch),
                 column_layout: bool = False):
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
        self.column_layout = column_layout

        # Existing initialization code...

        if column_layout:
            self._setup_two_column_template()

        # Styles
        self.styles = getSampleStyleSheet()
        self.custom_styles = {}

        # Content elements to be added to PDF
        self.elements = []

        self._create_custom_styles()

    def _setup_two_column_template(self):
        """
        Set up a two-column page layout
        """
        # Calculate column width and gutter
        page_width = self.pagesize[0]
        page_height = self.pagesize[1]

        # Define margins
        left_margin, top_margin, right_margin, bottom_margin = self.margins

        # Calculate column dimensions
        column_width = (page_width - left_margin - right_margin - 0.5 * inch) / 2
        gutter_width = 0.5 * inch

        # Create frames for two columns
        left_frame = Frame(
            left_margin,
            bottom_margin,
            column_width,
            page_height - top_margin - bottom_margin,
            id='left_column'
        )

        right_frame = Frame(
            left_margin + column_width + gutter_width,
            bottom_margin,
            column_width,
            page_height - top_margin - bottom_margin,
            id='right_column'
        )

        # Create page template with two columns
        two_column_template = PageTemplate(
            id='TwoColumnTemplate',
            frames=[left_frame, right_frame]
        )

        # Replace default template with two-column template
        self.doc.pageTemplates = [two_column_template]

    def switch_column(self):
        """
        Add a frame break to switch to the next column
        """
        if self.column_layout:
            self.elements.append(FrameBreak())

    def add_section_to_column(self, section_elements: list, column: int = 0):
        """
        Add a section to a specific column

        :param section_elements: List of elements to add
        :param column: 0 for left, 1 for right column
        """
        if not self.column_layout:
            raise ValueError("Column layout is not enabled")

        # Add section elements
        self.elements.extend(section_elements)

        # If not in the last column, add frame break
        if column == 0:
            self.switch_column()

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

        right_text_style = ParagraphStyle(
            'RightText',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.black,
            alignment=2  # right alignment
        )
        self.custom_styles['right_text'] = right_text_style

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

    from reportlab.platypus import PageBreak

    def add_text(self,
                 text: str,
                 style: str = 'Normal',
                 space_after: float = 0.1 * inch):
        """
        Add formatted text paragraph with space management.

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
        Add a horizontal line to the document, respecting column layout.

        :param line_color: Color of the horizontal line (hex or named color).
        :param line_thickness: Thickness of the horizontal line.
        :param line_width: Width of the line; defaults to column width.
        :param space_after: Space after the horizontal line.
        """
        if self.column_layout:
            # For two-column layout, use column width
            # Assumes symmetric column layout
            page_width = self.pagesize[0]
            left_margin, _, right_margin, _ = self.margins
            column_width = (page_width - left_margin - right_margin - 0.5 * inch) / 2
            line_width = line_width or column_width
        else:
            # For single column, use full document width
            line_width = line_width or self.doc.width

        drawing = Drawing(line_width, line_thickness)
        line = Line(0, 0, line_width, 0)  # Start at (0,0), end at (line_width,0)
        line.strokeColor = HexColor(line_color)
        line.strokeWidth = line_thickness
        drawing.add(line)
        self.elements.append(drawing)

        # Add optional spacing
        if space_after:
            self.elements.append(Spacer(line_width, space_after))

    def generate(self):
        """
        Generate the final PDF document

        :return: Path to the generated PDF
        """
        # Build PDF
        self.doc.build(self.elements)

        return self.filename
