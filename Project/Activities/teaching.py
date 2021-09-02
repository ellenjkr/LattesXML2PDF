class Teaching():
	def __init__(self, xml_content):
		super(Teaching, self).__init__()
		self.xml_content = xml_content
	
	def get_year_range(self, activity):
		start_month = activity.attrib['MES-INICIO']
		start_year = activity.attrib['ANO-INICIO']
		end_month = activity.attrib['MES-FIM']
		end_year = activity.attrib['ANO-FIM']

		start = f"{start_month}/{start_year}"
		end = f"{end_month}/{end_year}"

		year_range = f"{start} - {end}"
		if year_range[-1] == "/": # If "ANO-FIM" == ""
			year_range = year_range.replace(' /', ' ')
			year_range += "Atual"

		return year_range

	def get_table_content(self, activity_info):
		activity_string = "Ensino"
		if activity_info['major'] != "":
			activity_string += ", " + activity_info['major']
		if activity_info['level'] != "":
			activity_string += ", " + activity_info['level']

		if activity_info['subjects'] is not None:
			activity_string += f"\n\nDisciplinas ministradas\n{activity_info['subjects']}"

		table_content = {'year_range': activity_info['year_range'], 'content': activity_string}

		return table_content

	def get_subjects(self, activity):
		subjects = activity.findall('.//DISCIPLINA')
		if subjects != []:
			subjects_list = []
			for subject in subjects:
				subjects_list.append(subject.text)
			
			subjects_string = "\n".join(subjects_list)
			return subjects_string
		else:
			return None

	def get_info(self, activity):
		info = {'year_range': [], 'major': [], 'level': []}
		
		info['year_range'] = self.get_year_range(activity)
		info['major'] = activity.attrib['NOME-CURSO']
		
		level = activity.attrib['TIPO-ENSINO'].capitalize()
		if level == 'Graduacao':
			level = "Graduação"
		info['level'] = f"Nível: {level}"

		info['subjects'] = self.get_subjects(activity)
	
		return info
		
	def get_activities_list(self):
		activities_list = []

		for activity in self.xml_content:
			activity_info = self.get_info(activity)
			table_content = self.get_table_content(activity_info)

			activities_list.append(table_content)

		return activities_list