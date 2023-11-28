
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.dropdownitem import MDDropDownItem

kv="""
Screen:
    MDBoxLayout:
        id: main_screen

        MDBoxLayout:
            line_color: "green"

        MDBoxLayout:
            line_color: "green"
            
            MDDropDownItem:
                id: drop_item
                pos_hint: {'center_x': .5, 'center_y': .5}
                text: 'Item 0'
                on_release: app.menu.open()
                size_hint: 1, None

        MDBoxLayout:
            line_color: "green"

"""
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.card.card import MDSeparator
from kivymd.uix.dropdownitem.dropdownitem import _Triangle
from kivy.uix.label import Label

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        self.screen = Builder.load_string(kv)

        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"Item {i}",
                "height": dp(56),
                "ver_growth": "down",
                "hor_growth": "left",
                "on_release": lambda x=f"Item {i}": self.set_item(x),
            } for i in range(5)
        ]
        self.menu = MDDropdownMenu(
            size_hint=(1, None),
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.bind()

        dt = self.screen.ids.drop_item
        print(dt)
        print(dt.children)
        for c in dt.children:
            if type(c) == MDSeparator:
                # c.line_color = "red"
                ...
            elif type(c) == MDBoxLayout:
                # c.line_color = "yellow"
                c.size_hint = (1, None)
                # print(c.pos_hint)
                # print(c.pos)
                print(c.size)

                for c2 in c.children:
                    if type(c2) == _Triangle:
                        c2.size_hint = (1, None)
                        
                    elif type(c2) == Label:
                        # print(dir(c2))
                        print(c2.size)

                        c2.halign = "center"
        

        return self.screen
    
    def set_item(self, text_item):
        self.screen.ids.drop_item.set_item(text_item)
        self.menu.dismiss()

mainApp = MainApp()
mainApp.run()