import xml.etree.ElementTree as ET


class App():
	def __init__(self, resume_path):
		super(App, self).__init__()
		self.resume_path = resume_path
		
		self.xml_file = self.open_file()
		
		self.presentation = self.get_presentation() # Get author presentation
		self.abstract = self.get_abstract() # Get author abstract
		self.identification = self.get_identification() # Get author identification

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

		identification = {"Nome": author_name, "Nome em citações bibliográficas": citation_name, "Lattes iD": lattes_id, "Orcid iD": orcid_id}

		return identification