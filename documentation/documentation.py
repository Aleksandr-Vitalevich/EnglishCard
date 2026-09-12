import streamlit as st
from documentation.db_scheme import run_db_scheme_screen
from documentation.code_scanner import run_code_scanner_screen
from db_manager.bd_manager import BD_MANAGER

def run_documentation_screen(db) :
    '''Главный экран документации проекта'''
    st.title("Центр документации")
    st.write("---")

    doc_mode = st.radio(
        'Выберите раздел справки',
        options=["🛢️ Схема и история изменений БД","Документация модулей"],
        horizontal=True
    )
    st.write('---')
    match doc_mode :
        case "🛢️ Схема и история изменений БД" :
            run_db_scheme_screen()

        case "Документация модулей" :
            run_code_scanner_screen(db)