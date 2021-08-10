import pandas as pd


class Publications():
	def __init__(self, xml_file):
		super(Publications, self).__init__()
		self.xml_file = xml_file
		
		self.publications_dict = {}

		self.complete_articles, self.incomplete_articles = self.get_articles()
		self.complete_congress_works, self.congress_expanded_abstracts, self.congress_abstracts = self.get_congress_works()

		self.publications_dict["Artigos completos publicados em periódicos"] = self.complete_articles
		# self.publications_dict.append(self.incomplete_a¹rticles)
		self.publications_dict["Livros publicados/organizados ou edições"] = self.get_books()
		self.publications_dict["Capítulos de livros publicados"] = self.get_chapters()
		self.publications_dict["Textos em jornais de notícias/revistas"] = self.get_journal_texts()
		self.publications_dict["Trabalhos completos publicados em anais de congressos"] = self.complete_congress_works
		self.publications_dict["Resumos expandidos publicados em anais de congressos"] = self.congress_expanded_abstracts
		self.publications_dict["Resumos publicados em anais de congressos"] = self.congress_abstracts
		self.publications_dict["Apresentações de Trabalho"] = self.get_work_presentations()
		self.publications_dict["Outras produções bibliográficas"] = self.get_other_publications()

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

	def get_congress_works_strings(self, works_df):
		complete_works_strings = [] # Trabalhos completos
		expanded_abstracts_strings = [] # Resumos expandidos
		congress_abstracts = [] # Resumos

		for pos, work in enumerate(works_df["title"]):
			work_string = ""
			work_string += f"{works_df['authors'][pos]}. {works_df['title'][pos]}. In: {works_df['congress'][pos]}, {works_df['year'][pos]}, {works_df['congress_city'][pos]}. {works_df['proceedings'][pos]}. {works_df['publisher_city'][pos]}: {works_df['publisher'][pos]}, {works_df['year'][pos]}. {works_df['pages'][pos]}"

			if works_df["nature"][pos] == 'COMPLETO':
				complete_works_strings.append(work_string)
			elif works_df["nature"][pos] == 'RESUMO_EXPANDIDO':
				expanded_abstracts_strings.append(work_string)
			else:
				congress_abstracts.append(work_string)

		return (complete_works_strings, expanded_abstracts_strings, congress_abstracts)

	def get_congress_works(self):
		# Find the works
		xml_path = 'TRABALHO-EM-EVENTOS'
		works = self.xml_file.findall(f".//{xml_path}")

		# Define works dictionary
		works_dict = {"nature": [], "authors": [], "title": [], "congress": [], "year": [], "congress_city": [], "proceedings": [], "publisher_city": [], "publisher": [], "pages": []}

		for work in works:
			# Get the data
			authors_string = self.get_authors_string(work)

			work_basic_data = work.find(f".//DADOS-BASICOS-DO-TRABALHO")
			title = work_basic_data.attrib['TITULO-DO-TRABALHO']
			nature = work_basic_data.attrib['NATUREZA']

			work_details = work.find(f".//DETALHAMENTO-DO-TRABALHO")
			congress = work_details.attrib['NOME-DO-EVENTO']
			year = work_details.attrib['ANO-DE-REALIZACAO']
			congress_city = work_details.attrib['CIDADE-DO-EVENTO']
			proceedings = work_details.attrib['TITULO-DOS-ANAIS-OU-PROCEEDINGS']
			publisher_city = work_details.attrib['CIDADE-DA-EDITORA']
			publisher = work_details.attrib['NOME-DA-EDITORA']
			pages = f"p. {work_details.attrib['PAGINA-INICIAL']}-{work_details.attrib['PAGINA-FINAL']}"

			# Add data to the dictionary
			works_dict["nature"].append(nature)
			works_dict["authors"].append(authors_string)
			works_dict["title"].append(title)
			works_dict["congress"].append(congress)
			works_dict["year"].append(year)
			works_dict["congress_city"].append(congress_city)
			works_dict["proceedings"].append(proceedings)
			works_dict["publisher_city"].append(publisher_city)
			works_dict["publisher"].append(publisher)
			works_dict["pages"].append(pages)

		# Sort works by year
		works_df = self.sort_by_key(works_dict, "year", ascending=False)
		
		# Generate strings for each work
		complete_works_strings, expanded_abstracts_strings, abstract_strings = self.get_congress_works_strings(works_df)

		return (complete_works_strings, expanded_abstracts_strings, abstract_strings)

	def get_presentations_strings(self, presentations_df):
		presentations_strings = []
		for pos, presentation in enumerate(presentations_df["title"]):
			presentation_string = ""
			presentation_string = f"{presentations_df['authors'][pos]}. {presentation}. {presentations_df['year'][pos]}. {presentations_df['nature'][pos]}"

			presentations_strings.append(presentation_string)

		return presentations_strings

	def get_work_presentations(self):
		xml_path = 'APRESENTACAO-DE-TRABALHO'
		presentations = self.xml_file.findall(f".//{xml_path}")

		presentations_dict = {"authors": [], "title": [], "year": [], "nature": []}
		for presentation in presentations:	
			# Get data
			authors_string = self.get_authors_string(presentation)

			basic_data = presentation.find(f".//DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO")
			title = basic_data.attrib['TITULO']
			year = basic_data.attrib['ANO']
			nature = basic_data.attrib['NATUREZA']
		
			# Add data to the dictionary
			presentations_dict["authors"].append(authors_string)
			presentations_dict["title"].append(title)
			presentations_dict["year"].append(year)

			# Different types of nature
			if nature == "CONGRESSO":
				presentations_dict["nature"].append(f"(Apresentação de Trabalho/Congresso)")
			else:
				presentations_dict["nature"].append(f"(Apresentação de Trabalho/Conferência ou palestra)")
			
		# Sort presentations by year
		presentations_df = self.sort_by_key(presentations_dict, "year", ascending=False)

		# Generate strings for each presentation
		presentations_strings = self.get_presentations_strings(presentations_df)
			
		return presentations_strings

	def get_other_publications_strings(self, other_publications_df):
		other_publications_strings = []
		for pos, other_publication in enumerate(other_publications_df["title"]):
			other_publication_string = ""
			other_publication_string = f"{other_publications_df['authors'][pos]}. {other_publication}. {other_publications_df['publisher_city'][pos]}: {other_publications_df['publisher'][pos]}, {other_publications_df['year'][pos]} {other_publications_df['nature'][pos]}."

			other_publications_strings.append(other_publication_string)

		return other_publications_strings

	def get_other_publications(self):
		xml_path = 'OUTRA-PRODUCAO-BIBLIOGRAFICA'
		other_publications = self.xml_file.findall(f".//{xml_path}")

		other_publications_dict = {"authors": [], "title": [], "year": [], "nature": [], "publisher": [], "publisher_city": []}
		for other_publication in other_publications:	
			# Get data
			authors_string = self.get_authors_string(other_publication)

			basic_data = other_publication.find(f".//DADOS-BASICOS-DE-OUTRA-PRODUCAO")
			title = basic_data.attrib['TITULO']
			year = basic_data.attrib['ANO']
			nature = basic_data.attrib['NATUREZA']

			details = other_publication.find(f".//DETALHAMENTO-DE-OUTRA-PRODUCAO")
			publisher = details.attrib["EDITORA"]
			publisher_city = details.attrib["CIDADE-DA-EDITORA"]

			# Add data to the dictionary
			other_publications_dict["authors"].append(authors_string)
			other_publications_dict["title"].append(title)
			other_publications_dict["year"].append(year)
			other_publications_dict["nature"].append(f"({nature})")
			other_publications_dict["publisher"].append(publisher)
			other_publications_dict["publisher_city"].append(publisher_city)
			
		# Sort other_publications by year
		other_publications_df = self.sort_by_key(other_publications_dict, "year", ascending=False)

		# Generate strings for each other_publication
		other_publications_strings = self.get_other_publications_strings(other_publications_df)
			
		return other_publications_strings