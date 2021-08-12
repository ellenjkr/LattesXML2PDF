import pandas as pd


class Technical_Productions():
	def __init__(self, xml_file):
		super(Technical_Productions, self).__init__()
		self.xml_file = xml_file
		
		self.publications_dict = {}

		advice_and_consultancy, other_technical_works = self.get_technical_works()
		self.publications_dict["Assessoria e consultoria"] = advice_and_consultancy
		self.publications_dict["Programas de computador sem registro"] = self.get_not_registered_softwares() # Softwares without register
		self.publications_dict["Produtos tecnológicos"] = self.get_tech_products()
		self.publications_dict["Trabalhos técnicos"] = other_technical_works
		self.publications_dict["Entrevistas, mesas redondas, programas e comentários na mídia"] = self.get_other_productions()

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

	def get_technical_works_strings(self, productions_df):
		advice_and_consultancy = []
		other_technical_works = []
		for pos, production in enumerate(productions_df["title"]):
			production_string = ""
			production_string += f"{productions_df['authors'][pos]}. {production}. {productions_df['year'][pos]}."

			if productions_df['nature'][pos] == "CONSULTORIA" or productions_df['nature'][pos] == "ASSESSORIA":
				advice_and_consultancy.append(production_string)
			else:
				other_technical_works.append(production_string)

		return (advice_and_consultancy, other_technical_works)

	def get_technical_works(self):
		# Find the works
		xml_path = 'TRABALHO-TECNICO'
		works = self.xml_file.findall(f".//{xml_path}")

		# Define works dictionary
		works_dict = {"authors": [], "title": [], "year": [], "nature": []}

		for work in works:
			# Get the data
			authors_string = self.get_authors_string(work)

			basic_data = work.find(f".//DADOS-BASICOS-DO-TRABALHO-TECNICO")
			title = basic_data.attrib['TITULO-DO-TRABALHO-TECNICO']
			year = int(basic_data.attrib['ANO'])
			nature = basic_data.attrib['NATUREZA']

			# Add data to the dictionary
			works_dict["authors"].append(authors_string)
			works_dict["title"].append(title)
			works_dict["year"].append(year)
			works_dict["nature"].append(nature)

		# Sort works by year
		works_df = self.sort_by_key(works_dict, "year", ascending=False)
		
		# Generate strings for each work
		advice_and_consultancy, other_technical_works = self.get_technical_works_strings(works_df)

		return advice_and_consultancy, other_technical_works

	def get_softwares_strings(self, softwares_df):
		softwares_strings = []

		for pos, software in enumerate(softwares_df["title"]):
			software_string = ""
			software_string += f"{softwares_df['authors'][pos]}. {software}. {softwares_df['year'][pos]}."

			softwares_strings.append(software_string)

		return softwares_strings

	def get_not_registered_softwares(self):
		# Find the softwares
		xml_path = 'SOFTWARE'
		softwares = self.xml_file.findall(f".//{xml_path}")

		# Define softwares dictionary
		softwares_dict = {"authors": [], "title": [], "year": []}

		for software in softwares:
			# Get the data
			authors_string = self.get_authors_string(software)

			basic_data = software.find(f".//DADOS-BASICOS-DO-SOFTWARE")
			title = basic_data.attrib['TITULO-DO-SOFTWARE']
			year = int(basic_data.attrib['ANO'])

			details = software.find(f".//DETALHAMENTO-DO-SOFTWARE")

			if details.find(".//REGISTRO-OU-PATENTE") is None: # Accept only the softwares without register
				# Add data to the dictionary
				softwares_dict["authors"].append(authors_string)
				softwares_dict["title"].append(title)
				softwares_dict["year"].append(year)

		# Sort softwares by year
		softwares_df = self.sort_by_key(softwares_dict, "year", ascending=False)
		
		# Generate strings for each software
		softwares_strings = self.get_softwares_strings(softwares_df)

		return softwares_strings

	def get_tech_products_strings(self, tech_products_df):
		tech_products_strings = []

		for pos, tech_product in enumerate(tech_products_df["title"]):
			tech_product_string = ""
			tech_product_string += f"{tech_products_df['authors'][pos]}. {tech_product}. {tech_products_df['year'][pos]}."

			tech_products_strings.append(tech_product_string)

		return tech_products_strings

	def get_tech_products(self):
		# Find the productions
		xml_path = 'PRODUTO-TECNOLOGICO'
		tech_products = self.xml_file.findall(f".//{xml_path}")

		# Define tech_products dictionary
		tech_products_dict = {"authors": [], "title": [], "year": []}

		for tech_product in tech_products:
			# Get the data
			authors_string = self.get_authors_string(tech_product)

			basic_data = tech_product.find(f".//DADOS-BASICOS-DO-PRODUTO-TECNOLOGICO")
			title = basic_data.attrib['TITULO-DO-PRODUTO']
			year = int(basic_data.attrib['ANO'])

			# Add data to the dictionary
			tech_products_dict["authors"].append(authors_string)
			tech_products_dict["title"].append(title)
			tech_products_dict["year"].append(year)

		# Sort tech_products by year
		tech_products_df = self.sort_by_key(tech_products_dict, "year", ascending=False)
		
		# Generate strings for each tech_product
		tech_products_strings = self.get_tech_products_strings(tech_products_df)

		return tech_products_strings

	def get_other_productions_strings(self, productions_df):
		productions_strings = []

		for pos, production in enumerate(productions_df["title"]):
			production_string = ""
			production_string += f"{productions_df['authors'][pos]}. {production}. {productions_df['year'][pos]}."

			if productions_df['nature'][pos] == "MESA_REDONDA":
				production_string += " (Programa de rádio ou TV/Mesa redonda)."
			productions_strings.append(production_string)

		return productions_strings

	def get_other_productions(self):
		# Find the productions
		xml_path = 'PROGRAMA-DE-RADIO-OU-TV' # Implements only for radio and tv
		productions = self.xml_file.findall(f".//{xml_path}")

		# Define productions dictionary
		productions_dict = {"authors": [], "title": [], "year": [], "nature": []}

		for production in productions:
			# Get the data
			authors_string = self.get_authors_string(production)

			basic_data = production.find(f".//DADOS-BASICOS-DO-PROGRAMA-DE-RADIO-OU-TV")
			title = basic_data.attrib['TITULO']
			year = int(basic_data.attrib['ANO'])
			nature = basic_data.attrib['NATUREZA']

			# Add data to the dictionary
			productions_dict["authors"].append(authors_string)
			productions_dict["title"].append(title)
			productions_dict["year"].append(year)
			productions_dict["nature"].append(nature)

		# Sort productions by year
		productions_df = self.sort_by_key(productions_dict, "year", ascending=False)
		
		# Generate strings for each production
		productions_strings = self.get_other_productions_strings(productions_df)

		return productions_strings
