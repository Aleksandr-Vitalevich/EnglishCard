import streamlit as st
from pathlib import Path
import pandas as pd
from webscrapping.manager_data.read_json_file import read_json
from webscrapping.manager_data.scan_folder import get_all_files
from webscrapping.manager_db.ubdate_db import update_table

def tab2_operation() :
    '''Функция работает со 2й вкладкой модуля скрапинг'''
    st.subheader("Работа с данными")
    col1,col2 = st.columns(2)
    if "show_files_clicked" not in st.session_state :
        st.session_state.show_files_clicked = False
    if "file_read_clicked" not in st.session_state :
        st.session_state.file_read_clicked = False
    if "current_file" not in st.session_state :
        st.session_state.current_file = ""
    
    if col1.button("Показать мои файлы",use_container_width=True) :
        st.session_state.show_files_clicked = True
    if col2.button("Скрыть мои файлы",use_container_width=True) :
        st.session_state.show_files_clicked = False
        st.session_state.file_read_clicked = False
    
    if st.session_state.show_files_clicked :
        my_files = st.selectbox("Выберите файл из списка",get_all_files())
        project_root = Path(__file__).resolve().parent.parent.parent
        base_path = project_root / "webscrapping" / "manager_data" / "results"
        path = base_path/f"{my_files}.json"
        if st.button("Прочитать файл",use_container_width=True) :
            st.session_state.file_read_clicked = True
            st.session_state.current_file = my_files
    
        if st.session_state.file_read_clicked and st.session_state.current_file == my_files :
            rf = read_json(path)
            df = pd.DataFrame(rf)
            if "Select" not in df.columns :
                df.insert(0,"Select",False)
                st.markdown("***Выберите статьи для импорта в БД***")
                select_df = st.data_editor(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    num_rows = "fixes",
                    column_config={
                        "Select" : st.column_config.CheckboxColumn(
                        "Выбрать" ,
                        help = "Выберите статьи",
                        default=False,
                        )
                    }
                    )
                if st.button("Импортировать файлы в БД",use_container_width=True) :
                    select_rows = select_df[select_df["Select"] == True]
    
                    if not select_rows.empty :
                        rows_to_send = select_rows
                        message = f"Отправлено {len(rows_to_send)} статей"
                    else :
                        rows_to_send = select_df
                        message = "Отправлен весь файл"
                    try :
                        send_files = update_table(my_files,rows_to_send)
                        if send_files == "success":
                            st.success(message)
                        else :
                           st.warning("Ошибка отправки")
                    except Exception as e: 
                        print(f'Ошибка запроса {e}')
            else :
                st.error(f"Файл {my_files} не найден")