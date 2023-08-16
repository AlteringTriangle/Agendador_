from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty

Builder.load_string(
"""
<MainPageLayout>:
	bh:60
	orientation:'vertical'
	BoxLayout:
		size_hint_y:.2
		SwShButton:
			text: 'Adicionar tarefa'
			id:b1
		SwShButton:
			text: 'Gerar imagem'
			id:b2
		SwShButton:
			text: 'Gerenciar Eventos e Extras'	
			id:b3
	BoxLayout:
		orientation:'vertical'
		BoxLayout:
			size_hint_y:None
			height:root.bh
			Label:
				text:'placeholder'
		DataView:
			height:self.parent.height-root.bh
			width:self.parent.width
			size_hint_y:None
    		do_scroll_y: True
			DataGrid:
				cols:1
				row_default_height:root.bh
				row_force_default:True
				size_hint_y:None
				id:data
"""
	)


class MainPageLayout(BoxLayout):
	...

class SwShButton(Button):
	def on_size(self, *args):
		self.resize_text()

	def resize_text(self):
		s = len(self.text)/2+1
		c = self.width/s
		if c > self.height/2:
		    c = self.height/2
		
		self.font_size = c
		self.text_size = self.size
		self.padding = (0,self.height/2 - c/2)
		self.halign = 'center'

class SwShLabel(Label):
	def on_size(self, *args):
		self.resize_text()

	def resize_text(self):

		s = len(self.text)/2+1
		c = self.width/s
		if c > self.height/2:
		    c = self.height/2
		
		self.font_size = c
		self.text_size = self.size
		self.padding = (0,self.height/2 - c/2)
		self.halign = 'center'
		'''
		c = self.height/2
		self.font_size = c
		self.text_size = self.size
		self.padding = (0,self.height/2 - c/2)
		self.halign = 'center'
		'''
class DataView(ScrollView):
	...

class DataGrid(GridLayout):
	resize = NumericProperty(0)
	def on_resize(self, *args):
		if self.resize == 0:
			pass
		else:
			self.height = self.row_default_height*len(self.children)
			self.resize = 0

class MainPage(App):
	def build(self):
		return MainPageLayout()


if __name__ == '__main__':
	MainPage().run()
