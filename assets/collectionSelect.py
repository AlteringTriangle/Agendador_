from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty



class CollectionSelect(GridLayout):
	select = ObjectProperty('')
	def __init__(self,collection=None,**kwargs):
		super(CollectionSelect,self).__init__(**kwargs)
		self.cols = 3
		if collection == None:
			self.collection = ['']
		else:
			self.collection = collection
		self.construct()

	def construct(self, *args):
		for c in self.collection:
			button = Button(text=f'{c}')
			button.bind(on_release=self.on_event)
			self.add_widget(button)

	def on_event(self, obj, *args):
		self.select = obj.text
