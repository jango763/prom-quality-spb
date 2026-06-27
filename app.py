import streamlit as st
import pandas as pd

# ==============================================================================
# 1. КОРПОРАТИВНЫЕ СТИЛИ АКАДЕМИИ (B2B Контраст, Графит и Бирюза)
# ==============================================================================
st.set_page_config(page_title="Академия ПромКачество | Портал Сертификации", layout="wide", page_icon="🎓")

st.markdown("""
    <style>
        /* Главный чистый темный фон в стиле современной ИТ-платформы */
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        
        /* Фикс подписей label: ярко-белые и четкие */
        div[data-testid="stWidgetLabel"] p, label p {
            color: #FFFFFF !important; font-weight: 600 !important; font-size: 14px !important;
        }
        
        /* Главный Академический Баннер */
        .academy-banner {
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
            padding: 40px; border-radius: 14px; color: #FFFFFF; margin-bottom: 25px;
            border-left: 8px solid #06B6D4; box-shadow: 0 4px 20px rgba(6, 182, 212, 0.1);
        }
        .academy-title { font-size: 30px; font-weight: 800; color: #FFFFFF; }
        .academy-subtitle { font-size: 15px; color: #94A3B8; margin-top: 10px; line-height: 1.5; }

        /* Белые матовые b2b-контейнеры для форм (Glassmorphism) */
        div[data-testid="stForm"], .stAlert {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important; padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important; backdrop-filter: blur(10px);
        }

        /* Карточки курсов и KPI */
        .pyrus-card {
            background: #1E293B !important;
            border: 1px solid rgba(16, 182, 212, 0.2) !important;
            border-radius: 12px; padding: 22px; margin-bottom: 15px;
        }
        .pyrus-card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
        .pyrus-card-value { font-size: 24px; font-weight: 800; color: #06B6D4; margin-top: 5px; text-shadow: 0 0 10px #06B6D4; }
        
        /* Контрастные инпуты ввода */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important;
            border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 8px !important;
        }
        
        /* Текст вариантов в радио-кнопках */
        div[data-testid="stMarkdownContainer"] p { color: #E2E8F0 !important; }
        .passport-header { background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        div[data-testid="stDataFrame"] table { color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ СКВОЗНОЙ ОПЕРАТИВНОЙ ПАМЯТИ ПЛАТФОРМЫ
# ==============================================================================
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = [
        {"fio": "Никифоров Артур Владимирович", "phone": "+7(921)555-44-33", "email": "artur@mail.ru", "education": "Базовый курс по работе в Pyrus", "passport": "4012 987654", "diploma": "№78-05", "workbook": "№ТК-12", "contract_status": "Подписан", "progress": 100, "current_status": "Сертифицированный специалист"}
    ]

if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = [
        {"id": 1, "tariff": "Корпоративный Безлимит", "amount": 150000.0, "timestamp": "2026-03-15 12:00:00"}
    ]

if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

citizens_df = pd.DataFrame(st.session_state["citizens_data"])
payments_df = pd.DataFrame(st.session_state["payments_data"])
courses_df = pd.DataFrame(st.session_state["courses_data"])

# ==============================================================================
# 3. УПРАВЛЯЮЩИЙ СЕЛЕКТОР РОЛЕЙ В САЙДБАРЕ
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#06B6D4; font-weight:800; text-shadow: 0 0 15px rgba(6, 182, 212, 0.3);'>🔒 КОНТУР АПП</h2>", unsafe_allow_html=True)
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        [
            "🎓 Личный кабинет Студента", 
            "🏢 Личный кабинет Производства", 
            "🛠️ Кабинет Администратора (Аналитика)"
        ]
    )
    st.write("---")
    st.caption("Академия ПромКачество v3.0")

# Вывод главного Академического баннера
st.markdown("""
    <div class="academy-banner">
        <div class="academy-title">🎓 Станьте сертифицированным экспертом платформы</div>
        <div class="academy-subtitle">Портал автоматизации процессов и опережающего b2b-обучения. Проходите симуляторы и получайте допуски к оборудованию.</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# КАБИНЕТ №1: СТУДЕНТЫ (Паспорт навыков, Прогресс-бар и Тренажер)
# ==============================================================================
if user_role == "🎓 Личный кабинет Студента":
    st.markdown("<h3 style='color:#FFFFFF; font-weight:700;'>🎓 Портал обучения и Сертификации</h3>", unsafe_allow_html=True)
    tab_anketa, tab_exam = st.tabs(["📝 Профильная анкета и b2b-верификация", "🤖 Интерактивный мини-тренажер ЧПУ"])
    
    with tab_anketa:
        with st.form("student_form_mono", clear_on_submit=False):
            st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>📂 Загрузка документов центра компетенций</h4>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            c_fio = col1.text_input("ФИО специалиста полностью:", value="Иванов Игорь Игоревич")
            c_phone = col2.text_input("Номер телефона для связи:", value="+7(900)111-22-33")
            c_email = col3.text_input("Электронная почта (E-mail):", value="ivanov@spb.ru")
            
            col4, col5, col6 = st.columns(3)
            c_pass = col4.text_input("Паспорт РФ (Серия, Номер):", placeholder="4011 123456")
            c_diploma = col4.text_input("Диплом об образовании:", placeholder="№78-01")
            c_work = col6.text_input("Трудовая книжка (Номер):", placeholder="№ТК-99")
            
            c_edu_place = st.selectbox("Направление автоматизации / ДПО:", ["Базовый курс по работе в Pyrus", "Настройка Pyrus Service Desk", "Документооборот и API"])
            c_contract = st.selectbox("Статус юридического ученического договора с заводом:", ["Подписан", "Не подписан"])
            c_gdpr = st.checkbox("Согласие на обработку персональных данных сотрудников", value=True)
            
            if st.form_submit_button("Зафиксировать Паспорт Навыков", type="primary"):
                if c_fio.strip() and c_phone.strip():
                    progress = 25
                    if c_pass.strip(): progress += 25
                    if c_diploma.strip(): progress += 25
                    if c_work.strip(): progress += 25
                    if progress > 100: progress = 100
                    
                    st.session_state["citizens_data"].append({
                        "fio": c_fio.strip(), "phone": c_phone.strip(), "email": c_email.strip(), 
                        "education": c_edu_place, "passport": c_pass.strip(), "diploma": c_diploma.strip(), 
                        "workbook": c_work.strip(), "contract_status": c_contract, "progress": progress, "current_status": "Обучение"
                    })
                    st.toast("✓ Документы успешно сохранены в памяти!")
                    st.rerun()

        if st.session_state["citizens_data"]:
            curr = st.session_state["citizens_data"][-1]
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="passport-header">
                    <span style='color:#06B6D4; font-weight:700;'>💳 ЦИФРОВОЙ ПАСПОРТ НАВЫКОВ ЭКСПЕРТА:</span> {curr['fio']}<br>
                    <small style='color:#FFFFFF;'>Курс: {curr.get('education', 'ДПО')} | Юридический договор: {curr.get('contract_status', 'Не подписан')}</small>
                </div>
            """, unsafe_allow_html=True)
            prog_val = int(curr.get("progress", 25))
            st.write(f"📊 Текущий процент готовности на симуляторе процессов: **{prog_val}%**")
            st.progress(prog_val / 100)

    with tab_exam:
        with st.form("exam_form_mono"):
            st.markdown("<h4 style='color:#06B6D4; font-weight:700;'>🤖 Проверка знаний и финальное тестирование</h4>", unsafe_allow_html=True)
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
                    st.balloons()
