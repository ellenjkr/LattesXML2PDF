import xml.etree.ElementTree as ET

import pandas as pd

from bibliographic_productions import Bibliographic_Productions
from other_professional_activities import OtherProfessionalActivities
from projects import Projects
from technical_productions import Technical_Productions
from professional_activities import ProfessionalActivities
from orientations import Orientations


class Resume():
	def __init__(self, resume_path):
		super(Resume, self).__init__()
		self.resume_path = resume_path
		
		self.xml_file = self.open_file()
		
		self.abstract = self.get_abstract()
		self.presentation = self.get_presentation()
		self.identification = self.get_identification()
		self.address = self.get_address()
		self.academic_titles = self.get_academic_titles()
		self.complementary_courses = self.get_complementary_courses()

		professional_activities = ProfessionalActivities(self.xml_file)
		self.professional_activities_list = professional_activities.professional_activities

		self.lines_of_research = self.get_lines_of_research()

		projects = Projects(self.xml_file)
		self.projects_dict = projects.projects_dict

		other_professional_activities = OtherProfessionalActivities(self.xml_file)
		self.other_professional_activities_dict = other_professional_activities.activities_dict

		self.areas_of_expertise = self.get_areas_of_expertise()
		self.languages = self.get_languages()
		self.awards = self.get_awards()

		bibliographic_productions = Bibliographic_Productions(self.xml_file)
		self.bibliographic_productions_dict = bibliographic_productions.publications_dict

		technical_productions = Technical_Productions(self.xml_file)
		self.technical_productions_dict = technical_productions.publications_dict

		# self.other_technical_productions = self.get_other_technical_productions()
		# self.registers = self.get_registers()

		orientations = Orientations(self.xml_file)
		self.orientations = orientations.orientations_dict

	def open_file(self):
		xml_file = ET.parse(self.resume_path)  # Open file
		xml_file = xml_file.getroot()

		return xml_file

	def format_update_date(self, date):  # Format date from text to "00/00/0000"
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

		identification = {"Nome": author_name, "Nome em citações bibliográficas": citation_name, "Lattes iD": lattes_id, "Orcid iD": orcid_id}  # Build dictionary with the data

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

	def get_key_words(self, xml_content):
		keywords_xml_path = 'PALAVRAS-CHAVE'
		keywords = xml_content.find(f".//{keywords_xml_path}")  # Get keywords
		if keywords != None and keywords != []:  # Check if the xml content has keywords
			keywords_string = "Palavras-chave: "
			for key in keywords.attrib.keys():  # For each key
				if keywords.attrib[key] != "":  # Check if it is empty
					keywords_string += f"{keywords.attrib[key]}; "  # Add the keyword to the string

			keywords_string = keywords_string[: -2]  # Remove the ", " after the last keyword
			keywords_string += '.'  # Add a "." after the last keyword

		else:
			keywords_string = ""

		return keywords_string

	def get_lines_of_research(self):
		# Find the tag
		xml_path = 'LINHA-DE-PESQUISA'
		researches = self.xml_file.findall(f".//{xml_path}")

		info = {'title': [], 'goals': [], 'key_words': []}

		for research in researches:
			title = research.attrib['TITULO-DA-LINHA-DE-PESQUISA']
			goals = research.attrib['OBJETIVOS-LINHA-DE-PESQUISA']
			
			keywords_string = self.get_key_words(research)
			
			info['title'].append(title)
			info['goals'].append(f"Objetivo: {goals}")
			info['key_words'].append(keywords_string)

		return info

	def get_areas_of_expertise_strings(self, info):
		strings = []
		fields = zip(info['great_area'], info['area'], info['sub_area'], info['specialty'])  # Select fields

		for great_area, area, sub_area, specialty in fields:  # Get info from each field
			great_area = great_area.capitalize().replace('_', ' ')
			string = f"Grande área: {great_area} / Área: {area} / Subárea: {sub_area} / Especialidade: {specialty}."
			strings.append(string)

		return strings

	def get_areas_of_expertise(self):
		# Find the tag
		xml_path = 'AREA-DE-ATUACAO'
		areas = self.xml_file.findall(f".//{xml_path}")

		info = {'great_area': [], 'area': [], 'sub_area': [], 'specialty': []}
		for area in areas:
			great_area = area.attrib['NOME-GRANDE-AREA-DO-CONHECIMENTO']
			main_area = area.attrib['NOME-DA-AREA-DO-CONHECIMENTO']
			sub_area = area.attrib['NOME-DA-SUB-AREA-DO-CONHECIMENTO']
			specialty = area.attrib['NOME-DA-ESPECIALIDADE']

			info['great_area'].append(great_area)
			info['area'].append(main_area)
			info['sub_area'].append(sub_area)
			info['specialty'].append(specialty)
		
		areas_strings = self.get_areas_of_expertise_strings(info)

		return areas_strings

	def get_languages(self):
		# Find the tag
		xml_path = 'IDIOMA'
		languages = self.xml_file.findall(f".//{xml_path}")

		info = {'language': [], 'string': []}

		for language in languages:
			language_name = language.attrib['DESCRICAO-DO-IDIOMA'].capitalize()
			listening = "Compreende " + language.attrib['PROFICIENCIA-DE-COMPREENSAO'].capitalize()
			speaking = "Fala " + language.attrib['PROFICIENCIA-DE-FALA'].capitalize()
			reading = "Lê " + language.attrib['PROFICIENCIA-DE-LEITURA'].capitalize()
			writing = "Escreve " + language.attrib['PROFICIENCIA-DE-ESCRITA'].capitalize()

			string = f"{listening}, {speaking}, {reading}, {writing}."

			info['language'].append(language_name)
			info['string'].append(string)

		return info

	def sort_by_key(self, data_dict, key, ascending=True):
		data_df = pd.DataFrame(data_dict)
		data_df.sort_values(by=[key], inplace=True, ascending=ascending)
		data_df.reset_index(drop=True, inplace=True)

		return data_df

	def get_awards(self):
		# Find the tag
		xml_path = 'PREMIO-TITULO'
		awards = self.xml_file.findall(f".//{xml_path}")

		info = {'year': [], 'string': []}

		for award in awards:
			year = award.attrib['ANO-DA-PREMIACAO']
			title = award.attrib['NOME-DO-PREMIO-OU-TITULO']
			entity = award.attrib['NOME-DA-ENTIDADE-PROMOTORA']

			string = f"{title}, {entity}"
			info['year'].append(year)
			info['string'].append(string)

		# Sort awards by year
		info_df = self.sort_by_key(info, "year", ascending=False)

		return info_df

	def get_academic_titles(self):
		# Find the tag
		xml_path = 'FORMACAO-ACADEMICA-TITULACAO'
		titles = self.xml_file.find(f".//{xml_path}")

		info = {'year_range': [], 'academic_title': [], 'institution': [], 'project_title': [], 'advisor': [], 'scholarship': [], 'key_words': []}
		for title in titles:
			year_range = f"{title.attrib['ANO-DE-INICIO']} - {title.attrib['ANO-DE-CONCLUSAO']}"
			if year_range[-1] == " ":  # If "ANO-FIM" == ""
				year_range += "Atual"
			graduation = title.attrib['NOME-CURSO']
			academic_title = f"{title.tag.capitalize()} em {graduation.title()}"
			institution = title.attrib['NOME-INSTITUICAO']
			if 'TITULO-DA-DISSERTACAO-TESE' in title.attrib.keys():
				title_year = title.attrib['ANO-DE-OBTENCAO-DO-TITULO']
				project_title = f"Título: {title.attrib['TITULO-DA-DISSERTACAO-TESE']}, Ano de obtenção: {title_year}."
			else:
				project_title = ''

			if 'NOME-COMPLETO-DO-ORIENTADOR' in title.attrib.keys():
				advisor = f"Orientador: {title.attrib['NOME-COMPLETO-DO-ORIENTADOR']}"
			else:
				advisor = ''
			
			if title.attrib['NOME-AGENCIA'] != "":
				scholarship = f"Bolsista do(a): {title.attrib['NOME-AGENCIA']}" 
			else:
				scholarship = ""
			keywords = self.get_key_words(title)
	
			info['year_range'].append(year_range)
			info['academic_title'].append(academic_title)
			info['institution'].append(institution)
			info['project_title'].append(project_title)
			info['advisor'].append(advisor)
			info['scholarship'].append(scholarship)
			info['key_words'].append(keywords)

		info_df = self.sort_by_key(info, "year_range", ascending=False)

		return info_df

	def get_complementary_courses(self):
		# Find the tag
		xml_path = 'FORMACAO-COMPLEMENTAR'
		courses = self.xml_file.find(f".//{xml_path}")

		info = {'year_range': [], 'course_name': [], 'institution': []}
		for course in courses:
			year_range = f"{course.attrib['ANO-DE-INICIO']} - {course.attrib['ANO-DE-CONCLUSAO']}"
			if year_range[-1] == " ":  # If "ANO-FIM" == ""
				year_range += "Atual"
			
			course_name = f"{course.attrib['NOME-CURSO']}. (Carga horária: {course.attrib['CARGA-HORARIA']}h)."
			if course.tag == 'FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA':
				course_name = f"Extensão universitária em {course_name}"
			
			institution = course.attrib['NOME-INSTITUICAO']
		
			info['year_range'].append(year_range)
			info['course_name'].append(course_name)
			info['institution'].append(institution)

		info_df = self.sort_by_key(info, "year_range", ascending=False)

		return info_df

	def get_authors_string(self, xml_child):
		authors_string = ""
		authors = xml_child.findall(f".//AUTORES")
		for pos, author in enumerate(authors):
			if pos != 0:
				authors_string += '; '
			authors_string += author.attrib['NOME-PARA-CITACAO']

		return authors_string

	# def get_other_technical_productions(self):
	# 	# Find the tag
	# 	xml_path = 'DEMAIS-TIPOS-DE-PRODUCAO-TECNICA'
	# 	productions = self.xml_file.find(f".//{xml_path}")

	# 	info = {'authors': [], 'year': [], 'title': [], 'production_type': [], 'level': []}
	# 	for production in productions:
	# 		if production.tag != 'APRESENTACAO-DE-TRABALHO':
	# 			year = None
	# 			title = None
	# 			production_type = None
	# 			level = None
	# 			for tag in production:
	# 				if 'DADOS-BASICOS' in tag.tag:
	# 					year = tag.attrib['ANO']
	# 					title = tag.attrib['TITULO']
	# 					production_type = production.tag.replace('-', ' ').capitalize()
	# 					if 'NIVEL-DO-CURSO' in tag.attrib.keys():
	# 						level = tag.attrib['NIVEL-DO-CURSO']

	# 			info['authors'].append(self.get_authors_string(production))
	# 			info['year'].append(year)
	# 			info['title'].append(title)
	# 			info['production_type'].append(production_type)
	# 			info['level'].append(level)

	# 	print(info)

	# 	info_df = self.sort_by_key(info, "year", ascending=False)

	# 	return info_df

	# <AUTORES 
	# 	NOME-PARA-CITACAO

	# <DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO
	# 	NIVEL-DO-CURSO="EXTENSAO" 
	# 	TITULO
	# 	ANO

	# NOME-PARA-CITACAO. TITULO. ANO. Curso de curta duração ministrado/Extensão)

	# def get_registers(self):
	# 	# Find the tag
	# 	xml_path = 'REGISTRO-OU-PATENTE'
	# 	registers = self.xml_file.findall(f".//{xml_path}")

	# 	info = {'authors': [], 'year': [], 'title': [], 'register_type': [], 'level': []}
	# 	for register in registers:
	# 		if register.tag != 'APRESENTACAO-DE-TRABALHO':
	# 			year = None
	# 			title = None
	# 			register_type = None
	# 			level = None
	# 			for tag in register:
	# 				if 'DADOS-BASICOS' in tag.tag:
	# 					year = tag.attrib['ANO']
	# 					title = tag.attrib['TITULO']
	# 					register_type = register.tag.replace('-', ' ').capitalize()
	# 					if 'NIVEL-DO-CURSO' in tag.attrib.keys():
	# 						level = tag.attrib['NIVEL-DO-CURSO']

	# 			info['authors'].append(self.get_authors_string(register))
	# 			info['year'].append(year)
	# 			info['title'].append(title)
	# 			info['register_type'].append(register_type)
	# 			info['level'].append(level)

	# 	print(info)

	# 	info_df = self.sort_by_key(info, "year", ascending=False)

	# 	return info_df