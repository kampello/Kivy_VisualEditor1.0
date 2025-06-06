from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

class RootWidget(FloatLayout):
    pass

class MyApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    Builder.load_file('kivy.kv')
    MyApp().run()
