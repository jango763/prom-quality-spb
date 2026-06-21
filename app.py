import streamlit as st
import pandas as pd
import io

# ==============================================================================
# 1. СТИЛИ ИЗ CODEPEN (Идеальный контраст, Glassmorphism, яркий белый текст)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        /* Полное переопределение фона и базовых шрифтов под тему CodePen */
        .stApp {
            background-color: #0B0F19 !important;
            color: #F8FAFC !important;
        }
        
        /* Фикс читаемости: делаем подписи (label) над инпутами ярко-белыми */
        div[data-testid="stWidgetLabel"] p, label p {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5);
        }
        
        /* Наш особый премиум Hero-баннер АПП */
        .hero-banner {
            background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important;
            padding: 35px;
            border-radius: 16px;
            color: #FFFFFF;
            margin-bottom: 25px;
            border-left: 8px solid #10B981;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
        }
        .hero-title {
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(90deg, #10B981, #34D399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 14px;
            color: #94A3B8;
            margin-top: 8px;
            line-height: 1.4;
        }

        /* Интерактивные матовые B2B-контейнеры без грязных серых теней (Glassmorphism) */
        div[data-testid="stForm"], div[data-testid="stExpander"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important;
            padding: 25px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(12px);
        }

        /* Объемные b2b-карточки KPI из CodePen с изумрудным неоновым бликом */
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: inset 0 0 15px rgba(16, 185, 129, 0.05);
        }
        .card-title {
            font-size: 12px;
            font-weight: 700;
            color: #94A3B8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .card-value {
            font-size: 24px;
            font-weight: 800;
            color: #10B981;
            margin-top: 5px;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }

        /* Тарифные коробки */
        .tariff-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            margin-bottom: 15px;
        }
        .tariff-box.popular {
            border-color: #10B981 !important;
            background: rgba(16, 185, 129, 0.02) !important;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.1) !important;
        }
        .price {
            font-size: 36px;
            font-weight: 900;
            color: #10B981;
            margin: 10px 0;
            text-shadow: 0 0 10px rgba(16, 185, 129, 0.2);
        }
        .desc {
            font-size: 13px;
            color: #94A3B8;
        }

        /* Фикс полей ввода: делаем текст внутри инпутов идеально белым и контрастным */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important;
            color: #FFFFFF !important;
            font-weight: 500 !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: 8px !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #10B981 !important;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.3) !important;
        }

        /* Текст вариантов в радио-кнопках */
        div[data-testid="stMarkdownContainer"] p {
            color: #E2E8F0 !important;
        }

        /* Вкладки навигации */
        .stTabs [data-baseweb="tab"] { font-size: 16px; font-weight: 600; color: #94A3B8; }
        .stTabs [aria-selected="true"] { color: #10B981 !important; border-bottom-color: #10B981 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ БЕЗОПАСНОЙ ПАМЯТИ ПЛАТФОРМЫ (ST.SESSION_STATE)
# ==============================================================================
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = [
        {
            "fio": "Никифоров Артур Владимирович", 
            "phone": "+7(921)555-44-33", 
            "email": "artur@mail.ru", 
            "education": "Высшее техническое", 
            "passport": "4012 987654", 
            "diploma": "№78-05", 
            "workbook": "№ТК-12", 
            "skills": "Фрезеровщик ЧПУ 4 разряда", 
            "gdpr": 1, 
            "current_status": "Железный специалист"
        }
    ]

if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = [
        {"id": 1, "tariff": "Безлимитный Год", "amount": 150000.0, "timestamp": "2026-03-15 12:00:00"}
    ]

if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

# Конвертируем в DataFrame для удобного вывода в таблицы Ассоциации
citizens_df = pd.DataFrame(st.session_state["citizens_data"])
payments_df = pd.DataFrame(st.session_state["payments_data"])
courses_df = pd.DataFrame(st.session_state["courses_data"])

# ==============================================================================
# 3. НАВИГАЦИЯ (Переключатель кабинетов в сайдбаре как на CodePen)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#10B981; font-weight:800; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3);'>🔒 КОНТУР АПП</h2>", unsafe_allow_html=True)
    user_role = st.selectbox(
        "Выберите личный кабинет:",
        [
            "🎓 Личный кабинет Физического лица", 
            "🏢 Личный кабинет Производства", 
            "🛠️ Кабинет Ассоциации (Управление)"
        ]
    )
    st.write("---")
    st.caption("ПромКачество.СПб v2.0")

# Вывод премиум Hero-баннера АПП
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ</div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# КАБИНЕТ №1: ГРАЖДАНЕ РФ (СОИСКАТЕЛИ)
# ==============================================================================
if user_role == "🎓 Личный кабинет Физического лица":
    st.markdown("<h3 style='color:#FFFFFF; font-weight:700;'>🎓 Портал обучения и Паспорт Навыков</h3>", unsafe_allow_html=True)
    
    with st.form("citizen_form", clear_on_submit=False):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>📝 Профильная анкетa и загрузка документов</h4>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        c_fio = col1.text_input("ФИО соискателя полностью:", value="Иванов Игорь Игоревич")
        c_phone = col2.text_input("Номер телефона для связи:", value="+7(900)111-22-33")
        c_email = col3.text_input("E-mail соискателя:", value="ivanov@spb.ru")
        
        col4, col5, col6 = st.columns(3)
        c_pass = col4.text_input("Паспорт (Серия, Номер):", placeholder="4011 123456")
        c_diploma = col5.text_input("Диплом (Серия, Номер):", placeholder="№78-01")
        c_work = col6.text_input("Трудовая книжка (Номер):", placeholder="№ТК-99")
        
        c_skills = st.text_area("Расскажите о ваших навыках и опыте работы (анкета о себе):")
        c_gdpr = st.checkbox("Согласие на обработку персональных данных граждан РФ", value=True)
        
        if st.form_submit_button("Сохранить анкету соискателя", type="primary"):
            if c_fio.strip() and c_phone.strip():
                st.session_state["citizens_data"].append({
                    "fio": c_fio.strip(), 
                    "phone": c_phone.strip(), 
                    "email": c_email.strip(), 
                    "education": "Высшее техническое", 
                    "passport": c_pass.strip(), 
                    "diploma": c_diploma.strip(), 
                    "workbook": c_work.strip(), 
                    "skills": c_skills.strip(), 
                    "gdpr": 1 if c_gdpr else 0, 
                    "current_status": "Обучение"
                })
                st.toast("✓ Анкета соискателя успешно сохранена в системе!")
                st.rerun()

    # Блок теста компетенций с ЖЁСТКИМ СИСТЕМНЫМ ОБНОВЛЕНИЕМ СТАТУСА
    with st.form("test_form"):
        st.markdown("<h4 style='color:#34D399; font-weight:700;'>🤖 Тест компетенций на производстве</h4>", unsafe_allow_html=True)
