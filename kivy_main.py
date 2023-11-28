from typing import Dict
from traceback import print_exc

# Run this before importing any other modules
from kivy.config import Config

Config.set("input", "mouse", "mouse,multitouch_on_demand")

from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.metrics import dp


from kivymd.app import MDApp
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.dropdownitem.dropdownitem import _Triangle
from kivymd.uix.dropdownitem import MDDropDownItem

from kivy_components import KivyCamera, main_builder_string

kv = """
Screen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "Sign Language Translation App"
            elevation: 8

        # Main Area
        FloatLayout:
            # Left Panel for video display
            BoxLayout:
                size_hint: 0.75, 1
                pos_hint: {'x': 0}

                FloatLayout:
                    # Video Area
                    BoxLayout:
                        size_hint: 1, 0.8
                        pos_hint: {'y': 0.2}
                        id: video_area

                    # Text Output Area
                    BoxLayout:
                        size_hint: 1, 0.2
                        pos_hint: {'y': 0}
                        orientation: "vertical"
                        padding: 10

                        MDBoxLayout:
                            md_bg_color: app.theme_cls.bg_light
                            radius: '6dp'
                            padding: '20dp', '10dp', '20dp', '10dp'
                            orientation: "vertical"

                            MDLabel: 
                                adaptive_height: True
                                text: "RAW OUTPUT"
                                font_style: "Caption"
                                color: "grey"
                                
                            MDLabel: 
                                id: raw_output_box
                                text: "I want an apple yummy yummy"
                                font_style: "H5"
                                bold: True
                                color: "#bfbfbf"

                        MDBoxLayout:
                            adaptive_height: True
                            height: "10dp"

                        MDBoxLayout:
                            md_bg_color: app.theme_cls.bg_light
                            radius: '6dp'
                            padding: '20dp', '10dp', '20dp', '10dp'
                            orientation: "vertical"

                            MDLabel: 
                                adaptive_height: True
                                text: "TRANSFORMED OUTPUT"
                                font_style: "Caption"
                                color: "grey"
                                
                            MDLabel: 
                                id: transformed_output_box
                                text: "I want an apple yummy yummy"
                                font_style: "H5"
                                bold: True
                                color: "#bfbfbf"

            # Right Panel for output/translation display
            BoxLayout:
                size_hint: 0.25, 1
                pos_hint: {'x': 0.75}

                ScrollView:
                    MDStackLayout:
                        id: settings_screen
                        line_color: "green"
                        line_width: 1
                        radius: 15
                        padding: '8dp', '16dp', '8dp', '16dp'
                        spacing: '5dp'
                        orientation: "tb-rl"

                        # Title
                        MDLabel:
                            adaptive_height: True
                            text: "SETTINGS"
                            halign: "center"
                            font_style: "H4"

                        # Play/Stop Button
                        MDRelativeLayout:
                            adaptive_height: True
                            size_hint_x: 1
                            line_color: "yellow"

                            MDFillRoundFlatIconButton:
                                id: play_stop_button
                                text: "Start Detection"
                                icon: "play"
                                pos_hint: {"center_x" : 0.5, "center_y": 0.5}
                                padding: '20dp'
                                font_style: "H6"
                                on_release: app.toggle_play_stop_button(*args)
                                md_bg_color: "green"

                        # Detection Mode Swapping Switch
                        MDBoxLayout:
                            adaptive_height: True
                            padding: '20dp', '5dp', '20dp', '0dp'
                            id: detection_mode_box

                        # Prediction Mode Swapping Switch
                        MDBoxLayout:
                            adaptive_height: True
                            padding: '20dp', '5dp', '20dp', '0dp'
                            id: prediction_mode_box
                        
                        # Sentence Assembler
                        ExpandableBox:
                            id: sentence_assembler
                            settings_name: "sentence_assembler"
                            switchLabel: "Sentence Assembler"
                            switchActive: True

                        # Text-to-Speech
                        ExpandableBox:
                            id: text_to_speech
                            settings_name: "text_to_speech"
                            switchLabel: "Text-to-Speech"
                            switchActive: False

                        # Translation
                        ExpandableBox:
                            id: translate
                            settings_name: "translate"
                            switchLabel: "Translate to Another Language"
                            switchActive: False

                        # DropdownSelect:
                        #     id: translate_target
                        #     label: "Translate to:"
                        #     menu_name: "translate_menu"
            
<DropdownSelect>
    adaptive_height: True
    orientation: "horizontal"
    settings_name: root.settings_name

    MDLabel:
        adaptive_height: True 
        text: root.label
        font_style: "Subtitle1"
        pos_hint: {'center_x': .5, 'center_y': .6}
        
    MDDropDownItem:
        is_target_field: True
        pos_hint: {'center_x': .5, 'center_y': .5}
        size_hint: 1, None
        text: root.initial_item
        on_release: app._open_menu(root.menu_name)

<ToggleSwitch>
    adaptive_height: True
    spacing: '4dp'
    padding: 0, 0, 0, '5dp'
    settings_name: root.settings_name

    MDLabel: 
        adaptive_height: True
        text: root.switchTitle + ":"
        font_style: "Button"
        halign: "center"
        
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
    padding: '20dp', '5dp', '20dp', '5dp'
    settings_name: root.settings_name
    
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
            text: " " + root.switchLabel
    
    MDStackLayout: 
        adaptive_height: True
        is_expandable_box: True
        opacity: 0
        size_hint_y: 0
        height: 0
        disabled: True
        padding: 0, 0, 0, 0
"""


