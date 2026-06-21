import streamlit as st
import pandas as pd

# Подгружаем фирменные b2b-стили CodePen
st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(12px);
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important; border-radius: 8px !important;
        }
        div[data-testid="stWidgetLabel"] p, label p { color: #FFFFFF !important; font-weight: 600 !important; }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #10B981 !important; border-bottom-color: #10B981 !important; }
        
        /* Кастомный стиль для цифрового паспорта */
        .passport-header {
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 15px; border-radius: 8px; margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🎓 Портал обучения граждан РФ и Цифровой Паспорт Навыков</h2>", unsafe_allow_html=True)

if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = []

tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и документы", "🤖 Тест компетенций на производстве"])

with tab_anketa:
    with st.form("citizen_reg_form_v2", clear_on_submit=False):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📂 Ввод персональных данных и b2b-верификация</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        c_fio = col1.text_input("ФИО соискателя полностью:", value="Иванов Игорь Игоревич")
        c_phone = col2.text_input("Номер мобильного телефона:", value="+7(900)111-22-33")
        c_email = col3.text_input("Электронная почта (E-mail):", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        c_pass = col4.text_input("Паспорт гражданина РФ (Серия, Номер):", placeholder="4011 123456")
        c_diploma = col5.text_input("Диплом об образовании (Серия, Номер):", placeholder="№78-01")
        c_work = col6.text_input("Трудовая книжка (Серия, Номер):", placeholder="№ТК-99")
        
        c_edu_place = st.selectbox("Укажите ваше учебное заведение (ДПО/ВУЗ):", ["СПбПУ (Политех)", "Университет ИТМО", "Колледж ТКУиК", "Другое профильное"])
        c_contract = st.selectbox("Статус ученического договора с заводом:", ["Подписан", "Не подписан"])
        c_gdpr = st.checkbox("Согласие на обработку персональных данных граждан РФ", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", type="primary"):
            if c_fio.strip() and c_phone.strip():
                # Расчет базового прогресса за заполнение доков (каждый док дает 20%)
                base_progress = 20
                if c_pass.strip(): base_progress += 20
                if c_diploma.strip(): base_progress += 20
                if c_work.strip(): base_progress += 20
                
                st.session_state["citizens_data"].append({
                    "fio": c_fio.strip(), "phone": c_phone.strip(), "email": c_email.strip(),
                    "education": c_edu_place, "passport": c_pass.strip(), "diploma": c_diploma.strip(), 
                    "workbook": c_work.strip(), "contract_status": c_contract, "progress": base_progress, "current_status": "Обучение"
                })
                st.toast("✓ Анкета и b2b-документы зафиксированы!")
                st.rerun()

    # ЖИВОЙ ЦИФРОВОЙ ПАСПОРТ НАВЫКОВ С PROGRESS BAR
    if st.session_state["citizens_data"]:
        current_student = st.session_state["citizens_data"][-1]
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="passport-header">
                <span style='color:#10B981; font-weight:700;'>💳 ЦИФРОВОЙ ПАСПОРТ НАВЫКОВ:</span> {current_student['fio']}<br>
                <small style='color:#94A3B8;'>Учебное заведение: {current_student['education']} | Договор: {current_student['contract_status']}</small>
            </div>
        """, unsafe_allow_html=True)
        
        # Визуальный прогресс-бар готовности студента к отправке на завод
        prog_val = int(current_student["progress"])
        st.write(f"📊 Общий уровень готовности специалиста к допуску: **{prog_val}%**")
        st.progress(prog_val / 100)

with tab_exam:
    st.markdown("<h4 style='color:#34D399; font-weight:700;'>🖥️ Интерактивный мини-тренажер ЧПУ</h4>", unsafe_allow_html=True)
    
    with st.form("exam_test_form_v2"):
        st.info("КЕЙС: На пульте управления дорогостоящего станка ЧПУ датчик стойки Syntec выдал критический перегрев шпинделя. Каковы ваши экстренные действия?")
        ans = st.radio("Выберите строго один правильный алгоритм действий:", [
            "Игнорировать предупреждение автоматики и закончить фрезеровку текущей детали",
            "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха",
            "Вручную снизить обороты шпинделя на 20% через потенциометр пульта"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы экзамена на проверку", type="primary"):
            if ans == "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха":
                if st.session_state["citizens_data"]:
                    # Правильный ответ выводит прогресс на максимум (100%) и дает статус
                    st.session_state["citizens_data"][-1]["current_status"] = "Железный специалист"
                    st.session_state["citizens_data"][-1]["progress"] = 100
                st.success("🎯 ТРЕНАЖЕР ПРОЙДЕН! Готовность 100%. Вам присвоен статус: ЖЕЛЕЗНЫЙ СПЕЦИАЛИСТ.")
                st.balloons()
                st.rerun()
            else:
                if st.session_state["citizens_data"]:
                    st.session_state["citizens_data"][-1]["current_status"] = "Обучение"
                st.error("❌ ТРЕНАЖЕР ПРОВАЛЕН! Произошла виртуальная авария шпинделя станка ЧПУ. Повторите регламент ТБ.")
