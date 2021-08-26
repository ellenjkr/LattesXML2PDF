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
		bonds = {'bond': [], 'other_occupation': [], 'hours': [], 'regime': [], 'year_range': [], 'other_info': []}
		# These other activities (other bonds) are placed on a different part of the resume
		other_professional_activities = ['Membro de corpo editorial', 'Membro de comitê de assessoramento', 'Membro de comitê assessor', 'Revisor de periódico', 'Revisor de projeto de fomento']

		bond_content = xml_content.findall(".//VINCULOS")
		for bond_info in bond_content:
			if bond_info.attrib['OUTRO-VINCULO-INFORMADO'] == "": # This attribute holds the other_professional_activities bonds
				year_range = self.get_year_range(bond_info)
				bond = bond_info.attrib['TIPO-DE-VINCULO']
				other_occupation = bond_info.attrib['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO']
				hours = bond_info.attrib['CARGA-HORARIA-SEMANAL']
				
				regime = bond_info.attrib['FLAG-DEDICACAO-EXCLUSIVA']
				if regime == 'SIM':
					regime = 'Dedicação exclusiva'
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
					hours = bond_info.attrib['CARGA-HORARIA-SEMANAL']

					regime = bond_info.attrib['FLAG-DEDICACAO-EXCLUSIVA']
					if regime == 'SIM':
						regime = 'Dedicação exclusiva'
					else:
						regime = ''

					other_info = bond_info.attrib['OUTRAS-INFORMACOES']

					bonds['bond'].append(bond)
					bonds['other_occupation'].append(other_occupation)
					bonds['hours'].append(hours)
					bonds['regime'].append(regime)
					bonds['year_range'].append(year_range)
					bonds['other_info'].append(other_info)

		if all(key_list == [] for key_list in bonds.values()): # If the whole dictionary is empty return nothing
			return None
		else:
			return bonds

	def get_activities(self, xml_content):
		activities = {}

		activities_dict = {}
		activities_dict['ATIVIDADES-DE-PESQUISA-E-DESENVOLVIMENTO'] = 'Pesquisa e desenvolvimento'
		activities_dict['ATIVIDADES-DE-ESTAGIO'] = 'Estágios'
		activities_dict['ATIVIDADES-DE-ENSINO'] = 'Ensino'
		activities_dict['ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO'] = 'Direção e administração'
		activities_dict['ATIVIDADES-DE-TREINAMENTO-MINISTRADO'] = 'Treinamentos ministrados'
		activities_dict['ATIVIDADES-DE-CONSELHO-COMISSAO-E-CONSULTORIA'] = 'Conselhos, Comissões e Consultoria'
		activities_dict['OUTRAS-ATIVIDADES-TECNICO-CIENTIFICA'] = 'Outras atividades técnico-científicas'


		# MES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# estagio

		# year_range	Estágios , Departamento de Desenvolvimento de Produtos, Automação da Manufatura.

		# 		Estágio realizado
		# 		Desenvolvimento de software de supervis�o industrial.

		# NOME-ORGAO="Departamento de Desenvolvimento de Produtos"
		# NOME-UNIDADE="Automa��o da Manufatura"
		# ESTAGIO-REALIZADO="Desenvolvimento de software de supervis�o industrial"

		# ==================================================================================

		# MES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# conselho comissao e consultoria

		# year_range	Conselhos, Comissões e Consultoria, Departamento de Desenvolvimento de Produtos, Automação da Manufatura.

		# 		Cargo ou função
		# 		Vice-Coordenador.

		# NOME-ORGAO="CECCI - Comiss�o Especial de Concep��o de Circuitos e Sistemas Integrados"
		# NOME-UNIDADE=""
		# ESPECIFICACAO="Vice-Coordenador"

		# ==================================================================================

		# MES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# Outras atividades técnico-científicas

		# year_range	Outras atividades técnico-científicas, Representa��o Institucional UNIVALI, Representa��o Institucional UNIVALI.

		# 		Atividade realizada
		# 		Representante Institucional da SBC na Universidade do Vale do Itaja�

		# NOME-ORGAO="Representa��o Institucional UNIVALI"
		# NOME-UNIDADE="Representa��o Institucional UNIVALI"
		# ATIVIDADE-REALIZADA="Representante Institucional da SBC na Universidade do Vale do Itaja�"

		# ==================================================================================

		# MES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# Pesquisa e desenvolvimento

		# year_range	Pesquisa e desenvolvimento, Centro Tecnol�gico, Departamento de Engenharia El�trica

		# NOME-ORGAO="Centro Tecnol�gico"
		# NOME-UNIDADE="Departamento de Engenharia El�trica"

		# ==================================================================================

		# MES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# Ensino

		# year_range	Ensino, Ci�ncia da Computa��o, Nível: Graduação

		# 		Disciplinas ministradas
		# 		Arquitetura de Computadores
		# 		Circuitos Digitais

		# TIPO-ENSINO="GRADUACAO"
		# NOME-CURSO="Ci�ncia da Computa��o"
		# <DISCIPLINA SEQUENCIA-ESPECIFICACAO="1">Arquitetura de Computadores</DISCIPLINA>

		# ==================================================================================

		# ES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# Treinamentos ministrados

		# year_range	Treinamentos ministrados, Pr� Reitoria de Ensino, Se��o Pedag�gica do Cttmar.

		# 		Treinamentos ministrados
		# 		Programa de Forma��o Continuada para Docentes do Ensino Superior da UNIVALI - Tem�tica: Metodologia da Pesquisa Cient�fica - Curso: Professor Marcante (4 h/a)


		# NOME-ORGAO="Pr� Reitoria de Ensino"
		# NOME-UNIDADE="Se��o Pedag�gica do Cttmar"
		# <TREINAMENTO SEQUENCIA-ESPECIFICACAO="1">Programa de Forma��o Continuada para Docentes do Ensino Superior da UNIVALI - Tem�tica: Metodologia da Pesquisa Cient�fica - Curso: Professor Marcante (4 h/a)</TREINAMENTO>

		# ==================================================================================

		# ES-INICIO="1" ANO-INICIO="1993" MES-FIM="7" ANO-FIM="1993"


		# Direção e administração

		# year_range	Direção e administração, Vice-Reitoria de Pesquisa, P�s-Gradua��o e Inova��o

		# 		Cargo ou função
		# 		Gerente de Pesquisa e P�s-Gradua��o (Portaria No 190/2018)


		# NOME-ORGAO="Vice-Reitoria de Pesquisa, P�s-Gradua��o e Inova��o"
		# CARGO-OU-FUNCAO="Gerente de Pesquisa e P�s-Gradua��o (Portaria No 190/2018)"

		# ==================================================================================

			
	def get_professional_activities(self):
		# Find the tag
		xml_path = 'ATUACAO-PROFISSIONAL'
		xml_content = self.xml_file.findall(f".//{xml_path}")

		all_professional_activities = []

		for tag in xml_content:
			bonds = self.get_bonds(tag)
			if bonds is not None:
				activities = self.get_activities(tag)

				professional_activity = {'Vínculo institucional': None, 'Atividades': None}
				professional_activity['Vínculo institucional'] = bonds
				professional_activity['Atividades'] = activities

				all_professional_activities.append(professional_activity)

		# info_df = self.sort_by_key(info, "year_range", ascending=False)
		
		# return info_df