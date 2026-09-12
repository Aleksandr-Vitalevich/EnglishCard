import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def run_user_stats_feature(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, показывает статистику'''
    st.title("Статистика ")
    st.divider()
    if "stats_page" not in st.session_state :
        st.session_state.stats_page = "words_list"
    stats_menu = [
                    {
                        "label" : "Мои слова" ,"page" : "words_list"
                    },
                    {
                        "label" : "Мои очки" ,"page" : "points"
                    },
                    {
                        "label" : "Диаграмма","page" : "diagrams"
                    },
                    {
                        "label" : "Внешние тренажеры","page" : "API_points"
                    }
                ]
    stats_col = st.columns(len(stats_menu))
    for i,btn in enumerate(stats_menu) :
        if stats_col[i].button(btn["label"],use_container_width=True,key=f"stats_btn_{btn['page']}") :
            st.session_state.stats_page = btn["page"]
            st.rerun()
    st.divider()
    match st.session_state.stats_page :
        case "words_list" :
            st.subheader("Мои слова по статусам")
            with st.form(key="stats_status_form") :
                user_status_choise = st.selectbox(
                    "Выберите статус слова",
                    [
                    "Изучается","Изучено","В ожидании"
                    ]
                    )
                filter_words = st.form_submit_button('Показать слова',use_container_width=True)
            if filter_words :
                user_words_list = db.get_user_words(st.session_state.current_user_id,user_status_choise)
                if user_words_list is None :
                    st.error("Ошибка получения слов")
                elif not user_words_list :
                    st.info("Нет слов с данным статусом")
                else :
                    st.success(f"Найдено {len(user_words_list)}")
                    table_date = []
                    for date in user_words_list :
                        table_date.append(
                            {
                                "Английское слово" : date.words_english,
                                "Русское слово" : date.words_russian,
                                "Статус слова" : user_status_choise
                            }
                                )
                    st.dataframe(table_date,use_container_width=True)
        case "points" :
            st.subheader("Очки")
            user_points = db.get_points(st.session_state.current_user_id)
            st.metric(label="Всего очков",value=user_points)
    
        case "diagrams" :
            st.subheader("График")
            stats_user = db.get_user_stats(st.session_state.current_user_id)
            if not stats_user :
                st.info("Нет данных для построения графика . Проходите тесты")
            else :
                import pandas as pd
                df = pd.DataFrame(stats_user)
                df.set_index("words_english",inplace=True)
                st.markdown("### Попытки и правильные ответы")
                st.bar_chart(df[["Всего попыток ","Правильные ответы "]])
                st.write("---")
                st.markdown("Последний тест")
                st.dataframe(df,use_container_width=True)

        case "API_points" :
            st.subheader("Внешние тренажеры")
            with st.form(key="Api_user_points") :
                user_choice = st.selectbox(
                    "Выберите тренажер",
                    db.get_api_info(st.session_state.current_user_id)
                )
                filter_simulator = st.form_submit_button('показать мои очки',use_container_width=True)
            if filter_simulator :
                api_stats = db.get_api_points(st.session_state.current_user_id,user_choice)
                st.metric(label=f"Очки в тренажере {user_choice}",value=api_stats)