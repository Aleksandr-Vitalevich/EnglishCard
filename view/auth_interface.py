import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def autorization_interface(db) :
    '''Функция авторизации принимает параметры БД'''
    st.title("Вход в систему EnglishCard")
    st.subheader("""
    Привет 👋 Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.""")
    st.markdown("***У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения***")
    st.markdown("""Для этого воспрользуйся инструментами:\n
    добавить слово ➕,\n
    удалить слово 🗑️.\n
    Ну что, начнём ⬇️\n""")
    login_input = st.text_input("Введите ваш логин:")
    password_input = st.text_input("Введите ваш пароль:", type="password")
            
    col1, col2 = st.columns(2)
            
    with col1:
        if st.button("Войти", use_container_width=True):
            user = db.get_authorization(login_input.strip().lower(), password_input)
            if user:
                st.session_state.is_authenticated = True
                st.session_state.current_user_id = user.user_id
                st.session_state.current_user_name = user.name
                st.success(f"Добро пожаловать, {user.name}!")
                st.rerun()
            else:
                st.error("Неверный логин или пароль!")
                        
    with col2:
        if st.button("Зарегистрироваться", use_container_width=True):
            result = db.add_user(login_input.strip().lower(), password_input)
            if result == "exists":
                st.warning("Такое имя пользователя уже занято!")
            elif result:
                st.success("Профиль успешно создан! Теперь нажмите 'Войти'")
            else:
                st.error("Ошибка при создании профиля.")
