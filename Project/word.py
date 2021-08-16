from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.shared import RGBColor


class WordFile():
	def __init__(self, presentation, abstract, identification, address, bibliographic_productions_dict, technical_productions_dict):
		super(WordFile, self).__init__()
		self.presentation = presentation
		self.abstract = abstract
		self.identification = identification
		self.address = address
		self.bibliographic_productions_dict = bibliographic_productions_dict
		self.technical_productions_dict = technical_productions_dict

		self.document = Document()

		self.define_style()
		self.document.add_heading("Apresentação", 0) # Add a section
		self.add_presentation()
		self.add_abstract()
		self.add_identification()
		self.add_address()
		self.document.add_heading("Produções", 0) # Add a section
		self.add_productions(self.bibliographic_productions_dict, "Produção bibliográfica")
		self.add_productions(self.technical_productions_dict, "Produção técnica")
		
		# # self.add_incomplete_articles()

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

	def set_cell_background(self, cell, fill, color=None, val=None):
	    from docx.oxml.shared import qn  # feel free to move these out
	    from docx.oxml.xmlchemy import OxmlElement

	    cell_properties = cell._element.tcPr
	    try:
	        cell_shading = cell_properties.xpath('w:shd')[0]  # in case there's already shading
	    except IndexError:
	        cell_shading = OxmlElement('w:shd') # add new w:shd element to it
	    if fill:
	        cell_shading.set(qn('w:fill'), fill)  # set fill property, respecting namespace
	    if color:
	        pass # TODO
	    if val:
	        pass # TODO
	    cell_properties.append(cell_shading)  # finally extend cell props with shading element

	def add_subsection(self, subsection):
		table = self.document.add_table(rows=0, cols=1) # Create table row
		row_cells = table.add_row().cells # Get cells from first row
		paragraph = row_cells[0].paragraphs[0] # Get the paragraph

		paragraph_format = paragraph.paragraph_format # Get the paragraph format
		# Adjust space before and after
		paragraph_format.space_before = Pt(3)
		paragraph_format.space_after = Pt(3)

		# Add a new run to the paragraph, make the text bold and white and change the size and the background color
		paragraph.add_run(subsection).bold = True # Add a number for each publication and make it bold
		run = paragraph.runs[0]
		font = run.font
		font.size = Pt(13)
		font.color.rgb = RGBColor.from_string('FFFFFF')
		self.set_cell_background(row_cells[0], '0b306b')

	def add_productions(self, productions_dict, subsection):
		self.add_subsection(subsection)

		for key, publication_type in productions_dict.items():
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