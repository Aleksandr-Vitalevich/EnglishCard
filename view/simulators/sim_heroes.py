import streamlit as st
from db_manager.bd_manager import BD_MANAGER
from time import sleep
from api_services.super_hero_api import get_info_super_hero
from random import randint
import os
from gtts import gTTS
import requests
from re import sub
from api_services.YANDEX_DISK import YandexDiskService
from dotenv import load_dotenv
load_dotenv()
ydt = os.getenv('YANDEX_DISK_TOKEN')

def run_heroes_simulator(db) :
    '''Функция работы с тренажером Напиши имя героя'''
    st.subheader("Имя героя")
    if st.session_state.current_hero is None :
        with st.spinner("Выбираем героя") :
            while True :
                hero = get_info_super_hero(randint(1,731))
                hero_photo = hero.get("photo")
                if hero_photo and isinstance(hero_photo,str) and hero_photo.startswith("http") :
                    st.session_state.current_hero = hero
                    break
        st.session_state.wrong_attempts = 0
    current_photo = st.session_state.current_hero.get("photo")
    if current_photo :
        st.image(current_photo,width=400)
    st.write("---")
    st.markdown("### Вы можете прослушать произношение")
    SIM_DIR = os.path.dirname(os.path.abspath(__file__))
    VIEW_DIR = os.path.dirname(SIM_DIR)
    BASE_DIR = os.path.dirname(VIEW_DIR) 
    local_audio_path = os.path.join(BASE_DIR, "media_cache", "hero_voice.mp3")
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
    if "answer_correct" not in st.session_state :
        st.session_state.answer_correct = False
    if not st.session_state.answer_correct :
        check_button = st.button("Проверить ответ",use_container_width=True)
        skip_button = st.button("Следующий герой",use_container_width=True)
        if check_button :
            clear_string1 = sub(r"[^a-z]+",'',st.session_state.current_hero.get("name",'').lower()) 
            clear_string2 = sub(r"[^a-z]+",'',user_input)
                    
            if clear_string1 == clear_string2 :
                st.session_state.answer_correct = True
                db.add_api_points(st.session_state.current_user_id,"Напиши имя героя")
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
    else :
        st.success(f"Вы ввели верное имя {st.session_state.current_hero.get("name",'')}")
        save_mode = st.radio(
            "Выберите способ сохранения картинки",
            ["На Яндекс диск","На компьютер"],
            horizontal=True
            )
        save_picture = st.button("Сохранить картинку",use_container_width=True)
        if save_picture :
            try :
                if isinstance(current_photo,str) and current_photo.startswith("http"):
                    img_bytes = requests.get(current_photo).content
                else :
                    img_bytes = current_photo
                filename = f"{hero_name}.jpg"

                if save_mode == "На Яндекс диск" :
                    with st.spinner("Загрузка картинки на облако"):
                        cloud_path = f"disk:/Hero/{filename}"
                        sleep(1)
                        save_hero_picture = YandexDiskService(y_token=ydt)
                        res = save_hero_picture.send_file(img_bytes,cloud_path)
                    if res == 201 or res == 200 :
                        st.info("Картинка успешно сохранена на Яндекс диск")
                    else :
                        st.error(f"Ошибка загрузки статус ответа яндекса {res}")
                else :
                    with st.spinner("Загрузка картинки на компьютер") :
                        CURRENT_BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                        local_folder = os.path.join(CURRENT_BASE, "downloads")
                        os.makedirs(local_folder, exist_ok=True)
                        local_path = os.path.join(local_folder, filename)
                        with open(local_path,"wb") as file :
                            file.write(img_bytes)
                        sleep(1)
                        st.info("Картинка успешно сохранена на компьютер")
            except Exception as e :
                st.error(f"Не удалось сохранить файл {e}")
        if st.button("Следующий герой",key="next_after_success",use_container_width=True) :
            st.session_state.current_hero = None
            st.session_state.answer_correct = False
            st.rerun()