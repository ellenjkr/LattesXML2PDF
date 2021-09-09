import pandas as pd


class Orientations():
	def __init__(self, xml_file):
		super(Orientations, self).__init__()
		self.xml_file = xml_file

		self.orientations_dict = {'Orientações e supervisões em andamento': self.get_orientations_in_progress(), 'Orientações e supervisões concluídas': self.get_finished_orientations()}

	def sort_by_key(self, data_dict, key, ascending=True):
		data_df = pd.DataFrame(data_dict)
		data_df.sort_values(by=[key], inplace=True, ascending=ascending)
		data_df.reset_index(drop=True, inplace=True)

		return data_df

	def get_inprogress_strings(self, orientation_type):
		orientations_strings = []
		for pos, orientation in enumerate(orientation_type['title']):
			if orientation_type['agency'][pos] == "":
				string = f"{orientation_type['student'][pos]}. {orientation}. Início: {orientation_type['year'][pos]}. {orientation_type['orientation_type'][pos]} em {orientation_type['course'][pos]} - {orientation_type['institution'][pos]}. ({orientation_type['type'][pos]})."
			else:
				string = f"{orientation_type['student'][pos]}. {orientation}. Início: {orientation_type['year'][pos]}. {orientation_type['orientation_type'][pos]} em {orientation_type['course'][pos]} - {orientation_type['institution'][pos]}, {orientation_type['agency'][pos]}. ({orientation_type['type'][pos]})."

			orientations_strings.append(string)

		return orientations_strings

	def get_orientations_in_progress(self):
		# Find the tag
		xml_path = 'ORIENTACOES-EM-ANDAMENTO'
		orientations = self.xml_file.find(f".//{xml_path}")

		types = {}  # Dictionary with the orientation types

		for orientation in orientations:
			for tag in orientation:
				if 'DADOS-BASICOS' in tag.tag:
					orientation_type = tag.attrib['NATUREZA']
					if orientation_type not in types.keys():  # Check if the orientation type is already a dictionary key
						types[orientation_type] = {'orientation_type': [], 'title': [], 'year': [], 'type': [], 'student': [], 'institution': [], 'agency': [], 'course': []}  # Add the orientation type to the dictionary

					types[orientation_type]['orientation_type'].append(orientation_type)
					types[orientation_type]['title'].append(tag.attrib['TITULO-DO-TRABALHO'])
					types[orientation_type]['year'].append(tag.attrib['ANO'])

				elif 'DETALHAMENTO' in tag.tag:
					if 'TIPO-DE-ORIENTACAO' in tag.attrib.keys():
						types[orientation_type]['type'].append(tag.attrib['TIPO-DE-ORIENTACAO'].replace('_', ' ').capitalize())
					else:
						types[orientation_type]['type'].append('Orientador')
					types[orientation_type]['student'].append(tag.attrib['NOME-DO-ORIENTANDO'])
					types[orientation_type]['institution'].append(tag.attrib['NOME-INSTITUICAO'])
					types[orientation_type]['agency'].append(tag.attrib['NOME-DA-AGENCIA'])
					types[orientation_type]['course'].append(tag.attrib['NOME-CURSO'])

		for orientation_type in types.keys():
			types[orientation_type] = self.sort_by_key(types[orientation_type], "year", ascending=False)  # Turn it into a dataframe and sort by year
			types[orientation_type] = self.get_inprogress_strings(types[orientation_type])  # Turn it into a list of strings

		return types

	def get_finished_strings(self, orientation_type):
		orientations_strings = []
		for pos, orientation in enumerate(orientation_type['title']):
			if orientation_type['agency'][pos] == "":
				string = f"{orientation_type['student'][pos]}. {orientation}. {orientation_type['year'][pos]}. ({orientation_type['orientation_type'][pos]} em {orientation_type['course'][pos]}) - {orientation_type['institution'][pos]}. ({orientation_type['type'][pos]})."
			else:
				string = f"{orientation_type['student'][pos]}. {orientation}. {orientation_type['year'][pos]}. ({orientation_type['orientation_type'][pos]} em {orientation_type['course'][pos]}) - {orientation_type['institution'][pos]}, {orientation_type['agency'][pos]}. ({orientation_type['type'][pos]})."

			orientations_strings.append(string)

		return orientations_strings

	def get_finished_orientations(self):
		# Find the tag
		xml_path = 'ORIENTACOES-CONCLUIDAS'
		orientations = self.xml_file.find(f".//{xml_path}")

		types = {}  # Dictionary with the orientation types

		for orientation in orientations:
			for tag in orientation:
				if 'DADOS-BASICOS' in tag.tag:
					orientation_type = tag.attrib['NATUREZA'].replace('_', ' ').capitalize()
					if orientation_type not in types.keys():  # Check if the orientation type is already a dictionary key
						types[orientation_type] = {'orientation_type': [], 'title': [], 'year': [], 'type': [], 'student': [], 'institution': [], 'agency': [], 'course': []}  # Add the orientation type to the dictionary

					types[orientation_type]['orientation_type'].append(orientation_type)
					types[orientation_type]['title'].append(tag.attrib['TITULO'])
					types[orientation_type]['year'].append(tag.attrib['ANO'])

				elif 'DETALHAMENTO' in tag.tag:
					if 'TIPO-DE-ORIENTACAO' in tag.attrib.keys():
						types[orientation_type]['type'].append(tag.attrib['TIPO-DE-ORIENTACAO'].replace('_', ' ').capitalize())
					else:
						types[orientation_type]['type'].append('Orientador')
					types[orientation_type]['student'].append(tag.attrib['NOME-DO-ORIENTADO'])
					types[orientation_type]['institution'].append(tag.attrib['NOME-DA-INSTITUICAO'])
					types[orientation_type]['agency'].append(tag.attrib['NOME-DA-AGENCIA'])
					types[orientation_type]['course'].append(tag.attrib['NOME-DO-CURSO'])

		for orientation_type in types.keys():
			types[orientation_type] = self.sort_by_key(types[orientation_type], "year", ascending=False)  # Turn it into a dataframe and sort by year
			types[orientation_type] = self.get_finished_strings(types[orientation_type])  # Turn it into a list of strings

		return types