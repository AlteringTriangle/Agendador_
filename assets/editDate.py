from kivy.app import App
from kivy.clock import Clock

from  assets.addTask import AddTaskLayout



class EditDateLayout(AddTaskLayout):
	def __init__(self, **kwargs):
		super(EditDateLayout, self).__init__(**kwargs)
		self.remove_widget(self.children[1])
		self.children[0].children[-1].text = "Mudar Data"


class EditateApp(App):
	def build(self):
		return EditDateLayout()


if __name__ == "__main__":
	EditateApp().run()
