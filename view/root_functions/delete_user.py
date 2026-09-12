import streamlit as st
from db_manager.bd_manager import BD_MANAGER

def delete_user_root(db) :
    '''Функция отвечает за нажатие кнопки в интерфейсе, удаления пользователя из базы данных'''
    st.subheader("Удаление пользователя")
    if st.session_state.current_user_name != "root" :
        st.error("Доступ запрещен")
        st.stop()
    user_name = st.text_input("Введите имя пользователя",key="delete_user").strip().lower()
    user_id = st.text_input("Введите id пользователя",key="delete_user_use_id").strip().lower()
    if st.button("Удалить пользователя",use_container_width=True,key="btn_delete_user"):
        if user_name or user_id :
            delete_user = db.delete_user_admin(user_name,user_id)
            if delete_user :
                st.success(f"Пользователь успешно удален из базы {user_name or user_id}")
            elif delete_user is None :
                st.warning(f"Пользователь {user_name or user_id} не найден в базе")
            else :
                st.error('Ошибка удаления')
        else :
            st.info("Необходимо заполнить одно или более полей")