from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ListProperty, BooleanProperty
from assets.mainPage import MainPageLayout
from assets.addTask import AddTaskLayout


import numpy as np
import json

'''
tasks
	-> O Manager cuidará de todos os processos de escrever e salvar no arquivo json principal. Para
	que as outras seções possam acessar e manipular os dados, devem copiar os dados do Manager, e para
	alterar os dados devem chamar uma função do Manager do qual trate de adicionar, tirar ou alterar os dados.
	Caso algum dado seja alterado, adicionado, ou eliminado, todas as seções que dependem desses dados devem ser notificadas
	pelo Manager para que possam novamente copiar os dados novos.
	-> adicionar um método que, ao mudar o arquivo json, em epecial a agenda, ordenar as tarefas por data
'''

Builder.load_string("""
<Manager>:
	MainPageScreen:
		name:'mainpagescreen'
		id:mps
	AddTaskScreen:
		name:'addtaskscreen'
		id:ats

<MainPageScreen>:
	MainPageLayout:

<AddTaskScreen>:
	AddTaskLayout:

""")

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super(Manager,self).__init__(**kwargs)
		self.current = 'mainpagescreen'
		self.open(sort=True)

	def open(self,sort=False):
		with open('eventos.json', encoding="utf-8") as f:
			data = json.load(f)

		if sort == True:
			self.agenda = json_data_sorter(data, 'agenda')		
		else:
			self.agenda = data['agenda']
		self.extra = data['extra']
		self.eventos = data['eventos']

	def write(self, string):
		with open("eventos.json", "w") as f:
			f.write(json.dumps(string, indent=4))

		self.open(sort=True)

		self.notify()

	def notify(self):
		'''
		Manager muda a propriedade change in data da página principal e da página de adicionar
		tarefas, pois estas dependem do conteúdo do json.
		Quando a propriedade muda, a classe detentora desta propriedade executa uma função para
		atualizar seus parâmetros
		'''
		self.ids.mps.change_in_data = True
		self.ids.ats.change_in_data = True


class MainPageScreen(Screen):
	change_in_data = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(MainPageScreen,self).__init__(**kwargs)
		# self.App auxiliará a acessar o root/Manager em outras funções
		self.App = App.get_running_app()
		# change in data é colocado como true para que a classe saiba que precisa atualizar os dados
		self.newc = None
		self.data = ...	

	def on_enter(self, *args):
		# no exato momento de enter, MainPageScreen não possui widgets childrens, portanto
		# configure_screen é agendado para o ciclo
		Clock.schedule_once(self.configure_screen,0)

	def configure_screen(self, *args, **kwargs):
		# dá aos botões suas funcionalidades
		self.children[0].ids.b1.bind(on_release=self.changeCurrent('addtaskscreen'))
		# requisita uma atualização nos dados
		self.change_in_data = True		

	def on_change_in_data(self, *args):
		# sempre que change in data for modificado esta função será chamada
		if self.change_in_data == True:
			'''
			se change in data for True, significa que os dados precisam ser requisitados do manager
			assim que os dados são atualizados, change in data é alterado para false, chamando novamente esta
			função entretanto dessa vez sem passar for nenhuma condição
			no caso de mainpagescreen, se os dados mudam, a agenda deve ser carregada novamente
			'''
			self.data = self.App.root.agenda
			self.change_in_data = False
			self.load_agenda()

	def changeCurrent(self,newc, *args):
		# modifica newc para que change saiba para qual tela mudar
		self.newc = newc
		return self.change

	def load_agenda(self):
		# define uma variavel para identificar o grid de dados
		datagrid = self.children[0].ids.data
		# verifica se há dados já escritos no grid de dados, e limpa os dados se necessário
		if len(datagrid.children) != 0:
			datagrid.clear_widgets()
		for c in self.data:
			c = c.replace("\t"," ")
			datagrid.add_widget(Label(text=f'{c}'))
		datagrid.resize = 1

	def change(self, *args):
		# chama o Manager para que este troque de tela
		self.App.root.current = self.newc


class AddTaskScreen(Screen):
	change_in_data = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(AddTaskScreen,self).__init__(**kwargs)
		self.App = App.get_running_app()
		self.eventos = ...
		self.extras = ...
		self.data = ...

	def on_enter(self, *args):
		Clock.schedule_once(self.bindings,0)

	def bindings(self, *args, **kwargs):
		# adiciona as funcionalidades dos botões
		ids_selector = self.children[0].ids
		ids_selector.back.bind(on_release=self.back)
		ids_selector.commit.bind(on_release=self.commit)
		# requisita uma mudança nos dados
		self.change_in_data = True
				
	def back(self, *args):
		'''volta para a tela principal'''
		self.App.root.current = 'mainpagescreen'

	def on_change_in_data(self, *args):
		if self.change_in_data == True:
			'''
			Carrega as informações do json que foram salvas em Manager
			atualiza as coleções de eventos e extras
			muda change in data para false
			'''

			self.eventos = self.App.root.eventos
			self.extras = self.App.root.extra
			self.data = self.App.root.agenda
			ids_selector = self.children[0].ids
			ids_selector.eb.collection = self.eventos
			ids_selector.ab.collection = self.extras
			
			self.change_in_data = False

	def commit(self, *args):
		'''
		Armazena em variáveis as opções selecionadas e as formata
		A string formatada é então usada para criar um dicionario que é enviado para
		o Manager poder alterar as informações no json, atualizar seus dados e notificar
		classes dependentes destas informações que devem atualizar os seus dados novamente
		'''
		ids_selector = self.children[0].ids
		dia = ids_selector.dia.text
		mes = ids_selector.mes.text
		ano = ids_selector.ano.text
		evento = ids_selector.eb.text
		extra = ids_selector.ab.text
		string = f'{evento}\t{extra}\t{dia}/{mes}/{ano}'

		self.data.append(string)
		new = {"eventos":self.eventos,"extra":self.extras,"agenda":self.data}
		self.App.root.write(new)

class MyApp(App):
	def build(self):
		return Manager()


def json_data_sorter(data, key, sep='/'):
	l = list()
	eventos = list()
	for i,date in enumerate(data[key]):
		d = date.split(sep)
		eventos.append(d[0][0:-2])
		d[0] = d[0][-2:]
		d.append(i)
		l.append(tuple(d))


	b = np.array(l, dtype=[('day', int), ('month', int), ('year', int), ('id', int)])
	b = np.sort(b, axis=0, order=['year','month','day'])
	
	flist = list()

	for element in b:
		event = eventos[element[-1]]
		date = f'{element[0]}{sep}{element[1]}{sep}{element[2]}'
		flist.append(f'{event}\t{date}')

	return flist


if __name__ == '__main__':
	MyApp().run()

