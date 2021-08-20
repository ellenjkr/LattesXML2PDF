import pandas as pd


class OtherProfessionalActivities():
	def __init__(self, xml_file):
		super(OtherProfessionalActivities, self).__init__()
		self.xml_file = xml_file

		activities = self.get_other_professional_activities()
		self.activities_dict = {}
		self.activities_dict["Membro de corpo editorial"] = self.select_by_bond(activities, "Membro de corpo editorial")
		self.activities_dict["Membro de comitê de assessoramento"] = self.select_by_bond(activities, "Membro de comitê assessor")
		self.activities_dict["Revisor de periódico"] = self.select_by_bond(activities, "Revisor de periódico")
		self.activities_dict["Revisor de projeto de fomento"] = self.select_by_bond(activities, "Revisor de projeto de fomento")
		
	def sort_by_key(self, data_dict, key, ascending=True):
		data_df = pd.DataFrame(data_dict)
		data_df.sort_values(by=[key], inplace=True, ascending=ascending)
		data_df.reset_index(drop=True, inplace=True)

		return data_df

	def get_other_professional_activities(self):
		# Find the tag
		xml_path = 'ATUACAO-PROFISSIONAL'
		xml_content = self.xml_file.findall(f".//{xml_path}")

		info = {'institution': [], 'year_range': [], 'bond': []}

		for tag in xml_content:
			bond_content = tag.findall(".//VINCULOS")
			
			for bond_info in bond_content:
				if "OUTRO-VINCULO-INFORMADO" in bond_info.attrib.keys(): # The "ATUACAO-PROFISSIONAL" tag for this type of content has to have the "OUTRO-VINCULO-INFORMADO" tag
					if bond_info.attrib['OUTRO-VINCULO-INFORMADO'] != "":
						bond = bond_info.attrib['OUTRO-VINCULO-INFORMADO']
						institution = tag.attrib['NOME-INSTITUICAO']
						# if bond_content != []: 
						print(tag.attrib.keys())
						year_range = f"{bond_info.attrib['ANO-INICIO']} - {bond_info.attrib['ANO-FIM']}"
						if year_range[-1] == " ": # If "ANO-FIM" == ""
							year_range += "Atual"

						info['institution'].append(institution)
						info['year_range'].append(year_range)
						info['bond'].append(bond)

		info_df = self.sort_by_key(info, "year_range", ascending=False)
		
		return info_df

	def select_by_bond(self, activities, bond):
		filtered_activities = activities.loc[activities["bond"] == bond]
		filtered_activities.reset_index(drop=True, inplace=True)

		return filtered_activities