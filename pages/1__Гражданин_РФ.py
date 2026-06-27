import streamlit as st

st.markdown("""
    <style>
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        div[data-testid="stForm"], .stAlert { background: rgba(30, 41, 59, 0.7) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-radius: 12px !important; padding: 25px !important; backdrop-filter: blur(10px); }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] { background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important; border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 8px !important; }
        div[data-testid="stWidgetLabel"] p, label p { color: #FFFFFF !important; font-weight: 600 !important; }
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #06B6D4 !important; border-bottom-color: #06B6D4 !important; }
        .passport-header { background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); padding: 20px; border-radius: 8px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3>🎓 Портал обучения и Сертификации специалистов</h3>", unsafe_allow_html=True)

tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и b2b-верификация", "🖥️ Интерактивный мини-тренажер / Тестирование"])

with tab_anketa:
    with st.form("citizen_reg_form_v3", clear_on_submit=False):
        st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📂 Загрузка документов центра компетенций</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        c_fio = col1.text_input("ФИО специалиста полностью:", value="Иванов Игорь Игоревич")
        c_phone = col2.text_input("Номер телефона:", value="+7(900)111-22-33")
        c_email = col3.text_input("E-mail:", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        c_pass = col4.text_input("Паспорт РФ (Серия, Номер):", placeholder="4011 123456")
        c_diploma = col5.text_input("Диплом об образовании:", placeholder="№78-01")
        c_work = col6.text_input("Трудовая книжка (Номер):", placeholder="№ТК-99")
        
        c_edu_place = st.selectbox("Направление автоматизации / ДПО:", ["Базовый курс по работе", "Настройка Service Desk", "Документооборот и API"])
        c_contract = st.selectbox("Статус юридического договора обучения:", ["Подписан", "Не подписан"])
        c_gdpr = st.checkbox("Согласие на обработку персональных данных сотрудников", value=True)
        
        if st.form_submit_button("Зафиксировать Паспорт Навыков", type="primary"):
            if c_fio.strip() and c_phone.strip():
                progress = 25
                if c_pass.strip(): progress += 25
                if c_diploma.strip(): progress += 25
                if c_work.strip(): progress += 25
                
                st.session_state["citizens_data"].append({
                    "fio": c_fio.strip(), "phone": c_phone.strip(), "email": c_email.strip(),
                    "education": c_edu_place, "passport": c_pass.strip(), "diploma": c_diploma.strip(), 
                    "workbook": c_work.strip(), "contract_status": c_contract, "progress": progress, "current_status": "Обучение"
                })
                st.toast("✓ Документы успешно внесены в сессию!")
                st.rerun()

    if "citizens_data" in st.session_state and st.session_state["citizens_data"]:
        curr = st.session_state["citizens_data"][-1]
        st.markdown(f"""
            <div class="passport-header">
                <span style='color:#06B6D4; font-weight:700;'>💳 ЦИФРОВОЙ ПАСПОРТ НАВЫКОВ ЭКСПЕРТА:</span> {curr['fio']}<br>
                <small style='color:#FFFFFF;'>Курс: {curr['education']} | Юридический договор: {curr['contract_status']}</small>
            </div>
        """, unsafe_allow_html=True)
        prog = int(curr.get("progress", 25))
        st.write(f"📊 Текущий процент готовности на симуляторе процессов: **{prog}%**")
        st.progress(prog / 100)

with tab_exam:
    st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>🤖 Проверка знаний и финальное тестирование</h4>", unsafe_allow_html=True)
    with st.form("exam_form_v3"):
        st.info("КЕЙС: На пульте управления дорогостоящего станка ЧПУ датчик стойки Syntec выдал критический перегрев шпинделя за 20 млн рублей. Ваши действия?")
        ans = st.radio("Выберите строго один правильный алгоритм действий:", [
            "Игнорировать предупреждение автоматики и закончить фрезеровку детали",
            "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха",
            "Вручную снизить обороты шпинделя на 20% через потенциометр"
        ], index=None)
        
        if st.form_submit_button("Отправить ответы на проверку экспертам", type="primary"):
            if ans == "Немедленно активировать аварийную кнопку STOP, перекрыть подачу СОЖ и вызвать наставника цеха":
                if st.session_state["citizens_data"]:
                    st.session_state["citizens_data"][-1]["current_status"] = "Сертифицированный специалист"
                    st.session_state["citizens_data"][-1]["progress"] = 100
                st.success("🎯 ТЕСТИРОВАНИЕ ПРОЙДЕНО! Прогресс выведен на 100%. Присвоен статус: СЕРТИФИЦИРОВАННЫЙ СПЕЦИАЛИСТ.")
                st.rerun()
            else:
                st.error("❌ ОШИБКА В РЕГЛАМЕНТЕ! Допуск заблокирован автоматикой. Повторите видеоуроки по технике безопасности.")
