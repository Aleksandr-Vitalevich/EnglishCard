import streamlit as st
from view.simulators.sim_variants import run_variants_simulator
from view.simulators.sim_writing import run_writing_simulator
from view.simulators.sim_heroes import run_heroes_simulator
from view.simulators.sim_dogs import run_dogs_simulator

def run_simulators_dispatcher(db) :
    '''Главный диспетчер режима обучения'''
    st.title("Меню режима изучения")
    study_choise = st.radio(
        "Выберите режим",
        options=[
            "Выбор из 4х вариантов",
            "Письменный тест (ввести правильное слово)",
            "Напиши имя героя",
            "Напиши породу собаки"
            ],
        horizontal=True
        )
    st.divider()

    match study_choise :
        case "Выбор из 4х вариантов" :
            run_variants_simulator(db)

        case "Письменный тест (ввести правильное слово)" :
            run_writing_simulator(db)

        case "Напиши имя героя" :
            run_heroes_simulator(db)

        case "Напиши породу собаки" :
            run_dogs_simulator(db)