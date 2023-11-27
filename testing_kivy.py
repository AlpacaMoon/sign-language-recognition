
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.uix.label import MDLabel
from kivymd.uix.stacklayout import MDStackLayout

kv = '''
MDStackLayout:
    id: main_screen
    line_color: app.theme_cls.primary_color
    line_width: 1
    radius: 15
    padding: 5

    orientation: "tb-rl"
    

    Custom1:
        text: "1"
    Custom1:
        text: "2"
    Custom1:
        text: "3"
    Custom1:
        text: "4"
    Custom1:
        text: "5"
    Custom1:
        text: "6"
    Custom1:
        text: "7"
    Custom1:
        text: "8"
    Custom1:
        text: "9"
    Custom1:
        text: "10"
    Custom1:
        text: "11"
    

<Custom1>
    line_color: "green"
    line_width: 0.5
    radius: 10
    size_hint_x: 1
    adaptive_height: True
    MDLabel:
        text: "YES"
        adaptive_height: True
'''

class Custom1(MDStackLayout):
    ...

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        self.screen = Builder.load_string(kv)
        return self.screen

MainApp().run()
