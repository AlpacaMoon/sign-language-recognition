import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from action_feature_extraction import extractFeatures, testFunc

from streamlit.runtime.scriptrunner import add_script_run_ctx
from concurrent.futures import ThreadPoolExecutor
import os

import av
import numpy as np
import traceback

try:
    stss = st.session_state

    if "initialized" not in stss:
        stss.initialized = True

        stss.recognition_mode = "dynamic"
        stss.tts = False
        stss.translate = False
        stss.translate_to = "English"
        stss.sentence_assembler = True
        stss.show_fps = False

    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')
    col1, colspacing, col2 = st.columns([0.7, 0.02, 0.28])

    # Inject CSS
    st.markdown(
        """
        <style>
            [data-baseweb="select"] > * {
                cursor: pointer;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    def npSaveFile(filename, data):
        np.save(filename, data)


    def video_frame_callback(frame):
        img = frame.to_ndarray(format="bgr24")
        

        img = np.fliplr(img)

        print("Start Do")
        try:
            print("A")
            detectionResults, finalImg = extractFeatures(img)
        except Exception as e:
            print("Exception: ", e)
            traceback.print_exc()
        finally:
            print("Finally")

        return av.VideoFrame.from_ndarray(img, format="bgr24")


    def toggle_recognition_mode():
        if stss.recognition_mode == "dynamic":
            stss.recognition_mode = "static"
        else:
            stss.recognition_mode = "dynamic"


    def toggle_state(x):
        stss[x] = not stss[x]


    def update_translate_language():
        stss.translate_to = chosen_translate_option


    with st.sidebar:
        st.title("Settings")

        st.subheader(
            "Currently Detecting: "
            + ("Static Signs" if stss.recognition_mode == "static" else "Dynamic Signs")
        )
        st.button(
            "Switch to Static Sign Recognition Mode"
            if stss.recognition_mode == "dynamic"
            else "Switch to Dynamic Sign Recognition Mode",
            on_click=toggle_recognition_mode,
        )

        st.divider()

        st.toggle(
            "Text to Speech", on_change=lambda: toggle_state("tts"), value=stss.tts
        )

        st.toggle(
            "Translate to Another Language",
            on_change=lambda: toggle_state("translate"),
            value=stss.translate,
        )
        if stss.translate:
            chosen_translate_option = st.selectbox(
                "Translate to:",
                ("Chinese", "English", "Malay"),
                on_change=update_translate_language,
            )

        st.empty()

        st.toggle(
            "Sentence Assembler",
            on_change=lambda: toggle_state("sentence_assembler"),
            value=stss.sentence_assembler,
            help="Transforms the Raw Output into Human-readable sentences",
        )

        st.toggle("Show FPS", on_change=lambda: toggle_state("show_fps"), value=stss.show_fps)

    with col1:
        webrtc_streamer(
            key="media-constraints",
            mode=WebRtcMode.SENDRECV,
            # rtc_configuration={"iceServers": get_ice_servers()},
            media_stream_constraints={
                "video": {
                    "width": {"min": 640, "ideal": 1280, "max": 2560},
                    "height": {"min": 480, "ideal": 720, "max": 1440},
                },
                "audio": False,
            },
            video_html_attrs={
                # "style": {"width": "50%", "margin": "0 auto", "border": "5px yellow solid"},
                "style": {"width": "100%"},
                "controls": False,
                "autoPlay": True,
            },
            video_frame_callback=video_frame_callback,
        )

    with col2:
        st.subheader("Raw Output:")
        st.code("I/Me eat cake")

        st.divider()

        st.subheader("Transformed Output:")
        st.code("I eat cake.")
except Exception as e:
    print(e)
    traceback.print_exc()