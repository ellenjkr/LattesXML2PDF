import pandas as pd


class Projects():
	def __init__(self, xml_file):
		super(Projects, self).__init__()
		self.xml_file = xml_file

		projects = self.get_projects()
		self.projects_dict = {} 
		self.projects_dict["Projetos de pesquisa"] = self.select_by_nature(projects, "PESQUISA")
		self.projects_dict["Projetos de extensão"] = self.select_by_nature(projects, "EXTENSAO")
		self.projects_dict["Projetos de desenvolvimento"] = self.select_by_nature(projects, "DESENVOLVIMENTO")
		self.projects_dict["Outros Projetos"] = self.select_by_nature(projects, "OUTRA")
	
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

	def get_projects(self):
		# Find the tag
		xml_path = 'PROJETO-DE-PESQUISA'
		researches = self.xml_file.findall(f".//{xml_path}")

		info = {'year_range': [], 'title': [], 'description': [], 'situation/nature': [], 'students': [], 'members': [], 'financiers': [], 'num_of_productions': [], "nature": []}

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
			info["nature"].append(research.attrib['NATUREZA'])

		info_df = self.sort_by_key(info, "year_range", ascending=False)
		
		return info_df

	def select_by_nature(self, projects, nature):
		filtered_projects = projects.loc[projects["nature"] == nature]
		filtered_projects.reset_index(drop=True, inplace=True)

		return filtered_projects
		