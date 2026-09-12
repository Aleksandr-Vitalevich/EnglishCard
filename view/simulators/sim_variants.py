import streamlit as st
from time import sleep
import random
from db_manager.bd_manager import BD_MANAGER
from db_manager.models import words,user_words


def run_variants_simulator(db) :
    '''Функция работы с тренажером Выбор из 4х вариантов'''
    st.subheader("Режим тест выбор верного ответа")
    if "current_for_cards" not in st.session_state or st.session_state.current_for_cards is None :
        st.session_state.current_for_cards = db.get_card_random(st.session_state.current_user_id)
        if "test_option" in st.session_state :
            del st.session_state.test_option
    card = st.session_state.current_for_cards
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
            if add_word:
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
            if delete_word:
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
        if "test_option" not in st.session_state :
            wrong_choise = db.get_wrong_choise(card.word_id)
            correct_words = card.words_english
            while len(wrong_choise) < 3 :
                base_words = ["time", "water", "book", "dog", "cat", "apple", "window"]
                random_base_words = random.choice(base_words)
                if random_base_words != correct_words and random_base_words not in wrong_choise :
                    wrong_choise.append(random_base_words)
            all_choises = wrong_choise + [correct_words]
            st.session_state.test_option = random.sample(all_choises,len(all_choises))

        options = st.session_state.test_option

        left_table,right_table = st.columns(2)
        clicked_button = None

        with left_table :
            if left_table.button(options[0],use_container_width=True,key='opt_0') :
                clicked_button = options[0]
            if left_table.button(options[1],use_container_width=True,key='opt_1') :
                clicked_button = options[1]
        with right_table :
            if right_table.button(options[2],use_container_width=True,key='opt_2') :
                clicked_button = options[2]
            if right_table.button(options[3],use_container_width=True,key='opt_3') :
                clicked_button = options[3]

        if clicked_button is not None :
            if clicked_button == card.words_english :
                st.success("Вы ответили правильно")
                db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=True)
            else :
                st.error(f"Ошибка Верный ответ {card.words_english}")
                db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=False)
        st.write("---")
        if st.button("Следующее слово ->",use_container_width=True,key="skip_answer") :
            st.session_state.current_for_cards = None
            if "test_option" in st.session_state :
                del st.session_state.test_option
            st.rerun()