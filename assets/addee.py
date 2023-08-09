from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty


from assets.mainPage import MainPageLayout


class AddEELayout(MainPageLayout):
	def on_enter(self, *args):
		Clock.schedule_once(self.inst, 0)

	def inst(self, *args):
		button_grid = self.children[1]
		buttons = button_grid.children
		buttons[2].text = 'Adicionar evento'
		buttons[1].text = 'Adicionar extra'
		buttons[0].text = 'Voltar'

