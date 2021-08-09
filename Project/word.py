from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.shared import RGBColor


class WordFile():
	def __init__(self, presentation, abstract, identification, address, publications_dict):
		super(WordFile, self).__init__()
		self.presentation = presentation
		self.abstract = abstract
		self.identification = identification
		self.address = address
		self.publications_dict = publications_dict

		self.document = Document()

		self.define_style()
		self.add_presentation()
		self.add_abstract()
		self.add_identification()
		self.add_address()
		self.add_publications()
		# # self.add_incomplete_articles()
		# # self.add_incomplete_congress_works()

	def define_style(self):
		style = self.document.styles['Normal']
		font = style.font
		font.name = 'Arial'
		font.size = Pt(10)

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

	def add_address(self):
		self.document.add_heading("Endereço", 1) # Add "Endereço" as a title

		table = self.document.add_table(rows=0, cols=2)

		row_cells = table.add_row().cells
		row_cells[0].text = "Endereço Profissional"
		row_cells[1].text = self.address[0]
		
		for value in self.address[1:]:
			row_cells = table.add_row().cells
			row_cells[1].text = value

	def add_publications(self):
		for key, publication_type in self.publications_dict.items():
			self.document.add_heading(key, 1) # Add the key as a title

			table = self.document.add_table(rows=0, cols=2) # Create table

			for pos, publication in enumerate(publication_type):
				row_cells = table.add_row().cells # Get cells from row
				row_cells[0].width = 5 # Make the first cell smaller
				paragraph = row_cells[0].paragraphs[0] # Get the paragraph
				paragraph.add_run(str(pos + 1)).bold = True # Add a number for each publication and make it bold
				run = paragraph.runs[0]
				font = run.font
				font.color.rgb = RGBColor.from_string('0b306b')
				
				row_cells[1].width = Pt(500) # Make the second cell bigger
				paragraph = row_cells[1].paragraphs[0] # Get the cell paragraph
				paragraph.text = publication # Add the publication to the paragraph
				paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY # Justify the paragraph

	def save_document(self, document_name):
		self.document.save(f'{document_name}.docx')