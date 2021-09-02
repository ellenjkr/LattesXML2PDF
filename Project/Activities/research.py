class Research():
	def __init__(self, xml_content):
		super(Research, self).__init__()
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
		activity_string = "Pesquisa e desenvolvimento"
		if activity_info['agency'] != "":
			activity_string += ", " + activity_info['agency']
		if activity_info['unit'] != "":
			activity_string += ", " + activity_info['unit']

		if activity_info['researches'] is not None:
			activity_string += f"\n\nLinhas de pesquisa\n{activity_info['researches']}"

		table_content = {'year_range': activity_info['year_range'], 'content': activity_string}

		return table_content

	def get_researches(self, activity):
		researches = activity.findall('.//LINHA-DE-PESQUISA')
		if researches != []:
			researches_list = []
			for research in researches:
				researches_list.append(research.attrib['TITULO-DA-LINHA-DE-PESQUISA'])
			
			researches_string = "\n".join(researches_list)
			return researches_string
		else:
			return None

	def get_info(self, activity):
		info = {'year_range': [], 'agency': [], 'unit': []}
		
		info['year_range'] = self.get_year_range(activity)
		info['agency'] = activity.attrib['NOME-ORGAO']
		info['unit'] = activity.attrib['NOME-UNIDADE']

		info['researches'] = self.get_researches(activity)
	
		return info
		
	def get_activities_list(self):
		activities_list = []

		for activity in self.xml_content:
			activity_info = self.get_info(activity)
			table_content = self.get_table_content(activity_info)

			activities_list.append(table_content)

		return activities_list