import streamlit as st
from bd_manager import *
from documentation import * 
from translater import *
from get_photos_dog_random import *
import time
from super_hero_api import *
from random import randint
from re import sub
from gtts import gTTS
from GET_IP import *
import os
load_dotenv()
ipify = os.getenv('IPIFY_TOKEN')

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

def site_menu_interface(db) :
    '''Функция отрисовки меню сайта. Принимает параметры БД'''
    st.title("📚*EnglishCard - Изучай английский с удовольствием!*")
    st.divider()

    if "menu_page" not in st.session_state :
        st.session_state.menu_page = "main"

    st.sidebar.header("*👤 Профиль*")
    st.sidebar.markdown(f"***Вы вошли как {st.session_state.current_user_name}***")
    st.sidebar.divider()
    if "current_ip" not in st.session_state or st.session_state.current_ip is None :
        try :
            ip_user = GET_IP(ipify)
            st.session_state.current_ip = ip_user.get_ip()
            st.session_state.current_city = ip_user.get_city()
        except Exception as e :
            st.session_state.current_ip = "127.0.0.1"
            st.session_state.current_city = "Не определен"
            print(f"Ошибка IP: {e}")
    
    st.sidebar.markdown(f"***Ваш ip {st.session_state.current_ip}***")
    st.sidebar.markdown(f"***Ваш Город {st.session_state.current_city}***")
    if st.sidebar.button("Выход",use_container_width=True) :
        st.session_state.current_ip = None
        st.session_state.current_city = None
        st.session_state.menu_page = "exit"
        st.rerun()

    menu_buttons = [
        {"label": "📖 Изучение", "page": "study"},
        {"label": "📊 Статистика", "page": "stats"},
        {"label": "📂 Документация", "page": "documentation"},
        {"label": "🌐 Переводчик", "page": "translater"}
    ]

    if st.session_state.current_user_name == "root":
        menu_buttons.insert(1, {"label": "➕ Добавить слово", "page": "add"})
        menu_buttons.insert(2, {"label": "🗑️ Удалить слово", "page": "delete"})
        menu_buttons.insert(3, {"label" : "👥 Добавить пользователя","page" : "add_user"})
        menu_buttons.insert(4, {"label" : "👤❌ Удалить пользователя","page" : "delete_user"})

    col = st.columns(len(menu_buttons))
    for i,btn in enumerate(menu_buttons) :
        if col[i].button(btn["label"],use_container_width=True) :
            st.session_state.menu_page = btn["page"]
            st.rerun()

    st.divider()

    scheme = st.button("🛢️ Схема базы данных",use_container_width=True)
    if scheme :
        st.session_state.menu_page = "scheme"

    match st.session_state.menu_page :
        case "study" :
            st.title("Меню режима изучения")
            study_choise = st.radio(
                "Выберите режим",
                options=[
                    "Выбор из 4х вариантов",
                    "Письменный тест (ввести правильное слово)",
                    "Напиши имя героя"
                ],
                horizontal=True
            )
            st.divider()
            if study_choise == "Выбор из 4х вариантов" :
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
                            time.sleep(1.5)
                            st.rerun()
                        elif add_word == "exists" :
                            st.warning(f'Слово {card.words_english} - {card.words_russian} уже есть в личном кабинете')
                            time.sleep(1.5)
                            st.rerun()
                        else :
                            st.error("Ошибка добавления записи")
                    if delete_button :
                        delete_word = db.delete_word_personal(st.session_state.current_user_id,card.word_id)
                        if delete_word:
                            st.success(f'Слово {card.words_english} - {card.words_russian} успешно удалено из личного кабинета')
                            time.sleep(1.5)
                            st.rerun()
                        elif delete_word == "not_found" :
                            st.warning(f'Слово {card.words_english} - {card.words_russian} не найдено в личном кабинете')
                            time.sleep(1.5)
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
                        import random
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
                            dog_photo = get_photos_random()
                            if dog_photo != "error" :
                                st.image(dog_photo)
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

            elif study_choise == "Письменный тест (ввести правильное слово)" :
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
                            time.sleep(1.5)
                            st.rerun()
                        elif add_word == "exists" :
                            st.warning(f'Слово {card.words_english} - {card.words_russian} уже есть в личном кабинете')
                            time.sleep(1.5)
                            st.rerun()
                        else :
                            st.error("Ошибка добавления записи")
                    if delete_button :
                        delete_word = db.delete_word_personal(st.session_state.current_user_id,card.word_id)
                        if delete_word :
                            st.success(f'Слово {card.words_english} - {card.words_russian} успешно удалено из личного кабинета')
                            time.sleep(1.5)
                            st.rerun()
                        elif delete_word == "not_found" :
                            st.warning(f'Слово {card.words_english} - {card.words_russian} не найдено в личном кабинете')
                            time.sleep(1.5)
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
                            dog_photo = get_photos_random()
                            if dog_photo != "error" :
                                st.image(dog_photo)
                            db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=True)
                        else :
                            st.warning("Попробуйте еще")
                            db.get_and_update_status(st.session_state.current_user_id,card.word_id,is_correct=False)
                    if skip_button.button("Следующее слово ->",use_container_width=True) :
                            st.session_state.current_card = None
                            st.rerun()
            elif study_choise == "Напиши имя героя" :
                st.subheader("Имя героя")
                if st.session_state.current_hero is None :
                    st.session_state.current_hero = get_info_super_hero(randint(1,731))
                    st.session_state.wrong_attempts = 0
                hero_photo = st.session_state.current_hero.get("photo")
                if hero_photo :
                    st.image(hero_photo,width=400)
                else :
                    st.warning("У этого героя нет фото")
                st.write("---")
                st.markdown("### Вы можете прослушать произношение")
                local_audio_path = "hero_voice.mp3"
                hero_name = st.session_state.current_hero.get("name","Hero")
                try :
                    tts = gTTS(text=hero_name,lang="en")
                    tts.save(local_audio_path)
                    with open(local_audio_path,"rb") as audio_file :
                        audio_b = audio_file.read() 
                    st.audio(audio_b,format="audio/mp3")
                except Exception as e :
                    st.error("Не удалось сформировать озвучку")
                    print(f"Ошибка gTTS {e}")
                user_input = st.text_input("Введите имя героя").lower().strip()
                check_button = st.button("Проверить ответ",use_container_width=True)
                skip_button = st.button("Следующий герой",use_container_width=True)
                if check_button :
                    clear_string1 = sub(r"[^a-z]+",'',st.session_state.current_hero.get("name",'').lower()) 
                    clear_string2 = sub(r"[^a-z]+",'',user_input)
                    
                    if clear_string1 == clear_string2 :
                        st.success(f"Вы ввели верное имя {st.session_state.current_hero.get("name",'')}")
                        time.sleep(1.5)
                        st.rerun()
                    else :
                        st.session_state.wrong_attempts += 1
                        if st.session_state.wrong_attempts >= 3 :
                            st.error(f"Вы ответили не правильно 3 раза ")
                            st.info(f"Имя героя ***{st.session_state.current_hero.get("name")} ***")
                        else :
                            st.error(f"Ошибка. Попробуйте еще раз Попытка {st.session_state.wrong_attempts} из 3")
                elif skip_button :
                    st.session_state.current_hero = None 
                    st.rerun()

        case "add" :
            st.subheader("Добавление слова ")
            if st.session_state.current_user_name == "root" :
                english = st.text_input("Введите английское слово : ").strip()
                russian = st.text_input("Введите перевод слова : ").strip()
                if st.button("Добавить") :
                    if english and russian :
                        add_word_admin = db.add_word_admin(english,russian)
                        if add_word_admin == "duplicate" :
                            st.warning("Слово уже есть в словаре")
                        elif add_word_admin :
                            st.success("Слово добавлено в базу")
                        else :
                            st.error("Ошибка добавления")
                    else :
                        st.error("Ошибка добавления , не все поля заполнены")
        case "delete" :
            st.subheader("Удаление слова ")
            if st.session_state.current_user_name == "root" :
                st.text("Введите или русское или английское слово или оба слова ")
                english = st.text_input("Введите английское слово : ").strip()
                russian = st.text_input("Введите русское слово : ").strip()
                if english or russian :
                    if st.button("Удалить") :
                        delete_word = db.delete_word_admin(english=english,russian=russian)
                        if delete_word == "not_found" :
                            st.warning("Запись не найдена в бд")
                        elif delete_word :
                            st.success("Запись успешно удалена из бд")
                        else :
                            st.error("Ошибка удаления")
        case "stats"  :
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

        case "scheme" :
            st.subheader("Схема")
            st.image("Курсовая.drawio.png")
        case "enter" :
            st.subheader("👤 Авторизация")
            user_name = st.text_input("Введите ваш логин :")
            user_password = st.text_input("Введите пароль :",type="password")
            if st.button("Войти в систему") :
                if user_name and user_password :
                    enter = db.get_authorization(user_name,user_password)
                    if enter :
                        st.session_state.is_authenticated = True
                        st.session_state.current_user_id = enter.user_id
                        st.session_state.current_user_name = enter.name
                        st.success(f"Добро пожаловать {st.session_state.current_user_name}")

                        st.session_state.menu_page = "study"
                        st.rerun()
                    else :
                        st.error("Ошибка авторизаации") 
                else :
                    st.warning("Заполните все поля")
        case "documentation" :
            st.subheader("Документация")
            if st.session_state.current_user_name == "root" :
                col1,col2 = st.columns(2)
                with col1 :
                    choise_admin = st.selectbox(
                        "Выберите функцию для получения документации БД админ версия",
                        ["БД : read_file_json","БД : add_words_to_bd","БД : add_word_admin",
                        "БД : add_word_personal","БД : delete_word_admin","БД : delete_word_personal",
                        "БД : change_status","БД : add_user","БД : delete_user_admin","БД : get_authorization",
                        "БД : get_card_random","БД : get_wrong_choise","БД : get_and_update_status",
                        "UI : autorization_interface","UI : site_menu_interface",
                        "doc : get_doc_admin","doc : get_ui_documentation",
                        "api : translate_word","api : get_photos_random",
                        "БД : get_user_words","БД : get_points","БД : get_user_stats",
                        "api : get_info_super_hero"]
                                        )
                    if choise_admin.startswith("БД : ") :
                        clear_string = choise_admin.replace("БД : ",'')
                        get_info = get_doc_admin(db,clear_string)
                    elif choise_admin.startswith("UI : ") :
                        clear_string = choise_admin.replace("UI : ",'')
                        import sys
                        current_module = sys.modules[__name__]
                        func = getattr(current_module,clear_string,None)
                        get_info = func.__doc__ if func else "Функция UI не найдена"
                    elif choise_admin.startswith("doc : ") :
                        clear_string = choise_admin.replace("doc : ",'')
                        import documentation
                        func = getattr(documentation,clear_string,None)
                        get_info = func.__doc__ if func else "Функция модуля documentation не найдена"
                    elif choise_admin.startswith("api : ") :
                        clear_string = choise_admin.replace("api : ",'')
                        import translater,get_photos_dog_random,super_hero_api,GET_IP
                        func = getattr(translater,clear_string,None) or getattr(get_photos_dog_random,clear_string,None) or getattr(super_hero_api,clear_string,None)
                        get_info = func.__doc__ if func else "Функция api не найдена"
                    st.info(get_info)
                with col2 :
                    choise = st.selectbox(
                                        "Выберите функцию для получения документации",
                                        ["Изучение", "Добавить слово","Удалить слово", 
                                        "Статистика", "Документация", "Схема базы данных","Вход","Выход"]
                                    ) 
                    
                    get_info_ui = get_ui_documentation(choise)
                    st.markdown(get_info_ui)
            else :
                choise = st.selectbox(
                    "Выберите функцию для получения документации",
                    ["Изучение", "Добавить слово","Удалить слово", 
                     "Статистика", "Документация", "Схема базы данных","Вход","Выход"]
                )
                get_info_ui = get_ui_documentation(choise)
                st.markdown(get_info_ui)
        case "translater" :
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
        case "exit" :
            st.subheader("Выход из системы")
            st.session_state.is_authenticated = False
            st.session_state.current_user_id = None
            st.session_state.current_user_name = None
            st.session_state.current_card = None
            st.warning("Вы вышли из системы")
            st.session_state.menu_page = "study"
            st.rerun()
        case "add_user" :
            st.subheader("Добавление нового пользователя")
            if st.session_state.current_user_name != "root" :
                st.error("Доступ запрещен")
                st.stop()
            user_name = st.text_input("Введите имя пользователя",key="add_user_new").strip().lower()
            user_password = st.text_input("Введите пароль",key="add_password_new_user",type="password").strip().lower()
            if st.button("Добавить пользователя",use_container_width=True,key="btn_add_user"):
                if user_name and user_password :
                    add_new_user = db.add_user(user_name,user_password)
                    if add_new_user :
                        st.success(f"Пользователь успешно добавлен в базу {user_name}")
                    elif add_new_user == "exists" :
                        st.warning(f"Пользователь уже есть в системе {user_name}")
                    else :
                        st.error('Ошибка добавления')
                else :
                    st.info("Необходимо заполнить все поля")
        case "delete_user" :
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
        case _ :
            st.info("Выберите меню тренажера ")   

if __name__ == "__main__" :
    autorization_interface()
    site_menu_interface()