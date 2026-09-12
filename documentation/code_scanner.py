import streamlit as st
import inspect

import db_manager.bd_manager as bd_manager

import api_services.GET_IP as GET_IP
import api_services.get_photos_dog_random as get_photos_dog_random
import api_services.super_hero_api as super_hero_api
import api_services.translater as translater
import api_services.YANDEX_DISK as YANDEX_DISK

import utils.security as security

import view.root_functions as root_functions
import view.simulators as simulators
import view.user_functions as user_functions
import view.auth_interface as auth_interface
import view.menu_config as menu_config
import view.site_view as site_view

import documentation.documentation as documentation_
import documentation.db_scheme as db_scheme
import documentation.code_scanner as code_scanner_

def run_code_scanner_screen(db) :
    '''Модуль автоматического сканирования и документирования кода'''
    st.markdown('### Автоматический сканер модулей кода')
    st.write('---')

    choise = st.selectbox(
        "Выберите пакет/модуль для анализа",
        [
            "Управление БД",
            "API сервисы",
            "Функции безопасности",
            "Функции отрисовки интерфейсы и логики работы с ним",
            "Документация"
        ]
    )
    function_dict = {}

    if choise == "Управление БД" :
        methods = inspect.getmembers(db,predicate=inspect.ismethod)
        function_dict = {name:func for name,func in methods if not name.startswith("_")}
    elif choise == "API сервисы" :
        all_api_funcs = (
            inspect.getmembers(GET_IP,predicate=inspect.ismethod) +
            inspect.getmembers(get_photos_dog_random,predicate=inspect.isfunction) +
            inspect.getmembers(super_hero_api,predicate=inspect.isfunction) +
            inspect.getmembers(translater,predicate=inspect.isfunction) +
            inspect.getmembers(YANDEX_DISK,predicate=inspect.ismethod)
        )
        function_dict = {name : func for name,func in all_api_funcs if not name.startswith("_")}
    elif choise == "Функции безопасности" :
        all_security_func = inspect.getmembers(security,predicate=inspect.isfunction)
        function_dict = {name : func for name,func in all_security_func if not name.startswith("_")}
    elif choise == "Функции отрисовки интерфейсы и логики работы с ним" :
        all_view_func = (
            inspect.getmembers(root_functions,predicate=inspect.isfunction) +
            inspect.getmembers(simulators,predicate=inspect.isfunction) +
            inspect.getmembers(user_functions,predicate=inspect.isfunction) +
            inspect.getmembers(auth_interface,predicate=inspect.isfunction) +
            inspect.getmembers(menu_config,predicate=inspect.isfunction) +
            inspect.getmembers(site_view,predicate=inspect.isfunction)
        )
        function_dict = {name : func for name,func in all_view_func if not name.startswith("_")}
    elif choise == "Документация" :
        all_documentation_func = (
            inspect.getmembers(documentation_,predicate=inspect.isfunction) +
            inspect.getmembers(db_scheme,predicate=inspect.isfunction) +
            inspect.getmembers(code_scanner_,predicate=inspect.isfunction)
        )
        function_dict = {name : func for name,func in all_documentation_func if not name.startswith("_")}

    if function_dict :
        sorted_func_names = sorted(list(function_dict.keys()))
        selected_func_name = st.selectbox(
            "Выберите функцию для чтения документации",
            options=sorted_func_names
        )
        selected_func_object = function_dict[selected_func_name]
        docstring = selected_func_object.__doc__
        st.write("---")
        st.markdown(f"### Документация для функции : `{selected_func_name}()`")

        if docstring :
            st.info(docstring.strip())
        else :
            st.warning("Для функции нет документации")
    else :
        st.error("Не удалось получить информацию для модуля")