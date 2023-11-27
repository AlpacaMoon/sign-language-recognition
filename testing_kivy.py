from typing import Dict

from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout


kv = """
Screen:
    MDStackLayout:
        id: main_screen
        line_color: "green"
        line_width: 1
        radius: 15
        padding: 5
        spacing: 5
        orientation: "tb-rl"

        ExpandableBox:
            id: text_to_speech
            settings_name: "text_to_speech"
            switchLabel: " Text-to-Speech"
            switchActive: True

        ToggleSwitch:
            id: detection_mode_control
            settings_name: "detection_mode_control"
            switchTitle: "Detection Mode"
            leftLabel: "Dynamic"
            rightLabel: "Static"

        DropdownSelect:
            id: translate_target
            label: "Translate to:"
            menu_name: "translate_menu"

        
<DropdownSelect>
    adaptive_height: True
    orientation: "horizontal"

    MDLabel:
        adaptive_height: True 
        text: root.label
        font_style: "Subtitle1"
        pos_hint: {'center_x': .5, 'center_y': .6}
        
    MDDropDownItem:
        is_target_field: True
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint_x: 1
        text: "Chinese"
        on_release: app._open_menu(root.menu_name)

<ToggleSwitch>
    adaptive_height: True
    spacing: '4dp'

    MDLabel: 
        adaptive_height: True
        text: root.switchTitle
        font_style: "Subtitle1"
        
    MDSegmentedControl:
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        segment_color: app.theme_cls.primary_color
        md_bg_color: app.theme_cls.bg_light
        on_active: app.on_toggle_switch(*args)

        MDSegmentedControlItem:
            text: root.leftLabel

        MDSegmentedControlItem:
            text: root.rightLabel

<ExpandableBox>
    line_color: app.theme_cls.bg_normal
    line_width: 0.5
    radius: 10
    size_hint_x: 1
    adaptive_height: True
    padding: '20dp', '5dp', '20dp', '0dp'
    
    MDBoxLayout:
        adaptive_height: True
        orientation: "horizontal"
        spacing: '16dp'

        MDSwitch:
            pos_hint: {'center_x': .5, 'center_y': .5}
            icon_active: "check"
            is_active: root.switchActive
            on_active: app.on_active_expand(*args)

        MDLabel:
            text: root.switchLabel
    
    MDStackLayout: 
        adaptive_height: True
        is_expandable_box: True
        opacity: 0
        size_hint_y: 0
        height: 0
        disabled: True
        
        MDBoxLayout:
            adaptive_height: True
            expandable_box_container: True
"""


class ExpandableBox(MDStackLayout):
    switchLabel = StringProperty()
    switchActive = BooleanProperty()


class ToggleSwitch(MDStackLayout):
    switchTitle = StringProperty()
    leftLabel = StringProperty()
    rightLabel = StringProperty()


class DropdownSelect(MDBoxLayout):
    label = StringProperty()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        Window.maximize()

        self.screen = Builder.load_string(kv)

        self._init__settings()

        self._get_expandable_container('text_to_speech').add_widget(
            ToggleSwitch(
                id='detection_mode',
                settings_name='detection_mode',
                switchTitle="This is a switch",
                leftLabel="Lefty",
                rightLabel="Righty" 
            )
        )

        return self.screen

    def _init__settings(self):
        self.settings = {}

        self.settings['translate_target'] = ""
        self.settings['supported_languages'] = {
            'cn': "Chinese", 
            'my': "Malay", 
            "hk": "Hong Kong", 
            "jp": "Japanese", 
            "en": "English", 
            "es": "Spanish",
        }

        self.menus = {}
        self.create_menu(
            menu_name="translate_menu",
            settings_name="translate_target",
            dropdown_select_id="translate_target",
            dict_of_items=self.settings['supported_languages']
        )


    def on_start(self):
        ...

    # Given the ID of an ExpandableBox Widget, 
    # Returns the expandable container widget 
    # Used to .add_widget() to the expandable container
    def _get_expandable_container(self, parent_id):
        for c in self.screen.ids[parent_id].children:
            if hasattr(c, 'is_expandable_box'):
                for c2 in c.children:
                    if hasattr(c2, 'expandable_box_container'):
                        return c2

    # Accepts the ID of a DropdownSelect Widget,
    # Returns the MDDropdownItem Widget within it
    #   Used in initializing MDDropdownMenu (setup the caller)
    def _get_target_field(self, parent_id):
        for c in self.screen.ids[parent_id].children:
            if hasattr(c, "is_target_field"):
                return c

    # Event function that launches when user clicks on a MDDropdownItem
    # Opens the corresponding MDDropdownMenu
    def _open_menu(self, menu_name):
        temp = self.menus.get(menu_name)
        if temp:
            temp.open()

    # Create a MDDropdownMenu that corresponds to a given DropdownSelect id
    # Requires passing a dictionary of drop down items, where key is t
    def create_menu(
        self,
        menu_name,
        settings_name,
        dropdown_select_id,
        dict_of_items: Dict,
        position="bottom",
        width_mult=4,
    ):
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": v,
                "on_release": lambda x=k: self._close_menu(
                    x, menu_name, settings_name, dropdown_select_id, dict_of_items
                ),
                "height": dp(56),
            }
            for k, v in dict_of_items.items()
        ]

        self.menus[menu_name] = MDDropdownMenu(
            caller=self._get_target_field(dropdown_select_id),
            items=menu_items,
            position=position,
            width_mult=width_mult,
        )

    def _close_menu(
        self, x, menu_name, settings_name, dropdown_select_id, dict_of_items: Dict
    ):
        self.settings[settings_name] = x
        self._get_target_field(dropdown_select_id).text = dict_of_items[x]
        self.menus[menu_name].dismiss()

    def on_toggle_switch(
        self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ):
        self.settings[segmented_control.parent.settings_name] = segmented_item.text

    def on_active_expand(self, instance, active_value: bool):
        self.settings[instance.parent.parent.settings_name] = active_value
        for c in instance.parent.parent.children:
            if hasattr(c, "is_expandable_box"):
                if active_value:
                    self._showWidget(c)
                else:
                    self._hideWidget(c)

    def _showWidget(self, target_widget):
        target_widget.opacity = 1
        target_widget.size_hint_y = None
        target_widget.height = target_widget.minimum_height
        target_widget.disabled = False
        target_widget.parent.line_color = self.theme_cls.primary_color
        target_widget.parent.padding = ("20dp", "5dp", "20dp", "15dp")

    def _hideWidget(self, target_widget):
        target_widget.opacity = 0
        target_widget.size_hint_y = 0
        target_widget.height = 0
        target_widget.disabled = True
        target_widget.parent.line_color = self.theme_cls.bg_normal
        target_widget.parent.padding = ("20dp", "5dp", "20dp", "0dp")


MainApp().run()
