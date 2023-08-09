from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.clock import Clock
import datetime


class SeeTaskLayout(GridLayout):
	def __init__(self,**kwargs):
		super(SeeTaskLayout,self).__init__(**kwargs)
		self.cols = 3
		self.add_widget(Label(text='Evento',size_hint_x=.5))
		self.add_widget(Label(text='Extra',size_hint_x=.5))
		self.add_widget(Label(text='Data',size_hint_x=1))
		self.add_widget(Button(size_hint_x=.5))
		self.add_widget(Button())
		self.add_widget(Button())



class SeeTask(App):
	def build(self):
		return SeeTaskLayout()


if __name__ == '__main__':
	SeeTask().run()
