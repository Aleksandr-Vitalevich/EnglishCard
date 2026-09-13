import streamlit as st
from webscrapping.manager_data.manager_config_sites import load_file_config,add_new_config
from webscrapping.manager_data.requests_site import get_data
from webscrapping.manager_data.write_json_file import create_json
from re import sub
import pandas as pd

def tab1_operation() :
    '''Функция работает с 1й вкладкой модуля скрапинг'''
    st.subheader("Получение данных с сайта")
    st.markdown("***Способ ввода***")
    user_choice = st.selectbox(
            "Выберите вариант",
            ["Выбор из списка","Ручной ввод"]
            )
    if user_choice == "Выбор из списка" :
        get_data_config = load_file_config()
        site_name = st.selectbox("Выберите сайт для парсинга",list(get_data_config.keys()))
        site_select = get_data_config[site_name]
        url_select = site_select.get("url")
        args_select = site_select.get("args")
        words_to_search = st.text_input("Введите ключевые слова для поиска статей, через пробел").strip().split()
        if words_to_search :
            st.info(f"Введены следующие слова {words_to_search}")
        else :
            st.warning(f"Массив пуст. Введите слова")
        with st.form(key="auto_input") :
            st.markdown(f"Выбран сайт ***{site_name}***")
            url_text = st.text_input("Адрес сайта",value=url_select,disabled=True)
            article_site = st.text_input("Главный тег",value=args_select[0],disabled=True)
            title__link_site = st.text_input("Класс заголовка",value=args_select[1],disabled=True)
            href_atrb_site = st.text_input("Атрибут ссылки",value=args_select[2],disabled=True)
            time_site = st.text_input("Тег времени",value=args_select[3],disabled=True)
            submit_btn_form = st.form_submit_button("Запустить скрапинг")
            if submit_btn_form :
                st.info(f"Запуск скрапинга для сайта {site_name}")
                name_file = sub(r"\.","_",url_text.split("/")[2])
                ret = get_data(url_text,words_to_search,args=(article_site,title__link_site,href_atrb_site,time_site))
                wf = create_json(ret,name_file)
                if ret :
                    st.success(f"Получено статей {len(ret[0])}")
                    df = pd.DataFrame(ret[0])
                    st.dataframe(df,use_container_width=True,hide_index=True)
                else :
                    st.warning("Статей не найдено")
    
    if user_choice == "Ручной ввод" :
        words_to_search = st.text_input("Введите ключевые слова для поиска статей, через пробел").strip().split()
        if words_to_search :
            st.info(f"Введены следующие слова {words_to_search}")
        else :
            st.warning(f"Массив пуст. Введите слова")
        with st.form(key="user_input_data") :
            st.markdown("***Заполните селекторы для парсинга***")
            name_site = st.text_input("Введите название сайта. Пример Хабр")
            url_text = st.text_input("Ввод адреса сайта")
            article_site = st.text_input("Ввод главного тега. Обычно -> article",value="article")
            title__link_site = st.text_input("Ввод класса заголовка. Пример .tm-title__link",value=".tm-title__link")
            href_atrb_site = st.text_input("Ввод атрибута ссылки. Пример href",value="href")
            time_site = st.text_input("Ввод тега отвечающего за время создания статьи. Обычно -> time",value="time")
            save_config = st.checkbox("Сохранить этот сайт")
            submit_btn_form = st.form_submit_button("Запустить скрапинг")
            if submit_btn_form :
                if not url_text :
                    st.error("Ошибка поле ссылки на сайт не заполнено")
                else :
                    st.info(f"Запуск скрапинга для сайта {name_site}")
                    ret = get_data(url_text,words_to_search,args=(article_site,title__link_site,href_atrb_site,time_site))
                    if ret :
                        name_file = sub(r"\.","_",url_text.split("/")[2])
                        wf = create_json(ret,name_file)
                        st.success(f"Получено статей {len(ret[0])}")
                        df = pd.DataFrame(ret[0])
                        st.dataframe(df,use_container_width=True,hide_index=True)
                        if save_config :
                            try :
                                add_new_config(
                                    name_site,
                                    url_text,
                                    [article_site,title__link_site,href_atrb_site,time_site],
                                )
                                st.success(f"Новый сайт {name_site} успешно добавлен")
                            except Exception as e :
                                st.error("Ошибка добавления сайта")
                    else :
                        st.warning("Статей не найдено")