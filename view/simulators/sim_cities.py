import streamlit as st
from db_manager.bd_manager import BD_MANAGER
from gtts import gTTS
import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
geo_code = os.getenv('GEOCODE')
SIM_DIR = os.path.dirname(os.path.abspath(__file__)) 
VIEW_DIR = os.path.dirname(SIM_DIR)                  
BASE_DIR = os.path.dirname(VIEW_DIR)  

def run_cities_simulator(db) :
    st.subheader("Города")
    if "current_geo_city" not in st.session_state or st.session_state.current_geo_city is None:
        st.session_state.current_geo_city = db.get_random_city()
    city = st.session_state.current_geo_city
    if "city_attempts" not in st.session_state:
        st.session_state.city_attempts = 3
    with st.form(key="write_cities") :
        st.markdown(f"### Напишите город {city.words_russian} на английском. Вы можете прослушать произношение ###")
        local_audio_path = os.path.join(BASE_DIR, "media_cache", "city_voice.mp3")
        try :
            tts = gTTS(text=city.words_english,lang="en")
            tts.save(local_audio_path)
            with open(local_audio_path,"rb") as audio_file :
                audio_b = audio_file.read() 
                st.audio(audio_b,format="audio/mp3")
        except Exception as e :
                st.error("Не удалось сформировать озвучку")
                print(f"Ошибка gTTS {e}")
        user_input = st.text_input("Введите название города").lower().strip()
        check_button = st.form_submit_button("Проверить ответ",use_container_width=True)
        next_button = st.form_submit_button("Следующее слово",use_container_width=True)
        if check_button :
            if user_input == city.words_english.lower() :
                st.success(f"Вы ответили правильно {city.words_english}")
                db.add_api_points(st.session_state.current_user_id,"Напиши город правильно")
                st.session_state.city_attempts = 3 
                with st.spinner("Загрузка интерактивной карты города") :
                    try :
                        url = f"https://geocode.maps.co/search?q={city.words_english}&api_key={geo_code}"
                        response = requests.get(url, timeout=5)
                        data = response.json()
                        if data and len(data) > 0 :
                            lat = float(data[0]["lat"])
                            lon = float(data[0]["lon"])
                            map_data = pd.DataFrame({"lat" : [lat],"lon" : [lon]})
                            st.markdown(f'### Расположение города {city.words_russian} на карте')
                            st.map(map_data,zoom=10)
                        else :
                            st.warning(f'Не удалось найти координаты города {city.words_russian}')
                    except Exception as geo_error:
                        st.error("Ошибка подключения к сервису geocode")
                        print(f'Ошибка геокодирования {geo_error}')
            else :
                st.session_state.city_attempts -= 1
                if st.session_state.city_attempts > 0 :
                    st.warning(f'Вы ответили не правильно Осталось попыток: {st.session_state.city_attempts}')
                else :
                    st.error(f'Попытки закончились . Правильный ответ {city.words_english}')
                    

        if next_button :
            st.session_state.current_geo_city = None
            st.session_state.city_attempts = 3
            st.rerun()
            


           
        
        