from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

from assets.mainPage import SwShButton
from assets.mainPage import DataGrid, DataView

Builder.load_string("""
<CollectionSelect>:   
    BoxLayout:
    	orientation:'vertical'
	    DataView:
		    height:self.parent.height
		    width:self.parent.width
		    size_hint_y:None
    		do_scroll_y: True
		    DataGrid:
		    	id:data
			    cols:1
			    row_default_height:40
			    row_force_default:True
			    size_hint_y:None
""")
	

class CollectionSelect(GridLayout):
	select = ObjectProperty('')
	def __init__(self,collection=None,**kwargs):
		super(CollectionSelect,self).__init__(**kwargs)
		self.cols = 3
		if collection == None:
			self.collection = ['']
		else:
			self.collection = collection
		Clock.schedule_once(self.construct, 0)
		self.change_in_text = False
		
	def on_enter(self, *args):
		print('enter')
	def construct(self, *args):
		print('construct enter')
		datagrid = self.ids.data
		for c in self.collection:
			button = SwShButton(text=f'{c}')
			button.bind(on_release=self.on_event)
			datagrid.add_widget(button)
			datagrid.height += 40

	def on_event(self, obj, *args):
		self.change_in_text = True
		self.select = obj.text
		
	def thing(self, *args):
		print(self.ids)


