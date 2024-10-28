from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import markdown2
from io import StringIO 

def create_pdf(filename, text):
    # Convert Markdown to HTML
    html_text = markdown2.markdown(text)

    # Create a PDF document with a fixed page size
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Use the 'BodyText' style for regular paragraphs
    body_style = styles['BodyText']
    story = []

    # Split the HTML text into lines and add each to the PDF as a Paragraph
    for line in html_text.splitlines():
        if line.strip():  # Skip empty lines
            story.append(Paragraph(line, body_style))
            story.append(Spacer(1, 10))  # Add consistent space between lines

    # Build the PDF
    doc.build(story)

def create_pdf2(filename, text, font_name="Helvetica", font_size=12, margin=100):
    # Define the canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set font and calculate line height
    c.setFont(font_name, font_size)
    line_height = font_size + 2  # Space between lines

    # Calculate maximum text width (page width minus margins)
    max_text_width = width - 2 * margin

    # Split text into lines that fit within the max width
    x, y = margin, height - margin
    for paragraph in text.splitlines():
        # Split paragraph into lines that fit within max_text_width
        words = paragraph.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            # Check if line width exceeds max_text_width
            if c.stringWidth(test_line, font_name, font_size) <= max_text_width:
                line = test_line
            else:
                # Draw current line and start a new one
                c.drawString(x, y, line)
                y -= line_height
                line = word
        # Draw any remaining text in line
        if line:
            c.drawString(x, y, line)
            y -= line_height

    # Save the PDF
    c.save()