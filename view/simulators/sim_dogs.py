import streamlit as st
from api_services.get_photos_dog_random import get_photos_random
import os
from gtts import gTTS
from re import sub
from time import sleep
from db_manager.bd_manager import BD_MANAGER
from api_services.YANDEX_DISK import YandexDiskService
from dotenv import load_dotenv
load_dotenv()
ydt = os.getenv('YANDEX_DISK_TOKEN')

def run_dogs_simulator(db) :
    '''Функция работы с тренажером Напиши породу собаки'''
    st.subheader("Порода Собаки")
    if "current_dog_url" not in st.session_state or st.session_state.current_dog_url is None :
        with st.spinner("Выбираем породу") :
            while True :
                breed_url,breed_name,breed_bytes = get_photos_random()
                if breed_url and breed_name :
                    st.session_state.current_dog_url = breed_url
                    st.session_state.current_dog_name = breed_name.replace("-"," ").strip()
                    st.session_state.wrong_attempts = 0
                    st.session_state.current_breed_bytes = breed_bytes
                    break
    if st.session_state.current_dog_url :
        st.image(st.session_state.current_breed_bytes,width=200)
        st.write("---")
        st.markdown("### Вы можете прослушать произношение")
        SIM_DIR = os.path.dirname(os.path.abspath(__file__)) 
        VIEW_DIR = os.path.dirname(SIM_DIR)                  
        BASE_DIR = os.path.dirname(VIEW_DIR)     
        local_audio_path = os.path.join(BASE_DIR, "media_cache", "breed_voice.mp3")
        try :
            tts = gTTS(text=st.session_state.current_dog_name,lang="en")
            tts.save(local_audio_path)
            with open(local_audio_path,"rb") as audio_file :
                audio_b = audio_file.read() 
            st.audio(audio_b,format="audio/mp3")
        except Exception as e :
            st.error("Не удалось сформировать озвучку")
            print(f"Ошибка gTTS {e}")
        user_input = st.text_input("Введите название породы").lower().strip()
        if "answer_correct" not in st.session_state :
            st.session_state.answer_correct = False
        if not st.session_state.answer_correct :
            check_button = st.button("Проверить ответ",use_container_width=True)
            skip_button = st.button("Следующий герой",use_container_width=True)
            if check_button :
                clear_string1 = sub(r"[^a-z]+",'',st.session_state.current_dog_name).lower()
                clear_string2 = sub(r"[^a-z]+",'',user_input)
                                    
                if clear_string1 == clear_string2 :
                    st.session_state.answer_correct = True
                    db.add_api_points(st.session_state.current_user_id,"Напиши породу собаки")
                    st.rerun()
                else :
                    st.session_state.wrong_attempts += 1
                    if st.session_state.wrong_attempts >= 3 :
                        st.error(f"Вы ответили не правильно 3 раза ")
                        st.info(f"Название породы ***{st.session_state.current_dog_name} ***")
                    else :
                        st.error(f"Ошибка. Попробуйте еще раз Попытка {st.session_state.wrong_attempts} из 3")
            elif skip_button :
                st.session_state.current_dog_url = None 
                st.session_state.current_dog_name = None
                st.session_state.wrong_attempts = 0
                st.rerun()
            else :
                st.success(f"Вы ввели верную породу {st.session_state.current_dog_name}")
                save_mode = st.radio(
                        "Выберите способ сохранения картинки",
                        ["На Яндекс диск","На компьютер"],
                        horizontal=True
                        )
                save_picture = st.button("Сохранить картинку",use_container_width=True)
                if save_picture :
                    try :
                        if st.session_state.current_dog_url and st.session_state.current_dog_url.startswith("http"):
                            with st.spinner("Скачиваем картинку из сети ") :
                                filename = f"{st.session_state.current_dog_name.replace(" ","-")}.jpg"
                
                                if save_mode == "На Яндекс диск" :
                                    with st.spinner("Загрузка картинки на облако"):
                                        cloud_path = f"disk:/Dog/{filename}"
                                        sleep(1)
                                        save_dog_picture = YandexDiskService(y_token=ydt)
                                        res = save_dog_picture.send_file(st.session_state.current_breed_bytes,cloud_path)
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
                                            file.write(st.session_state.current_breed_bytes)
                                        sleep(1)
                                        st.info("Картинка успешно сохранена на компьютер")
                    except Exception as e :
                        st.error(f"Не удалось сохранить файл {e}")
                if st.button("Следующая порода",key="next_after_success",use_container_width=True) :
                    st.session_state.current_dog_url = None 
                    st.session_state.current_dog_name = None
                    st.session_state.answer_correct = False
                    st.rerun()      