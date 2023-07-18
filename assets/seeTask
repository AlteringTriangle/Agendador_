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
from assets.numberSelect import NumberSelect
from assets.collectionSelect import CollectionSelect
import datetime

Builder.load_string(
"""
<AddTaskLayout>:
	orientation:'vertical'
	size_hint:.9,.9
	pos_hint:{'center_y':.5,'center_x':.5}
	GridLayout:
		cols:3
		Label:
			text:'Dia'
		Label:
			text:'Mês'
		Label:
			text:'Ano'
		DayButton:
			id:dia
		MonthButton:
			id:mes
		YearButton:
			id:ano
	BoxLayout:
		size_hint_y:.75
		GridLayout:
			cols:2
			Label:
				text:'Evento'
			Label:
				text:'Extra'
			EventButton:
				id:eb
			AppendixButton:
				id:ab
	BoxLayout:
		size_hint_y:.25
		CommitButton:
			text:'Agendar'
			id:commit
		CloseButton:
			text:'Voltar'
			id:back

"""
	)


class DayButton(Button):
	def __init__(self, **kwargs):
		super(DayButton,self).__init__(**kwargs)
		self.a = datetime.date.today()
		self.text = self.a.strftime('%d')
		self.inst = ...
		Clock.schedule_once(self.instantiate)
		self.bind(on_release=self.selector)

	def instantiate(self, *args):
		self.popup = Popup(title='Choice a day',size_hint=[.5,.5],pos_hint={'center_x':.5,'center_y':.5})
		self.inst = NumberSelect(7,1,31)
		self.inst.bind(on_touch_up=Clock.schedule_once(self.dismiss))
		self.popup.content = self.inst
		Clock.schedule_once(self.retext)
	
	def retext(self, *args):
		self.text = self.a.strftime('%d')

	def selector(self, *args):
		self.popup.open()


	def dismiss(self, *args):
		self.popup.dismiss()
		self.selected = self.inst.select
		self.text = f'{self.selected}'

class MonthButton(DayButton):

	def instantiate(self, *args):
		self.popup = Popup(title='Choice a week',size_hint=[.5,.5],pos_hint={'center_x':.5,'center_y':.5})
		self.inst = NumberSelect(3,1,12)
		self.inst.bind(on_touch_up=Clock.schedule_once(self.dismiss))
		self.popup.content = self.inst
		Clock.schedule_once(self.retext)
	
	def retext(self, *args):
		self.text = self.a.strftime('%m')

class YearButton(DayButton):
	def instantiate(self, *args):
		self.popup = Popup(title='Choice a Year',size_hint=[.5,.5],pos_hint={'center_x':.5,'center_y':.5})
		self.inst = NumberSelect(3,2023,2031,minimal=2023)
		self.inst.bind(on_touch_up=Clock.schedule_once(self.dismiss))
		self.popup.content = self.inst
		Clock.schedule_once(self.retext)
	
	def retext(self, *args):
		self.text = self.a.strftime('%Y')

class EventButton(Button):
	collection = ListProperty([''])
	def __init__(self,collection=None, **kwargs):
		super(EventButton,self).__init__(**kwargs)
		if collection != None:
			self.collection = collection
		self.text = self.collection[0]
		self.popup = Popup(title='Choice a event',size_hint=[.5,.5],
			pos_hint={'center_x':.5,'center_y':.5},)
		self.inst = ...
		self.bind(on_release=self.selector)


	def on_collection(self, *args):
		self.inst = CollectionSelect(collection=self.collection)
		self.inst.bind(on_touch_up=Clock.schedule_once(self.dismiss))
		self.popup.content = self.inst


	def selector(self, *args):
		self.popup.open()

	def dismiss(self, *args):
		self.selected = self.inst.select
		self.text = f'{self.selected}'
		self.popup.dismiss()

class AppendixButton(EventButton):
	def __init__(self, **kwargs):
		super(AppendixButton, self).__init__(**kwargs)
		self.popup = Popup(title='Choice an additional info',size_hint=[.5,.5],pos_hint={'center_x':.5,'center_y':.5})


class CloseButton(Button):
	...

class CommitButton(Button):
	...

class AddTaskLayout(BoxLayout):
	...


class AddTaskPage(App):
	def build(self):
		return AddTaskLayout()


if __name__ == '__main__':
	AddTaskPage().run()