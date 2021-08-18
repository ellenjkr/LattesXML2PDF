import pandas as pd
import xml.etree.ElementTree as ET

from bibliographic_productions import Bibliographic_Productions
from technical_productions import Technical_Productions

class Resume():
	def __init__(self, resume_path):
		super(Resume, self).__init__()
		self.resume_path = resume_path
		
		self.xml_file = self.open_file()
		
		self.abstract = self.get_abstract()
		self.presentation = self.get_presentation()
		self.identification = self.get_identification()
		self.address = self.get_address()

		self.bibliographic_productions = Bibliographic_Productions(self.xml_file)
		self.bibliographic_productions_dict = self.bibliographic_productions.publications_dict

		self.technical_productions = Technical_Productions(self.xml_file)
		self.technical_productions_dict = self.technical_productions.publications_dict
		
		self.lines_of_research = self.get_lines_of_research()
		self.research_projects = self.get_research_projects()

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


	def get_lines_of_research(self):
		# Find the tag
		xml_path = 'LINHA-DE-PESQUISA'
		researches = self.xml_file.findall(f".//{xml_path}")

		info = {'title': [], 'goals': [], 'key_words': []}

		for research in researches:
			title = research.attrib['TITULO-DA-LINHA-DE-PESQUISA']
			goals = research.attrib['OBJETIVOS-LINHA-DE-PESQUISA']
			
			keywords_xml_path = 'PALAVRAS-CHAVE'
			keywords = research.find(f".//{keywords_xml_path}") # Get keywords
			if keywords != None and keywords != []: # Check if the line of research has keywords
				keywords_string = "Palavras-chave: "
				for key in keywords.attrib.keys(): # For each key
					if keywords.attrib[key] != "": # Check if it is empty
						keywords_string += f"{keywords.attrib[key]}; " # Add the keyword to the string

				keywords_string = keywords_string[: -2] # Remove the ", " after the last keyword
				keywords_string += '.' # Add a "." after the last keyword
	
			else:
				keywords_string = ""
			
			info['title'].append(title)
			info['goals'].append(f"Objetivo: {goals}")
			info['key_words'].append(keywords_string)

		return info

	def get_research_students(self, research):
		grad = research.attrib['NUMERO-GRADUACAO'] if research.attrib['NUMERO-GRADUACAO'] != "" else "0"
		acad_master = research.attrib['NUMERO-MESTRADO-ACADEMICO'] if research.attrib['NUMERO-MESTRADO-ACADEMICO'] != "" else "0"
		espec = research.attrib['NUMERO-ESPECIALIZACAO'] if research.attrib['NUMERO-ESPECIALIZACAO'] != "" else "0"
		prof_master = research.attrib['NUMERO-MESTRADO-PROF'] if research.attrib['NUMERO-MESTRADO-PROF'] != "" else "0"
		doctorate = research.attrib['NUMERO-DOUTORADO'] if research.attrib['NUMERO-DOUTORADO'] != "" else "0"

		string = f"Alunos envolvidos: Graduação: ({grad}) / Especialização: ({espec}) / Mestrado acadêmico: ({acad_master}) / Mestrado profissional: ({prof_master}) / Doutorado: ({doctorate})."

		return string

	def get_research_financiers(self, research):
		financiers_list = []
		for financier in research.findall(f".//{'FINANCIADOR-DO-PROJETO'}"):
			name = financier.attrib['NOME-INSTITUICAO']
			nature = financier.attrib['NATUREZA'].replace('_', ' ').capitalize()
			nature = "Cooperação" if nature == "COOPERACAO" else nature

			financier_string = f"{name} - {nature}"
			financiers_list.append(financier_string)

		if financiers_list:
			financiers = "Financiador(es): " + " / ".join(financiers_list)  # Turn the list of names into a string
		else:
			financiers = None
		return financiers

	def sort_by_key(self, data_dict, key, ascending=True):
		data_df = pd.DataFrame(data_dict)
		data_df.sort_values(by=[key], inplace=True, ascending=ascending)
		data_df.reset_index(drop=True, inplace=True)

		return data_df

	def get_research_projects(self):
		# Find the tag
		xml_path = 'PROJETO-DE-PESQUISA'
		researches = self.xml_file.findall(f".//{xml_path}")

		info = {'year_range': [], 'title': [], 'description': [], 'situation/nature': [], 'students': [], 'members': [], 'financiers': [], 'num_of_productions': []}

		for research in researches:
			year_range = f"{research.attrib['ANO-INICIO']} - {research.attrib['ANO-FIM']}"
			if year_range[-1] == " ": # If "ANO-FIM" == ""
				year_range += "Atual"
			title = research.attrib['NOME-DO-PROJETO']
			description = "Descrição: " + research.attrib['DESCRICAO-DO-PROJETO']
			situation_nature = f"Situação: {research.attrib['SITUACAO'].replace('_', ' ').capitalize()}; Natureza: {research.attrib['NATUREZA'].replace('_', ' ').capitalize()}."
			students = self.get_research_students(research)

			members_list = [member.attrib['NOME-COMPLETO'] for member in research.findall(f".//{'INTEGRANTES-DO-PROJETO'}")] # Get the name of each member
			members = "Integrantes: " + " / ".join(members_list)  # Turn the list of names into a string

			financiers = self.get_research_financiers(research)
			
			num_of_productions = "Número de produções C, T & A: " + str(len(research.findall(f".//{'PRODUCAO-CT-DO-PROJETO'}")))

			info['year_range'].append(year_range)
			info['title'].append(title)
			info['description'].append(description)
			info['situation/nature'].append(situation_nature)
			info['students'].append(students)
			info['members'].append(members)
			info['financiers'].append(financiers)
			info['num_of_productions'].append(num_of_productions)

		info_df = self.sort_by_key(info, "year_range", ascending=False)
		
		return info