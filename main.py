import streamlit as st
from site_view import *
from bd_manager import *
from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()

if "db" not in st.session_state :
        st.session_state.db = BD_MANAGER(
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                host = os.getenv("DB_HOST"),
                port = os.getenv("DB_PORT"),
                db_name = os.getenv("DB_NAME")
        )

        file_json_path = Path("words_first_data.json")
        st.session_state.db.add_words_to_bd(file_json_path)
        print("База данных успешно подключена")

db = st.session_state.db

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
    st.session_state.current_user_id = None
    st.session_state.current_user_name = None
    st.session_state.current_card = None
    st.session_state.cucurrent_for_cards = None

if not st.session_state.is_authenticated:
    autorization_interface(db)
else:
    site_menu_interface(db)