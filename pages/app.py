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

        /* Белые матовые b2b-контейнеры для форм */
        div[data-testid="stForm"], .stAlert {
            background: rgba(30, 41, 59, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important; padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important; backdrop-filter: blur(10px);
        }

        /* Карточки курсов и KPI в стиле Академии Pyrus */
        .pyrus-card {
            background: #1E293B !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px; padding: 22px; margin-bottom: 15px;
            transition: transform 0.2s;
        }
        .pyrus-card:hover { border-color: #06B6D4 !important; }
        .pyrus-card-title { font-size: 13px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
        .pyrus-card-value { font-size: 26px; font-weight: 800; color: #06B6D4; margin-top: 5px; }
        
        /* Контрастные b2b инпуты */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important;
            border: 1px solid rgba(6, 182, 212, 0.2) !important; border-radius: 8px !important;
        }
        
        /* Боковое меню навигации */
        section[data-testid="stSidebarNav"] { background-color: #0F172A !important; }
        section[data-testid="stSidebarNav"] span { color: #F8FAFC !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. ИНИЦИАЛИЗАЦИЯ СКВОЗНОЙ ПАМЯТИ АКАДЕМИИ (SESSION STATE)
# ==============================================================================
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = [
        {"fio": "Никифоров Артур Владимирович", "phone": "+7(921)555-44-33", "email": "artur@mail.ru", "education": "Высшее техническое", "passport": "4012 987654", "diploma": "№78-05", "workbook": "№ТК-12", "contract_status": "Подписан", "progress": 100, "current_status": "Сертифицированный специалист"}
    ]

if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = [
        {"id": 1, "tariff": "Корпоративный Безлимит", "amount": 150000.0, "timestamp": "2026-03-15 12:00:00"}
    ]

if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

# ==============================================================================
# 3. НАВИГАЦИОННАЯ СВЯЗКА С АНГЛИЙСКИМИ ФАЙЛАМИ СТРАНИЦ
# ==============================================================================
page_citizen = st.Page("pages/citizen.py", title="🎓 Кабинет Специалиста (Паспорт навыков)", icon="🎓", url_path="student")
page_factory = st.Page("pages/factory.py", title="🏢 Портал Партнеров и Заводов", icon="🏢", url_path="factory")
page_association = st.Page("pages/association.py", title="🛠️ Панель Руководителя (Центр компетенций)", icon="🛠️", url_path="association")

pg = st.navigation({
    "АКАДЕМИЯ PYRUS / ПРОМКАЧЕСТВО": [page_citizen, page_factory, page_association]
})

# Вывод баннера Академии
st.markdown("""
    <div class="academy-banner">
        <div class="academy-title">🎓 Станьте сертифицированным экспертом платформы</div>
        <div class="academy-subtitle">Академия ПромКачество — это портал для b2b-специалистов, которые занимаются автоматизацией процессов и развитием производств. Выбирайте треки, проходите симуляторы и получайте допуски.</div>
    </div>
""", unsafe_allow_html=True)

pg.run()
