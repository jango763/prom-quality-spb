import streamlit as st
import pandas as pd

# 1. Подгружаем премиум-стили CodePen для сохранения внешки
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
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🎓 Портал обучения граждан РФ и Паспорт Навыков</h2>", unsafe_allow_html=True)

# Защита памяти: если данные не созданы, инициализируем пустой список
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = []

# Вкладки интерактива соискателя
tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и документы", "🤖 Тест компетенций на производстве"])

with tab_anketa:
    with st.form("citizen_reg_form_clean", clear_on_submit=False):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📂 Ввод персональных данных и квалификации</h4>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        c_fio = col1.text_input("ФИО соискателя полностью:", value="Иванов Игорь Игоревич")
        c_phone = col2.text_input("Номер мобильного телефона:", value="+7(900)111-22-33")
        c_email = col3.text_input("Электронная почта (E-mail):", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        c_pass = col4.text_input("Паспорт гражданина РФ (Серия, Номер):", placeholder="4011 123456")
        c_diploma = col5.text_input("Диплом об образовании (Серия, Номер):", placeholder="№78-01")
        c_work = col6.text_input("Трудовая книжка (Серия, Номер):", placeholder="№ТК-99")
        
        c_skills = st.text_area("Анкета о себе (Ваши навыки, разряды, работа на станках ЧПУ):")
        c_gdpr = st.checkbox("Согласие на обработку персональных данных граждан РФ", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", type="primary"):
            if c_fio.strip() and c_phone.strip():
                st.session_state["citizens_data"].append({
                    "fio": c_fio.strip(), "phone": c_phone.strip(), "email": c_email.strip(),
                    "education": "Высшее техническое", "passport": c_pass.strip(), 
                    "diploma": c_diploma.strip(), "workbook": c_work.strip(), 
                    "skills": c_skills.strip(), "gdpr": 1 if c_gdpr else 0, "current_status": "Обучение"
                })
                st.toast("✓ Анкета соискателя успешно сохранена в системе!")
                st.rerun()

with tab_exam:
    st.markdown("<h4 style='color:#34D399; font-weight:700;'>🖥️ Автоматизированный экзаменационный барьер ТБ</h4>", unsafe_allow_html=True)
    
    with st.form("exam_test_form_clean"):
        st.info("КЕЙС: На пульте управления дорогостоящего станка ЧПУ датчик стойки Syntec выдал критический перегрев шпинделя. Каковы ваши экстренные действия?")
        ans = st.radio("Выберите строго один правильный алгоритм действий:", [
            "Игнорировать предупреждение автоматики и закончить фрезеровку текущей детали",
            "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха",
            "Вручную снизить обороты шпинделя на 20% через потенциометр пульта"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы экзамена на проверку", type="primary"):
            if ans == "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха":
                if st.session_state["citizens_data"]:
                    st.session_state["citizens_data"][-1]["current_status"] = "Железный специалист"
                st.success("🎯 ЭКЗАМЕН СДАН НА 100%! Алгоритм абсолютно верен. Вам присвоен статус: ЖЕЛЕЗНЫЙ СПЕЦИАЛИСТ. Допуск в цех открыт.")
                st.balloons()
            else:
                if st.session_state["citizens_data"]:
                    st.session_state["citizens_data"][-1]["current_status"] = "Обучение"
                st.error("❌ Алгоритм неверен! Допуск к оборудованию заблокирован автоматикой платформы.")