class SettingControl:
    settings_name = StringProperty()


class ExpandableBox(MDStackLayout, SettingControl):
    switchLabel = StringProperty()
    switchActive = BooleanProperty()


class ToggleSwitch(MDStackLayout, SettingControl):
    switchTitle = StringProperty()
    leftLabel = StringProperty()
    rightLabel = StringProperty()

    def __init__(self, **kwargs):
        super(MDStackLayout, self).__init__(**kwargs)
        for c in self.children:
            if type(c) == MDSegmentedControl:
                c.size_hint = (1, None)
                c.ids.segment_panel.size_hint = (1, None)


class DropdownSelect(MDBoxLayout, SettingControl):
    label = StringProperty()
    menu_name = StringProperty()
    initial_item = StringProperty()

    def __init__(self, **kwargs):
        super(MDBoxLayout, self).__init__(**kwargs)
        
        for c in self.children:
            if type(c) == MDDropDownItem:
                for c2 in c.children:
                    if type(c2) == MDBoxLayout:
                        c2.size_hint = (1, None)
                        for c3 in c2.children:
                            if type(c3) == _Triangle:
                                c3.size_hint = (1, None)
                                break

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        Window.maximize()
        self.screen = Builder.load_string(kv)

        # Initialize self.settings and other stuff
        self._init__settings()

        # Add custom widgets manually
        #   Detection Mode Swapping Switch
        self.screen.ids.detection_mode_box.add_widget(
            ToggleSwitch(
                id="detection_mode",
                settings_name="detection_mode",
                switchTitle="Sign Detection Mode",
                leftLabel="Dynamic",
                rightLabel="Static",
            )
        )

        #   Prediction Mode Swapping
        self.screen.ids.prediction_mode_box.add_widget(
            ToggleSwitch(
                id="prediction_mode",
                settings_name="prediction_mode",
                switchTitle="Sign Prediction Mode",
                leftLabel="Local",
                rightLabel="Remote",
            )
        )

        #   Text-to-Speech
        self._get_expandable_container("text_to_speech").add_widget(
            ToggleSwitch(
                id="text_to_speech_engine",
                settings_name="text_to_speech_engine",
                switchTitle="Speech Engine",
                leftLabel="Google",
                rightLabel="Pyttsx3",
            )
        )

        #   Translation
        self.dropdownSelects["translate_target"] = DropdownSelect(
            id="translate_target",
            label="Translate to:",
            menu_name="translate_menu",
            initial_item=self.settings['supported_languages']['cn']
        )
        translate_expand_container = self._get_expandable_container("translate")
        translate_expand_container.add_widget(
            ToggleSwitch(
                id="translate_engine",
                settings_name="translate_engine",
                switchTitle="Translation Engine",
                leftLabel="Google",
                rightLabel="MyMemory",
            )
        )
        translate_expand_container.add_widget(
            self.dropdownSelects['translate_target']
        )
        self.create_menu(
            menu_name="translate_menu",
            settings_name="translate_target",
            dropdown_select_id="translate_target",
            dict_of_items=self.settings["supported_languages"],
        )

        # Webcam
        self.kvcamera = KivyCamera(fps=30, translation_settings=self.settings)
        self.screen.ids.video_area.add_widget(self.kvcamera)

        return self.screen

    def _init__settings(self):
        # Settings
        self.settings = {}

        #   Video
        self.settings["playing"] = False
        self.settings["detection_mode"] = "Dynamic"
        self.settings["prediction_mode"] = "Local"

        #   Translation
        self.settings["translate"] = False
        self.settings["translate_target"] = ""
        self.settings["translate_engine"] = "Google"

        self.settings["supported_languages"] = {
            "cn": "Chinese",
            "my": "Malay",
            "hk": "Hong Kong",
            "jp": "Japanese",
            "en": "English",
            "es": "Spanish",
        }

        #   Text-to-speech
        self.settings["text_to_speech"] = False
        self.settings["text_to_speech_engine"] = "Google"  # Google or MyMemory

        #   Show FPS
        self.settings["show_fps"] = False

        #   Sentence Assembler
        self.settings["sentence_assembler"] = True

        #   Others
        self.settings["raw_output"] = []
        self.settings["transformed_output"] = []
        self.settings["max_output_len"] = 10
        self.settings["update_label_func"] = self.updateLabel

        # Menus
        self.menus = {}

        # Dropdowns
        self.dropdownSelects = {}

    def on_start(self):
        ...

    # Given the ID of an ExpandableBox Widget,
    # Returns the expandable container widget
    # Used to .add_widget() to the expandable container
    def _get_expandable_container(self, parent_id):
        for c in self.screen.ids[parent_id].children:
            if hasattr(c, "is_expandable_box"):
                for c2 in c.children:
                    if hasattr(c2, "expandable_box_container"):
                        return c2

                # If this is the first time to add widget:
                c.add_widget(
                    Builder.load_string(
                        """
MDBoxLayout:
    adaptive_height: True
    expandable_box_container: True
    padding: 0, '5dp', 0, '5dp'
    orientation: "vertical"
                    """
                    )
                )
                for c2 in c.children:
                    if hasattr(c2, "expandable_box_container"):
                        return c2

    # Accepts the ID of a DropdownSelect Widget,
    # Returns the MDDropdownItem Widget within it
    #   Used in initializing MDDropdownMenu (setup the caller)
    def _get_dropdownSelect(self, dropdown_select_id):
        for c in self.dropdownSelects[dropdown_select_id].children:
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
            caller=self._get_dropdownSelect(dropdown_select_id),
            items=menu_items,
            position=position,
            width_mult=width_mult,
        )

    def _close_menu(
        self, x, menu_name, settings_name, dropdown_select_id, dict_of_items: Dict
    ):
        self.settings[settings_name] = x
        self._get_dropdownSelect(dropdown_select_id).text = dict_of_items[x]
        self.menus[menu_name].dismiss()

        print(self.settings)

    def on_toggle_switch(
        self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ):
        self.settings[segmented_control.parent.settings_name] = segmented_item.text
        print(self.settings)


    def on_active_expand(self, instance, active_value: bool):
        self.settings[instance.parent.parent.settings_name] = active_value
        for c in instance.parent.parent.children:
            if hasattr(c, "is_expandable_box"):
                if active_value:
                    self._showWidget(c)
                else:
                    self._hideWidget(c)
        print(self.settings)
            

    def _showWidget(self, target_widget):
        target_widget.opacity = 1
        target_widget.size_hint_y = None
        target_widget.height = target_widget.minimum_height
        target_widget.disabled = False
        target_widget.padding = (0, 0, 0, 0)

        target_widget.parent.line_color = self.theme_cls.primary_color
        target_widget.parent.padding = ("20dp", "5dp", "20dp", "5dp")

    def _hideWidget(self, target_widget):
        target_widget.opacity = 0
        target_widget.size_hint_y = 0
        target_widget.height = 0
        target_widget.disabled = True
        target_widget.padding = (0, 0, 0, 0)

        target_widget.parent.line_color = self.theme_cls.bg_normal
        target_widget.parent.padding = ("20dp", "5dp", "20dp", "5dp")

    def updateLabel(self, text_list, label_id):
        self.screen.ids[label_id].text = str(" ".join(text_list))

    def toggle_play_stop_button(self, instance: MDFillRoundFlatIconButton):
        self.settings["playing"] = not self.settings["playing"]

        if self.settings["playing"]:
            self.kvcamera.start()
            instance.md_bg_color = self.theme_cls.primary_color
            instance.text = "Stop Detection"
            instance.icon = "stop-circle"
        else:
            self.kvcamera.stop()
            instance.md_bg_color = "green"
            instance.text = "Start Detection"
            instance.icon = "play"


if __name__ == "__main__":
    try:
        # # Server Communication API Link
        # action_translation_uri = "ws://your-server-ip:8000/ws"

        # # Shared Queue with the server communication thread
        # server_comm_queue = Queue()

        # # Start server communication thread
        # server_comm_thread = Thread(
        #     target=start_websocket_task, args=(action_translation_uri, server_comm_queue)
        # )
        # server_comm_thread.start()

        mainApp = MainApp()
        mainApp.run()
    except Exception as e:
        print(e)
        print_exc()
    finally:
        if hasattr(mainApp, "kvcamera"):
            mainApp.kvcamera.stop()
