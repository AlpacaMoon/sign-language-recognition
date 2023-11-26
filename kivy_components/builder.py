main_builder_string = """
Screen:
    MDNavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: "vertical"
                   
                    MDTopAppBar:
                        title: "Sign Language Translation App"
                        right_action_items: [["cog", lambda x: nav_drawer.set_state("open")]]
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

                                    BoxLayout:
                                        MDCard:
                                            padding: 10
                                            size_hint: 1, 1
                                            MDRelativeLayout:
                                                MDLabel:
                                                    id: raw_output_box
                                                    text: "Something"
                                                    color: "grey"
                                                    halign: "left"
                                                    valign: "center"
                                                    bold: True
                                                    font_style: "H6"

                                    BoxLayout:
                                        size_hint_y: None
                                        height: "10dp"

                                    BoxLayout:
                                        MDCard:
                                            padding: 10
                                            size_hint: 1, 1
                                            
                                            MDRelativeLayout:
                                                MDLabel:
                                                    id: transformed_output_box
                                                    text: "Something"
                                                    color: "grey"
                                                    halign: "left"
                                                    valign: "center"
                                                    bold: True
                                                    font_style: "H6"

                        # Right Panel for output/translation display
                        BoxLayout:
                            size_hint: 0.25, 1
                            pos_hint: {'x': 0.75}
                            padding: '8dp'
                            
                            ScrollView:
                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: '8dp'
                                    spacing: '8dp'

                                    AdaptiveHeightLabel:
                                        text: "SETTINGS"
                                        halign: "center"
                                        font_style: "H4"

                                    MDBoxLayout:
                                        height: '10dp'
                                        size_hint_y: None

                                    MDFillRoundFlatIconButton:
                                        id: play_stop_button
                                        text: "Start Detection"
                                        icon: "play"
                                        pos_hint: {"center_x" : 0.5}
                                        padding: '20dp'
                                        font_style: "H6"
                                        on_release: app.toggle_play_stop_button(*args)
                                        md_bg_color: "green"

                                    MDBoxLayout:
                                        height: '10dp'
                                        size_hint_y: None
                                        

                                    AdaptiveHeightLabel: 
                                        text: "Sign Detection Mode"
                                        font_style: "Subtitle1"
                                        
                                    MDSegmentedControl:
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        segment_color: app.theme_cls.primary_color
                                        md_bg_color: app.theme_cls.bg_light
                                        on_active: app.on_active_detection_mode_control(*args)
                                        id: detection_mode_control

                                        MDSegmentedControlItem:
                                            text: "Dynamic"

                                        MDSegmentedControlItem:
                                            text: "Static"

                                            
                                    AdaptiveHeightLabel: 
                                        text: "Prediction Mode"
                                        font_style: "Subtitle1"
                                        
                                    MDSegmentedControl:
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        segment_color: app.theme_cls.primary_color
                                        md_bg_color: app.theme_cls.bg_light
                                        on_active: app.on_active_model_running_location(*args)
                                        id: detection_mode_control

                                        MDSegmentedControlItem:
                                            text: "Local"

                                        MDSegmentedControlItem:
                                            text: "Remote"

                                    MDBoxLayout:
                                        adaptive_height: True
                                        orientation: "horizontal"
                                        spacing: '16dp'
                                        MDSwitch:
                                            pos_hint: {'center_x': .5, 'center_y': .5}
                                            icon_active: "check"
                                            on_active: app.on_active_sentence_assembler(*args)
                                            active: True
                                        MDLabel:
                                            text: " Sentence Assembler"

                                    MDBoxLayout:
                                        adaptive_height: True
                                        orientation: "horizontal"
                                        spacing: '16dp'
                                        MDSwitch:
                                            pos_hint: {'center_x': .5, 'center_y': .5}
                                            icon_active: "check"
                                            on_active: app.on_active_tts(*args)
                                        MDLabel:
                                            text: " Text-to-Speech"
                                
                                    MDBoxLayout:
                                        adaptive_height: True
                                        orientation: "horizontal"
                                        spacing: '16dp'
                                        MDSwitch:
                                            pos_hint: {'center_x': .5, 'center_y': .5}
                                            icon_active: "check"
                                            on_active: app.on_active_show_fps(*args)
                                        MDLabel:
                                            text: " Show FPS"
                                    
                                    MDBoxLayout:
                                        adaptive_height: True
                                        orientation: "horizontal"
                                        spacing: '16dp'
                                        MDSwitch:
                                            pos_hint: {'center_x': .5, 'center_y': .5}
                                            icon_active: "check"
                                            on_active: app.on_active_translation(*args)
                                        MDLabel:
                                            text: " Translate Output"

                                    MDBoxLayout:
                                        adaptive_height: True
                                        orientation: "horizontal"
                                        
                                        MDTextField:
                                            id: translate_target_field
                                            pos_hint: {'center_x': .5, 'center_y': .6}
                                            size_hint_x: 1
                                            # width: '200dp'
                                            hint_text: "Translate to ..."
                                            on_focus: if self.focus: app.translate_menu.open()
                                            
                                    ScrollView:

        MDNavigationDrawer:
            id: nav_drawer
            anchor: 'right'  

            BoxLayout:
                orientation: "vertical"
                spacing: '8dp'
                padding: '8dp'

                MDLabel: 
                    text: "SLR App"
                    font_style: "H3"
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: "center"
                    
                MDLabel: 
                    text: "Menu Settings"
                    font_style: "Subtitle1"
                    size_hint_y: None
                    height: self.texture_size[1]
                    halign: "center"

                ScrollView:

<AdaptiveHeightLabel>
    size_hint_y: None
    height: self.texture_size[1]
"""
