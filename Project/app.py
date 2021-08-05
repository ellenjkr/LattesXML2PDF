import xml.etree.ElementTree as ET
import pandas as pd


class App():
	def __init__(self, resume_path):
		super(App, self).__init__()
		self.resume_path = resume_path
		
		self.xml_file = self.open_file()
		
		self.abstract = self.get_abstract() # Get author abstract
		self.presentation = self.get_presentation() # Get author presentation
		self.identification = self.get_identification() # Get author identification
		self.address = self.get_address() # Get professional address
		self.complete_articles, self.incomplete_articles = self.get_articles() # Get articles
		self.books = self.get_books()
		self.chapters = self.get_chapters()
		self.journal_texts = self.get_journal_texts()
		
	def open_file(self):
		xml_file = ET.parse(self.resume_path) # Open file
		xml_file = xml_file.getroot()

		return xml_file

	def format_update_date(self, date): # Format date from text to "00/00/0000"
		day = date[:2]
		month = date[2:4]
		year = date[4:]
		update_date = "Última atualização do currículo em " + day + "/" + month + "/" + year
		return update_date

	def get_presentation(self):
		# Find general data tag
		xml_path = 'DADOS-GERAIS'
		general_data = self.xml_file.find(f".//{xml_path}")

		# Get data
		author_name = general_data.attrib['NOME-COMPLETO']
		lattes_id = self.xml_file.attrib['NUMERO-IDENTIFICADOR']
		lattes_address = 'Endereço para acessar este CV: http://lattes.cnpq.br/' + lattes_id
		lattes_id = "ID Lattes: " + lattes_id
		
		update_date = self.xml_file.attrib['DATA-ATUALIZACAO']
		update_date = self.format_update_date(update_date)

		# Add data to a list
		presentation = []
		presentation.append(author_name)
		presentation.append(lattes_address)
		presentation.append(lattes_id)
		presentation.append(update_date)

		return presentation

	def get_abstract(self):
		# Find tag and access it's abstract attribute
		xml_path = 'RESUMO-CV'
		abstract = self.xml_file.find(f".//{xml_path}").attrib['TEXTO-RESUMO-CV-RH'] 

		return abstract

	def get_identification(self):
		# Find general data tag
		xml_path = 'DADOS-GERAIS'
		general_data = self.xml_file.find(f".//{xml_path}")

		# Get data
		author_name = general_data.attrib['NOME-COMPLETO']
		citation_name = general_data.attrib['NOME-EM-CITACOES-BIBLIOGRAFICAS']
		orcid_id = general_data.attrib['ORCID-ID']
		lattes_id = self.xml_file.attrib['NUMERO-IDENTIFICADOR']

		identification = {"Nome": author_name, "Nome em citações bibliográficas": citation_name, "Lattes iD": lattes_id, "Orcid iD": orcid_id} # Build dictionary with the data

		return identification

	def get_address(self):
		# Find the tag
		xml_path = 'ENDERECO-PROFISSIONAL'
		institution_address = self.xml_file.find(f".//{xml_path}")
		
		# Get data
		institution = institution_address.attrib["NOME-INSTITUICAO-EMPRESA"]
		orgao_name = institution_address.attrib["NOME-ORGAO"]
		address = institution_address.attrib["LOGRADOURO-COMPLEMENTO"]
		district = institution_address.attrib["BAIRRO"]
		cep = institution_address.attrib["CEP"]
		city = institution_address.attrib["CIDADE"]
		uf = institution_address.attrib["UF"]
		country = institution_address.attrib["PAIS"]
		mailbox = institution_address.attrib["CAIXA-POSTAL"]
		ddd = institution_address.attrib["DDD"]
		telephone = institution_address.attrib["TELEFONE"]
		fax = institution_address.attrib["FAX"]

		# Separate the data through lines
		first_line = f"{institution}, {orgao_name}"
		second_line = address
		third_line = district
		fourth_line = f"{cep} - {city}, {uf} - {country} - Caixa-postal: {mailbox}"
		fifth_line = f"Telefone: ({ddd}) {telephone}"
		sixth_line = f"Fax: ({ddd}) {fax}"

		address = [first_line, second_line, third_line, fourth_line, fifth_line, sixth_line]

		return address

	def get_authors_string(self, xml_child):
		authors_string = ""
		authors = xml_child.findall(f".//AUTORES")
		for pos, author in enumerate(authors):
			if pos != 0:
				authors_string += '; '
			authors_string += author.attrib['NOME-PARA-CITACAO']

		return authors_string

	def sort_by_key(self, data_dict, key, ascending=True):
		data_df = pd.DataFrame(data_dict)
		data_df.sort_values(by=[key], inplace=True, ascending=ascending)
		data_df.reset_index(drop=True, inplace=True)

		return data_df

	def get_articles_strings(self, articles_df):
		complete_articles_strings = []
		incomplete_articles_strings = []
		for pos, article in enumerate(articles_df["title"]):
			article_string = ""
			article_string += f"{articles_df['authors'][pos]}. {article}. {articles_df['journal'][pos]}, {articles_df['vol'][pos]}, {articles_df['pages'][pos]}, {articles_df['year'][pos]}."

			if articles_df["nature"][pos] == 'COMPLETO':
				complete_articles_strings.append(article_string)
			else:
				incomplete_articles_strings.append(article_string)

		return (complete_articles_strings, incomplete_articles_strings)

	def get_articles(self):
		# Find the articles
		xml_path = 'ARTIGO-PUBLICADO'
		articles = self.xml_file.findall(f".//{xml_path}")

		# Define articles dictionary
		articles_dict = {"title": [], "year": [], "journal": [], "vol": [], "pages": [], "authors": [], "nature": []}

		for article in articles:
			# Get the data
			article_basic_data = article.find(f".//DADOS-BASICOS-DO-ARTIGO")
			title = article_basic_data.attrib['TITULO-DO-ARTIGO']
			year = int(article_basic_data.attrib['ANO-DO-ARTIGO'])
			nature = article_basic_data.attrib['NATUREZA']

			article_details = article.find(f".//DETALHAMENTO-DO-ARTIGO")
			journal = article_details.attrib['TITULO-DO-PERIODICO-OU-REVISTA']
			vol = f"v. {article_details.attrib['VOLUME']}"
			pages = f"p. {article_details.attrib['PAGINA-INICIAL']}-{article_details.attrib['PAGINA-FINAL']}"

			authors_string = self.get_authors_string(article)

			# Add data to the dictionary
			articles_dict["title"].append(title)
			articles_dict["year"].append(year)
			articles_dict["journal"].append(journal)
			articles_dict["vol"].append(vol)
			articles_dict["pages"].append(pages)
			articles_dict["authors"].append(authors_string)
			articles_dict["nature"].append(nature)

		# Sort articles by year
		articles_df = self.sort_by_key(articles_dict, "year", ascending=False)
		
		# Generate strings for each article
		complete_articles_strings, incomplete_articles_strings = self.get_articles_strings(articles_df)

		return (complete_articles_strings, incomplete_articles_strings)
	
	def get_books_strings(self, books_df):
		books_strings = []
		for pos, book in enumerate(books_df["title"]):
			book_string = ""
			book_string = f"{books_df['authors'][pos]}. {book}. {books_df['edition'][pos]}. ed. {books_df['publisher_city'][pos]}: {books_df['publisher'][pos]}, {books_df['year'][pos]}. v. {books_df['vol'][pos]}. {books_df['pages'][pos]}p."
			books_strings.append(book_string)

		return books_strings

	def get_books(self):
		xml_path = 'LIVRO-PUBLICADO-OU-ORGANIZADO'
		books = self.xml_file.findall(f".//{xml_path}")

		books_dict = {"authors": [], "title": [], "year": [], "edition": [], "publisher_city": [], "publisher": [], "vol": [], "pages": []}
		for book in books:	
			# Get data
			authors_string = self.get_authors_string(book)

			basic_data = book.find(f".//DADOS-BASICOS-DO-LIVRO")
			title = basic_data.attrib['TITULO-DO-LIVRO']
			year = basic_data.attrib['ANO']

			details = book.find(f".//DETALHAMENTO-DO-LIVRO")
			edition = details.attrib['NUMERO-DA-EDICAO-REVISAO']
			publisher_city = details.attrib['CIDADE-DA-EDITORA']
			publisher = details.attrib['NOME-DA-EDITORA']
			vol = details.attrib['NUMERO-DE-VOLUMES']
			pages = details.attrib['NUMERO-DE-PAGINAS']

			# Add data to the dictionary
			books_dict["authors"].append(authors_string)
			books_dict["title"].append(title)
			books_dict["year"].append(year)
			books_dict["edition"].append(edition)
			books_dict["publisher_city"].append(publisher_city)
			books_dict["publisher"].append(publisher)
			books_dict["vol"].append(vol)
			books_dict["pages"].append(pages)

		# Sort books by year
		books_df = self.sort_by_key(books_dict, "year", ascending=False)

		# Generate strings for each book
		books_strings = self.get_books_strings(books_df)
			
		return books_strings

	def get_chapters_strings(self, chapters_df):
		chapters_strings = []
		for pos, chapter in enumerate(chapters_df["title"]):
			chapter_string = ""
			chapter_string += f"{chapters_df['authors'][pos]}. {chapter}. In: "
			
			if chapters_df['org'][pos] != "":
				if "org" not in chapters_df['org'][pos].lower():
					chapter_string += f"{chapters_df['org'][pos]} (Org.)."
				else:
					chapter_string += f" {chapters_df['org'][pos]}"

			chapter_string += f" {chapters_df['book'][pos]}"

			if chapters_df['edition'][pos] != "":
				chapter_string += f" {chapters_df['edition'][pos]} ed."

			chapter_string += f" {chapters_df['publisher_city'][pos]}: {chapters_df['publisher'][pos]}, {chapters_df['year'][pos]}, "

			if chapters_df['vol'][pos] != "":
				chapter_string += f"vol. {chapters_df['vol'][pos]}, "

			chapter_string += f"{chapters_df['pages'][pos]}."
			
			chapters_strings.append(chapter_string)

		return chapters_strings

	def get_chapters(self):
		xml_path = 'CAPITULO-DE-LIVRO-PUBLICADO'
		chapters = self.xml_file.findall(f".//{xml_path}")

		chapters_dict = {"authors": [], "org": [], "title": [], "year": [], "book": [], "vol": [], "edition": [], "pages": [], "publisher_city": [], "publisher": []}
		for chapter in chapters:	
			basic_data = chapter.find(f".//DADOS-BASICOS-DO-CAPITULO")
			details = chapter.find(f".//DETALHAMENTO-DO-CAPITULO")
			
			# Get data
			authors_string = self.get_authors_string(chapter)

			title = basic_data.attrib['TITULO-DO-CAPITULO-DO-LIVRO']
			year = basic_data.attrib['ANO']

			book = details.attrib['TITULO-DO-LIVRO']
			vol = details.attrib['NUMERO-DE-VOLUMES']
			org = details.attrib['ORGANIZADORES']
			pages = f"p. {details.attrib['PAGINA-INICIAL']}-{details.attrib['PAGINA-FINAL']}"
			publisher_city = details.attrib['CIDADE-DA-EDITORA']
			publisher = details.attrib['NOME-DA-EDITORA']
			edition = details.attrib['NUMERO-DA-EDICAO-REVISAO']

			# Add data to the dictionary
			chapters_dict["authors"].append(authors_string)
			chapters_dict["org"].append(org)
			chapters_dict["title"].append(title)
			chapters_dict["year"].append(year)
			chapters_dict["book"].append(book)
			chapters_dict["vol"].append(vol)
			chapters_dict["edition"].append(edition)
			chapters_dict["pages"].append(pages)
			chapters_dict["publisher_city"].append(publisher_city)
			chapters_dict["publisher"].append(publisher)

		# Sort chapters by year
		chapters_df = self.sort_by_key(chapters_dict, "year", ascending=False)

		# Generate strings for each book
		chapters_strings = self.get_chapters_strings(chapters_df)
			
		return chapters_strings

	def get_texts_strings(self, texts_df):
		texts_strings = []
		for pos, text in enumerate(texts_df["title"]):
			text_string = ""
			text_string = f"{texts_df['authors'][pos]}. {text}. {texts_df['journal'][pos]}, {texts_df['city'][pos]}, {texts_df['pages'][pos]}, {texts_df['year'][pos]}."
			texts_strings.append(text_string)

		return texts_strings

	def get_journal_texts(self):
		xml_path = 'TEXTO-EM-JORNAL-OU-REVISTA'
		texts = self.xml_file.findall(f".//{xml_path}")

		texts_dict = {"authors": [], "title": [], "journal": [], "city": [], "pages": [], "year": []}
		for text in texts:	
			basic_data = text.find(f".//DADOS-BASICOS-DO-TEXTO")
			details = text.find(f".//DETALHAMENTO-DO-TEXTO")
			
			# Get data
			authors_string = self.get_authors_string(text)

			title = basic_data.attrib['TITULO-DO-TEXTO']
			
			journal = details.attrib['TITULO-DO-JORNAL-OU-REVISTA']
			city = details.attrib['LOCAL-DE-PUBLICACAO']
			pages = f"p. {details.attrib['PAGINA-INICIAL']}-{details.attrib['PAGINA-FINAL']}"
			year = details.attrib['DATA-DE-PUBLICACAO'][4:]

			# Add data to the dictionary
			texts_dict["authors"].append(authors_string)
			texts_dict["title"].append(title)
			texts_dict["journal"].append(journal)
			texts_dict["city"].append(city)
			texts_dict["pages"].append(pages)
			texts_dict["year"].append(year)
			
		# Sort texts by year
		texts_df = self.sort_by_key(texts_dict, "year", ascending=False)

		# Generate strings for each book
		texts_strings = self.get_texts_strings(texts_df)
			
		return texts_strings




		