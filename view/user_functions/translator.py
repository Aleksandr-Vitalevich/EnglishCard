import streamlit as st
from api_services.translater import translate_word

def translate_words() :
    '''Функция отвечает за нажатие кнопки в интерфейсе, работает с API yandex переводчик'''
    st.subheader("Перевод слова")
    direction_choise = st.radio(
            "Направление перевода",
            [
            "Русский -> Английский",
            "Английский -> Русский"
            ],
            horizontal=True
            )
    lang_direction = "ru-en" if direction_choise == "Русский -> Английский" else "en-ru"
    text = "Введите слово на русском языке" if lang_direction == "ru-en" else "Введите слово на английском языке"
    word = st.text_input(text).strip().lower()
    if st.button("Перевести слово") :
        if word :
            translate = translate_word(word,direction=lang_direction)
            st.success(translate)
        else :
            st.warning("Введите слово")