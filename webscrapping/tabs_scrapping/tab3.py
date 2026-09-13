import streamlit as st
from time import sleep
from re import sub
from webscrapping.manager_db.show_all_db import select_all_files
from webscrapping.manager_db.update_status import change_status
from webscrapping.manager_db.show_filter_db import select_filter_files
from webscrapping.manager_db.delete_article_db import delete_article

def tab3_operation() :
    '''Функция работает с 3й вкладкой модуля скрапинг'''
    if st.session_state.current_user_name != "root":
        st.session_state.db_action = "show_all"
        st.subheader("📚 Доступные статьи для чтения")
    else :
        st.subheader("Админка для базы данных")
        col1,col2,col3 = st.columns(3)
        if "db_action" not in st.session_state :
            st.session_state.db_action = ""
        
        if col1.button("Показать все статьи",use_container_width=True) :
            st.session_state.db_action = "show_all"
        if col2.button("Найти статью",use_container_width=True) :
            st.session_state.db_action = "search"
        if col3.button("Удалить статью",use_container_width=True) :
            st.session_state.db_action = "delete"
        
        st.write("---")
    
    if st.session_state.db_action == "show_all" :
        st.markdown("### Все статьи в базе данных")
        df_db = select_all_files()
        if not df_db.empty :
            df_db.insert(0,"Выбрать",False)
            df_db['is_read'] = df_db['is_read'].map({0 : "Не прочитано", 1 : "Прочитано"})
            df_db.columns=["✔","Номер","Название сайта","Дата","Описание","Ссылка","Статус"]
            edited_db = st.data_editor(df_db,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config={
                    "✔" : st.column_config.CheckboxColumn("Выбрать",default=False),
                    "Ссылка" : st.column_config.LinkColumn(
                    "Ссылка",
                    help="Открыть статью на сайте",
                    display_text="Открыть статью на сайте"
                    )
                }
                            )
            if st.session_state.current_user_name == "root":
                if st.button("Отметить выбранные статьи как прочитанные",use_container_width=True) :
                    selected_to_read = edited_db[edited_db["✔"] == True]
                    if not selected_to_read.empty :
                        for _ , row in selected_to_read.iterrows() :
                            article_id = int(row["Номер"])
                            change_status(article_id)
                        st.success('Статус успешно изменен')
                        sleep(1)
                        st.rerun()
                    else :
                        st.warning('Нет отмеченных статей')
        else :
            st.info("В базе нет сохраненных статей")
    
    if st.session_state.db_action == "search" :
        st.markdown("### Поиск по базе данных")
        search_query = st.text_input("Введите ключевое слово для поиска")
        if search_query :
            st.info(f"Ищем статью по запросу {search_query}")
            df_db = select_filter_files(search_query)
            if not df_db.empty :
                df_db.insert(0,"Выбрать",False)
                df_db['is_read'] = df_db['is_read'].map({0 : "Не прочитано", 1 : "Прочитано"})
                df_db.columns=["✔","Номер","Название сайта","Дата","Описание","Ссылка","Статус"]
                edited_db = st.data_editor(df_db,
                    use_container_width=True,
                    hide_index=True,
                    num_rows="fixed",
                    column_config={
                            "✔" : st.column_config.CheckboxColumn("Выбрать",default=False),
                            "Ссылка" : st.column_config.LinkColumn(
                            "Ссылка",
                            help="Открыть статью на сайте",
                            display_text="Открыть статью на сайте"
                            )
                        }
                        )
                if st.button("Отметить выбранные статьи как прочитанные",use_container_width=True) :
                    selected_to_read = edited_db[edited_db["✔"] == True]
                    if not selected_to_read.empty :
                        for _ , row in selected_to_read.iterrows() :
                            article_id = int(row["Номер"])
                            change_status(article_id)
                            st.success('Статус успешно изменен')
                            sleep(1)
                            st.rerun()
                    else :
                        st.warning('Нет отмеченных статей')
            else :
                    st.info(f"По запросу {search_query} статей не найдено")
    
    if st.session_state.db_action == "delete" :
        st.markdown("### Удаление статьи из базы данных")
        delete_id = st.text_input("Введите id статьи для удаления. Можно указать несколько статей -> через пробел").strip()
        if delete_id :
            check_string = sub(r"\D+"," ",delete_id)
            list_of_id = [int(num) for num in check_string.split()]
            if list_of_id :
                st.info(f'Список id {list_of_id}')
                if st.button("Удалить",use_container_width=True) :
                    delete = delete_article(id_list=list_of_id)
                    if delete == "success" :
                        st.info('Статьи успешно удалены')
                        sleep(1)
                        st.session_state.db_action = "show_all"
                        st.rerun()
        else :
            st.info("вы не ввели ни одного id")