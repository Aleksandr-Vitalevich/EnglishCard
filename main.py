import streamlit as st
from view.site_view import *
from db_manager.bd_manager import *
import os
from db_manager.config import DB_USER,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME,FILE_JSON_PATH,FILE_XML_PATH
from view import autorization_interface

st.set_page_config(
        page_title="EnglishCard",
        layout="wide"
        )
if "db" not in st.session_state :
        st.session_state.db = BD_MANAGER(
                user = DB_USER,
                password = DB_PASSWORD,
                host = DB_HOST,
                port = DB_PORT,
                db_name = DB_NAME,
        )
        st.session_state.db.add_words_to_bd(FILE_JSON_PATH,'json')
        st.session_state.db.add_words_to_bd(FILE_XML_PATH,'xml')
        print("База данных успешно подключена")

db = st.session_state.db

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
    st.session_state.current_user_id = None
    st.session_state.current_user_name = None
    st.session_state.current_card = None
    st.session_state.cucurrent_for_cards = None
    st.session_state.current_hero = None
    st.session_state.current_city = None
    st.session_state.current_ip = None
    st.session_state.answer_correct = False
    st.session_state.current_geo_city = None
if not st.session_state.is_authenticated:
    autorization_interface(db)
else:
    site_menu_interface(db)