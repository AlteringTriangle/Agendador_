


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ListProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window

from assets.mainPage import MainPageLayout, SwShLabel
from assets.addTask import AddTaskLayout
from assets.addee import AddEELayout

from numpy import array as nparray
from numpy import sort as npsort
import json




'''
tasks
	-> Finalizar o popup de adicionar extras e eventos
	-> Modificar as listas para que possam ser deslizadas para ver o nome completo do evento evitando
	o uso de textos adaptativos semelhantes aos botões 
	-> Dar funcionalidades ou excluir botoes de editar
		-> modificação de data para mainPage
		-> modificação de extra p/ evento ou vice e versa para addee
		-> modificação de nome de evento ou extra addee
'''

Builder.load_string("""
<Manager>:

	MainPageScreen:
	    name:'mainpagescreen'
	    id:mps
	AddTaskScreen:
	    name:'addtaskscreen'
	    id:ats
	AddEEScreen:
	    name:'addeescreen'
	    id:aees

<MainPageScreen>:
	MainPageLayout:

<AddTaskScreen>:
	AddTaskLayout:

<AddEEScreen>:
	AddEELayout:


<LabelScroll>
	height:60
	size_hint_x:None
	do_scroll_x:True
	SwShLabel:
		size_hint_x:None
		height:root.height
		width:root.width
		text:'placeholder'
		id:data
""")

class Manager(ScreenManager):

	def __init__(self, **kwargs):
		super(Manager,self).__init__(**kwargs)
		#self.current = 'mainpagescreen'
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
		self.ids.aees.change_in_data = True

	def remove_task(self, pos):
		self.agenda.pop(pos)
		new = {"eventos":self.eventos,"extra":self.extra,"agenda":self.agenda}
		self.write(new)

	def remove_event(self,pos):
		self.eventos.pop(pos)
		new = {"eventos":self.eventos,"extra":self.extra,"agenda":self.agenda}
		self.write(new)

	def remove_extra(self, pos):
		self.extra.pop(pos)
		new = {"eventos":self.eventos,"extra":self.extra,"agenda":self.agenda}
		self.write(new)

class MainPageScreen(Screen):
	change_in_data = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(MainPageScreen, self).__init__(**kwargs)
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
		self.children[0].ids.b1.bind(on_release=lambda x:self.change('addtaskscreen'))
		self.children[0].ids.b3.bind(on_release=lambda x:self.change('addeescreen'))
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

	def load_agenda(self):
		'''
		A agenda é um grid de dados contendo as informações do evento,
		e dois botoões para editar a data do evento e remover o evento 	
		'''
		# define uma variavel para identificar o grid de dados
		datagrid = self.children[0].ids.data
		# verifica se há dados já escritos no grid de dados, e limpa os dados se necessário
		if len(datagrid.children) != 0:
			datagrid.clear_widgets()
		for ind,c in enumerate(self.data):
			c = c.replace("\t"," ")
			widget = BoxLayout()


			label = LabelScroll()
			
			label.ids.data.text = f"{c}"
			rmbutton = IndexButton(index=ind,text='X', size_hint_x=.15)
			edbutton = IndexButton(index=ind, text='Editar', size_hint_x=.15)

			Clock.schedule_once(lambda x:print(widget.width,'\n->',rmbutton.width), 6)
			rmbutton.bind(on_press=lambda x: self.remove(x))


			widget.add_widget(SwShLabel(text=f'{c}'))
			# label.width = label.parent.width
			widget.add_widget(rmbutton)
			widget.add_widget(edbutton)
			datagrid.add_widget(widget)
		datagrid.resize = 1


	def change(self,newc, *args):
		# chama o Manager para que este troque de tela
		self.App.root.current = newc

	def remove(self, inst ,*args):
		# chama o Manager para que este remova a tarefa
		self.App.root.remove_task(inst.index)

