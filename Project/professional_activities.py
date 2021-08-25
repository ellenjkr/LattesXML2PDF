import pandas as pd


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

	def get_bonds(self, xml_content):
		bonds = {'bond': [], 'other_occupation': [], 'year_range': [], 'other_info': []}
		# These other activities (other bonds) are placed on a different part of the resume
		other_professional_activities = ['Membro de corpo editorial', 'Membro de comitê de assessoramento', 'Membro de comitê assessor', 'Revisor de periódico', 'Revisor de projeto de fomento']

		bond_content = xml_content.findall(".//VINCULOS")
		for bond_info in bond_content:
			if bond_info.attrib['OUTRO-VINCULO-INFORMADO'] == "": # This attribute holds the other_professional_activities bonds
				year_range = self.get_year_range(bond_info)
				bond = bond_info.attrib['TIPO-DE-VINCULO']
				other_occupation = bond_info.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']
				other_info = bond_info.attrib['OUTRAS-INFORMACOES']

				bonds['bond'].append(bond)
				bonds['other_occupation'].append(other_occupation)
				bonds['year_range'].append(year_range)
				bonds['other_info'].append(other_info)
			else:
				bond = bond_info.attrib['OUTRO-VINCULO-INFORMADO']
				
				# Verify if the bond is one of the other_professional_activities, otherwise the bond is added
				if bond not in other_professional_activities:
					year_range = self.get_year_range(bond_info)
					other_occupation = bond_info.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']
					other_info = bond_info.attrib['OUTRAS-INFORMACOES']

					bonds['bond'].append(bond)
					bonds['other_occupation'].append(other_occupation)
					bonds['year_range'].append(year_range)
					bonds['other_info'].append(other_info)

		if all(key_list == [] for key_list in bonds.values()): # If the whole dictionary is empty return nothing
			return None
		else:
			print(xml_content.attrib['NOME-INSTITUICAO'], bonds)
			print()
			print()
			return bonds
			
	def get_professional_activities(self):
		# Find the tag
		xml_path = 'ATUACAO-PROFISSIONAL'
		xml_content = self.xml_file.findall(f".//{xml_path}")

		activities = {}
		professional_activity = {'Vínculo institucional': [], 'Atividades': []}
		all_professional_activities = []

		for tag in xml_content:
			bonds = self.get_bonds(tag)
			if bonds is not None:
				pass

		# info_df = self.sort_by_key(info, "year_range", ascending=False)
		
		# return info_df