import pandas as pd


class Technical_Productions():
	def __init__(self, xml_file):
		super(Technical_Productions, self).__init__()
		self.xml_file = xml_file
		
		self.publications_dict = {}

		advice_and_consultancy, other_technical_works = self.get_technical_works()
		self.publications_dict["Assessoria e consultoria"] = advice_and_consultancy
		self.publications_dict["Programas de computador sem registro"] = self.get_not_registered_softwares() # Softwares without register
		self.publications_dict["Trabalhos técnicos"] = other_technical_works

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
		# Find the productions
		xml_path = 'TRABALHO-TECNICO'
		productions = self.xml_file.findall(f".//{xml_path}")

		# Define productions dictionary
		productions_dict = {"authors": [], "title": [], "year": [], "nature": []}

		for production in productions:
			# Get the data
			authors_string = self.get_authors_string(production)

			basic_data = production.find(f".//DADOS-BASICOS-DO-TRABALHO-TECNICO")
			title = basic_data.attrib['TITULO-DO-TRABALHO-TECNICO']
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
		advice_and_consultancy, other_technical_works = self.get_technical_works_strings(productions_df)

		return advice_and_consultancy, other_technical_works

	def get_softwares_strings(self, softwares_df):
		softwares_strings = []

		for pos, software in enumerate(softwares_df["title"]):
			software_string = ""
			software_string += f"{softwares_df['authors'][pos]}. {software}. {softwares_df['year'][pos]}."

			softwares_strings.append(software_string)

		return softwares_strings

	def get_not_registered_softwares(self):
		# Find the productions
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