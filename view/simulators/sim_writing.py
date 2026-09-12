import streamlit as st
from db_manager.bd_manager import BD_MANAGER
from time import sleep

def run_writing_simulator(db) :
    '''Функция работы с тренажером Письменный тест (ввести правильное слово)'''
    st.subheader("Письменный тест")
    if st.session_state.current_card is None :
        st.session_state.current_card = db.get_card_random(st.session_state.current_user_id)
    card = st.session_state.current_card
    if not card :
        st.info("Нет слов для изучения")
    else :
        st.markdown(f'Перевод слова ***{card.words_russian}*** на английский!')
        add_button = None
        delete_button = None
        add_button = st.button("Добавить слово",use_container_width=True,key="add_new_word")
        delete_button = st.button("Удалить слово",use_container_width=True,key="delete_word")
        if add_button :
            add_word = db.add_word_personal(st.session_state.current_user_id,card.word_id)
            if add_word :
                st.success(f'Слово {card.words_english} - {card.words_russian} успешно добавлено в личный кабинет')
                sleep(1.5)
                st.rerun()
            elif add_word == "exists" :
                st.warning(f'Слово {card.words_english} - {card.words_russian} уже есть в личном кабинете')
                sleep(1.5)
                st.rerun()
            else :
                st.error("Ошибка добавления записи")
        if delete_button :
            delete_word = db.delete_word_personal(st.session_state.current_user_id,card.word_id)
            if delete_word :
                st.success(f'Слово {card.words_english} - {card.words_russian} успешно удалено из личного кабинета')
                sleep(1.5)
                st.rerun()
            elif delete_word == "not_found" :
                st.warning(f'Слово {card.words_english} - {card.words_russian} не найдено в личном кабинете')
                sleep(1.5)
                st.rerun()
            else :
                st.error("Ошибка удаления записи")
        st.write("---")
        with st.form(key=f"status_form_{card.word_id}") :
            st.markdown("Управление статусом слова")
            user_choise = st.selectbox(
                "Выбор статуса карточки",
                    [
                        "Изучается","Изучено","В ожидании"
                    ],key=f"status_select_{card.word_id}"
                )
            change_status = st.form_submit_button("Сохранить статус",use_container_width=True)
        if change_status :
            change_status_word_user = db.change_status(st.session_state.current_user_id,card.word_id,user_choise)
            if change_status_word_user :
                st.success(f'Статус успешно изменен на {user_choise}')
            elif change_status_word_user is False :
                st.warning(f"Слово {card.words_english} - {card.words_russian} не найденов личном кабинете добавьте себе слово")
            else :
                st.error("Ошибка изменения статуса")

        user_answer = st.text_input("Введите перевод слова").strip().lower()
        check_button,skip_button = st.columns([1,1])
        if check_button.button("Проверить ответ",use_container_width=True):
            if user_answer == card.words_english.strip().lower() :
                st.success("Вы ответили правильно")
                db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=True)
            else :
                st.warning("Попробуйте еще")
                db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=False)
        if skip_button.button("Следующее слово ->",use_container_width=True) :
                st.session_state.current_card = None
                st.rerun()