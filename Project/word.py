from docx import Document
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


class WordFile():
	def __init__(self, presentation, abstract, identification):
		super(WordFile, self).__init__()
		self.presentation = presentation
		self.abstract = abstract
		self.identification = identification

		self.document = Document()

		self.define_style()
		self.add_presentation()
		self.add_abstract()
		self.add_identification()

	def define_style(self):
		style = self.document.styles['Normal']
		font = style.font
		font.name = 'Arial'
		font.size = Pt(12)

	def add_presentation(self):
		self.document.add_heading(self.presentation[0], 1) # Add the name as a title

		for item in self.presentation[1:]: # Add the other items
			paragraph = self.document.add_paragraph(item)
			# Format paragraph
			paragraph_format = paragraph.paragraph_format
			paragraph_format.space_before = Pt(4)
			paragraph_format.space_after = Pt(4)

	def add_abstract(self):
		self.document.add_heading("Resumo", 1) # Add "Resumo" as a title
		
		self.abstract = self.abstract[0].upper() + self.abstract[1:] # First letter uppercased
		paragraph = self.document.add_paragraph(self.abstract)

		# Format paragraph
		paragraph_format = paragraph.paragraph_format
		paragraph_format.line_spacing = Pt(15)
	
		paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

	def add_identification(self):
		self.document.add_heading("Identificação", 1) # Add "Identificação" as a title

		table = self.document.add_table(rows=0, cols=2)

		for key, value in self.identification.items():
		    row_cells = table.add_row().cells
		    row_cells[0].text = key
		    row_cells[1].text = value

	def save_document(self, document_name):
		self.document.save(f'{document_name}.docx')