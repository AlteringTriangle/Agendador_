from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty



class NumberSelect(GridLayout):
	select = ObjectProperty('')
	def __init__(self,cols,initial_value,end,minimal=1,**kwargs):
		super(NumberSelect,self).__init__(**kwargs)
		self.cols = cols
		self.start = minimal
		self.end = end + 1
		self.construct()

	def construct(self, *args):
		for c in range (self.start,self.end):
			if c < 10:
				c = f'0{c}'
			button = Button(text=f'{c}')
			button.bind(on_release=self.on_event)
			self.add_widget(button)

	def on_event(self, obj, *args):
		self.select = obj.text

