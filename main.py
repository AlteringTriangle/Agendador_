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

import json


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
		self.open()

	def open(self):
		with open('eventos.json', encoding="utf-8") as f:
			data = json.load(f)
		self.agenda = data['agenda']
		self.extra = data['extra']
		self.eventos = data['eventos']

	def write(self, string):
		with open("eventos.json", "w") as f:
			f.write(json.dumps(string, indent=4))

		self.notify()

	def notify(self):
		self.ids.mps.change_in_data = True
		self.ids.mps.change_in_data = True


class MainPageScreen(Screen):
	def __init__(self, **kwargs):
		super(MainPageScreen,self).__init__(**kwargs)
		self.App = App.get_running_app()
		self.newc = None
		self.data = ...
		

	def on_enter(self, *args):
		Clock.schedule_once(self.letmesee,0)

	def letmesee(self, *args, **kwargs):
		self.children[0].ids.b1.bind(on_release=self.changeCurrent('addtaskscreen'))
		self.load_agenda()

	def changeCurrent(self,newc, *args):
		self.newc = newc
		return self.change

	def load_agenda(self):
		# atualiza os dados da agenda
		self.data = App.get_running_app().root.agenda
		# define a variavel do grid de dados
		datagrid = self.children[0].ids.data

		# verifica se há mais dados do que a demonstração anterior
		numeros_de_linhas = len(datagrid.children)
		numero_de_dados = len(self.data)
		if numero_de_dados > numeros_de_linhas:
			if len(datagrid.children) != 0:
				datagrid.clear_widgets()
			for c in self.data:
				c = c.replace("\t"," ")
				datagrid.add_widget(Label(text=f'{c}'))
			datagrid.resize = 1


	def change(self, *args):
		self.App.root.current = self.newc


class AddTaskScreen(Screen):
	def __init__(self, **kwargs):
		super(AddTaskScreen,self).__init__(**kwargs)
		self.App = App.get_running_app()
		self.eventos = ...
		self.extras = ...
		self.data = ...

	def on_enter(self, *args):
		Clock.schedule_once(self.bindings,0)

	def bindings(self, *args, **kwargs):
		# da bind nos botoes de voltar e adicionar tarefas
		# também atualiza as colecões de eventos e extras
		ids_selector = self.children[0].ids
		ids_selector.back.bind(on_release=self.back)
		ids_selector.commit.bind(on_release=self.commit)
		self.open()

		ids_selector.eb.collection = self.eventos
		ids_selector.ab.collection = self.extras
		
	def back(self, *args):
		# volta para a tela principal
		self.App.root.current = 'mainpagescreen'

	def open(self):
		# Carrega as informações do json que foram salvas em Manager
		self.eventos = self.App.root.eventos
		self.extras = self.App.root.extra
		self.data = self.App.root.agenda

	def commit(self, *args):
		# guarda o texto do dia/mes/ano do evento
		ids_selector = self.children[0].ids
		dia = ids_selector.dia.text
		mes = ids_selector.mes.text
		ano = ids_selector.ano.text
		# guarda o evento e o extra
		evento = ids_selector.eb.text
		extra = ids_selector.ab.text
		# formata as informações
		string = f'{evento}\t{extra}\t{dia}/{mes}/{ano}'
		# adiciona a informações a data
		self.data.append(string)
		# salva as alterações no arquivo
		new = {"eventos":self.eventos,"extra":self.extras,"agenda":self.data}

		self.App.root.write(new)
		self.open()

		print(string)

class MyApp(App):
	def build(self):
		return Manager()


if __name__ == '__main__':
	MyApp().run()

