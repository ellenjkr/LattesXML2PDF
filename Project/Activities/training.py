class Training():
	def __init__(self, xml_content):
		super(Training, self).__init__()
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
		activity_string = "Treinamentos ministrados"
		if activity_info['agency'] != "":
			activity_string += ", " + activity_info['agency']
		if activity_info['unit'] != "":
			activity_string += ", " + activity_info['unit']

		if activity_info['trainings'] is not None:
			activity_string += f"\n\nTreinamentos ministrados\n{activity_info['trainings']}"

		table_content = {'year_range': activity_info['year_range'], 'content': activity_string}

		return table_content

	def get_trainings(self, activity):
		trainings = activity.findall('.//TREINAMENTO')
		if trainings != []:
			trainings_list = []
			for training in trainings:
				trainings_list.append(training.text)
			
			trainings_string = "\n".join(trainings_list)
			return trainings_string
		else:
			return None

	def get_info(self, activity):
		info = {'year_range': [], 'agency': [], 'unit': []}
		
		info['year_range'] = self.get_year_range(activity)
		info['agency'] = activity.attrib['NOME-ORGAO']
		info['unit'] = activity.attrib['NOME-UNIDADE']

		info['trainings'] = self.get_trainings(activity)
	
		return info
		
	def get_activities_list(self):
		activities_list = []

		for activity in self.xml_content:
			activity_info = self.get_info(activity)
			table_content = self.get_table_content(activity_info)

			activities_list.append(table_content)

		return activities_list