from queue import Queue
from threading import Thread
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from traceback import print_exc

from kivymd.uix.label import MDLabel
from kivymd.uix.segmentedcontrol import MDSegmentedControl, MDSegmentedControlItem
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from client.server_comm import start_websocket_task
from kivy_components import KivyCamera, main_builder_string

class AdaptiveHeightLabel(MDLabel):
    ...


class MainApp(MDApp):
    def build(self):
        # UI Init
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "600"

        # Window
        Window.maximize()

        # Initialize Variables
        self.settings = {}
        self.settings['playing'] = False
        self.settings['detectionMode'] = "Dynamic"
        self.settings['predictionMode'] = "Local"

        self.settings['sentence_assembler'] = True
        
        self.settings['text_to_speech'] = False
        
        self.settings['translate'] = False
        self.settings['translate_target'] = ""
        self.settings['translate_engine'] = "Google"
        
        self.settings['show_fps'] = False

        self.settings['raw_output'] = []
        self.settings['transformed_output'] = []
        self.settings['max_output_len'] = 10
        self.settings['update_label_func'] = self.updateLabel

        # Build Screen
        self.screen = Builder.load_string(main_builder_string)


        # Init Menu Options
        #   - Language Translation
        self.settings['supported_languages'] = {
            'cn': "Chinese", 
            'my': "Malay", 
            "hk": "Hong Kong", 
            "jp": "Japanese", 
            "en": "English", 
            "es": "Spanish",
        }
        translate_menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": v, 
                "on_release": lambda x = k:self.set_translate_target(x),
                "height": dp(56),
            } for k, v in self.settings['supported_languages'].items()
        ]
        self.translate_menu = MDDropdownMenu(
            caller=self.screen.ids.translate_target_field, 
            items=translate_menu_items, 
            position="bottom", 
            width_mult=4,
        )

        #   - Webcam
        self.kvcamera = KivyCamera(fps=30, translation_settings=self.settings)
        
        self.screen.ids.video_area.add_widget(self.kvcamera)

        return self.screen
    
    def on_start(self):
        self._updateWidgetVisibility(self.screen.ids.translate_expand_container, self.settings['translate'])

    def toggle_play_stop_button(self, instance: MDFillRoundFlatIconButton):
        self.settings['playing'] = not self.settings['playing']

        if self.settings['playing']:
            self.kvcamera.start()
            instance.md_bg_color = self.theme_cls.primary_color
            instance.text = "Stop Detection"
            instance.icon = "stop-circle"
        else:
            self.kvcamera.stop()
            instance.md_bg_color = "green"
            instance.text = "Start Detection"
            instance.icon = "play"

    def on_active_detection_mode_control(
        self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ):
        self.settings['detectionMode'] = segmented_item.text

    def on_active_model_running_location(
        self,
        segmented_control: MDSegmentedControl,
        segmented_item: MDSegmentedControlItem,
    ):
        self.settings['predictionMode'] = segmented_item.text

    def on_active_tts(self, instance_switch, active_value: bool):
        self.settings['text_to_speech'] = active_value

    def on_active_sentence_assembler(self, instance_switch, active_value: bool):
        self.settings['sentence_assembler'] = active_value

    def on_active_translation(self, instance_switch, active_value: bool):
        self.settings['translate'] = active_value
        self._updateWidgetVisibility(self.screen.ids.translate_expand_container, self.settings['translate'])


    def set_translate_target(self, x):
        self.settings['translate_target'] = x
        self.screen.ids.translate_target_field.text = self.settings['supported_languages'][x]
        self.translate_menu.dismiss()
    

    def on_active_show_fps(self, instance_switch, active_value: bool):
        self.settings['show_fps'] = active_value

    def updateLabel(self, text_list, label_id):    
        self.screen.ids[label_id].text = str(' '.join(text_list))

    def _showWidget(self, target_widget):
        target_widget.opacity = 1
        target_widget.size_hint_y = None
        target_widget.disabled = False

    def _hideWidget(self, target_widget):
        target_widget.opacity = 0
        target_widget.size_hint_y = 0
        target_widget.disabled = True

    def _updateWidgetVisibility(self, target_widget, show):
        if show:
            self._showWidget(target_widget)
        else:
            self._hideWidget(target_widget)
        

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
        if hasattr(mainApp, 'kvcamera'):
            mainApp.kvcamera.stop()
