main_builder_string = """
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
                                
                                text: "リンゴが欲しいのですが、これはだまされやすい膵炎のせいです、それともキツネが一度ならず二度、あるいはシマウマのように柵を飛び越えたのかもしれません"
                                # text: "-------------------------"
                                font_style: "H5"
                                bold: True
                                color: "#bfbfbf"
                                font_name: "fonts/NotoSerifJP-Bold.otf"

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
                                text: "I want an apple 你是苹果我是李"
                                # text: "-------------------------"
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
                        line_color: "gray"
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
                        
                        # Sentence Assembler
                        ExpandableBox:
                            id: sentence_assembler
                            settings_name: "sentence_assembler"
                            switchLabel: "Sentence Assembler"
                            switchActive: True
                           
                        # Clear output button 
                        MDStackLayout:
                            adaptive_height: True
                            size_hint_x: 1
                            line_color: "gray"
                            
                            MDBoxLayout:
                                adaptive_height: True
                                MDFillRoundFlatIconButton:
                                    id: clear_output
                                    text: "Clear Output"
                                    icon: ""
                                    pos_hint: {"center_x" : 0.5, "center_y": 0.5}
                                    padding: '20dp'
                                    font_style: "H6"
                                    on_release: app.toggle_clear_output()
                                    md_bg_color: "green"

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
