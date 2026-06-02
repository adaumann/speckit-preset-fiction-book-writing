#!/usr/bin/env python3
"""create_docx_templates.py — Generate DOCX reference templates for speckit.export.

Creates the Shunn manuscript and Smashwords DOCX templates that are referenced
by export.py but not included in the preset (binary files).

Usage:
    python create_docx_templates.py [--output-dir PATH]

Options:
    --output-dir PATH   Directory to write templates (default: scripts/templates/)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("Error: python-docx is required. Install with: pip install python-docx", file=sys.stderr)
    sys.exit(1)


def create_shunn_template() -> Document:
    """Create Shunn manuscript format DOCX template.
    
    Shunn format specifications:
    - Times New Roman 12pt
    - Double-spaced
    - 1-inch margins
    - Running header (author last name / title / page number)
    - First line indent 0.5 inch
    - No extra spacing between paragraphs
    """
    doc = Document()
    
    # Set default style (Normal)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # Set paragraph formatting
    para_format = style.paragraph_format
    para_format.space_before = Pt(0)
    para_format.space_after = Pt(0)
    para_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    para_format.first_line_indent = Inches(0.5)
    
    # Set margins (1 inch)
    for section in doc.sections:
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
    
    # Create Heading 1 style (Chapter headings)
    heading1 = doc.styles['Heading 1']
    heading1_font = heading1.font
    heading1_font.name = 'Times New Roman'
    heading1_font.size = Pt(12)
    heading1_font.bold = True
    heading1_para = heading1.paragraph_format
    heading1_para.space_before = Pt(24)
    heading1_para.space_after = Pt(12)
    heading1_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Create Heading 2 style (Scene headings)
    heading2 = doc.styles['Heading 2']
    heading2_font = heading2.font
    heading2_font.name = 'Times New Roman'
    heading2_font.size = Pt(12)
    heading2_font.bold = True
    heading2_para = heading2.paragraph_format
    heading2_para.space_before = Pt(12)
    heading2_para.space_after = Pt(6)
    
    # Add a sample paragraph to establish the style
    doc.add_paragraph("Sample text for Shunn manuscript format. Times New Roman 12pt, double-spaced, with first line indent.")
    
    return doc


def create_smashwords_template() -> Document:
    """Create Smashwords minimal DOCX template.
    
    Smashwords format specifications:
    - Minimal styles (Normal, Heading 1, Heading 2 only)
    - No tabs
    - No manual line breaks
    - Simple formatting for their auto-converter
    """
    doc = Document()
    
    # Set default style (Normal) - simple, no special formatting
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    para_format = style.paragraph_format
    para_format.space_before = Pt(0)
    para_format.space_after = Pt(0)
    para_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    
    # Set margins
    for section in doc.sections:
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
    
    # Heading 1 - chapter titles
    heading1 = doc.styles['Heading 1']
    heading1_font = heading1.font
    heading1_font.name = 'Times New Roman'
    heading1_font.size = Pt(14)
    heading1_font.bold = True
    heading1_para = heading1.paragraph_format
    heading1_para.space_before = Pt(18)
    heading1_para.space_after = Pt(12)
    heading1_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Heading 2 - scene titles
    heading2 = doc.styles['Heading 2']
    heading2_font = heading2.font
    heading2_font.name = 'Times New Roman'
    heading2_font.size = Pt(12)
    heading2_font.bold = True
    heading2_para = heading2.paragraph_format
    heading2_para.space_before = Pt(12)
    heading2_para.space_after = Pt(6)
    
    # Add sample paragraph
    doc.add_paragraph("Sample text for Smashwords format. Minimal styles for their auto-converter.")
    
    return doc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate DOCX reference templates for speckit.export",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory to write templates (default: scripts/templates/)",
    )
    args = parser.parse_args()
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        # Default: scripts/templates/ relative to this script
        output_dir = Path(__file__).resolve().parent.parent / "templates"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create Shunn template
    shunn_path = output_dir / "docx-shunn.docx"
    shunn_doc = create_shunn_template()
    shunn_doc.save(shunn_path)
    print(f"Created: {shunn_path}")
    
    # Create Smashwords template
    smashwords_path = output_dir / "docx-smashwords.docx"
    smashwords_doc = create_smashwords_template()
    smashwords_doc.save(smashwords_path)
    print(f"Created: {smashwords_path}")
    
    print("\nDone. Templates are ready for use with speckit.export docx --platform shunn/smashwords")


if __name__ == "__main__":
    main()