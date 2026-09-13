import streamlit as st

def get_menu_buttons(user_name) :
    '''Возвращает список кнопок меню в зависимости от роли пользователя'''
    menu_buttons = [
            {"label": "📖 Изучение", "page": "study"},
            {"label": "📊 Статистика", "page": "stats"},
            {"label": "🌐 Переводчик", "page": "translater"},
            {"label": "📂 Web Scraping", "page": "web_scraping"}
        ]

    if st.session_state.current_user_name == "root":
        menu_buttons.insert(1, {"label": "➕ Добавить слово", "page": "add"})
        menu_buttons.insert(2, {"label": "🗑️ Удалить слово", "page": "delete"})
        menu_buttons.insert(3, {"label" : "👥 Добавить пользователя","page" : "add_user"})
        menu_buttons.insert(4, {"label" : "👤❌ Удалить пользователя","page" : "delete_user"})
        menu_buttons.insert(5, {"label" : "👥 Показать пользователей","page" : "show_users"})
        menu_buttons.insert(6, {"label": "📂 Документация", "page": "documentation"})
        

        
    return menu_buttons