class AddTaskScreen(Screen):
	change_in_data = BooleanProperty(False)
	def __init__(self, **kwargs):
		super(AddTaskScreen,self).__init__(**kwargs)
		self.App = App.get_running_app()
		self.eventos = ...
		self.extra = ...
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
			atualiza as coleções de eventos e extra
			muda change in data para false
			'''

			self.eventos = self.App.root.eventos
			self.extra = self.App.root.extra
			self.data = self.App.root.agenda
			ids_selector = self.children[0].ids
			ids_selector.eb.collection = self.eventos
			ids_selector.ab.collection = self.extra
			
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
		print(string)
		new = {"eventos":self.eventos,"extra":self.extra,"agenda":self.data}
		self.App.root.write(new)

class AddEEScreen(MainPageScreen):
	change_in_data = BooleanProperty(False)

	def on_pre_enter(self, *args, **kwargs):
		# como o add events extras não é a primeira página, não há necessidade de configurar 1 frame
		# após o aplicativo iniciar, e devido a herdar o layout e a classe da mainpage, antes de entrar
		# os nomes e as funções são modificados
		self.children[0].ids.b3.bind(on_release=lambda x:self.change('mainpagescreen'))
		self.children[0].ids.b1.bind(on_release=self.addevent)
		self.children[0].ids.b2.bind(on_release=self.addextra)
		self.children[0].ids.b3.text = "voltar"
		self.children[0].ids.b1.text = "adicionar evento"
		self.children[0].ids.b2.text = "adicionar extra"
		self.change_in_data = True	

	# limpando configure_screen para não dar a addeescreen as funcionalidades de mainpagescreen
	def configure_screen(self, *args):
		...

	def on_change_in_data(self, *args):
		if self.change_in_data == True:
			# os dados são uma mescla de eventos e extras
			self.data = [self.App.root.eventos[:-1], self.App.root.extra[:-1]]
			self.change_in_data = False
			Clock.schedule_once(self.load_agenda,0)
	def load_agenda(self, *args):
		datagrid = self.children[0].ids.data
		if len(datagrid.children) != 0:
			datagrid.clear_widgets()

		def func(prefix, c, rm_type='event'):
			widget = BoxLayout()
			widget.add_widget(Label(text=f'{prefix}{c}'))
			rmbutton = IndexButton(index=ind,text='X', size_hint_x=.05)
			edbutton = IndexButton(index=ind, text='Editar',size_hint_x=.25)
			rmbutton.bind(on_press=lambda x: self.remove(x, rm_type))
			widget.add_widget(rmbutton)
			widget.add_widget(edbutton)
			datagrid.add_widget(widget)

		# para cada set de dados teremos uma lista própria
		for ind,c in enumerate(self.data[0]):
			func('Eventos -> ', c)
			
		for ind,c in enumerate(self.data[1]):
			func('Extras -> ', c, 'extra')

		datagrid.resize = 1

	def add_base(self, *args):
		root = self.App.root
		box = BoxLayout(size_hint=[None,None],width=root.width/2,height=root.width/2,
			pos_hint={'center_y':.5,'center_x':.5}, orientation='vertical')
		text_input = TextInput(multiline=False)
		b = Button(text='close', on_release=lambda x:self.dismiss(x))
		box.add_widget(text_input)
		box.add_widget(b)
		self.add_widget(box)
		return text_input

	def addevent(self, *args):
		t = self.add_base()
		t.bind(on_text_validate=lambda x:self.commitevent(x))

	def addextra(self, *args):
		t = self.add_base()
		t.bind(on_text_validate=lambda x:self.commitextra(x))

	def commit_base(self,inst, *args):
		root = self.App.root
		# faz uma cópia dos dados de root
		evento = root.eventos
		extra = root.extra
		agenda = root.agenda
		self.dismiss(inst)
		return evento, extra, agenda

	def commitevent(self, inst, *args):
		evento, extra, agenda = self.commit_base(inst)
		# em eventos especificamente, adicionamos o texto do text input
		evento.pop()
		evento.append(inst.text)
		evento.append('')
		new = {"eventos":evento,"extra":extra,"agenda":agenda}
		self.App.root.write(new)
		
	def commitextra(self, inst, *args):
		evento, extra, agenda = self.commit_base(inst)
		extra.pop()
		extra.append(inst.text)
		extra.append('')
		new = {"eventos":evento,"extra":extra,"agenda":agenda}
		self.App.root.write(new)

	def dismiss(self, inst, *args):
		self.remove_widget(inst.parent)


	def remove(self, inst, rm_type ,*args):	
		# chama o Manager para que este remova o evento ou self.extra
		if rm_type == 'event' and self.App.root.eventos[inst.index] != '':
			self.App.root.remove_event(inst.index)
		elif rm_type == 'extra' and self.App.root.extra[inst.index] != '':
			self.App.root.remove_extra(inst.index)

class LabelScroll(ScrollView):
	def resize(self, *args):
		self.width = Window.width*.7

class IndexButton(Button):
	index = NumericProperty(0)



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


	b = nparray(l, dtype=[('day', int), ('month', int), ('year', int), ('id', int)])
	b = npsort(b, axis=0, order=['year','month','day'])
	
	flist = list()

	for element in b:
		event = eventos[element[-1]]
		date = f'{element[0]}{sep}{element[1]}{sep}{element[2]}'
		flist.append(f'{event}\t{date}')

	return flist


if __name__ == '__main__':
	MyApp().run()


