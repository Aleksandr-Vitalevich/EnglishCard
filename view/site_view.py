import streamlit as st
from view.menu_config import get_menu_buttons
from db_manager.bd_manager import *
from api_services.GET_IP import *
import os
ipify = os.getenv('IPIFY_TOKEN')
load_dotenv()

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
        db.save_info_login_ip(user_id = st.session_state.current_user_id,ip_user = st.session_state.current_ip,user_city = st.session_state.current_city)
    st.sidebar.markdown(f"***Ваш ip {st.session_state.current_ip}***")
    st.sidebar.markdown(f"***Ваш Город {st.session_state.current_city}***")
    import datetime
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    current_time = datetime.datetime.now().strftime("%H:%M")
    st.sidebar.markdown(f"***Текущая дата {current_date}***")
    st.sidebar.markdown(f"***Текущее время {current_time}***")
    if "show_ip_history" not in st.session_state :
            st.session_state.show_ip_history = False
    if st.sidebar.button("Показать Мои сессии",use_container_width=True) :
        st.session_state.show_ip_history = not st.session_state.show_ip_history
    if st.session_state.show_ip_history :
        import pandas as pd
        st.markdown("### Ваша история сессий")
        try :
            raw_data = db.show_info_login_ip(st.session_state.current_user_id)
            df_view = pd.DataFrame(raw_data)
            if not df_view.empty :
                st.dataframe(df_view,use_container_width=True)
            else :
                st.info("История сессий в данный момент пуста")
        except Exception as e :
            st.error(f"Не удалось загрузить историю сессий {e}") 

    if st.sidebar.button("Выход",use_container_width=True) :
        st.session_state.current_ip = None
        st.session_state.current_city = None
        st.session_state.is_authenticated = False
        st.session_state.current_user_id = None
        st.session_state.current_user_name = None
        st.session_state.current_card = None
        st.session_state.cucurrent_for_cards = None
        st.session_state.current_hero = None
        st.session_state.answer_correct = False
        st.session_state.menu_page = "main"
        st.session_state.current_geo_city = None
        st.rerun()

    menu_buttons = get_menu_buttons(st.session_state.current_user_name)
    col = st.columns(len(menu_buttons))
    for i,btn in enumerate(menu_buttons) :
        if col[i].button(btn["label"],use_container_width=True) :
            st.session_state.menu_page = btn["page"]
            st.rerun()

    match st.session_state.menu_page :
        case "study" :  
            from view.simulators.sim_dispatcher import run_simulators_dispatcher
            run_simulators_dispatcher(db)
            
        case "add" :
            from view.root_functions.add_word import add_word_root
            add_word_root(db)

        case "delete" :
            from view.root_functions.delete_word import delete_word_root
            delete_word_root(db)
        
        case "stats"  :
            from view.user_functions.stats import run_user_stats_feature
            run_user_stats_feature(db)
            
        case "documentation" :
            from documentation.documentation import run_documentation_screen
            run_documentation_screen(db)

        case "translater" :
            from view.user_functions.translator import translate_words
            translate_words()

        case "add_user" :
            from view.root_functions.add_user import add_user_root
            add_user_root(db)

        case "delete_user" :
            from view.root_functions.delete_user import delete_user_root
            delete_user_root(db)
                    
        case "show_users" :
            from view.root_functions.show_users import show_users_root
            show_users_root(db)

        case _ :
            st.info("Выберите меню тренажера ")   

#if __name__ == "__main__" :
#    autorization_interface()
#    site_menu_interface()