import streamlit as st
import pandas as pd

# ==============================================================================
# 1. СКВОЗНЫЕ ПРЕМИУМ-СТИЛИ ИЗ CODEPEN (Glassmorphism, Неон, Фон #0B0F19)
# ==============================================================================
st.set_page_config(page_title="ПромКачество.СПб | Система Допусков", layout="wide", page_icon="🏭")

st.markdown("""
    <style>
        /* Глобальная киберпанк-тема CodePen */
        .stApp { background-color: #0B0F19 !important; color: #F8FAFC !important; }
        
        /* Фикс контраста подписей документов и ФИО во всех кабинетах */
        div[data-testid="stWidgetLabel"] p, label p {
            color: #FFFFFF !important; font-weight: 600 !important; font-size: 14px !important;
        }
        
        /* Наш особый премиум Hero-баннер АПП */
        .hero-banner {
            background: linear-gradient(135deg, #0F172A 0%, #111827 100%) !important;
            padding: 35px; border-radius: 16px; color: #FFFFFF; margin-bottom: 25px;
            border-left: 8px solid #10B981; box-shadow: 0 0 25px rgba(16, 185, 129, 0.15);
        }
        .hero-title {
            font-size: 28px; font-weight: 800;
            background: linear-gradient(90deg, #10B981, #34D399);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero-subtitle { font-size: 14px; color: #94A3B8; margin-top: 8px; line-height: 1.4; }

        /* Матовые контейнеры Glassmorphism */
        div[data-testid="stForm"], div[data-testid="stExpander"], .stAlert {
            background: rgba(17, 24, 39, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px !important; padding: 25px !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(12px);
        }

        /* Карточки KPI с изумрудным неоновым бликом */
        .glass-card {
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
            border-radius: 12px; padding: 20px; margin-bottom: 15px;
        }
        .card-title { font-size: 12px; font-weight: 700; color: #94A3B8; text-transform: uppercase; }
        .card-value { font-size: 24px; font-weight: 800; color: #10B981; margin-top: 5px; text-shadow: 0 0 10px #10B981; }

        /* Поля ввода */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.8) !important; color: #FFFFFF !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important; border-radius: 8px !important;
        }
        
        /* Стилизация официального бокового меню навигации Streamlit */
        section[data-testid="stSidebarNav"] { background-color: #0D1322 !important; }
        section[data-testid="stSidebarNav"] span { color: #F8FAFC !important; font-weight: 600 !important; }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. СКВОЗНАЯ ЕДИНАЯ СЕССИЯ ДАННЫХ ДЛЯ ВСЕХ ОТДЕЛЬНЫХ СТРАНИЦ
# ==============================================================================
if "citizens_data" not in st.session_state:
    st.session_state["citizens_data"] = [
        {"fio": "Никифоров Артур Владимирович", "phone": "+7(921)555-44-33", "email": "artur@mail.ru", "education": "Высшее техническое", "passport": "4012 987654", "diploma": "№78-05", "workbook": "№ТК-12", "skills": "Фрезеровщик ЧПУ", "gdpr": 1, "contract_status": "Подписан", "progress": 100, "current_status": "Железный специалист"}
    ]

if "payments_data" not in st.session_state:
    st.session_state["payments_data"] = [
        {"id": 1, "tariff": "Безлимитный Год", "amount": 150000.0, "timestamp": "2026-03-15 12:00:00"}
    ]

if "courses_data" not in st.session_state:
    st.session_state["courses_data"] = []

# Конвертируем массивы сессии в DataFrame
citizens_df = pd.DataFrame(st.session_state["citizens_data"])
payments_df = pd.DataFrame(st.session_state["payments_data"])
courses_df = pd.DataFrame(st.session_state["courses_data"])

# ==============================================================================
# 3. ОФИЦИАЛЬНОЕ ЖЕСТКОЕ НАПРАВЛЕНИЕ ПУТИ В ПАПКИ PAGES (С ЗАЩИТОЙ URL)
# ==============================================================================
# url_path принудительно делает веб-ссылки английскими во избежание сбоев автопереводчиков
page_citizen = st.Page("pages/1_🎓_Гражданин_РФ.py", title="🎓 Личный кабинет Физического лица", icon="🎓", url_path="student")
page_factory = st.Page("pages/2_🏢_Производство.py", title="🏢 Личный кабинет Производства", icon="🏢", url_path="factory")
page_association = st.Page("pages/3_🛠️_Ассоциация.py", title="🛠️ Кабинет Ассоциации (Управление)", icon="🛠️", url_path="association")

# Склеиваем страницы в общее меню
pg = st.navigation({
    "🔒 КОНТУР УПРАВЛЕНИЯ АПП": [page_citizen, page_factory, page_association]
})

# ==============================================================================
# 4. СТАРТОВАЯ ВИТРИНА ЭКОСИСТЕМЫ АПП СПБ
# ==============================================================================
# Вывод премиум Hero-баннера АПП
st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🏭 Промышленная экосистема опережающего ДПО «ПромКачество»</div>
        <div class="hero-subtitle">Цифровой механизм формирования рынков сбыта отечественного оборудования через обучение граждан РФ. Используйте меню навигации слева.</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='color:#10B981; font-weight:800;'>📊 Текущие KPI платформы в реальном времени</h3>", unsafe_allow_html=True)
col_k1, col_k2, col_k3 = st.columns(3)

with col_k1:
    st.markdown(f'<div class="glass-card"><div class="card-title">Развернуто b2b-стандартов</div><div class="card-value">{len(courses_df)} моделей</div></div>', unsafe_allow_html=True)
with col_k2:
    st.markdown(f'<div class="glass-card"><div class="card-title">Зарегистрировано граждан</div><div class="card-value">{len(citizens_df)} анкет</div></div>', unsafe_allow_html=True)
with col_k3:
    total_rev = payments_df['amount'].sum() if not payments_df.empty else 0
    st.markdown(f'<div class="glass-card"><div class="card-title">Общая сумма привлеченных оплат</div><div class="card-value" style="color:#F59E0B;">{total_rev:,.0f} ₽</div></div>', unsafe_allow_html=True)

st.write("---")

# Передаем управление кодовой базе страниц папки pages
pg.run()
