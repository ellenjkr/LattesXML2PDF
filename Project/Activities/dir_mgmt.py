class Direction_Management():
	def __init__(self, xml_content):
		super(Direction_Management, self).__init__()
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
		activity_string = "Direção e administração"
		if activity_info['agency'] != "":
			activity_string += ", " + activity_info['agency']

		activity_string += "\n\n"
		activity_string += "Cargo ou função\n"
		activity_string += activity_info['role']

		table_content = {'year_range': activity_info['year_range'], 'content': activity_string}

		return table_content

	def get_info(self, activity):
		info = {'year_range': [], 'agency': [], 'role': []}
		
		info['year_range'] = self.get_year_range(activity)
		info['agency'] = activity.attrib['NOME-ORGAO']
		info['role'] = activity.attrib['CARGO-OU-FUNCAO']

		return info
		
	def get_activities_list(self):
		activities_list = []

		for activity in self.xml_content:
			activity_info = self.get_info(activity)
			table_content = self.get_table_content(activity_info)

			activities_list.append(table_content)

		return activities_list