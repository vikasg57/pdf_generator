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

    def load_styles_from_config(self, config_path: str):
        """
        Load styles from a JSON configuration file.
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

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

        self.custom_styles['section'].fontName = font_styles.get("section_header", "Helvetica-Bold")
        self.custom_styles['section'].fontSize = font_sizes.get("section_header", 14)

        # Update default Normal style
        self.styles['Normal'].fontName = font_styles.get("normal", "Helvetica")
        self.styles['Normal'].fontSize = font_sizes.get("normal", 12)

        self.custom_styles['subtitle'].fontName = font_styles.get("subtitle", "Helvetica")
        self.custom_styles['subtitle'].fontSize = font_sizes.get("subtitle", 12)

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

    def create_hyperlink(self, url: str, text: str = None):
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
