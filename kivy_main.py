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

from translation_module import TranslationModule


# Custom components
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

# Main App
class MainApp(MDApp):
    def build(self):
        # Themeing
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.material_style = "M2"

        # Maximize window, sometimes doesn't work??
        Window.maximize()

        # Build initial screen
        self.screen = Builder.load_string(main_builder_string)

        # Initialize self.settings and other stuff
        self._init__settings()

        # Add custom widgets manually on top of the initial screen
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

        # Translation Module
        #   Create Dropdown Menu Widgets
        self.dropdownSelects["translate_target_google"] = DropdownSelect(
            id="translate_target_google",
            label="Translate to:",
            menu_name="translate_menu_google",
            initial_item=self.settings[
                "translate_instance"
            ].getSupportedLanguagesByEngine("Google")["en"],
            opacity=1,
            size_hint_y=None,
            disabled=False,
            padding=(0, 0, 0, 0),
        )
        self.dropdownSelects["translate_target_mymemory"] = DropdownSelect(
            id="translate_target_mymemory",
            label="Translate to:",
            menu_name="translate_menu_mymemory",
            initial_item=self.settings[
                "translate_instance"
            ].getSupportedLanguagesByEngine("MyMemory")["en-GB"],
            opacity=0,
            size_hint_y=0,
            height=0,
            disabled=True,
            padding=(0, 0, 0, 0),
        )

        # Add dropdown widgets to expandable container
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
            self.dropdownSelects["translate_target_google"]
        )
        translate_expand_container.add_widget(
            self.dropdownSelects["translate_target_mymemory"]
        )

        # Create menu instances for the dropdown menus
        self.create_menu(
            menu_name="translate_menu_google",
            settings_name="translate_target_google",
            dropdown_select_id="translate_target_google",
            dict_of_items=self.settings[
                "translate_instance"
            ].getSupportedLanguagesByEngine("Google"),
        )
        self.create_menu(
            menu_name="translate_menu_mymemory",
            settings_name="translate_target_mymemory",
            dropdown_select_id="translate_target_mymemory",
            dict_of_items=self.settings[
                "translate_instance"
            ].getSupportedLanguagesByEngine("MyMemory"),
        )

        # Webcam
        self.kvcamera = KivyCamera(fps=30, translation_settings=self.settings)
        self.screen.ids.video_area.add_widget(self.kvcamera)

        # Render screen
        return self.screen

    def _init__settings(self):
        # Settings
        self.settings = {}

        #   Video
        self.settings["playing"] = False
        self.settings["detection_mode"] = "Dynamic"  # Dynamic or Static

        #   Translation
        self.settings["translate"] = False
        self.settings["translate_target"] = "en"
        self.settings["translate_target_google"] = "en"
        self.settings["translate_target_mymemory"] = "en-GB"
        self.settings["translate_engine"] = "Google"
        self.settings["translate_instance"] = TranslationModule()
        self.settings['language_changed'] = False

        #   Text-to-speech
        self.settings["text_to_speech"] = False
        self.settings['update_display_font'] = self.updateDisplayFont

        #   Show FPS
        self.settings["show_fps"] = False

        #   Sentence Assembler
        self.settings["sentence_assembler"] = False
        self.settings["processed_raw_output"] = []

        #   Others
        self.settings["raw_output"] = []
        self.settings["transformed_output"] = ""
        self.settings["final_raw_output"] = ""
        self.settings["final_transformed_output"] = ""
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
        dict_of_items: dict,
        position="bottom",
        width_mult=5,
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
        self, x, menu_name, settings_name, dropdown_select_id, dict_of_items: dict
    ):
        self.settings[settings_name] = x
        self._get_dropdownSelect(dropdown_select_id).text = dict_of_items[x]
        self.menus[menu_name].dismiss()

        if (
            settings_name == "translate_target_google"
            or settings_name == "translate_target_mymemory"
        ):
            self.settings['translate_instance'].setTarget(x)
            self.settings['language_changed'] = True
            print('langChanged', self.settings['language_changed'])

    def on_toggle_switch(
        self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ):
        self.settings[segmented_control.parent.settings_name] = segmented_item.text
        # Special toggle for translation module (switch between different dropdowns)
        if segmented_control.parent.settings_name == "translate_engine":
            self._toggle_translation_dropdowns(segmented_item.text)
            self.settings['translate_instance'].setTranslator(segmented_item.text)

    def on_active_expand(self, instance, active_value: bool):
        thisP = instance.parent.parent
        self.settings[thisP.settings_name] = active_value

        for c in thisP.children:
            if hasattr(c, "is_expandable_box"):
                if active_value:
                    self._showWidget(c)
                else:
                    self._hideWidget(c)

    def _showWidget(self, target_widget, modify_parent=True):
        target_widget.opacity = 1
        target_widget.size_hint_y = None
        target_widget.height = target_widget.minimum_height
        target_widget.disabled = False
        target_widget.padding = (0, 0, 0, 0)

        if modify_parent:
            target_widget.parent.line_color = self.theme_cls.primary_color
            target_widget.parent.padding = ("20dp", "5dp", "20dp", "5dp")

    def _hideWidget(self, target_widget, modify_parent=True):
        target_widget.opacity = 0
        target_widget.size_hint_y = 0
        target_widget.height = 0
        target_widget.disabled = True
        target_widget.padding = (0, 0, 0, 0)

        if modify_parent:
            target_widget.parent.line_color = self.theme_cls.bg_normal
            target_widget.parent.padding = ("20dp", "5dp", "20dp", "5dp")

    def updateLabel(self, text_list, label_id):
        if len(text_list) == 0:
            text_list = "-------------------------"
        
        self.screen.ids[label_id].text = str(text_list)

    def updateDisplayFont(self, rawOutputFont, transformedOutputFont):
        self.screen.ids['raw_output_box'].font_name = rawOutputFont
        self.screen.ids['transformed_output_box'].font_name = transformedOutputFont

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
            
    def toggle_clear_output(self):
        self.settings["raw_output"] = []
        self.settings["transformed_output"] = ""
        self.settings["final_raw_output"] = ""
        self.settings["final_transformed_output"] = ""
        self.settings['processed_raw_output'] = []

        # Manually update label if not running (not in the loop)
        if not self.settings["playing"]:
            self.settings["update_label_func"](
                self.settings["final_raw_output"], "raw_output_box"
            )
            self.settings["update_label_func"](
                self.settings["final_transformed_output"], "transformed_output_box"
            )

    def _toggle_translation_dropdowns(self, translation_engine):
        if translation_engine == "Google":
            self._showWidget(
                self.dropdownSelects["translate_target_google"], modify_parent=False
            )
            self._hideWidget(
                self.dropdownSelects["translate_target_mymemory"], modify_parent=False
            )
        else:
            self._hideWidget(
                self.dropdownSelects["translate_target_google"], modify_parent=False
            )
            self._showWidget(
                self.dropdownSelects["translate_target_mymemory"], modify_parent=False
            )


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
