from Activities.advice_commissions_consulting import Advice_Commission_Consulting
from Activities.dir_mgmt import Direction_Management
from Activities.internship import Intership
from Activities.research import Research
from Activities.teaching import Teaching
from Activities.technical_scientific import TechnicalScientific
from Activities.training import Training


class ProfessionalActivities():
	def __init__(self, xml_file):
		super(ProfessionalActivities, self).__init__()
		self.xml_file = xml_file
		
		self.professional_activities = self.get_professional_activities()

	def get_year_range(self, bond_info):
		start_month = bond_info.attrib['MES-INICIO']
		start_year = bond_info.attrib['ANO-INICIO']
		end_month = bond_info.attrib['MES-FIM']
		end_year = bond_info.attrib['ANO-FIM']

		start = f"{start_month}/{start_year}"
		end = f"{end_month}/{end_year}"

		year_range = f"{start} - {end}"
		if year_range[-1] == "/": # If "ANO-FIM" == ""
			year_range = year_range.replace(' /', ' ')
			year_range += "Atual"

		return year_range

	def get_bonds_table_content(self, bonds):
		# bonds = {'bond': [], 'other_occupation': [], 'hours': [], 'regime': [], 'year_range': [], 'other_info': []}
		
		bonds_table_content = []
		for pos, bond in enumerate(bonds['bond']):
			bond_dict = {'year_range': bonds['year_range'][pos], 'content': None}
			info_list = [bonds[key][pos] for key in bonds.keys() if key not in ['year_range', 'other_info'] and bonds[key][pos] != ""]

			info_string = ", ".join(info_list)

			bond_dict['content'] = info_string
			if bonds['other_info'][pos] != "":
				bond_dict['second_line'] = 'Outras informações'
				bond_dict['second_line_content'] = bonds['other_info'][pos]

			bonds_table_content.append(bond_dict)

		return bonds_table_content

	def get_bonds(self, xml_content):
		bonds = {'bond': [], 'other_occupation': [], 'hours': [], 'regime': [], 'year_range': [], 'other_info': []}
		# These other activities (other bonds) are placed on a different part of the resume
		other_professional_activities = ['Membro de corpo editorial', 'Membro de comitê de assessoramento', 'Membro de comitê assessor', 'Revisor de periódico', 'Revisor de projeto de fomento']

		bond_content = xml_content.findall(".//VINCULOS")
		for bond_info in bond_content:
			if bond_info.attrib['OUTRO-VINCULO-INFORMADO'] == "": # This attribute holds the other_professional_activities bonds
				year_range = self.get_year_range(bond_info)
				bond = f"Vínculo: {bond_info.attrib['TIPO-DE-VINCULO'].capitalize()}"
				other_occupation = bond_info.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']
				if other_occupation != "":
					other_occupation = f"Enquadramento Funcional: {other_occupation}"
				hours = bond_info.attrib['CARGA-HORARIA-SEMANAL']
				if hours != "":
					hours = f"Carga horária: {hours}"
				
				regime = bond_info.attrib['FLAG-DEDICACAO-EXCLUSIVA']
				if regime == 'SIM':
					regime = 'Regime: Dedicação exclusiva'
				else:
					regime = ''

				other_info = bond_info.attrib['OUTRAS-INFORMACOES']

				bonds['bond'].append(bond)
				bonds['other_occupation'].append(other_occupation)
				bonds['hours'].append(hours)
				bonds['regime'].append(regime)
				bonds['year_range'].append(year_range)
				bonds['other_info'].append(other_info)
			else:
				bond = bond_info.attrib['OUTRO-VINCULO-INFORMADO']
				
				# Verify if the bond is one of the other_professional_activities, otherwise the bond is added
				if bond not in other_professional_activities:
					year_range = self.get_year_range(bond_info)
					other_occupation = bond_info.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']
					if other_occupation != "":
						other_occupation = f"Enquadramento Funcional: {other_occupation}"
					hours = bond_info.attrib['CARGA-HORARIA-SEMANAL']
					if hours != "":
						hours = f"Carga horária: {hours}"

					regime = bond_info.attrib['FLAG-DEDICACAO-EXCLUSIVA']
					if regime == 'SIM':
						regime = 'Regime: Dedicação exclusiva'
					else:
						regime = ''

					other_info = bond_info.attrib['OUTRAS-INFORMACOES']

					bonds['bond'].append(f"Vínculo: {bond.capitalize()}")
					bonds['other_occupation'].append(other_occupation)
					bonds['hours'].append(hours)
					bonds['regime'].append(regime)
					bonds['year_range'].append(year_range)
					bonds['other_info'].append(other_info)

		if all(key_list == [] for key_list in bonds.values()): # If the whole dictionary is empty return nothing
			return None
		else:
			bonds_table_content = self.get_bonds_table_content(bonds)

			return bonds_table_content

	def get_activities(self, xml_content):
		activities_table_content = [] # List with the activities 
		
		for tag in xml_content:
			if 'ATIVIDADES' in tag.tag: # If the tag is an activity
				# Get the activities of the type specified by tha tag name
				if tag.tag == 'ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO':
					activities_table_content.extend(Research(tag).get_activities_list())
				elif tag.tag == 'ATIVIDADES-DE-ESTAGIO':
					activities_table_content.extend(Intership(tag).get_activities_list())
				elif tag.tag == 'ATIVIDADES-DE-ENSINO':
					activities_table_content.extend(Teaching(tag).get_activities_list())
				elif tag.tag == 'ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO':
					activities_table_content.extend(Direction_Management(tag).get_activities_list())
				elif tag.tag == 'ATIVIDADES-DE-TREINAMENTO-MINISTRADO':
					activities_table_content.extend(Training(tag).get_activities_list())
				elif tag.tag == 'ATIVIDADES-DE-CONSELHO-COMISSAO-E-CONSULTORIA':
					activities_table_content.extend(Advice_Commission_Consulting(tag).get_activities_list())
				elif tag.tag == 'OUTRAS-ATIVIDADES-TECNICO-CIENTIFICA':
					activities_table_content.extend(TechnicalScientific(tag).get_activities_list())

		if activities_table_content != []:
			return activities_table_content
		else:
			return None

	def get_professional_activities(self):
		# Find the tag
		xml_path = 'ATUACAO-PROFISSIONAL'
		xml_content = self.xml_file.findall(f".//{xml_path}")

		all_professional_activities = []

		for tag in xml_content:
			bonds = self.get_bonds(tag)
			if bonds is not None:
				activities = self.get_activities(tag)

				professional_activity = {'institution': None, 'Vínculo institucional': None, 'Atividades': None}
				professional_activity['institution'] = tag.attrib['NOME-INSTITUICAO']
				professional_activity['Vínculo institucional'] = bonds
				professional_activity['Atividades'] = activities

				all_professional_activities.append(professional_activity)

		return all_professional_activities