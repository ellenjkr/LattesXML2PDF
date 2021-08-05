from docx import Document
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


class WordFile():
	def __init__(self, presentation, abstract, identification, address, complete_articles, incomplete_articles, books, chapters, journal_texts):
		super(WordFile, self).__init__()
		self.presentation = presentation
		self.abstract = abstract
		self.identification = identification
		self.address = address
		self.complete_articles = complete_articles
		self.incomplete_articles = incomplete_articles
		self.books = books
		self.chapters = chapters
		self.journal_texts = journal_texts

		self.document = Document()

		self.define_style()
		self.add_presentation()
		self.add_abstract()
		self.add_identification()
		self.add_address()
		self.add_complete_articles()
		# self.add_incomplete_articles()
		self.add_books()
		self.add_chapters()
		self.add_journal_texts()

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

	def add_complete_articles(self):
		self.document.add_heading("Artigos completos publicados em periódicos", 1) # Add "Artigos publicados em periódicos" as a title
		
		for article in self.complete_articles:
			paragraph = self.document.add_paragraph(article, style='List Bullet')
			
			# Format paragraph
			paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
			paragraph_format = paragraph.paragraph_format
			paragraph_format.line_spacing = Pt(15)

	def add_books(self):
		self.document.add_heading("Livros publicados/organizados ou edições", 1) # Add "Livros publicados/organizados ou edições" as a title
		
		for book in self.books:
			paragraph = self.document.add_paragraph(book, style='List Bullet')
					
			# Format paragraph
			paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
			paragraph_format = paragraph.paragraph_format
			paragraph_format.line_spacing = Pt(15)

	def add_chapters(self):
		self.document.add_heading("Capítulos de livros publicados", 1) # Add "Capítulos de livros publicados" as a title
		
		for chapter in self.chapters:
			paragraph = self.document.add_paragraph(chapter, style='List Bullet')
					
			# Format paragraph
			paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
			paragraph_format = paragraph.paragraph_format
			paragraph_format.line_spacing = Pt(15)

	def add_journal_texts(self):
		self.document.add_heading("Textos em jornais de notícias/revistas", 1) # Add "Textos em jornais de notícias/revistas" as a title
		
		for text in self.journal_texts:
			paragraph = self.document.add_paragraph(text, style='List Bullet')
					
			# Format paragraph
			paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
			paragraph_format = paragraph.paragraph_format
			paragraph_format.line_spacing = Pt(15)

	def save_document(self, document_name):
		self.document.save(f'{document_name}.docx')